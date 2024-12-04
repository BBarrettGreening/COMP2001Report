import pathlib
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Base directory
basedir = pathlib.Path(__file__).parent.resolve()

# Create Connexion app
connex_app = connexion.App(__name__, specification_dir=basedir)

# Get Flask app instance
app = connex_app.app

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mssql+pyodbc://BBarrettGreening:OoxR792+@dist-6-505.uopnet.plymouth.ac.uk/"
    "COMP2001_BBarrettGreening?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes&Encrypt=yes"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy and Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)
