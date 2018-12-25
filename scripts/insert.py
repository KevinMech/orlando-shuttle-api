import sys
import os
import json
import psycopg2

JSON_DIRECTORY = '../geojson/'


def db_connect():
    """
    Open and test connection to the database
        Use -debug flag to connect to the localhost database

    Returns:
        conn (object): Connection object used to manage connection with database
    """

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
        print('[Error] Failed to Connect to Database:')
        print(error)
        sys.exit()


def read_files(cur):
    """
    Read all files in specified directory and then send to parse function to be parsed and inserted

    Parameters:
        cur (object): Cursor object used to execute SQL commands in psycopg2
    """

    print('Reading files...')
    for filename in os.listdir(JSON_DIRECTORY):
        if filename.endswith('.json'):
            parse_file(filename, cur)


def parse_file(file, cur):
    """
    Parse for values of JSON files to insert into database

    Parameters:
        file (string): Filename used to reference read file
        cur (object): Cursor object used to execute SQL commands in psycopg2
    """

    id = None
    print('Parsing ' + file + '...')
    with open(JSON_DIRECTORY + file) as file:
        geojson = json.load(file)

    # remove top level object
    geojson = geojson['features']

    id = parse_name(geojson)
    if id is not None:
        parse_features(geojson, id[0])
        print('Successfully added to database!')


def parse_name(geojson):
    """
    Parse JSON file for route name and return its assosciated ID

    Parameters:
        geojson (object): Deserialized JSON object specified to parse for name value

    Returns:
        id (int): Integer representing the ID of the bus name
    """

    id = None
    for features in geojson:
        if features['type'] == 'Feature':
            id = db_insert_name(features['properties']['name'], cur)
            break
    return id


def parse_features(geojson, id):
    """
    Parse JSON file for bus stop and bus route coordinates

    Parameters:
        geojson (object): Deserialized JSON object specified to parse for name value
    """

    for features in geojson:
        if features['geometry']['type'] == 'MultiPoint':
            for coords in features['geometry']['coordinates']:
                db_insert_stop_route(id, 'stops', coords[1], coords[0], cur)
        if features['geometry']['type'] == 'LineString':
            for coords in features['geometry']['coordinates']:
                db_insert_stop_route(id, 'routes', coords[1], coords[0], cur)


def db_insert_name(name, cur):
    """
    Insert route name into the database and return its corresponding ID

        Parameters:
        name (string): Filename used to reference file
        cur (object): Cursor object used to execute SQL commands in psycopg2

        Returns:
        id (int): Integer representing the ID of the bus name
    """

    print('Inserting ' + name + ' into database...')
    try:
        cur.execute("INSERT INTO buses (name) VALUES ('{0}');".format(name))
        cur.execute("SELECT id FROM buses WHERE name ='{0}';".format(name))
        return cur.fetchone()
    except (Exception, psycopg2.DatabaseError) as err:
        print('[Error] Failed to write ' + name + 's name to database:')
        print(err)


def db_insert_stop_route(id, table, longitude, latitude, cur):
    """
    Insert coordinates into either the stop or route tables in the database

    Parameters:
        id (int): Integer representing the ID of the bus name. Used for foreign key
        table (string): Represents the table to insert data into
        longitude (float): Longitude coordinates of the route or stop
        latitude (float): Latitude coordinates of the route or stop
        cur (object): Cursor object used to execute SQL commands in psycopg2
    """

    try:
        cur.execute("INSERT INTO {0} (id, longitude, latitude) VALUES ('{1}', '{2}', '{3}');".format(table, id, longitude, latitude))
    except (Exception, psycopg2.DatabaseError) as err:
        print('[Error] Failed to write' + table + 'to database:')
        print(err)


def reset_tables(cur):
    """
    Remove all data from all tables for rewriting purposes

    Parameters:
        cur (object): Cursor object used to execute SQL commands in psycopg2
    """

    print('Resetting tables in database...')
    try:
        cur.execute("TRUNCATE TABLE buses RESTART IDENTITY CASCADE;")
        print("Reset Complete!")
    except (Exception, psycopg2.DatabaseError) as err:
        print('[Error] Failed to reset database:')
        print(err)


if __name__ == "__main__":
    conn = db_connect()
    cur = conn.cursor()
    reset_tables(cur)
    read_files(cur)
    conn.commit()
    conn.close()
