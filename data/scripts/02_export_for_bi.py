import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5433")
DB_NAME = os.getenv("DB_NAME", "music_analysis")

DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URI)

export_dir = "data/processed/bi_exports"
os.makedirs(export_dir, exist_ok=True)

views_to_export = [
    "track_eras",
    "virality_analysis",
    "longevity_analysis",
    "grammy_analysis",
    "artist_summary_tier"
]

print("Starting BI Data Export...")

for view in views_to_export:
    print(f"Exporting {view}...")
    try:
        df = pd.read_sql(f"SELECT * FROM {view}", engine)
        
        # Save to BI export folder
        csv_path = os.path.join(export_dir, f"{view}.csv")
        df.to_csv(csv_path, index=False)
        print(f" -> Saved {len(df)} records to {csv_path}")
        
    except Exception as e:
        print(f"Error exporting {view}: {e}")

print("BI Data Export Complete!")
