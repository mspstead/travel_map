from app import db

class GeoPhotos(db.Model):

    __tablename__ = 'GeoPhotos'
    GeoPhotoID = db.Column(db.Integer, primary_key=True)
    PhotoPath = db.Column(db.String(), unique=True, nullable=False)
    DateTaken = db.Column(db.String())
    Latitude = db.Column(db.Float, nullable=False)
    Longitude = db.Column(db.Float, nullable=False)
