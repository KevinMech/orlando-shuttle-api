import sys
import os
import json
import psycopg2

JSON_DIRECTORY = '../geojson/'


def db_connect():
    try:
        if len(sys.argv) > 1 and sys.argv[1].lower() == '-debug':
            conn = psycopg2.connect('dbname=busroutedb user=postgres')
        else:
            env = os.environ['DATABASE_URL']
            conn = psycopg2.connect(env, sslmode='require')
        cur = conn.cursor()
        cur.execute('SELECT version()')
        version = cur.fetchone()
        print('Connected to PostgreSQL database!')
        print(version[0])
        print('--------------------------------------------------------------')
        return conn
    except (psycopg2.DatabaseError) as error:
        print('Connection Error:')
        print(error)
        sys.exit()


def parse_file(file):
    print('parsing ' + file)
    with open(JSON_DIRECTORY + file) as file:
        geojson = json.load(file)
    return geojson['features']


def poppulate_files():
    print('Reading files...')
    for filename in os.listdir(JSON_DIRECTORY):
        if filename.endswith('.json'):
            geojson = parse_file(filename)
            print(geojson)

if __name__ == "__main__":
    conn = db_connect()
    poppulate_files()
