# Global attributes: poll results

63 attributes · 4 voters · last ballot 2026-11-25

## The decision

| | Required (20) | Optional (32) | Not applicable (11) |
|---|---|---|---|
| **WHAT** | `Conventions`<br>`instrument`<br>`naming_authority`<br>`standard_name_vocabulary`<br>`summary`<br>`title` | `cdm_data_type`<br>`featureType`<br>`id`<br>`instrument_serial_number`<br>`instrument_vocabulary`<br>`keywords`<br>`keywords_vocabulary`<br>`metadata_link`<br>`platform`<br>`platform_vocabulary`<br>`product_version`<br>`program`<br>`project` | `ncei_template_version`<br>`sensorML`<br>`site_code/site`<br>`uuid` |
| **WHERE** | `geospatial_lat_min/max`<br>`geospatial_lon_min/max`<br>`geospatial_vertical_min/max` | `geospatial_bounds`<br>`geospatial_lat/lon_units`<br>`geospatial_vertical_positive`<br>`geospatial_vertical_units` | `geospatial_lat/lon/vertical_resolution`<br>`sea_name` |
| **WHEN** | `date_created`<br>`time_coverage_start/end` | `date_modified`<br>`time_coverage_duration` | `date_issued`<br>`date_metadata_modified`<br>`local_time_zone`<br>`time_coverage_resolution` |
| **WHO** | `acknowledgment`<br>`creator_email`<br>`creator_name`<br>`institution`<br>`publisher_email`<br>`publisher_name` | `contributor_name/role`<br>`creator_institution`<br>`creator_url`<br>`principal_investigator`<br>`publisher_type/url/institution` | `creator_type` |
| **HOW** | `license`<br>`processing_level`<br>`source` | `citation`<br>`comment`<br>`disclaimer`<br>`file_version_quality_control`<br>`history`<br>`lineage`<br>`quality_control_log`<br>`references` | – |

**Required:** a file is non-compliant without it. **Optional:** may be included, never blocks ingestion. **Not applicable:** not used in FVON files.

## Required attributes: who sets the value

| | Attributes |
|---|---|
| **One value for all of FVON** | `Conventions` · `naming_authority` · `standard_name_vocabulary` · `license` · `source` |
| **Set once by each network** | `acknowledgment` · `creator_email` · `creator_name` · `institution` · `publisher_email` · `publisher_name` |
| **Different in every file** | `instrument` · `summary` · `title` · `geospatial_lat_min/max` · `geospatial_lon_min/max` · `geospatial_vertical_min/max` · `date_created` · `time_coverage_start/end` · `processing_level` |

## Detail

<details>
<summary>Votes behind each result</summary>

