# -*- coding: utf-8 -*-
"""Tally the global attributes ballots posted in this repository's Discussions.

Reads every discussion titled "Global attributes vote | ...", parses each comment's
ballot lines ("attribute: Req, FVON  --> note"), and writes:

  RESULTS.md                 the results page for the group: the decision on one screen,
                             with the votes and comments folded underneath
  results/summary.csv        one row per attribute: the leading requirement and scope
  results/ballots.csv        one row per voter and attribute, as parsed, with the note,
                             sorted by section, then attribute
  results/participation.csv  one row per section: who voted and when

Requirement levels are Req (Required), Opt (Optional) and N/A (Not applicable).
Ballots written on the earlier four-level scale are read onto it: Rec and Sug count
as Opt, Not counts as N/A.

Runs locally (token from GH_TOKEN, GITHUB_TOKEN or `gh auth token`) or in GitHub Actions.
No third-party packages.
"""
import csv, json, os, re, subprocess, sys, urllib.request
from collections import Counter, OrderedDict
from pathlib import Path

OWNER, REPO = "FVON-GOOS", "global-attributes"
OUT = Path(__file__).resolve().parent.parent / "results"

REQ_CODES = ["Req", "Opt", "N/A"]
REQ_LABEL = {"Req": "Required", "Opt": "Optional", "N/A": "Not applicable"}
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


REQ_RE = re.compile(r"^\s*(req(?:uired)?|opt(?:ional)?|rec(?:ommended)?|sug(?:gested)?|n/a"
                    r"|not(?:\s+(?:needed|relevant|recommended|applicable))?)\b(\??)", re.I)
SCOPE_RE = re.compile(r"^\s*((?:FVON|NET|FILE|n/a)(?:\s*/\s*(?:FVON|NET|FILE|n/a))*)\b", re.I)


def parse_value(rest):
    """'Opt, NET/FVON --> note' -> ('Opt', ['NET','FVON'], 'note'). Rec/Sug -> Opt, Not -> N/A."""
    rest = rest.strip()
    req, scopes, note = "", [], rest
    m = REQ_RE.match(rest)
    if m:
        word = m.group(1).lower()
        req = {"req": "Req", "opt": "Opt", "rec": "Opt", "sug": "Opt"}.get(word[:3], "N/A")
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
def leading(counter, order):
    """The option(s) with most votes; ties are joined, e.g. 'Req / Rec'."""
    if not counter:
        return ""
    top = max(counter.values())
    return " / ".join(o for o in order if counter.get(o, 0) == top)


# ---------------------------------------------------------------- results page
def md(text):
    return text.replace("|", "\\|").replace("\n", " ")


def votes_text(reqs):
    """'Required 2 · Optional 1', in scale order, options with no votes left out."""
    return " · ".join(f"{REQ_LABEL[c]} {reqs[c]}" for c in REQ_CODES if reqs.get(c))


def scope_text(d):
    """The scope options that drew votes; n/a only counts when nothing else was named."""
    named = [(s, d["scopes"][s]) for s in SCOPE_CODES if s != "n/a" and d["scopes"].get(s)]
    if not named:
        return "–"
    if len(named) == 1:
        return named[0][0]
    return ", ".join(f"{s} {n}" for s, n in sorted(named, key=lambda x: -x[1]))


def result_of(d):
    """('Req'|'Opt'|'N/A'|'open', unanimous?)"""
    reqs = d["reqs"]
    if not reqs:
        return "open", False
    top = max(reqs.values())
    lead = [c for c in REQ_CODES if reqs.get(c, 0) == top]
    return (lead[0], len(reqs) == 1) if len(lead) == 1 else ("open", False)


