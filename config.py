import pathlib
import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import connexion
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory
basedir = pathlib.Path(__file__).parent.resolve()

# Initialize SQLAlchemy and Marshmallow globally
db = SQLAlchemy()
ma = Marshmallow()

# JWT utility functions
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_EXPIRATION_SECONDS = int(os.getenv("JWT_EXPIRATION_SECONDS", 1800))  # Default: 30 minutes

# Generate a JWT token with the given payload
def generate_jwt(payload):
    payload["exp"] = datetime.utcnow() + timedelta(seconds=JWT_EXPIRATION_SECONDS)
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return token

# Decodes and validates a JWT token
def decode_jwt(token):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")

# Validates a JWT token
def bearer_info_func(token):
    return decode_jwt(token)


# Create and configure Connexion app with Flask
def create_connexion_app():
    connex_app = connexion.App(__name__, specification_dir=str(basedir))

    # Add the API specification and register the bearer info function
    connex_app.add_api(
        "swagger.yml",
        strict_validation=True,
        validate_responses=True,
        options={"swagger_ui": True},
        resolver_error=404
    )

    # Register bearer_info_func globally for Connexion
    connex_app.app.bearer_info_func = bearer_info_func

    # Get the Flask app instance from Connexion
    flask_app = connex_app.app

    # Database configuration
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")  # Use .env for database URI
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    flask_app.secret_key = os.getenv("SECRET_KEY")  # Use .env for Flask secret key

    # Initialize SQLAlchemy and Marshmallow with the Flask app
    db.init_app(flask_app)
    ma.init_app(flask_app)

    return connex_app
