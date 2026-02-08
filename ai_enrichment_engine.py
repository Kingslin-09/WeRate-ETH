import psycopg2
import json

# 1. Define the logic at the top so it's available for the loop
def generate_ai_description(name, category, tags):
    """Generates a dynamic description based on business data."""
    cat_lower = category.lower()
    if "coffee" in cat_lower or "cafe" in cat_lower:
        return f"Sip on expertly crafted brews at {name}, your local go-to for the perfect caffeine fix."
    elif "gym" in cat_lower or "fitness" in cat_lower:
        return f"Crush your fitness goals at {name}, featuring state-of-the-art equipment and a motivating community."
    elif "restaurant" in cat_lower or "food" in cat_lower:
        return f"Indulge in a world of flavor at {name}, where authentic {tags} meets exceptional service."
    else:
        return f"Experience the best local service at {name}, a premier {category} known for its welcoming atmosphere."

# 2. Connect to Supabase
# replace with the password you created, follow the steps in README.md to copy the URI
conn = psycopg2.connect("postgresql://postgres.ofzgbwogusqavvnizkny:[PASSWORD]@aws-1-eu-west-2.pooler.supabase.com:6543/postgres")
cur = conn.cursor()

# 3. Fetch rows - Ensure you include all needed columns in the SELECT statement
cur.execute("SELECT id, name, category, raw_properties FROM businesses WHERE description IS NULL LIMIT 150")
rows = cur.fetchall()

print(f"Enriching {len(rows)} businesses...")

for row in rows:
    # 1. Unpack the row first
    biz_id, name, category, raw_props = row
    
    # 2. Define tags for the AI
    tags = raw_props.get('cuisine', 'general') if raw_props else 'general'

    # 3. DEFINE ai_desc HERE (This solves the error)
    # You must call your function so ai_desc has a value
    ai_desc = generate_ai_description(name, category, tags)

    # 4. Define price_range
    if category.lower() in ['hotel', 'fine_dining']:
        price_range = "$$$"
    else:
        price_range = "$$"

    # 5. NOW run the execute command
    cur.execute("""
        UPDATE businesses 
        SET description = %s, price_range = %s 
        WHERE id = %s
    """, (ai_desc, price_range, biz_id))

# Commit all changes after the loop finishes
conn.commit()
cur.close()
conn.close()
print("AI Enrichment complete and saved to Supabase!")