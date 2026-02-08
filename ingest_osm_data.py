import json
import psycopg2
import os

# 1. SET THE PATH (Use the full path to avoid FileNotFoundError)
file_path = 'export.geojson'

# 2. LOAD DATA (Explicitly use utf-8 to avoid UnicodeDecodeError)
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 3. CONNECT (Use your Supabase URI)
# Format: postgresql://postgres:[PASSWORD]@db.[REF].supabase.co:5432/postgres
conn = psycopg2.connect("postgresql://postgres.ofzgbwogusqavvnizkny:kinGsy09!12040@aws-1-eu-west-2.pooler.supabase.com:6543/postgres")
cur = conn.cursor()

print(f"Starting import of {len(data['features'])} items...")

# 4. INSERT LOOP
for feature in data['features']:
    props = feature.get('properties', {})
    geom = feature.get('geometry', {})
    
    if geom and geom['type'] == 'Point':
        name = props.get('name', 'Unnamed Business')
        category = props.get('amenity', props.get('shop', 'Business'))
        
        # Use ST_GeomFromGeoJSON for PostGIS compatibility
        cur.execute("""
            INSERT INTO businesses (name, category, location)
            VALUES (%s, %s, ST_SetSRID(ST_GeomFromGeoJSON(%s), 4326))
        """, (name, category, json.dumps(geom)))

# Updated ingestion logic
for feature in data['features']:
    props = feature.get('properties', {})
    
    # Extract real hours if they exist in the OpenStreetMap data
    opening_hours = props.get('opening_hours', 'Contact for hours')
    
    cur.execute("""
        INSERT INTO businesses (name, category, location, opening_hours)
        VALUES (%s, %s, ST_SetSRID(ST_GeomFromGeoJSON(%s), 4326), %s)
    """, (name, category, json.dumps(geom), opening_hours))


conn.commit()
cur.close()
conn.close()
print("Success! Data is now in Supabase.")