-- data/sql/01_schema.sql

-- Drop tables if they exist to allow clean reruns
DROP TABLE IF EXISTS artist_summary;
DROP TABLE IF EXISTS spotify_features;
DROP TABLE IF EXISTS grammys;
DROP TABLE IF EXISTS billboard;

-- Billboard Hot 100 Table
CREATE TABLE billboard (
    id SERIAL PRIMARY KEY,
    week_date DATE,
    song VARCHAR(255),
    artist VARCHAR(255),
    rank INT,
    peak_position INT,
    weeks_on_chart INT
);

-- Index for faster joins and grouping
CREATE INDEX idx_billboard_song_artist ON billboard(song, artist);

-- Grammy Awards Table
CREATE TABLE grammys (
    id SERIAL PRIMARY KEY,
    award_year INT,
    category TEXT,
    nominee TEXT,
    artist TEXT,
    winner BOOLEAN
);

CREATE INDEX idx_grammys_artist ON grammys(artist);
CREATE INDEX idx_grammys_nominee ON grammys(nominee);

-- Spotify Audio Features Table
CREATE TABLE spotify_features (
    id SERIAL PRIMARY KEY,
    song VARCHAR(255),
    artist VARCHAR(255),
    spotify_id VARCHAR(255),
    duration_ms INT,
    danceability DECIMAL(5, 4),
    energy DECIMAL(5, 4),
    valence DECIMAL(5, 4),
    tempo DECIMAL(6, 3),
    acousticness DECIMAL(5, 4),
    instrumentalness DECIMAL(6, 5),
    speechiness DECIMAL(5, 4),
    loudness DECIMAL(5, 2)
);

CREATE INDEX idx_spotify_song_artist ON spotify_features(song, artist);

-- Artist Summary Table (will be populated by our SQL analytics scripts)
CREATE TABLE artist_summary (
    artist VARCHAR(255) PRIMARY KEY,
    career_span_years INT,
    avg_chart_rank DECIMAL(5, 2),
    total_weeks_on_chart INT,
    grammy_wins INT,
    grammy_nominations INT,
    avg_danceability DECIMAL(5, 4),
    avg_energy DECIMAL(5, 4)
);
