# -*- coding: utf-8 -*-
"""Tally the global attributes ballots posted in this repository's Discussions.

Reads every discussion titled "Global attributes vote | ...", parses each comment's
ballot lines ("attribute: Req, FVON  --> note"), and writes three CSV files:

  results/summary.csv        one row per attribute: vote counts, leading option, agreement
  results/ballots.csv        one row per voter and attribute, as parsed, with the note
  results/participation.csv  one row per section: who voted and when

Runs locally (token from GH_TOKEN, GITHUB_TOKEN or `gh auth token`) or in GitHub Actions.
No third-party packages.
"""
import csv, json, os, re, subprocess, sys, urllib.request
from collections import Counter, OrderedDict
from pathlib import Path

OWNER, REPO = "FVON-GOOS", "global-attributes"
OUT = Path(__file__).resolve().parent.parent / "results"

REQ_CODES = ["Req", "Rec", "Sug", "Not"]
SCOPE_CODES = ["FVON", "NET", "FILE", "n/a"]
SECTION_ORDER = ["WHAT", "WHERE", "WHEN", "WHO", "HOW"]


# ---------------------------------------------------------------- GitHub
def token():
    for k in ("GH_TOKEN", "GITHUB_TOKEN"):
        if os.environ.get(k):
            return os.environ[k]
    return subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=True).stdout.strip()


