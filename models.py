from marshmallow import fields
from config import db, ma

# Account Model
class Account(db.Model):
    __tablename__ = 'Account'
    AccountID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Email_address = db.Column(db.String(255), nullable=False, unique=True)  # Enforce unique emails
    Role = db.Column(db.String(255), nullable=False)

# Trail Model
class Trail(db.Model):
    __tablename__ = 'Trail'
    TrailID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Trail_name = db.Column(db.String(255), nullable=False)
    Trail_Summary = db.Column(db.String(500), nullable=False)
    Trail_Description = db.Column(db.Text, nullable=False)
    Difficulty = db.Column(db.String(50), nullable=False)
    Location = db.Column(db.String(255), nullable=False)
    Length = db.Column(db.Float, nullable=False)
    Elevation_gain = db.Column(db.Integer, nullable=False)
    Route_type = db.Column(db.String(50), nullable=False)
    OwnerID = db.Column(db.Integer, db.ForeignKey('Account.AccountID'), nullable=False)

# Feature Model
class Feature(db.Model):
    __tablename__ = 'Feature'
    FeatureID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Feature_name = db.Column(db.String(255), nullable=False)

# LocationPoint Model
class LocationPoint(db.Model):
    __tablename__ = 'LocationPoint'
    LocationPointID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Latitude = db.Column(db.Float, nullable=False)
    Longitude = db.Column(db.Float, nullable=False)
    Description = db.Column(db.String(255), nullable=True)

# Account Schema
class AccountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Account
        load_instance = True
        sqla_session = db.session

# Trail Schema
class TrailSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        load_instance = True
        sqla_session = db.session

# Feature Schema
class FeatureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Feature
        load_instance = True
        sqla_session = db.session

# LocationPoint Schema
class LocationPointSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = LocationPoint
        load_instance = True
        sqla_session = db.session

# Instantiate schemas for serialization
account_schema = AccountSchema()
trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)

feature_schema = FeatureSchema()
features_schema = FeatureSchema(many=True)

location_point_schema = LocationPointSchema()
location_points_schema = LocationPointSchema(many=True)
