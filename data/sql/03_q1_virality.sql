-- data/sql/03_q1_virality.sql
-- Q1: What characterizes a "viral" or highly popular hit? 
-- Examines Spotify features vs Peak Position.

DROP VIEW IF EXISTS virality_analysis CASCADE;
CREATE OR REPLACE VIEW virality_analysis AS
WITH track_performance AS (
    SELECT 
        song, 
        artist, 
        MIN(peak_position) as best_peak_position,
        COALESCE(MAX(weeks_on_chart), 1) as total_weeks
    FROM billboard
    GROUP BY song, artist
)
SELECT 
    t.song,
    t.artist,
    e.musical_era,
    CASE 
        WHEN e.debut_year < 2005 THEN 'Pre-Social'
        WHEN e.debut_year <= 2015 THEN 'Early Social'
        ELSE 'TikTok Era'
    END as era_3,
    t.best_peak_position,
    t.total_weeks,
    s.danceability,
    s.energy,
    s.valence,
    s.tempo,
    s.acousticness,
    NTILE(4) OVER (ORDER BY t.best_peak_position ASC) as peak_quartile,
    CASE 
        WHEN t.best_peak_position = 1 THEN 'No. 1 Hit'
        WHEN t.best_peak_position <= 10 THEN 'Top 10 Hit'
        WHEN t.best_peak_position <= 40 THEN 'Top 40 Hit'
        ELSE 'Lower Chart'
    END as hit_category
FROM track_performance t
JOIN spotify_features s ON t.song = s.song AND t.artist = s.artist
LEFT JOIN track_eras e ON t.song = e.song AND t.artist = e.artist;
