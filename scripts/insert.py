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


def parse_file(file, cur):
    id = None
    print('parsing ' + file + '...')

    with open(JSON_DIRECTORY + file) as file:
        geojson = json.load(file)

    # remove top level object
    geojson = geojson['features']

    # parse JSON for name
    for features in geojson:
        if features['type'] == 'Feature':
            id = db_insert_name(features['properties']['name'], cur)
            break

    # parse JSON for stops
    if id is not None:
        for features in geojson:
            if features['geometry']['type'] == 'MultiPoint':
                for coords in features['geometry']['coordinates']:
                    db_insert_stop_route(id, 'stops', coords[1], coords[0], cur)
            if features['geometry']['type'] == 'LineString':
                for coords in features['geometry']['coordinates']:
                    db_insert_stop_route(id, 'routes', coords[1], coords[0], cur)
        print('Successfully added to database!')
    

def db_insert_name(name, cur):
    print('Inserting ' + name + ' into database...')
    try:
        cur.execute("INSERT INTO buses (name) VALUES ('{0}');".format(name))
        cur.execute("SELECT id FROM buses WHERE name ='{0}';".format(name))
        return cur.fetchone()
    except (Exception, psycopg2.DatabaseError) as err:
        print('Failed to write ' + name + 's name to database!')
        print(err)


def db_insert_stop_route(id, table, longitude, latitude, cur):
    try:
        cur.execute("INSERT INTO {0} (id, longitude, latitude) VALUES ('{1}', '{2}', '{3}');".format(table, id[0], longitude, latitude))
    except (Exception, psycopg2.DatabaseError) as err:
        print('Failed to write' + table + 'to database!')
        print(err)


def poppulate_files(cur):
    print('Reading files...')
    for filename in os.listdir(JSON_DIRECTORY):
        if filename.endswith('.json'):
            geojson = parse_file(filename, cur)


def reset_tables(cur):
    cur.execute("TRUNCATE TABLE buses RESTART IDENTITY CASCADE;")
    
if __name__ == "__main__":
    conn = db_connect()
    cur = conn.cursor()
    reset_tables(cur)
    poppulate_files(cur)
    conn.commit()
