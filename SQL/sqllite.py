import sqlite3
from sqlite3 import Error
from Lightstreamer import LightStreamer

from datetime import datetime


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(""" CREATE TABLE IF NOT EXISTS EURGBPtick (
                                        ticker text NOT NULL,
                                        dt text,
                                        igtime text,
                                        bid float,
                                        offer float
                                    ); """)
    except Error as e:
        print(e)

def insert_to_table(conn, row):
    sql = ''' INSERT INTO EURGBPtick(ticker, dt, igtime, bid, offer)
                  VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, row)
    conn.commit()
    return

def LS_listener(item_update):
    dt = datetime.now()
    igtime = item_update['values']['UPDATE_TIME']
    bid = float(item_update['values']['BID'])
    offer = float(item_update['values']['OFFER'])

    # datetime object containing current date and time

    print(dt, igtime, bid, offer)
    row = (dt, igtime, bid, offer)

    insert_to_table(conn, row)


conn = create_connection(r"flapDB.db")

# create tables
if conn is not None:
    # create projects table
    create_table(conn)
    print("success to create table")
else:
    print("Error! cannot create the database connection.")

LightStreamer.stream(LS_listener)




