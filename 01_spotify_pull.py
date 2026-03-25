import os
import time
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from tqdm import tqdm

load_dotenv()

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5433")
DB_NAME = os.getenv("DB_NAME", "music_analysis")

DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URI)

client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

if not client_id or not client_secret:
    print("Spotify API credentials missing in .env")
    exit(1)

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager, requests_timeout=10, retries=3)

def get_unique_songs(limit=500):
    query = f"""
    SELECT DISTINCT song, artist 
    FROM billboard 
    WHERE song NOT IN (SELECT song FROM spotify_features)
    LIMIT {limit};
    """
    return pd.read_sql(query, engine)

def fetch_spotify_data(df):
    features_list = []
    
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        song = row['song']
        artist = row['artist']
        
        try:
            # Search for the track
            # Removing special characters can help Spotify search
            clean_song = song.split('(')[0].strip() 
            clean_artist = artist.split('Featuring')[0].split('&')[0].strip()
            
            query = f"track:{clean_song} artist:{clean_artist}"
            results = sp.search(q=query, type='track', limit=1)
            items = results['tracks']['items']
            
            if len(items) > 0:
                track = items[0]
                track_id = track['id']
                
                # Try fetching audio features (often returns 403 now due to Spotify API changes)
                features = None
                try:
                    audio_features_result = sp.audio_features([track_id])
                    if audio_features_result and audio_features_result[0]:
                        features = audio_features_result[0]
                except spotipy.exceptions.SpotifyException as e:
                    if e.http_status == 429:
                        print("Rate limit reached. Stopping.")
                        break
                    print(f"API Error {e.http_status} for {song} by {artist}")
                    features = None
                
                if features:
                    features_list.append({
                        'song': song,
                        'artist': artist,
                        'spotify_id': track_id,
                        'duration_ms': features.get('duration_ms'),
                        'danceability': features.get('danceability'),
                        'energy': features.get('energy'),
                        'valence': features.get('valence'),
                        'tempo': features.get('tempo'),
                        'acousticness': features.get('acousticness'),
                        'instrumentalness': features.get('instrumentalness'),
                        'speechiness': features.get('speechiness'),
                        'loudness': features.get('loudness')
                    })
            
            time.sleep(0.05) # Rate limiting mitigation
                
        except Exception as e:
            # Skip on error and continue to the next song
            continue
            
    return pd.DataFrame(features_list)

if __name__ == "__main__":
    print("Fetching unique songs from database...")
    # NOTE: To get 10,000 songs, increase limit. Using 500 here to avoid hitting Spotify rate limits quickly.
    limit = 500
    df_songs = get_unique_songs(limit)
    
    # Inject international songs into the dataframe
    international_songs = pd.DataFrame([
        {'song': 'Dynamite', 'artist': 'BTS'},
        {'song': 'Butter', 'artist': 'BTS'},
        {'song': 'Tum Hi Ho', 'artist': 'Arijit Singh'},
        {'song': 'Chaleya', 'artist': 'Arijit Singh'},
        {'song': 'Despacito', 'artist': 'Luis Fonsi, Daddy Yankee'},
        {'song': 'Danza Kuduro', 'artist': 'Don Omar, Lucenzo'},
        {'song': 'Cupid', 'artist': 'FIFTY FIFTY'},
        {'song': 'Me Porto Bonito', 'artist': 'Bad Bunny'},
        {'song': 'As It Was', 'artist': 'Harry Styles'}, # UK
        {'song': 'Water', 'artist': 'Tyla'}, # South Africa
        {'song': 'Calm Down', 'artist': 'Rema, Selena Gomez'}, # Nigeria
        {'song': 'La Fama', 'artist': 'Rosalia'} # Spain
    ])
    
    # Exclude any international songs already in df_songs to avoid duplicates
    existing_pairs = set(zip(df_songs['song'], df_songs['artist']))
    international_songs = international_songs[~international_songs.apply(lambda row: (row['song'], row['artist']) in existing_pairs, axis=1)]
    
    df_songs = pd.concat([df_songs, international_songs], ignore_index=True)

    if len(df_songs) == 0:
        print("No new songs to process.")
        exit(0)
        
    print(f"Processing {len(df_songs)} songs from Spotify API...")
    df_features = fetch_spotify_data(df_songs)
    
    if not df_features.empty:
        print(f"Saving {len(df_features)} extracted features to database...")
        df_features.to_sql('spotify_features', engine, if_exists='append', index=False)
        print("Successfully saved Spotify features.")
        
        # Export to CSV for processed files
        csv_path = "data/processed/spotify_features.csv"
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        df_features.to_csv(csv_path, mode='a', header=not os.path.exists(csv_path), index=False)
        print(f"Also exported features to {csv_path}")
    else:
        print("No features extracted.")