| Section | Attribute | Result | Votes | Scope votes |
|---|---|---|---|---|
| WHAT | `cdm_data_type` | Optional | Optional 3 | FVON |
| WHAT | `Conventions` | Required | Required 3 | FVON |
| WHAT | `featureType` | Optional | Required 1 · Optional 2 | FVON 2, FILE 1 |
| WHAT | `id` | Optional | Optional 2 | FILE |
| WHAT | `instrument` | Required | Required 4 | FILE |
| WHAT | `instrument_serial_number` | Optional | Optional 4 | FILE |
| WHAT | `instrument_vocabulary` | Optional | Optional 2 · Not applicable 1 | FILE 2, FVON 1 |
| WHAT | `keywords` | Optional | Optional 3 | FVON 2, NET 1 |
| WHAT | `keywords_vocabulary` | Optional | Optional 3 | FVON 2, NET 1 |
| WHAT | `metadata_link` | Optional | Optional 3 | NET |
| WHAT | `naming_authority` | Required | Required 3 | FVON 2, NET 1 |
| WHAT | `ncei_template_version` | Not applicable | Optional 1 · Not applicable 2 | – |
| WHAT | `platform` | Optional | Required 1 · Optional 3 | FVON 2, NET 2, FILE 1 |
| WHAT | `platform_vocabulary` | Optional | Optional 3 | FVON 3, NET 2 |
| WHAT | `product_version` | Optional | Optional 3 | FILE |
| WHAT | `program` | Optional | Optional 3 | FVON |
| WHAT | `project` | Optional | Required 1 · Optional 3 | NET 3, FVON 1 |
| WHAT | `sensorML` | Not applicable | Optional 1 · Not applicable 2 | – |
| WHAT | `site_code/site` | Not applicable | Optional 1 · Not applicable 2 | – |
| WHAT | `standard_name_vocabulary` | Required | Required 3 | FVON |
| WHAT | `summary` | Required | Required 3 | FILE 3, NET 2 |
| WHAT | `title` | Required | Required 3 | FILE 3, NET 2 |
| WHAT | `uuid` | Not applicable | Optional 1 · Not applicable 2 | FILE |
| WHERE | `geospatial_bounds` | Optional | Optional 3 | FILE |
| WHERE | `geospatial_lat_min/max` | Required | Required 2 · Optional 1 | FILE |
| WHERE | `geospatial_lat/lon/vertical_resolution` | Not applicable | Optional 1 · Not applicable 2 | – |
| WHERE | `geospatial_lat/lon_units` | Optional | Optional 2 · Not applicable 1 | FVON 1, NET 1 |
| WHERE | `geospatial_lon_min/max` | Required | Required 2 · Optional 1 | FILE |
| WHERE | `geospatial_vertical_min/max` | Required | Required 2 · Optional 1 | FILE |
| WHERE | `geospatial_vertical_positive` | Optional | Optional 3 | FVON |
| WHERE | `geospatial_vertical_units` | Optional | Optional 3 | FVON |
| WHERE | `sea_name` | Not applicable | Optional 1 · Not applicable 2 | NET |
| WHEN | `date_created` | Required | Required 3 | FILE |
| WHEN | `date_issued` | Not applicable | Not applicable 2 | – |
| WHEN | `date_metadata_modified` | Not applicable | Required 1 · Not applicable 2 | FILE |
| WHEN | `date_modified` | Optional | Required 1 · Optional 2 | FILE |
| WHEN | `local_time_zone` | Not applicable | Not applicable 2 | – |
| WHEN | `time_coverage_duration` | Optional | Required 1 · Optional 2 | FILE |
| WHEN | `time_coverage_resolution` | Not applicable | Required 1 · Not applicable 2 | FILE |
| WHEN | `time_coverage_start/end` | Required | Required 3 | FILE |
| WHO | `acknowledgment` | Required | Required 3 | NET 2, FVON 1 |
| WHO | `contributor_name/role` | Optional | Optional 3 | FILE |
| WHO | `creator_email` | Required | Required 2 | NET |
| WHO | `creator_institution` | Optional | Required 1 · Optional 2 | NET |
| WHO | `creator_name` | Required | Required 2 | NET |
| WHO | `creator_type` | Not applicable | Not applicable 2 | – |
| WHO | `creator_url` | Optional | Optional 2 | NET |
| WHO | `institution` | Required | Required 3 | NET |
| WHO | `principal_investigator` | Optional | Required 1 · Optional 2 | NET 1, FILE 1 |
| WHO | `publisher_email` | Required | Required 2 | NET |
| WHO | `publisher_name` | Required | Required 3 | NET |
| WHO | `publisher_type/url/institution` | Optional | Optional 3 | NET |
| HOW | `citation` | Optional | Optional 3 | NET |
| HOW | `comment` | Optional | Optional 2 | NET 1, FILE 1 |
| HOW | `disclaimer` | Optional | Optional 3 | NET |
| HOW | `file_version_quality_control` | Optional | Optional 2 | NET |
| HOW | `history` | Optional | Required 1 · Optional 2 | FILE |
| HOW | `license` | Required | Required 3 | FVON 2, NET 1 |
| HOW | `lineage` | Optional | Optional 2 · Not applicable 1 | – |
| HOW | `processing_level` | Required | Required 3 | FILE 2, FVON 1 |
| HOW | `quality_control_log` | Optional | Required 1 · Optional 2 | FILE 2, FVON 1 |
| HOW | `references` | Optional | Required 1 · Optional 2 | NET 2, FVON 1 |
| HOW | `source` | Required | Required 3 | FVON |

</details>

<details>
<summary>Voter comments</summary>

