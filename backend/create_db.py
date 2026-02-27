import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Extract DB password from DATABASE_URL or DB_PASSWORD env var
def _get_db_password():
    db_url = os.environ.get('DATABASE_URL', '')
    if '://' in db_url:
        # Parse password from postgresql://user:password@host:port/db
        try:
            creds = db_url.split('://')[1].split('@')[0]
            if ':' in creds:
                return creds.split(':', 1)[1]
        except (IndexError, ValueError):
            pass
    return os.environ.get('DB_PASSWORD', '')

try:
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password=_get_db_password(),
        host='localhost'
    )
    conn.autocommit = True
    cur = conn.cursor()
    
    try:
        cur.execute('CREATE DATABASE hireskillz_db')
        print('✓ Database hireskillz_db created successfully!')
    except psycopg2.errors.DuplicateDatabase:
        print('✓ Database hireskillz_db already exists!')
    
    cur.close()
    conn.close()
except Exception as e:
    print(f'Error: {e}')
