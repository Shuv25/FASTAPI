import os
import mysql.connector
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(".env")
load_dotenv(dotenv_path=env_path,override=True)


mydb= mysql.connector.connect(
    host = os.getenv("host"),
    username = os.getenv("username"),
    password = os.getenv("password"),
    database = os.getenv("database")
)

try:
    if mydb:
        print("Database is connected")
except Exception as e:
    raise (f"Database is not connected due to this error {e}")

cursor = mydb.cursor(dictionary=True)
