from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


DEBUG = False
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel_db.db' #Database where geo-photos are stored
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config.from_object(__name__)
db = SQLAlchemy(app)

@app.route("/")
def map():
    from models import GeoPhotos
    map_photos = GeoPhotos.query.all() # get all the geo-tagged photos
    photos = [{"URL":photo.PhotoPath, "Lat":photo.Latitude,
               "Lon":photo.Longitude, "Date":photo.DateTaken} for photo in map_photos]
    return render_template('map.html',photos=photos) # pass the photos to the front-end.

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=False)