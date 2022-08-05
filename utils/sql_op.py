
# imoprt sql module
import sqlite3


# link to the database named "beijing_subway"
def link_db(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    return conn, c


def create_db(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS subway_lines(
        line_name TEXT,
        station_name TEXT,
        station_id TEXT,
        station_3D TEXT,
    )""")

    conn.commit()
    conn.close()


# insert a line into the database
def insert_line(db_name, line_name, station_name, station_id, station_3D):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("""INSERT INTO subway_lines VALUES (?,?,?,?)""",
              (line_name, station_name, station_id, station_3D))
    conn.commit()
    conn.close()


# insert a station image into the database
def insert_station_img(db_name, line_name, station_name, img_name, img_content):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("""INSERT INTO subway_lines VALUES (?,?,?,?)""",
              (line_name, station_name, img_name, img_content))
    conn.commit()
    conn.close()