def graphql(query):
    req = urllib.request.Request("https://api.github.com/graphql", data=json.dumps({"query": query}).encode(),
                                 headers={"Authorization": f"bearer {token()}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        data = json.load(r)
    if "errors" in data:
        raise SystemExit(f"GraphQL error: {data['errors']}")
    return data["data"]


def fetch():
    q = """query { repository(owner:"%s", name:"%s") { discussions(first:50) { nodes {
             number title url body
             comments(first:100) { nodes { author { login } createdAt updatedAt url body isMinimized } } } } } }""" % (OWNER, REPO)
    nodes = graphql(q)["repository"]["discussions"]["nodes"]
    return [n for n in nodes if n["title"].startswith("Global attributes vote")]


# ---------------------------------------------------------------- parsing
def section_of(title):
    m = re.search(r"\|\s*([A-Z]+)\s*:", title)
    return m.group(1) if m else title


def reference_table(body):
    """Reference rows (attribute, NCEI, IMOS) and the ballot template keys, in order."""
    rows = []
    for line in body.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 4 and cells[0].startswith("`"):
            rows.append(cells)
    m = re.search(r"```text\n(.*?)```", body, flags=re.S)
    keys = [l.split(":")[0].strip() for l in (m.group(1).splitlines() if m else []) if ":" in l]
    if len(rows) != len(keys):
        raise SystemExit(f"table rows ({len(rows)}) and ballot keys ({len(keys)}) do not line up")
    return [(k, r[0].replace("`", ""), r[1], r[2]) for k, r in zip(keys, rows)]


def norm_key(s):
    return re.sub(r"\s+", "", s).lower()


REQ_RE = re.compile(r"^\s*(req(?:uired)?|rec(?:ommended)?|sug(?:gested)?|not(?:\s+(?:needed|relevant|recommended))?)\b(\??)", re.I)
SCOPE_RE = re.compile(r"^\s*((?:FVON|NET|FILE|n/a)(?:\s*/\s*(?:FVON|NET|FILE|n/a))*)\b", re.I)


def parse_value(rest):
    """'Rec, NET/FVON --> note' -> ('Rec', ['NET','FVON'], 'note')"""
    rest = rest.strip()
    req, scopes, note = "", [], rest
    m = REQ_RE.match(rest)
    if m:
        word = m.group(1).lower()
        req = {"req": "Req", "rec": "Rec", "sug": "Sug"}.get(word[:3], "Not")
        if m.group(2):
            note = "(unsure)"
        rest = rest[m.end():]
        rest = re.sub(r"^\s*[,;]?\s*", "", rest)
        s = SCOPE_RE.match(rest)
        if s:
            scopes = [("n/a" if x.lower() == "n/a" else x.upper()) for x in re.findall(r"FVON|NET|FILE|n/a", s.group(1), flags=re.I)]
            rest = rest[s.end():]
        note = re.sub(r"^[\s,:;>\-]+", "", rest).strip()
        if m.group(2):
            note = ("(unsure) " + note).strip()
    return req, scopes, note


def parse_ballot(body, canon):
    """Return ({canonical_key: (req, scopes, note)}, general_comment)."""
    by_norm = {norm_key(k): k for k in canon}
    votes, general = OrderedDict(), []
    for raw in body.splitlines():
        line = raw.strip()
        if not line:
            continue
        if ":" in line:
            k, rest = line.split(":", 1)
            key = by_norm.get(norm_key(k))
            if key:
                req, scopes, note = parse_value(rest)
                if req or scopes or note:
                    votes[key] = (req, scopes, note)
                continue
        general.append(line)
    return votes, " ".join(general).strip()


# ---------------------------------------------------------------- stats
def leading(counter, voters, order):
    if voters == 0 or not counter:
        return "", 0.0, "no votes"
    top = max(counter.values())
    best = [o for o in order if counter.get(o, 0) == top]
    share = top / voters
    if len(best) > 1:
        label = "tie"
    elif share == 1:
        label = "unanimous"
    elif share > 0.5:
        label = "majority"
    else:
        label = "split"
    return " / ".join(best), round(share * 100), label


def main():
    discussions = sorted(fetch(), key=lambda d: SECTION_ORDER.index(section_of(d["title"]))
                         if section_of(d["title"]) in SECTION_ORDER else 99)
    summary, ballots, participation = [], [], []
    for d in discussions:
        sec = section_of(d["title"])
        ref = reference_table(d["body"])
        canon = [r[0] for r in ref]
        parsed = []
        for c in d["comments"]["nodes"]:
            if c.get("isMinimized"):
                continue
            votes, general = parse_ballot(c["body"], canon)
            if not votes:
                continue          # a discussion comment, not a ballot
            who = (c.get("author") or {}).get("login") or "ghost"
            parsed.append((who, c, votes))
            if general:
                ballots.append({"Section": sec, "Attribute": "(general comment)", "Voter": who,
                                "Date": c["updatedAt"][:10], "Requirement": "", "Scope": "", "Note": general, "Link": c["url"]})
            for key in canon:
                if key in votes:
                    req, scopes, note = votes[key]
                    ballots.append({"Section": sec, "Attribute": key, "Voter": who, "Date": c["updatedAt"][:10],
                                    "Requirement": req, "Scope": "/".join(scopes), "Note": note, "Link": c["url"]})
        participation.append({"Section": sec, "Discussion": d["url"], "Ballots": len(parsed),
                              "Voters": ", ".join(p[0] for p in parsed),
                              "Last ballot": max((p[1]["updatedAt"][:10] for p in parsed), default="")})
        for key, label, ncei, imos in ref:
            reqs, scopes, notes = Counter(), Counter(), []
            n_req = n_scope = 0
            for who, c, votes in parsed:
                if key not in votes:
                    continue
                req, sc, note = votes[key]
                if req:
                    reqs[req] += 1; n_req += 1
                if sc:
                    n_scope += 1
                    for s in set(sc):
                        scopes[s] += 1
                if note:
                    notes.append(f"{who}: {note}")
            lr, lr_share, lr_label = leading(reqs, n_req, REQ_CODES)
            ls, ls_share, ls_label = leading(scopes, n_scope, SCOPE_CODES)
            row = {"Section": sec, "Attribute": key, "NCEI": ncei, "IMOS": imos, "Voters": n_req}
            row.update({c: reqs.get(c, 0) for c in REQ_CODES})
            row.update({"Leading requirement": lr, "Requirement agreement %": lr_share, "Requirement status": lr_label})
            row.update({c: scopes.get(c, 0) for c in SCOPE_CODES})
            row.update({"Leading scope": ls, "Scope agreement %": ls_share, "Scope status": ls_label,
                        "Notes": " | ".join(notes)})
            summary.append(row)

    OUT.mkdir(exist_ok=True)
    def write(name, rows):
        with open(OUT / name, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader(); w.writerows(rows)
    write("summary.csv", summary)
    write("ballots.csv", ballots)
    write("participation.csv", participation)
    print(f"{len(summary)} attributes, {sum(p['Ballots'] for p in participation)} ballots in {len(participation)} sections -> {OUT}")


if __name__ == "__main__":
    main()
