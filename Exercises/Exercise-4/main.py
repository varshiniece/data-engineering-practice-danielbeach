import os
import json
import pandas as pd
from glob import glob

def flatten_json_file(json_file_path):
    """Load and flatten a JSON file, returning a DataFrame."""
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Normalize (flatten) JSON
    if isinstance(data, list):
        df = pd.json_normalize(data)
    else:
        df = pd.json_normalize([data])  # wrap in list if single object
    return df


def convert_all_json_to_csv(data_dir):
    """Walk through directory, convert each JSON file to CSV."""
    json_files = glob(os.path.join(data_dir, '**', '*.json'), recursive=True)

    if not json_files:
        print(f"No JSON files found in {data_dir}")
        return

    for json_path in json_files:
        try:
            df = flatten_json_file(json_path)
            csv_path = os.path.splitext(json_path)[0] + '.csv'
            df.to_csv(csv_path, index=False)
            print(f"✅ Converted: {json_path} → {csv_path}")
        except Exception as e:
            print(f"❌ Failed to process {json_path}: {e}")


if __name__ == "__main__":
    data_directory = r"C:\Users\varshini.chitti_sids\VData\data-engineering-practice\Exercises\Exercise-4\data"  # Change if needed
    convert_all_json_to_csv(data_directory)
