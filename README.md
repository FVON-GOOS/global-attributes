# FVON Data Management Subcommittee: Metadata Decision Draft
## Section 1: Global Attributes

**Status:** Working draft for discussion; nothing here is decided.
**Sources:** NCEI NetCDF Templates v2.0 (ACDD-1.3 / CF based) and IMOS NetCDF Conventions v1.4.2 (June 2021).

---

## 1. Decision framework

For each attribute the group makes **two** decisions:

### Decision A: Requirement level
| Code | Meaning |
|------|---------|
| **Req** (Required) | File is rejected / non-compliant without it |
| **Rec** (Recommended) | Expected wherever meaningful; absence never blocks ingestion |
| **Sug** (Suggested) | Not part of the core FVON spec; networks may add it where they find it useful |

> Terminology note: this deliberately reuses NCEI's own wording (Required / Recommended / Suggested, dropping their "Highly Recommended" middle tier), so the FVON decision reads on the same scale as the NCEI column in the tables. IMOS's two tiers map onto it as Mandatory → Required and Optional → Recommended/Suggested.

### Decision B: Value scope (who sets the value?)
| Code | Meaning | Example |
|------|---------|---------|
| **FVON** | One fixed value (or template) defined by FVON, identical across all networks | `Conventions`, `standard_name_vocabulary` |
| **NET** | Fixed per network, defined once by each network | `institution`, `citation` |
| **FILE** | Varies per file/deployment, usually auto-generated | `time_coverage_start`, `geospatial_lat_min` |

Some attributes may be hybrids (e.g. `project` could be "FVON" + network name).

**Neither decision is proposed here.** Both the requirement level and the value scope will be decided by Data Management Subcommittee members through a GitHub discussion, attribute by attribute. The tables below give the inputs for that discussion: what each source standard requires and an example.

