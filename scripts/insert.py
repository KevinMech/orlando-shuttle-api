import sys
import os
import psycopg2

    
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

def poppulate(conn):
    

if __name__ == "__main__":
    conn = connect()
    poppulate(conn)
