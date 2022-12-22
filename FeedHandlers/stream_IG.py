import sqlite3
from sqlite3 import Error
from Lightstreamer import LightStreamer

from datetime import datetime
from datetime import timedelta


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

    try:
        c = conn.cursor()
        c.execute(""" CREATE TABLE IF NOT EXISTS EURGBPprod (
                                        ticker text NOT NULL,
                                        dt text,
                                        igtime text,
                                        bid float,
                                        offer float
                                    ); """)
        print("tables insertion executed")
    except Error as e:
        print(e)

def insert_to_table(conn, row):
    sql = ''' INSERT INTO EURGBPprod(ticker, dt, igtime, bid, offer)
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

    row = ("EURGBP", dt, igtime, bid, offer)
    print(row)
    conn = create_connection(r"flapDB.db")

    # insert_to_table(conn, row)
    # create tables
    if conn is not None:
        # create projects table
        insert_to_table(conn, row)
        print("success writing row")
    else:
        print("Error! cannot create the database connection.")


if __name__=="__main__":
    conn = create_connection(r"flapDB.db")
    create_table(conn)
    LightStreamer.stream(LS_listener)




