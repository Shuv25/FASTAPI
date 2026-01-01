import json
from typing import List

DATA_FILE = "records.json"


def read_data():
    """Uilty function for reading the reords"""
    try:
        with open(DATA_FILE,'r') as f:
            data = json.load(f)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def write_data(data:List[dict])-> None:
    """Utility function for writing the records"""
    try:
        with open(DATA_FILE,'w') as f:
            json.dump(data,f,indent=4)
    except(FileNotFoundError):
        raise    