def results_page(detail, participation):
    groups = {"Req": [], "Opt": [], "N/A": [], "open": []}
    for d in detail:
        d["result"], d["unanimous"] = result_of(d)
        groups[d["result"]].append(d)
    voters = []
    for p in participation:
        for v in p["Voters"].split(", "):
            if v and v not in voters:
                voters.append(v)
    last = max((p["Last ballot"] for p in participation), default="")
    name = lambda d: f"`{d['attr']}`"
    cols = REQ_CODES + (["open"] if groups["open"] else [])       # an Undecided column only if a vote is tied
    label = dict(REQ_LABEL, open="Undecided (tied)")
    cell = lambda ds: "<br>".join(name(d) for d in ds) or "–"

    L = ["# Global attributes: poll results", "",
         f"{len(detail)} attributes · {len(voters)} voters · last ballot {last}", "",
         "## The decision", "",
         "| | " + " | ".join(f"{label[c]} ({len(groups[c])})" for c in cols) + " |",
         "|---|" + "---|" * len(cols)]
    for sec in SECTION_ORDER:
        row = [cell([d for d in groups[c] if d["sec"] == sec]) for c in cols]
        if any(r != "–" for r in row):
            L.append(f"| **{sec}** | " + " | ".join(row) + " |")
    L += ["",
          "**Required:** a file is non-compliant without it. **Optional:** may be included, never blocks "
          "ingestion. **Not applicable:** not used in FVON files.", ""]

    # who sets the value, for the required attributes
    scope_rows = [("FVON", "One value for all of FVON"), ("NET", "Set once by each network"),
                  ("FILE", "Different in every file")]
    by_scope = {s: [] for s, _ in scope_rows}
    unsettled = []
    for d in groups["Req"]:
        named = {s: d["scopes"][s] for s, _ in scope_rows if d["scopes"].get(s)}
        top = [s for s in named if named[s] == max(named.values())]
        (by_scope[top[0]] if len(top) == 1 else unsettled).append(d)
    L += ["## Required attributes: who sets the value", "", "| | Attributes |", "|---|---|"]
    L += [f"| **{text}** | {' · '.join(name(d) for d in by_scope[s])} |" for s, text in scope_rows if by_scope[s]]
    if unsettled:
        L.append(f"| **Not settled** | {' · '.join(name(d) for d in unsettled)} |")
    L.append("")

    # everything below is supporting detail, folded away
    L += ["## Detail", "", "<details>", "<summary>Votes behind each result</summary>", "",
          "| Section | Attribute | Result | Votes | Scope votes |", "|---|---|---|---|---|"]
    for d in detail:
        res = REQ_LABEL.get(d["result"], "Undecided")
        L.append(f"| {d['sec']} | {name(d)} | {res} | {votes_text(d['reqs'])} | {scope_text(d)} |")
    L += ["", "</details>", "", "<details>", "<summary>Voter comments</summary>", "",
          "| Section | Attribute | Voter | Comment |", "|---|---|---|---|"]
    for d in detail:
        for w, r, n in d["cast"]:
            if n:
                L.append(f"| {d['sec']} | {name(d)} | {w} | {md(n)} |")
    L += ["", "</details>", "",
          f"Voters: {', '.join(voters)}. Not every voter filled in every attribute. Ballots cast on the earlier "
          "scale count as: Recommended or Suggested = Optional, Not recommended = Not applicable. "
          "Scope: FVON = one value for all networks, NET = set once per network, FILE = varies per file.", "",
          "Generated by [`scripts/tally.py`](scripts/tally.py) from the ballots in the "
          "[Discussions](https://github.com/FVON-GOOS/global-attributes/discussions); do not edit by hand. "
          "Every ballot line is in [`results/ballots.csv`](results/ballots.csv).", ""]
    return "\n".join(L)


def main():
    discussions = sorted(fetch(), key=lambda d: SECTION_ORDER.index(section_of(d["title"]))
                         if section_of(d["title"]) in SECTION_ORDER else 99)
    summary, ballots, participation, detail = [], [], [], []
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
            reqs, scopes, cast = Counter(), Counter(), []
            for who, c, votes in parsed:
                if key not in votes:
                    continue
                req, sc, note = votes[key]
                if req:
                    reqs[req] += 1
                    cast.append((who, req, note))
                for s in set(sc):          # a split answer (NET/FVON) counts toward each option
                    scopes[s] += 1
            summary.append({"Section": sec, "Attribute": key, "NCEI": ncei, "IMOS": imos,
                            "Leading requirement": leading(reqs, REQ_CODES),
                            "Leading scope": leading(scopes, SCOPE_CODES)})
            detail.append({"sec": sec, "attr": key, "ncei": ncei, "imos": imos,
                           "reqs": reqs, "scopes": scopes, "cast": cast})

    # ballots: by section (WHAT, WHERE, WHEN, WHO, HOW), then attribute; voters keep posting order
    sec_rank = {s: i for i, s in enumerate(SECTION_ORDER)}
    ballots.sort(key=lambda b: (sec_rank.get(b["Section"], 99), b["Attribute"].lower()))

    OUT.mkdir(exist_ok=True)
    def write(name, rows):
        with open(OUT / name, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader(); w.writerows(rows)
    write("summary.csv", summary)
    write("ballots.csv", ballots)
    write("participation.csv", participation)
    (OUT.parent / "RESULTS.md").write_text(results_page(detail, participation), encoding="utf-8", newline="\n")
    print(f"{len(summary)} attributes, {sum(p['Ballots'] for p in participation)} ballots in {len(participation)} sections -> {OUT}")


if __name__ == "__main__":
    main()
