import os
import requests
import pandas as pd

# ---------------------------------
# Output Folder
# ---------------------------------
OUTPUT_FOLDER = "data/raw/live_nav"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ---------------------------------
# Mutual Fund Scheme Codes
# ---------------------------------
funds = {
    "HDFC_Top_100": 125497,
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_Large_Cap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841
}

print("=" * 80)
print("Fetching Live NAV Data")
print("=" * 80)

# ---------------------------------
# Download NAV
# ---------------------------------
for fund_name, scheme_code in funds.items():

    url = f"https://api.mfapi.in/mf/{scheme_code}"

    print(f"\nDownloading {fund_name}...")

    try:

        response = requests.get(url, timeout=20)

        if response.status_code == 200:

            data = response.json()

            nav_df = pd.DataFrame(data["data"])

            nav_df["Scheme Code"] = scheme_code
            nav_df["Scheme Name"] = data["meta"]["scheme_name"]

            nav_df.to_csv(
                os.path.join(
                    OUTPUT_FOLDER,
                    f"{fund_name}.csv"
                ),
                index=False
            )

            print("✓ Saved Successfully")
            print("Records:", len(nav_df))

        else:

            print("Request Failed:", response.status_code)

    except Exception as e:

        print("Error:", e)

print("\n")
print("=" * 80)
print("Completed")
print("=" * 80)