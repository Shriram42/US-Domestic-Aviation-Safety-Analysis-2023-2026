import os
import glob
import pandas as pd

# Look in the script's folder AND the parent Downloads folder
script_dir = os.path.dirname(os.path.abspath(__file__))
search_paths = [
    os.path.join(script_dir, "aids-20261114200918*"),
    os.path.join(os.path.dirname(script_dir), "aids-20261114200918*")
]

matched_files = []
for pattern in search_paths:
    matched_files.extend(glob.glob(pattern))

if not matched_files:
    raise FileNotFoundError("Could not find File, please check file name and/or location.")

file_path = matched_files[0]
print(f"Found file: {file_path}")
df = pd.read_csv(file_path, low_memory=False)

# 3. Keep Domestic U.S. records only (exclude 'ZZ' foreign code and missing states)
us_states_territories = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID",
    "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS",
    "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK",
    "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV",
    "WI", "WY", "DC", "PR", "VI", "GU", "AS", "MP"
}
df["State"] = df["State"].str.strip().str.upper()
df = df[df["State"].isin(us_states_territories)]

# 4. Standardize Aircraft Make names
make_mapping = {
    "CESSNA AIRCRAFT CO": "CESSNA",
    "TEXTRON AVIATION INC": "CESSNA",
    "PIPER AIRCRAFT INC": "PIPER",
    "PIPER AIRCRAFT CORPORATION": "PIPER",
    "NEW PIPER AIRCRAFT INC": "PIPER",
    "BOEING COMPANY": "BOEING",
    "AIRBUS INDUSTRIE": "AIRBUS",
    "AIRBUS SAS": "AIRBUS",
    "AIRBUS S A S": "AIRBUS",
    "BEECHCRAFT": "BEECH",
    "BEECHCRAFT CORP": "BEECH",
    "HAWKER BEECHCRAFT CORP": "BEECH",
    "RAYTHEON AIRCRAFT COMPANY": "BEECH",
    "ROBINSON HELICOPTER": "ROBINSON",
    "ROBINSON HELICOPTER CO": "ROBINSON",
    "ROBINSON HELICOPTER COMPANY": "ROBINSON",
    "CIRRUS": "CIRRUS DESIGN CORP",
    "BOMBARDIER": "BOMBARDIER INC",
    "BOMBARIER": "BOMBARDIER INC",
    "EMBRAER S A": "EMBRAER",
    "EMBRAER EXECUTIVE AIRCRAFT INC": "EMBRAER",
    "EMBRAER-EMPRESA BRASILEIRA DE": "EMBRAER"
}
df["Aircraft Make Clean"] = df["Aircraft Make"].replace(make_mapping).fillna("UNKNOWN")

# 5. Clean truncated labels and missing fields
df["Flight Phase"] = df["Flight Phase"].replace({"Ground/Ramp/Ma": "Ground/Ramp/Maintenance"}).fillna("Unknown")
df["Aircraft Damage"] = df["Aircraft Damage"].fillna("Unknown")
df["PIC Certification Type"] = df["PIC Certification Type"].fillna("UNSPECIFIED")

# 6. Deduplicate by Report Number (prevents double-counting multi-pilot/multi-aircraft events)
cleaned_df = df.groupby("Report Number", as_index=False).agg({
    "Event Date": "first",
    "City": "first",
    "State": "first",
    "Airport": "first",
    "Event Type": "first",
    "Aircraft Damage": "first",
    "Flight Phase": "first",
    "Aircraft Make Clean": "first",
    "Aircraft Model": "first",
    "Flight Conduct Code": "first",
    "Total Fatalities": "max",
    "Total Injuries": "max",
    "Engine Make": "first",
    "PIC Certification Type": lambda x: ", ".join(sorted(set(x.dropna())))
})

# 7. Save final dataset for Tableau
output_file = os.path.join(script_dir, "faa_domestic_2023_2026_tableau.csv")
cleaned_df.to_csv(output_file, index=False)
print(f"Success! Exported {len(cleaned_df)} clean domestic records to {output_file}.")

