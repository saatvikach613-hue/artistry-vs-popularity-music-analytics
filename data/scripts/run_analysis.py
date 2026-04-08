import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5433")
DB_NAME = os.getenv("DB_NAME", "music_analysis")

DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URI)

sql_files = [
    "data/sql/02_era_classification.sql",
    "data/sql/03_q1_virality.sql",
    "data/sql/04_q2_longevity.sql",
    "data/sql/05_q3_grammy.sql",
    "data/sql/06_kpi_exports.sql"
]

with engine.begin() as conn:
    for sql_file in sql_files:
        print(f"Executing {sql_file}...")
        with open(sql_file, "r") as f:
            sql_script = f.read()
            for statement in sql_script.split(';'):
                if statement.strip():
                    conn.execute(text(statement))

print("Analysis SQL execution complete!")
