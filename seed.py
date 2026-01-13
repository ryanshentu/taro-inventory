import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

try:
    print("Connecting to AWS Database...")
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    print("Checking if table exists...")
    create_table_query = """
    CREATE TABLE IF NOT EXISTS inventory (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        quantity INTEGER,
        unit VARCHAR(20),
        threshold INTEGER
    );
    """
    cursor.execute(create_table_query)

    print("Removing old data...")
    cursor.execute("DELETE FROM inventory;")

    new_items = [
        ("Vanilla", 100, "gallons", 10),
        ("Chocolate", 100, "gallons", 10),
        ("Strawberry", 100, "gallons", 10),
        ("Butter Pecan", 50, "gallons", 5),
        ("Cookie Dough", 50, "gallons", 5),
        ("Cookies n Cream", 50, "gallons", 5)
    ]

    print("Adding new flavors...")
    for item in new_items:
        cursor.execute(
            "INSERT INTO inventory (name, quantity, unit, threshold) VALUES (%s, %s, %s, %s)",
            item
        )

    conn.commit()
    print("✅ Success! The menu has been updated.")

except Exception as e:
    print("❌ Error:", e)

finally:
    if 'conn' in locals():
        conn.close()