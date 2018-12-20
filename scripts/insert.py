import sys
import os
import json
import psycopg2

JSON_DIRECTORY = '../geojson/'


def db_connect():
    try:
        if len(sys.argv) > 1 and sys.argv[1].lower() == '-debug':
            conn = psycopg2.connect(database="busroutedb", user="postgres")
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


def parse_file(file, conn):
    id = None

    print('parsing ' + file)

    with open(JSON_DIRECTORY + file) as file:
        geojson = json.load(file)
    # remove top level object
    geojson = geojson['features']
    # parse JSON for name
    for features in geojson:
        if features['type'] == 'Feature':
            print(features['properties']['name'])
            id = db_insert_name(features['properties']['name'], conn)
            print(id)
            break

    # return geojson


def db_insert_name(name, conn):
    print('Inserting ' + name + ' name into database')
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO buses (name) VALUES ('{0}');".format(name))
        cur.execute("SELECT id FROM buses WHERE name ='{0}';".format(name))
        return cur.fetchone()
    except (Exception, psycopg2.DatabaseError) as err:
        print('Failed to write' + name + 'to database!')
        print(err)


def poppulate_files(conn):
    print('Reading files...')
    for filename in os.listdir(JSON_DIRECTORY):
        if filename.endswith('.json'):
            geojson = parse_file(filename, conn)
            # db_insert(filename, geojson)

if __name__ == "__main__":
    conn = db_connect()
    poppulate_files(conn)
