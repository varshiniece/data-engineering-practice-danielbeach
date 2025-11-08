import requests
import os
import zipfile

download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",  # invalid URL (will 404)
]


def main():
    directory = "downloads"
    os.makedirs(directory, exist_ok=True)

    for uri in download_uris:
        filename = uri.split("/")[-1]
        file_path = os.path.join(directory, filename)
        print(f"⬇️  Downloading {filename}...")

        try:
            # --- Download the file ---
            response = requests.get(uri, stream=True)
            response.raise_for_status()  # will raise HTTPError for 4xx/5xx responses

            # --- Save the file ---
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"✅ Download complete: {file_path}")

        except requests.exceptions.HTTPError as e:
            print(f"❌ Failed to download {uri}: {e}")
            continue  # ⛔ skip extraction if download failed
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error for {uri}: {e}")
            continue

        # --- Extract only if file exists ---
        if os.path.exists(file_path):
            try:
                with zipfile.ZipFile(file_path, "r") as zip_ref:
                    zip_ref.extractall(directory)
                    print(f"📦 Extracted CSV files from {filename}")
                os.remove(file_path)
                print(f"🗑️  Deleted zip file: {filename}\n")
            except zipfile.BadZipFile:
                print(f"❌ Corrupted or invalid zip file: {filename}")
        else:
            print(f"⚠️  File not found after download: {file_path}\n")


if __name__ == "__main__":
    main()
