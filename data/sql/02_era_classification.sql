-- data/sql/02_era_classification.sql
-- Classify tracks into musical eras based on their earliest appearance on the Billboard Hot 100

CREATE OR REPLACE VIEW track_eras AS
WITH first_appearance AS (
    SELECT 
        song,
        artist,
        MIN(week_date) as debut_date,
        EXTRACT(YEAR FROM MIN(week_date)) as debut_year
    FROM billboard
    GROUP BY song, artist
)
SELECT 
    song,
    artist,
    debut_date,
    debut_year,
    CASE 
        WHEN debut_year < 1960 THEN 'Pre-1960s'
        WHEN debut_year BETWEEN 1960 AND 1969 THEN '1960s'
        WHEN debut_year BETWEEN 1970 AND 1979 THEN '1970s'
        WHEN debut_year BETWEEN 1980 AND 1989 THEN '1980s'
        WHEN debut_year BETWEEN 1990 AND 1999 THEN '1990s'
        WHEN debut_year BETWEEN 2000 AND 2009 THEN '2000s'
        WHEN debut_year BETWEEN 2010 AND 2019 THEN '2010s'
        WHEN debut_year >= 2020 THEN '2020s'
    END as musical_era
FROM first_appearance;
