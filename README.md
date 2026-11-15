# U.S. Domestic Aviation Safety Analysis (2023–2026)
An interactive aviation safety dashboard analyzing 6,852 U.S. domestic aviation events using Federal Aviation Administration (FAA) data from March 2023 through October 2026.

This project demonstrates an end-to-end analytics workflow, from cleaning and transforming raw aviation records with Python to developing an interactive Tableau dashboard for exploring incident severity, aircraft manufacturer comparisons, and geographic patterns.

## Key Findings

 - 6,852 aviation events analyzed, including 3,470 accidents and 3,382 incidents.

 - 1,009 fatalities and 1,681 injuries recorded across the dataset.

 - Florida, Texas, and California had the highest recorded event counts.

 - Cessna and Piper were the most frequently represented aircraft manufacturers.

## Technical Approach

 - Obtained aviation accident and incident records from the FAA Accident and Incident Data System (AIDS).

 - Used Python and Pandas to filter records to U.S. states and territories.

 - Standardized inconsistent aircraft manufacturer names and categorical fields.

 - Handled missing values and corrected truncated labels.

 - Deduplicated records using FAA report numbers and aggregated event-level information.

## Data Visualization

Developed an interactive Tableau dashboard featuring:

 - KPI indicators for total aviation events, fatalities, and injuries.

 - Fatal versus non-fatal event comparisons.

 - Boeing versus Airbus event distributions.

 - Geographic hotspot mapping across U.S. states.

## Data Source

[FAA Aviation Accident & Incident Data](https://asip.faa.gov/explore/aids/search)

## Limitations

This analysis uses a subset of FAA records covering March 2023–October 2026. Event counts are not normalized by flight activity, fleet size, or aircraft operating hours. Report-level aggregation may also omit details associated with multiple aircraft in the same report.
