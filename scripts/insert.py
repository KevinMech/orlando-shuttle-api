import sys
import os
import json
import psycopg2

json_directory = '../geojson/'
    
def connect():
    try:
        if len(sys.argv) > 1 and sys.argv[1].lower() == '-debug':
            conn = psycopg2.connect('dbname=busroutedb user=postgres')
        else:
            conn = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')
        cur = conn.cursor()
        cur.execute('SELECT version()')
        version = cur.fetchone()
        print('Connected to PostgreSQL database!')
        print(version[0])
        print('-------------------------------------------------------------------')
        return conn
    except (psycopg2.DatabaseError) as error:
        print('Connection Error:')
        print(error)
        sys.exit()

def read_files():
    print('Reading files...')
    for filename in os.listdir(json_directory):
        if filename.endswith('.json'):
            # geojson = parse_file(filename)
            

if __name__ == "__main__":
    conn = connect()
    read_files()
