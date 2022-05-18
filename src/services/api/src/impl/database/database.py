from importlib.metadata import MetadataPathFinder
from os import getenv

from databases import Database
from dotenv import load_dotenv
from sqlalchemy import MetaData

load_dotenv()

if not (DB_URI := getenv("DB_URI")):
    raise RuntimeError("Please provide a DB_URI field in your .env file.")


metadata = MetaData()
database = Database(DB_URI)
