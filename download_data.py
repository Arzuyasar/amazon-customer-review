from pathlib import Path
import subprocess
import sys

DATASET = "cynthiarempel/amazon-us-customer-reviews-dataset"

FILES = [
    "amazon_reviews_us_Electronics_v1_00.tsv",
    "amazon_reviews_us_Video_Games_v1_00.tsv",
    "amazon_reviews_us_Mobile_Electronics_v1_00.tsv",
]

OUT_DIR = Path("data")
OUT_DIR.mkdir(exist_ok=True)

for file_name in FILES:
    print(f"Downloading {file_name}...")

    subprocess.run(
        [
            sys.executable,
            "-m",
            "kaggle",
            "datasets",
            "download",
            "-d",
            DATASET,
            "-f",
            file_name,
            "-p",
            str(OUT_DIR),
            "--unzip",
        ],
        check=True,
    )

print(f"Downloaded files to: {OUT_DIR.resolve()}")
