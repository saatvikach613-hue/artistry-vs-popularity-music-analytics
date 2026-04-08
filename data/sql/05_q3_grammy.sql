-- data/sql/05_q3_grammy.sql
-- Q3: Do Grammys align with Billboard Popularity?
-- Compare Grammy nominated/winning tracks vs regular hits within era context.

DROP VIEW IF EXISTS grammy_analysis CASCADE;
CREATE OR REPLACE VIEW grammy_analysis AS
WITH grammy_artists AS (
    SELECT 
        artist,
        MIN(award_year) as first_grammy_year,
        SUM(CASE WHEN winner THEN 1 ELSE 0 END) as wins,
        COUNT(*) as nominations
    FROM grammys
    GROUP BY artist
),
billboard_performance AS (
    SELECT 
        b.song,
        b.artist,
        e.musical_era,
        CASE 
            WHEN e.debut_year < 2005 THEN 'Pre-Social'
            WHEN e.debut_year <= 2015 THEN 'Early Social'
            ELSE 'TikTok Era'
        END as era_3,
        e.debut_year,
        MIN(b.peak_position) as track_peak,
        MAX(b.weeks_on_chart) as track_weeks
    FROM billboard b
    LEFT JOIN track_eras e ON b.song = e.song AND b.artist = e.artist
    GROUP BY b.song, b.artist, e.musical_era, e.debut_year
)
SELECT 
    bp.artist,
    bp.song,
    bp.musical_era,
    bp.era_3,
    bp.track_peak,
    COALESCE(bp.track_weeks, 1) as total_weeks_on_chart,
    COALESCE(g.wins, 0) as grammy_wins,
    COALESCE(g.nominations, 0) as grammy_nominations,
    CASE WHEN g.wins > 0 THEN 'Grammy Winner'
         WHEN g.nominations > 0 THEN 'Grammy Nominee'
         ELSE 'No Grammy' 
    END as grammy_status,
    CASE 
         WHEN g.first_grammy_year IS NOT NULL AND bp.debut_year < g.first_grammy_year THEN 'Pre-Grammy Release'
         WHEN g.first_grammy_year IS NOT NULL AND bp.debut_year >= g.first_grammy_year THEN 'Post-Grammy Release'
         ELSE 'N/A'
    END as release_timing
FROM billboard_performance bp
LEFT JOIN grammy_artists g ON bp.artist = g.artist;