Attributes are listed **alphabetically** within each section.
NCEI column codes: Req = Required, HR = Highly Recommended, Rec = Recommended, Sug = Suggested (NCEI's own tiers). IMOS column: M = mandatory (Table 1), O = optional (Table 2). In any column, n/a = not defined / not applicable.

---

## 2. WHAT: identification and description

| Attribute | NCEI | IMOS | Example |
|---|---|---|---|
| `cdm_data_type` | Rec | O | Redundant with `featureType`; THREDDS-specific |
| `Conventions` | Req | M | `"CF-1.8, ACDD-1.3, FVON-1.0"` |
| `featureType` | (structural) | O | `"trajectoryProfile"` |
| `id` | Req | n/a | `"FVON_MOANA_XYZ123_20260715"` |
| `instrument` | Rec | O | `"ZebraTech Moana TD1050"` |
| `instrument_serial_number` | n/a | O | `"5124"` |
| `instrument_vocabulary` | Rec | n/a | `"NERC SeaVoX Device Catalogue (L22)"` |
| `keywords` | Rec | O | `"Oceans > Ocean Temperature > Water Temperature, ..."` |
| `keywords_vocabulary` | Rec | O | `"NASA/GCMD Earth Science Keywords"` |
| `metadata_link` (IMOS: `metadata`) | Sug | O | URL to catalogue record |
| `naming_authority` | Req | M | `"org.oceanops.fvon"` or per-network |
| `ncei_template_version` | Sug | n/a | Only relevant if archiving directly at NCEI |
| `platform` | Rec | O | `"fishing vessel"` (vocab term, not vessel name, to preserve fisher anonymity) |
| `platform_vocabulary` | Rec | n/a | `"NERC SeaVoX Platform Categories (L06)"` |
| `product_version` | Sug | n/a | `"v1.2"` |
| `program` | Sug | n/a | `"Global Ocean Observing System (GOOS)"` |
| `project` | Rec | M | `"Fishing Vessel Ocean Observing Network (FVON); Moana Project"` |
| `sensorML` | n/a | O | Low adoption; keep as network-defined extra if wanted |
| `site_code` / `site` | n/a | O | Fixed-site concept; doesn't fit mobile fishing vessels |
| `standard_name_vocabulary` | Rec | M | `"CF Standard Name Table v79"` |
| `summary` (IMOS: `abstract`) | Req | M | `"Temperature profiles collected by a sensor mounted on commercial trawl gear as part of the Moana Project, contributing to FVON..."` |
| `title` | Req | M | `"Temperature and depth observations from fishing-gear-mounted sensor, deployment XYZ123"` |
| `uuid` | Sug | n/a | Auto-generated |

---

## 3. WHERE: spatial coverage

| Attribute | NCEI | IMOS | Example |
|---|---|---|---|
| `geospatial_bounds` (+ `_crs`, `_vertical_crs`) | Sug | n/a | WKT polygon; overkill vs. min/max box *(revisit for gridded products)* |
| `geospatial_lat_min` / `_max` | Rec | M | `-41.2` / `-38.7` |
| `geospatial_lat_resolution` / `lon_resolution` / `vertical_resolution` | Rec | n/a | Meaningful for grids, not for opportunistic vessel tracks |
| `geospatial_lat_units` / `lon_units` | Rec | O | `"degrees_north"` / `"degrees_east"` (defaults per standard) |
| `geospatial_lon_min` / `_max` | Rec | M | `172.9` / `175.1` |
| `geospatial_vertical_min` / `_max` | Rec | M | `0.0` / `250.0` |
| `geospatial_vertical_positive` | Rec | M | `"down"` (fix one value for all networks) |
| `geospatial_vertical_units` | Rec | O | `"metres"` |
| `sea_name` | Rec | n/a | `"Tasman Sea"` (NCEI sea names list) |

---

## 4. WHEN: temporal coverage

| Attribute | NCEI | IMOS | Example |
|---|---|---|---|
| `date_created` | Rec | M | `"2026-07-16T09:00:00Z"` |
| `date_issued` | Rec | n/a | Rarely differs from `date_created` in this context |
| `date_metadata_modified` | Rec | n/a | Low value for file-level records |
| `date_modified` | Rec | O | Ties into `history` |
| `local_time_zone` | n/a | O | IMOS itself says not to use it for moving platforms |
| `time_coverage_duration` | Rec | n/a | Derivable from start/end |
| `time_coverage_resolution` | Rec | n/a | `"PT1S"` (useful given very different sampling regimes across networks) |
| `time_coverage_start` / `_end` | Rec | M | `"2026-07-15T04:12:00Z"` (ISO 8601, UTC) |

**FVON-wide rule to adopt regardless of columns:** all times UTC, ISO 8601 `YYYY-MM-DDThh:mm:ssZ` (both standards agree).

---

## 5. WHO: people and organisations

NCEI/ACDD and IMOS use different vocabularies here; proposal is to standardize on the **ACDD names** (better tooling/harvester support) with the IMOS equivalents noted:

| Attribute | NCEI | IMOS equivalent | Example |
|---|---|---|---|
| `acknowledgment` | Rec | M | `"Data collected in partnership with commercial fishers through [network], part of FVON..."` |
| `contributor_name` / `contributor_role` | Rec | n/a | Could credit vessels/skippers *where they consent* |
| `creator_email` | Rec | `author_email` (O) | `"info@moanaproject.org"` |
| `creator_institution` | Rec | n/a | Only if it differs from `institution` |
| `creator_name` | HR | `author` / `principal_investigator` (M) | `"Moana Project Data Team"` *(team/role rather than named person)* |
| `creator_type` | HR | n/a | `"group"` |
| `creator_url` | Rec | n/a | `"https://www.moanaproject.org"` |
| `institution` | HR | M | `"Moana Project / MetService New Zealand"` |
| `principal_investigator` (IMOS name) | n/a | M | Folded into `creator_*` / `contributor_*` |
| `publisher_email` | Rec | `data_centre_email` (M) | |
| `publisher_name` | Rec | `data_centre` (M) | `"MetOcean Solutions"` (or a shared FVON DAC?) |
| `publisher_type` / `_url` / `_institution` | Rec | n/a | |

---

## 6. HOW: provenance, quality, access

| Attribute | NCEI | IMOS | Example |
|---|---|---|---|
| `citation` | n/a | M | `"Moana Project (2026). Fishing vessel ocean observations. Accessed YYYY-MM-DD."` |
| `comment` | Rec | O | Free text |
| `disclaimer` | n/a | M (IMOS) | Standard liability text |
| `file_version_quality_control` | n/a | O | Merged into `processing_level` definitions |
| `history` | Rec | O | `"2026-07-16T09:00:00Z: created; 2026-07-16T09:01:12Z: QC v2.1 applied"` |
| `license` | Rec | M | `"https://creativecommons.org/licenses/by/4.0/"` |
| `lineage` | n/a | O | Overlaps `history` + `processing_level`; ISO 19115 concern, not file-level |
| `processing_level` (IMOS: `file_version`) | Rec | O | `"Level 1 - Quality controlled data"` |
| `quality_control_log` | n/a | O | Useful for QC transparency; verbose |
| `references` | Rec | O | DOI of network methods paper |
| `source` | Rec | O | `"Sensor mounted on commercial fishing gear"` (a short FVON-controlled list would aid discovery) |
