-- data/sql/04_q2_longevity.sql
-- Q2: Are songs getting shorter and more upbeat? Longevity analysis.
-- Examines how audio features change across eras.

DROP VIEW IF EXISTS longevity_analysis CASCADE;
CREATE OR REPLACE VIEW longevity_analysis AS
SELECT 
    e.musical_era,
    e.debut_year,
    CASE 
        WHEN e.debut_year < 2005 THEN 'Pre-Social'
        WHEN e.debut_year <= 2015 THEN 'Early Social'
        ELSE 'TikTok Era'
    END as era_3,
    (AVG(s.duration_ms) / 1000.0) / 60.0 as avg_duration_minutes,
    AVG(s.danceability) as avg_danceability,
    AVG(s.energy) as avg_energy,
    AVG(s.tempo) as avg_tempo,
    COUNT(s.id) as track_count
FROM track_eras e
JOIN spotify_features s ON e.song = s.song AND e.artist = s.artist
GROUP BY e.musical_era, e.debut_year, 
    CASE 
        WHEN e.debut_year < 2005 THEN 'Pre-Social'
        WHEN e.debut_year <= 2015 THEN 'Early Social'
        ELSE 'TikTok Era'
    END
ORDER BY e.debut_year;
