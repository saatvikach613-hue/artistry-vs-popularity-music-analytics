from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5433")
DB_NAME = os.getenv("DB_NAME", "music_analysis")

DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URI)

with engine.begin() as conn:
    conn.execute(text("ALTER TABLE grammys ALTER COLUMN category TYPE TEXT;"))
    conn.execute(text("ALTER TABLE grammys ALTER COLUMN nominee TYPE TEXT;"))
    conn.execute(text("ALTER TABLE grammys ALTER COLUMN artist TYPE TEXT;"))
print("Altered grammys table")
