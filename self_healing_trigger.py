import psycopg2
import datetime

# 1. Connect to your DB
# replace with the password you created, follow the steps in README.md to copy the URI
conn = psycopg2.connect("postgresql://postgres.ofzgbwogusqavvnizkny:[PASSWORD]@aws-1-eu-west-2.pooler.supabase.com:6543/postgres")
cur = conn.cursor()

def self_heal_database(business_name, new_social_text):
    """Detects new info from social text and heals the database."""
    print(f"--- Analyzing Social Media Feed for: {business_name} ---")
    
    # 2. Simulate AI extracting information
    new_hours = None
    if "11pm" in new_social_text.lower():
        new_hours = "9:00 AM - 11:00 PM"
    
    # 3. Find the business ID in the DB
    cur.execute("SELECT id, hours FROM businesses WHERE name = %s LIMIT 1", (business_name,))
    result = cur.fetchone()
    
    if result:
        biz_id, old_hours = result
        
        # 4. Apply the Self-Healing Update
        if new_hours and new_hours != old_hours:
            cur.execute("""
                UPDATE businesses 
                SET hours = %s, 
                    confidence_score = 0.9, 
                    last_updated = NOW(),
                    verification_source = 'AI_Social_Scraper'
                WHERE id = %s
            """, (new_hours, biz_id))
            conn.commit()
            print(f"✅ Success: {business_name} updated from '{old_hours}' to '{new_hours}'.")
        else:
            print(f"ℹ️ No update needed for {business_name}.")
    else:
        print(f"❌ Business '{business_name}' not found in database.")

# --- DEMO TRIGGER ---
# Simulate finding an Instagram post that says they are open late
self_heal_database("The Bear Inn", "We are now open late until 11pm! Come grab a drink.")

cur.close()
conn.close()