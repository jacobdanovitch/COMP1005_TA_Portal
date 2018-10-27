import os
from glob import glob
import json
from pathlib import Path

config_file = glob("./configs/a[1-9]*.json")[-1]

with open(config_file, "r") as f:
    config = json.load(f)

TEST_CASES = config['test_cases']
ASSIGNMENT_NUM = config['assignment_num']

ROOT_DIR = ("." if os.environ.get("FLASK_ENV") == "development" else "./COMP1005_TA_Portal")
MARKING_SCHEME = Path(os.path.join(ROOT_DIR, "solutions", f"a{ASSIGNMENT_NUM}", "marking.json"))

MARKED_BY = config['marked_by']

first, last = MARKED_BY.split()
EMAIL = f"{first}.{last}@carleton.ca".lower()

