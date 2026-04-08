import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database credentials
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "music_analysis")

# Construct SQLAlchemy engine URIs
# We use psycopg2 driver for PostgreSQL
DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URI)

def clean_column_names(df):
    """Standardize column names for database insertion"""
    df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('-', '_')
    return df

def load_billboard():
    file_path = "data/raw/billboardhot1002025.csv"
    if not os.path.exists(file_path):
        print(f"Warning: File {file_path} not found.")
        return
        
    print("Loading Billboard Hot 100 data...")
    df = pd.read_csv(file_path)
    df = clean_column_names(df)
    
    # Ensure column names match SQL schema
    # Rename specific columns if necessary based on your raw CSV header
    # Example: df.rename(columns={'song_name': 'song'}, inplace=True)
    
    # We only insert columns that match our schema
    expected_cols = ['week_date', 'song', 'artist', 'rank', 'peak_position', 'weeks_on_chart']
    available_cols = [c for c in expected_cols if c in df.columns]
    
    # Clean numeric columns that might contain '-' or other text
    for col in ['rank', 'peak_position', 'weeks_on_chart']:
        if col in available_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # In pandas to_sql, if we don't pass the ID, PostgreSQL SERIAL handles it automatically
    df[available_cols].to_sql('billboard', engine, if_exists='append', index=False)
    print(f"Successfully loaded {len(df)} rows to 'billboard' table.")

def load_grammys():
    file_path = "data/raw/grammyawardwinnerandnominee1958-2024.csv"
    if not os.path.exists(file_path):
        print(f"Warning: File {file_path} not found.")
        return
        
    print("Loading Grammy Awards data...")
    df = pd.read_csv(file_path)
    df = clean_column_names(df)
    
    # Ensure column names match SQL schema
    # Example mappings assuming typical CSV structure
    if 'year' in df.columns:
        df.rename(columns={'year': 'award_year'}, inplace=True)
        
    expected_cols = ['award_year', 'category', 'nominee', 'artist', 'winner']
    available_cols = [c for c in expected_cols if c in df.columns]

    df[available_cols].to_sql('grammys', engine, if_exists='append', index=False)
    print(f"Successfully loaded {len(df)} rows to 'grammys' table.")

if __name__ == "__main__":
    print("Starting data loading process...")
    try:
        # load_billboard() # Already loaded
        load_grammys()
        print("Data loading complete!")
    except Exception as e:
        print(f"Error occurred during execution: {e}")
