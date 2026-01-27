import psycopg2

try:
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        password='RODRO123456',
        host='localhost'
    )
    conn.autocommit = True
    cur = conn.cursor()
    
    try:
        cur.execute('CREATE DATABASE hireskill_db')
        print('✓ Database hireskill_db created successfully!')
    except psycopg2.errors.DuplicateDatabase:
        print('✓ Database hireskill_db already exists!')
    
    cur.close()
    conn.close()
except Exception as e:
    print(f'Error: {e}')
