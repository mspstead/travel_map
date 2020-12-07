from GPSPhoto import gpsphoto
import sqlite3
import sys
import os

def get_photo_meta_data(image_path):
    """
    :param image_path: file path of image
    :return: [Latitude, Longitude, Date Taken] or [] if None
    """
    data = gpsphoto.getGPSData(image_path)

    lat = data.get('Latitude')
    lon = data.get('Longitude')
    date_taken = data.get('Date')

    if not lat or not lon or not date_taken: #Check if any values are missing
        return []
    else:
        return [lat, lon, date_taken]

def connect_db(Database_Path):
    """
    Initialise SQLite database
    Connect to existing database or create new database at Path.
    """
    connection = None
    try:
        connection = sqlite3.connect(Database_Path)
        print("Connected to sqlite database at {} .".format(Database_Path))
        return connection
    except (sqlite3.OperationalError) as e:
        print('Connection failed: {}'.format(e))
        return connection

def close_connection(connection):
    """Close a database connection"""
    connection.close()

def create_geo_photos_table(connection):
    """
    :param connection: connection for a sqllite3 database.
    Create table to store geo-tagged timestamped images.
    """

    geo_photo_table = """CREATE TABLE IF NOT EXISTS GeoPhotos (
        GeoPhotoID INTEGER PRIMARY KEY,
        PhotoPath TEXT NOT NULL UNIQUE,
        DateTaken TEXT,
        Latitude REAL NOT NULL,
        Longitude REAL NOT NULL);
    """

    try:
        cursor = connection.cursor()
        cursor.execute(geo_photo_table)
        return True, 'GeoPhotos table created successfully'

    except:
        e = sys.exc_info()[0]
        return False, 'Failed execution: {}'.format(e)

def insert_map_photo(connection,photo):
    """
    :param connection: connection to sqlite3 database containing GeoPhotos table
    :param photo: [photo_path, DateTaken, Latitude, Logitude]
    Inserts a photo into the database.
    """

    insert_photo_sql = '''INSERT INTO GeoPhotos (PhotoPath,DateTaken,Latitude,Longitude)
                  VALUES(?,?,?,?) '''

    try:
        cursor = connection.cursor()
        cursor.execute(insert_photo_sql,photo)
        connection.commit()
        return cursor.lastrowid

    except sqlite3.IntegrityError as e:
        return -1

if __name__ == '__main__':

    database_path = '/PATH_TO_FLASK_WEBISTE_DIRECTORY/travel_map/travel_db.db'
    conn = connect_db(database_path) # connect to or create database at path

    create_geo_photos_table(conn) # create geo_photos table

    image_directory = '/PATH_TO_FLASK_WEBISTE_DIRECTORY/travel_map/static/geo-images/' # Directory where geo-tag images are stored
    folder = os.fsencode(image_directory)

    web_file_path = '/static/geo-images/' # This is the directory Flask will serve the image files from

    for file in os.listdir(folder):
        filename = os.fsdecode(file)
        if filename.endswith(('.jpeg', '.png', '.gif', '.JPG', '.jpg')):  # whatever image types you're using...

            data = get_photo_meta_data(image_directory + filename) # get the image's meta data

            if data!=[]:

                PhotoPath = web_file_path+filename
                Latitude = data[0]
                Longitude = data[1]
                DateTaken = data[2]

                insert_map_photo(conn,[PhotoPath,DateTaken,Latitude,Longitude]) #add the geo-tag photo to the database

    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM GeoPhotos;')
    count = cursor.fetchall()
    print(count[0][0], "geo-tagged and timestamped photos added to database.")
    close_connection(conn)