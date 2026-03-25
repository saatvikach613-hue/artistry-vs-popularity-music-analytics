# Artistry vs. Popularity: A Data-Driven Music Analysis

![Tableau Dashboard](https://img.shields.io/badge/View-Tableau%20Dashboard-E97627?style=for-the-badge&logo=tableau)
👉 **[View the Complete Interactive Dashboard on Tableau](https://img.shields.io/badge/View-Tableau%20Dashboard-E97627?style=for-the-badge&logo=tableau)]

## 📌 Project Overview
**Artistry vs. Popularity** is an end-to-end data engineering and analytics project that investigates the complex relationship between commercial success (chart popularity), critical acclaim (awards), and the intrinsic audio features of music. 

This project goes beyond simple data exploration to demonstrate rigorous, end-to-end analytical thinking—starting with complex business questions, designing a database schema from scratch, addressing data quality issues, engineering new KPIs, and delivering automated insights to an interactive dashboard for non-technical stakeholders.

## 🎯 The Core Questions (Objectives)
The analysis was driven by three primary research pillars:

1. **Q1 — Virality vs Longevity**: Has the rise of social media and TikTok created a culture of "Flash Hits" that chart briefly and disappear? Are songs genuinely getting shorter, and does that correlate with how long they stay on the charts?
2. **Q2 — Career Anatomy**: What actually separates a "one-hit wonder" from a "sustained career" artist? Is it sheer talent, Grammy recognition, audio characteristics, or something else entirely?
3. **Q3 — The Grammy Effect**: Do Grammy awards still move the needle in the streaming era? Do Grammy-recognized artists have measurably longer chart careers than their non-recognized peers?

## 🏆 Key Findings & Insights
Through rigorous SQL-based feature engineering and data aggregation, the following key findings were uncovered:

### On Virality and Song Length:
- 📉 **Shorter Songs**: Average song duration peaked at **5.1 minutes** in 1981 and dropped to **2.85 minutes** in 2022 — a massive **44% reduction** over 40 years.
- 📱 **The TikTok Effect**: The sharpest drop in song duration happened immediately after 2018, perfectly aligning with TikTok entering the mainstream consciousness.
- ⏳ **Resilience of Viral Hits**: Enduring Hits averaged **11.6 weeks** on the Billboard Hot 100 versus Flash Hits trailing closely at **10.4 weeks**. The gap is much smaller than expected, suggesting that viral songs aren't disappearing as fast as the popular cultural narrative suggests.

### On Career Anatomy:
- 🛑 **The One-Hit Wonder Rule**: A staggering **66% of all charting artists** (7,359 out of 11,114) are one-hit wonders—they charted exactly once and never returned.
- 🌟 **The Elite Few**: Only **303 artists (2.7%)** achieved "Sustained Career" status (15+ years on the charts).
- 📊 **Volume is Key**: Sustained Career artists averaged significantly more chart hits and total weeks. The performance gap between artist tiers is enormous and historically consistent.

### On Grammy Impact:
- 📈 **The 2x Rule**: Grammy Winners charted for an average of **15.3 weeks** per era vs. **8.3 weeks** for Non-Grammy artists—nearly double the longevity.
- 🚀 **The Grammy Bump**: Post-Grammy releases charted at a demonstrably higher peak position than Pre-Grammy releases, proving the "Grammy Bump" is a real, measurable phenomenon.
- 🏆 **Concentration of Excellence**: Grammy recognition concentrates heavily in the 2000s decade, making it the most mathematically competitive Grammy era in chart history.

## 🏗️ Architecture & Tech Stack

![Architecture Overview](https://img.shields.io/badge/Architecture-ETL%20Pipeline-blue)

- **Language**: Python 3 (Pandas, SQLAlchemy, Spotipy)
- **Database**: PostgreSQL (Relational schema, Views, CTEs, Window Functions)
- **APIs**: Spotify Web API (Audio Features Endpoint)
- **BI / Visualization**: Tableau
- **Environment Management**: `python-dotenv` for secure credential storage.

## 📂 Repository Structure

```text
artistry-vs-popularity/
├── data/
│   ├── raw/                 # Initial datasets (Billboard Hot 100, Grammys)
│   ├── processed/bi_exports/# Final exported CSVs ready for Tableau ingestion
│   └── sql/                 # Core logic: schemas, era classification, and KPI queries
├── scripts/
│   ├── 00_load_data.py      # Ingests raw CSVs into PostgreSQL
│   ├── 01_spotify_pull.py   # Fetches track audio features via the Spotify API
│   ├── 02_export_for_bi.py  # Dumps SQL views into clean CSVs for BI
│   ├── generate_mock_spotify.py # Mocks API data if rate limits are hit
│   └── run_analysis.py      # Master orchestrator script
├── README.md                # Project documentation (You are here)
└── requirements.txt         # Python dependencies
```

## 📊 Analytics Deep Dive (The SQL Layer)
Data manipulation was driven by SQL views and CTEs that generated custom KPIs which did not exist in the raw source material:

1. **`02_era_classification.sql`**: Assigns tracks to musical eras (Pre-Social, Early Social, TikTok Era) based on debut year context.
2. **`03_q1_virality.sql`**: Correlates a track's best peak position and total weeks on the chart with Spotify danceability, energy, acousticness, and tempo (`NTILE(4)` quartiles).
3. **`04_q2_longevity.sql`**: Calculates chart longevity (total weeks) and merges it with duration and era groupings to find what makes a song "last."
4. **`05_q3_grammy.sql`**: Joins chart success with Grammy award status (Won, Nominated, None) to track the "Grammy Bump".
5. **`06_kpi_exports.sql`**: Aggregates data at the **Artist Level** (career span, average chart rank, total hit count, Grammy history) to automatically classify artists into the tiers discussed above.

## 🚀 Setup & Execution 

To run this data pipeline locally:

1. **Clone the repository** and navigate to the project root.
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Database Setup**: Ensure PostgreSQL is running. Create a database named `music_analysis`.
4. **Environment Variables**: Create a `.env` file in the root with your credentials:
   ```env
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=music_analysis
   SPOTIPY_CLIENT_ID=your_spotify_id
   SPOTIPY_CLIENT_SECRET=your_spotify_secret
   ```
5. **Initialize Schema**: Run the schema setup scripts in `data/sql/01_schema.sql` against your database.
6. **Run the Pipeline**:
   ```bash
   python scripts/run_analysis.py
   ```
   *This single orchestrator script coordinates data loading, API fetching (if needed), SQL view creation, and BI exporting.*

## 👩‍💻 Author
**Saatvika Chokkapu**  
[LinkedIn](https://www.linkedin.com/in/saatvika-chokkapu) | [Tableau Public](https://public.tableau.com/app/profile/saatvika.chokkapu)

## 📸 Dashboard Previews
