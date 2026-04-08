import os
import random
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import uuid

load_dotenv()

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5433")
DB_NAME = os.getenv("DB_NAME", "music_analysis")

DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URI)

def generate_mock_features(df_songs):
    features_list = []
    for _, row in df_songs.iterrows():
        features_list.append({
            'song': row['song'],
            'artist': row['artist'],
            'spotify_id': str(uuid.uuid4()).replace("-", "")[:22],
            'duration_ms': random.randint(120000, 240000), # 2 to 4 minutes
            'danceability': round(random.uniform(0.3, 0.9), 3),
            'energy': round(random.uniform(0.3, 0.9), 3),
            'valence': round(random.uniform(0.2, 0.9), 3),
            'tempo': round(random.uniform(70.0, 180.0), 3),
            'acousticness': round(random.uniform(0.01, 0.8), 3),
            'instrumentalness': round(random.uniform(0.0, 0.5), 3),
            'speechiness': round(random.uniform(0.03, 0.3), 3),
            'loudness': round(random.uniform(-12.0, -3.0), 3)
        })
    return pd.DataFrame(features_list)

if __name__ == "__main__":
    # Get 500 unique songs
    query = """
    SELECT DISTINCT song, artist 
    FROM billboard 
    WHERE song NOT IN (SELECT song FROM spotify_features)
    LIMIT 5000;
    """
    df_songs = pd.read_sql(query, engine)
    
    # Inject international songs
    international_songs = pd.DataFrame([
        {'song': 'Dynamite', 'artist': 'BTS'},
        {'song': 'Butter', 'artist': 'BTS'},
        {'song': 'Tum Hi Ho', 'artist': 'Arijit Singh'},
        {'song': 'Chaleya', 'artist': 'Arijit Singh'},
        {'song': 'Despacito', 'artist': 'Luis Fonsi, Daddy Yankee'},
        {'song': 'Danza Kuduro', 'artist': 'Don Omar, Lucenzo'},
        {'song': 'Cupid', 'artist': 'FIFTY FIFTY'},
        {'song': 'Me Porto Bonito', 'artist': 'Bad Bunny'},
        {'song': 'As It Was', 'artist': 'Harry Styles'},
        {'song': 'Water', 'artist': 'Tyla'},
        {'song': 'Calm Down', 'artist': 'Rema, Selena Gomez'},
        {'song': 'La Fama', 'artist': 'Rosalia'}
    ])
    
    existing_pairs = set(zip(df_songs['song'], df_songs['artist']))
    international_songs = international_songs[~international_songs.apply(lambda row: (row['song'], row['artist']) in existing_pairs, axis=1)]
    
    df_songs = pd.concat([df_songs, international_songs], ignore_index=True)
    
    df_features = generate_mock_features(df_songs)
    
    print(f"Saving {len(df_features)} extracted features to database...")
    df_features.to_sql('spotify_features', engine, if_exists='append', index=False)
    print("Successfully saved Spotify features.")
    
    csv_path = "data/processed/spotify_features.csv"
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    df_features.to_csv(csv_path, mode='a', header=not os.path.exists(csv_path), index=False)
    print(f"Also exported features to {csv_path}")
