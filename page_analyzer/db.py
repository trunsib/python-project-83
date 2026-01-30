import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    database_url = os.getenv('DATABASE_URL')

    if not database_url:
        database_url = "postgresql://postgres:postgres@localhost:5432/postgres"

    return psycopg2.connect(
        database_url,
        cursor_factory=RealDictCursor
    )
