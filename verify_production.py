"""
Verify Topic 20 trong production database
"""

import psycopg2

CONNECTION_STRING = "postgresql://neondb_owner:npg_TBSbNV0XK4dZ@ep-rapid-sea-ao7qnzl8-pooler.c-2.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

def verify():
    conn = psycopg2.connect(CONNECTION_STRING)
    cur = conn.cursor()
    
    # Check Topic 20
    cur.execute(
        'SELECT name, name_vi, description FROM topics WHERE level = %s AND "order" = %s',
        ('A1', 20)
    )
    result = cur.fetchone()
    
    if result:
        print("=" * 70)
        print("TOPIC 20 IN PRODUCTION DATABASE:")
        print("=" * 70)
        print(f"Name: {result[0]}")
        print(f"Name (VI): {result[1]}")
        print(f"Description: {result[2]}")
        print("=" * 70)
    else:
        print("❌ Topic 20 not found!")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    verify()
