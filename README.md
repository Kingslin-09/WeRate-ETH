#### WeRate: Submission Execution Guide
This guide provides a comprehensive walkthrough for deploying the WeRate global business database using Supabase, PostGIS, and Python.


### Prerequisites
Python 3.11+ installed.

Supabase Account: Sign up at supabase.com.

PostgreSQL Client Library: Run pip install psycopg2 in your terminal.

## Step 1: Create Your Supabase Project
Log in to the Supabase Dashboard.

Click New Project and select your organization.

Project Name: WeRate-Global-DB.

Database Password: Create a strong password; save it securely as you will need it for the connection strings.


Region: Select West Europe (London) to ensure optimal performance for the challenge.

Click Create New Project.

## Step 2: Database Initialization (schema_setup.sql)
Before running Python scripts, you must prepare the database environment.

Navigate to the SQL Editor in the left sidebar of your Supabase dashboard.

Click New Query.

Copy and paste the entire content of schema_setup.sql into the editor.

Click Run.

Database Schema Overview
The following columns are created to store comprehensive business data:

Column Name,Data Type,Description
id,BIGINT,"Primary key, auto-generated identity."
name,TEXT,The official name of the business.
category,TEXT,"Business type (e.g., restaurant, cafe, gym)."
location,GEOGRAPHY,PostGIS Point (4326) for accurate Lat/Lng.
description,TEXT,AI-generated marketing copy.
price_range,TEXT,Denominated from $ to $$$$.
hours,TEXT,Opening and closing times.
average_rating,NUMERIC,Global rating aggregated across platforms.
confidence_score,FLOAT,Reliability of the data (0.0 to 1.0).
verification_source,TEXT,"Source of the last update (e.g., AI_Social_Scraper)."
last_updated,TIMESTAMP,Automatically tracks the freshless of the record.
raw_properties,JSONB,Stores original metadata from the source.

## Step 3: Configure Database Connection (URI)
Connect your Python environment to the Supabase cloud.

Click the Connect button at the top of your project screen.

Change the connection method to Transaction Pooler.

Copy the Connection URI (e.g., postgresql://postgres.[REF]:[PASSWORD]@aws-1-eu-west-2...).

Update the Scripts: Open ingest_osm_data.py, ai_enrichment_engine.py, and self_healing_trigger.py. Replace the placeholder URI in each file with your copied string, inserting your actual Database Password.

## Step 4: Data Ingestion (ingest_osm_data.py)
Populate the database with raw geographic coordinates.

Ensure export.geojson is located in the same directory as the script.

Run the following in your terminal:


python ingest_osm_data.py 


Outcome: The script populates the businesses table using ST_GeomFromGeoJSON to verify locations.

## Step 5: AI Enrichment (ai_enrichment_engine.py)
Transform raw data into a high-value consumer database.

Run the script:


python ai_enrichment_engine.py 


Outcome: The system identifies rows without descriptions and uses logic to generate dynamic AI descriptions and assign price ranges ($ to $$$) based on categories.
+1

## Step 6: Real-Time Self-Healing (self_healing_trigger.py)
Demonstrate the "Automatic Update" requirement.

Run the script:


python self_healing_trigger.py 

Outcome: The script simulates finding updated hours for "The Bear Inn". It automatically updates the database, changes the source to AI_Social_Scraper, and increases the confidence_score to 0.9.
+1

# Verifying the Results
To see the Top 10 most recently updated businesses in your global database, run this query in the Supabase SQL Editor:






WeRate: Submission Execution Guide
Prerequisites
Python 3.11+ installed.

PostgreSQL/Supabase account with an active project.

PostgreSQL Client Library: Install it via terminal:

Bash
pip install psycopg2
Step 1: Database Initialization (scheme_setup.sql)
Before running any scripts, you must prepare the environment in your Supabase SQL Editor.

Open your project in the Supabase Dashboard. While creating a project, give the region as West Europe (London)

Navigate to the SQL Editor in the left sidebar.

Copy and paste the entire content of scheme_setup.sql into the editor.

Click Run.

This command enables PostGIS, creates the businesses table, adds essential metadata columns (like raw_properties and confidence_score), and installs the get_nearby_businesses spatial search function.

Step 2: Data Ingestion (ingest_osm_data.py)
This script populates your database with raw geographic data from the provided GeoJSON.

Ensure the file path for export.geojson is correct in the script.

Run the script in your terminal:

Bash
python ingest_osm_data.py

click the connect in the above of the project screen and click connect and change the method to transaction pooler and copy the URI (eg:postgresql://postgres:[YOUR-PASSWORD]@db.nopyxngdianwkutddmqk.supabase.co:5432/postgres) and update this with the password used while creating the project.

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