| Section | Attribute | Voter | Comment |
|---|---|---|---|
| WHAT | `featureType` | novantonio | you have trajectory, timeseries and profiles |
| WHAT | `id` | verolago | N.B.: if using the id, note that the file count in the ZT sensor raw file names reset sporadically when the battery is low, so we shouldn't use that count in ID. |
| WHAT | `instrument_vocabulary` | verolago | (instrument dependant; should also have a voting category for those not needed/not relevant, lower than suggested) |
| WHAT | `instrument_vocabulary` | novantonio | https://vocab.nerc.ac.uk/collection/L05/current/ |
| WHAT | `keywords_vocabulary` | novantonio | CF |
| WHAT | `naming_authority` | novantonio | if it's FVON it shows stronger coordination |
| WHAT | `platform` | novantonio | https://vocab.nerc.ac.uk/collection/L06/current/ |
| WHAT | `platform` | TetsutaroTakikawa | (Not only fishing vessel, but also research/training vessels, etc.) |
| WHAT | `platform_vocabulary` | novantonio | https://vocab.nerc.ac.uk/collection/L06/current/ |
| WHAT | `project` | novantonio | use a DOI |
| WHAT | `standard_name_vocabulary` | novantonio | https://vocab.nerc.ac.uk/collection/P01/current/ |
| WHERE | `geospatial_lat_min/max` | novantonio | and you need 2 separated fields |
| WHERE | `geospatial_lat/lon_units` | verolago | (but definitely Req in latitude and longitude variable attributes) |
| WHERE | `geospatial_lat/lon_units` | novantonio | WGS84 |
| WHERE | `geospatial_lon_min/max` | novantonio | and you need 2 separated fields |
| WHERE | `geospatial_vertical_min/max` | novantonio | and you need 2 separated fields |
| WHERE | `geospatial_vertical_positive` | verolago | (but definitely mandatory in depth variable attributes) |
| WHERE | `geospatial_vertical_positive` | novantonio | it is depth and, considering that we need to be interoperable with other topics z is negative in the water and positive in the air |
| WHERE | `geospatial_vertical_units` | verolago | (but definitely mandatory in depth variable attributes) |
| WHERE | `sea_name` | verolago | (a vessel could start a deployment within the limit of one sea and finish outside, depending on boundary definition for example) |
| WHEN | `date_modified` | verolago | (already covered in other fields, but good to add) |
| WHEN | `local_time_zone` | verolago | (a vessel count start a deployment in a timezone and finish in another, UTC should be compulsory) |
| WHEN | `time_coverage_resolution` | verolago | (time coverage resolution varies within a file in the case of ZT sensor) |
| WHO | `acknowledgment` | verolago | (That is where we acknowledge indigenous data collection also) |
| WHO | `contributor_name/role` | novantonio | ORCID |
| WHO | `creator_email` | verolago | (e.g. need to be contactable if there is issues with the data) |
| WHO | `creator_institution` | novantonio | ROR |
| WHO | `creator_type` | verolago | (unsure) |
| WHO | `institution` | novantonio | ROR |
| WHO | `principal_investigator` | novantonio | ORCID |
| WHO | `publisher_name` | verolago | (in our case, we have to use AODN, can't change) |
| WHO | `publisher_name` | novantonio | ROR |
| HOW | `citation` | novantonio | use a DOI (e.g. in EU now all the projects have a CORDIS DOI) |
| HOW | `comment` | verolago | (we put the calculation method for depth from pressure, that information should at least be somewhere in the file) |
| HOW | `license` | verolago | (we can't change ours, although we might all have the same) |
| HOW | `license` | novantonio | (and hopefully CC-BY) - without license you cannot interoperate data, so you're not FAIR |
| HOW | `processing_level` | verolago | (same as file_version_quality_control?) |
| HOW | `processing_level` | novantonio | https://vocab.nerc.ac.uk/collection/EPL/current/ |
| HOW | `quality_control_log` | novantonio | https://vocab.nerc.ac.uk/collection/L20/current/ |
| HOW | `references` | verolago | (we have the link to the OBPS, when FVON has best practices also it should go here as well) |
| HOW | `references` | novantonio | if we add the practice (Best practice) it should be a doi pointing to https://repository.oceanbestpractices.org/home, if the practice is not there you're welcome to submit |
| HOW | `source` | verolago | (Could be where we put the attribution to FVON? IMOS has this example: "source = “Radar Observation” ", so for FVON it could be: "source = "FVON " " |
| HOW | `source` | novantonio | https://vocab.nerc.ac.uk/collection/L05/current/, or we can ask to set up a FVON categories |

</details>

Voters: CarlesODN, verolago, novantonio, TetsutaroTakikawa. Not every voter filled in every attribute. Ballots cast on the earlier scale count as: Recommended or Suggested = Optional, Not recommended = Not applicable. Scope: FVON = one value for all networks, NET = set once per network, FILE = varies per file.

Generated by [`scripts/tally.py`](scripts/tally.py) from the ballots in the [Discussions](https://github.com/FVON-GOOS/global-attributes/discussions); do not edit by hand. Every ballot line is in [`results/ballots.csv`](results/ballots.csv).
