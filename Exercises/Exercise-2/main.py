import os
import requests
from bs4 import BeautifulSoup 
import pandas as pd

BASE_URL = "https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/"
DOWNLOAD_DIR = "downloads_weather_2021"
TARGET_TIMESTAMP = "2024-01-19 14:58"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def find_file_by_timestamp():
    """Finds the file in the NOAA directory with a given last modified timestamp."""
    response = requests.get(BASE_URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.find_all("tr")

    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 2:
            file_name = cols[0].get_text(strip=True)
            last_modified = cols[1].get_text(strip=True)
            if TARGET_TIMESTAMP in last_modified:
                return file_name

    return None


def download_file(filename):
    """Downloads the file from NOAA to local disk."""
    file_url = BASE_URL + filename
    file_path = os.path.join(DOWNLOAD_DIR, filename)
    print(f"⬇️ Downloading {filename} ...")

    response = requests.get(file_url, stream=True)
    response.raise_for_status()

    with open(file_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"✅ Download complete: {file_path}")
    return file_path


def analyze_weather_data(file_path):
    """Reads the CSV and prints the record(s) with the highest HourlyDryBulbTemperature."""
    print("📊 Reading file with pandas...")
    df = pd.read_csv(file_path)

    # if "HourlyDryBulbTemperature" not in df.columns:
    #     print("❌ Column 'HourlyDryBulbTemperature' not found in CSV.")
    #     print("Available columns:", list(df.columns))
    #     return

    # Convert temperature column to numeric
    df["HourlyDryBulbTemperature"] = pd.to_numeric(df["HourlyDryBulbTemperature"], errors="coerce")

    max_temp = df["HourlyDryBulbTemperature"].max()
    hottest_records = df[df["HourlyDryBulbTemperature"] == max_temp]

    print("\n🔥 Highest HourlyDryBulbTemperature record(s):")
    print(hottest_records)
    print("\n🌡️ Max Temperature:", max_temp)


def main():
    print("🔍 Searching for file last modified on", TARGET_TIMESTAMP)
    filename = find_file_by_timestamp()

    if not filename:
        print("❌ No file found with that timestamp.")
        return

    print(f"✅ Found file: {filename}")
    file_path = download_file(filename)
    analyze_weather_data(file_path)


if __name__ == "__main__":
    main()
