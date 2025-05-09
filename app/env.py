import os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

print(DATABASE_URL)

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
# PROJECT_DIR/models/*.py
ORM_DIR = os.path.join(PROJECT_DIR, "models")
