-- data/sql/06_kpi_exports.sql
-- Populate the artist_summary table and prepare views for BI extraction

TRUNCATE TABLE artist_summary;

INSERT INTO artist_summary (
    artist, career_span_years, avg_chart_rank, total_weeks_on_chart, 
    grammy_wins, grammy_nominations, avg_danceability, avg_energy
)
WITH artist_career AS (
    SELECT 
        artist,
        EXTRACT(YEAR FROM MAX(week_date)) - EXTRACT(YEAR FROM MIN(week_date)) as career_span_years,
        AVG(rank) as avg_chart_rank,
        SUM(weeks_on_chart) as total_weeks_on_chart,
        COUNT(DISTINCT song) as chart_hits
    FROM billboard
    GROUP BY artist
),
artist_grammy AS (
    SELECT 
        artist,
        SUM(CASE WHEN winner THEN 1 ELSE 0 END) as grammy_wins,
        COUNT(*) as grammy_nominations
    FROM grammys
    GROUP BY artist
),
artist_features AS (
    SELECT 
        artist,
        AVG(danceability) as avg_danceability,
        AVG(energy) as avg_energy
    FROM spotify_features
    GROUP BY artist
)
SELECT 
    c.artist,
    c.career_span_years,
    c.avg_chart_rank,
    COALESCE(c.total_weeks_on_chart, 1) as total_weeks_on_chart,
    COALESCE(g.grammy_wins, 0),
    COALESCE(g.grammy_nominations, 0),
    f.avg_danceability,
    f.avg_energy
FROM artist_career c
LEFT JOIN artist_grammy g ON c.artist = g.artist
LEFT JOIN artist_features f ON c.artist = f.artist;

-- View for Artist Tier
CREATE OR REPLACE VIEW artist_summary_tier AS
SELECT 
    artist,
    career_span_years,
    avg_chart_rank,
    total_weeks_on_chart,
    grammy_wins,
    grammy_nominations,
    avg_danceability,
    avg_energy,
    CASE 
        WHEN career_span_years < 2 AND total_weeks_on_chart <= 20 THEN 'One-Hit Wonder'
        WHEN career_span_years < 5 THEN 'Short Career'
        WHEN career_span_years <= 15 THEN 'Mid Career'
        ELSE 'Sustained Career (15+ Years)'
    END as artist_tier,
    CASE 
        WHEN avg_danceability IS NULL THEN 'No Audio Data'
        ELSE 'Has Audio Data'
    END as has_audio_data
FROM artist_summary;
