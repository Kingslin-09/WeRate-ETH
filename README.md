WeRate: Submission Execution Guide
Prerequisites
Python 3.11+ installed.

PostgreSQL/Supabase account with an active project.

PostgreSQL Client Library: Install it via terminal:

Bash
pip install psycopg2
Step 1: Database Initialization (WeRate.sql)
Before running any scripts, you must prepare the environment in your Supabase SQL Editor.

Open your project in the Supabase Dashboard.

Navigate to the SQL Editor in the left sidebar.

Copy and paste the entire content of WeRate.sql into the editor.

Click Run.

This command enables PostGIS, creates the businesses table, adds essential metadata columns (like raw_properties and confidence_score), and installs the get_nearby_businesses spatial search function.

Step 2: Data Ingestion (ingest_osm_data.py)
This script populates your database with raw geographic data from the provided GeoJSON.

Ensure the file path for export.geojson is correct in the script (defaulting to c:\ETH_Oxford\export.geojson).

Run the script in your terminal:

Bash
python ingest_osm_data.py
Result: Standardized global business data (Names, Categories, and Opening Hours) will be uploaded into Supabase with accurate Lat/Lng coordinates.

Step 3: AI Enrichment (ai_enrichment_engine.py)
This script processes the raw data to add the "value-add" features required by the challenge.

Run the script:

Bash
python ai_enrichment_engine.py
Result: The system identifies rows without descriptions, generates AI Descriptions based on business tags, and assigns a Price Range ($ to $$$) based on the business category.

Step 4: Real-Time Self-Healing (self_healing_trigger.py)
This script demonstrates the "Automatic Update" requirement by simulating a data conflict and resolving it.

Run the script:

Bash
python self_healing_trigger.py
Result: The script simulates an AI "reading" a social media post about updated hours for "The Bear Inn." It automatically detects the change, updates the database, and increases the confidence_score for that record.

Verifying the Results
To see your global database in action, you can run this query in your Supabase SQL Editor to see the 10 most recently updated businesses:

SQL
SELECT name, category, description, price_range, hours, confidence_score 
FROM businesses 
ORDER BY last_updated DESC 
LIMIT 10;