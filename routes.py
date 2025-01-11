from flask import Blueprint, request, jsonify, render_template
from functools import wraps
from sqlalchemy.sql import text
from trails import create, update, delete, read_all_admin, read_all_standard, read_one_admin, read_one_standard
from features import add_features, remove_feature
from location_points import update_location_points, remove_location_point
import requests
import config
from models import trail_schema, trails_schema, feature_schema, features_schema, location_point_schema, location_points_schema

routes_blueprint = Blueprint("routes", __name__)

AUTH_URL = 'https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users'


# Middleware to check authentication
def login_required(role=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                return jsonify({"error": "Authorization header is missing"}), 401

            try:
                token = auth_header.split(" ")[1]
                payload = config.decode_jwt(token)
            except ValueError as e:
                return jsonify({"error": str(e)}), 401

            if role and payload.get("role") != role:
                return jsonify({"error": "Forbidden: You do not have access to this resource"}), 403

            request.user = payload
            return func(*args, **kwargs)
        return wrapper
    return decorator


@routes_blueprint.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@routes_blueprint.route("/login", methods=["POST"])
def login():
    email = request.json.get("username")
    password = request.json.get("password")

    if not email or not password:
        return jsonify({"error": "Username and password are required"}), 400

    credentials = {"email": email, "password": password}
    response = requests.post(AUTH_URL, json=credentials)

    if response.status_code == 200:
        response_data = response.json()
        if response_data == ['Verified', 'True']:
            query = config.db.session.execute(
                text("SELECT AccountID, Role FROM CW2.Account WHERE Email_address = :email"),
                {"email": email}
            ).fetchone()

            if query:
                payload = {
                    "user_id": query.AccountID,
                    "role": query.Role,
                }
                token = config.generate_jwt(payload)
                return jsonify({"message": "Login successful", "token": token, "role": query.Role}), 200
            else:
                return jsonify({"error": "Invalid credentials"}), 401
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    else:
        return jsonify({"error": "Authentication service unavailable"}), 500


@routes_blueprint.route("/trails/admin", methods=["GET"])
@login_required(role="Administrator")
def admin_trails():
    return read_all_admin()


@routes_blueprint.route("/trails/standard", methods=["GET"])
@login_required(role="Standard")
def standard_trails():
    return read_all_standard()


@routes_blueprint.route("/trails/admin/<int:trail_id>", methods=["GET"])
@login_required(role="Administrator")
def trail_by_id_admin(trail_id):
    return read_one_admin(trail_id)


@routes_blueprint.route("/trails/standard/<int:trail_id>", methods=["GET"])
@login_required(role="Standard")
def trail_by_id_standard(trail_id):
    return read_one_standard(trail_id)


@routes_blueprint.route("/trails/add", methods=["POST"])
@login_required(role="Administrator")
def add_trail():
    trail_data = request.json
    return create(trail_data)


@routes_blueprint.route("/trails/update/<int:trail_id>", methods=["PUT"])
@login_required(role="Administrator")
def edit_trail(trail_id):
    trail_data = request.json
    return update(trail_id, trail_data)


@routes_blueprint.route("/trails/delete/<int:trail_id>", methods=["DELETE"])
@login_required(role="Administrator")
def remove_trail(trail_id):
    return delete(trail_id)

# Features routes
@routes_blueprint.route("/trails/<int:trail_id>/features", methods=["POST"])
@login_required(role="Administrator")
def add_trail_features(trail_id):
    try:
        features = request.json  # Expecting a list of feature names (strings)
        result = add_features(trail_id, features)
        return result
    except Exception as e:
        return jsonify({"error": f"Failed to add features: {str(e)}"}), 400


@routes_blueprint.route("/trails/<int:trail_id>/features/<int:feature_id>", methods=["DELETE"])
@login_required(role="Administrator")
def remove_trail_feature(trail_id, feature_id):
    try:
        removed_feature = remove_feature(trail_id, feature_id)
        serialized_feature = feature_schema.dump(removed_feature)
        return jsonify({"message": "Feature removed successfully", "feature": serialized_feature}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to remove feature: {str(e)}"}), 400


# Location points routes
@routes_blueprint.route("/trails/<int:trail_id>/location-points", methods=["PUT"])
@login_required(role="Administrator")
def edit_location_points(trail_id):
    try:
        location_points = request.json
        updated_points = update_location_points(trail_id, location_points)
        serialized_points = location_points_schema.dump(updated_points)
        return jsonify({"location_points": serialized_points}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to update location points: {str(e)}"}), 400


@routes_blueprint.route("/trails/<int:trail_id>/location-points/<int:location_point_id>", methods=["DELETE"])
@login_required(role="Administrator")
def delete_location_point(trail_id, location_point_id):
    try:
        removed_point = remove_location_point(trail_id, location_point_id)
        serialized_point = location_point_schema.dump(removed_point)
        return jsonify({"message": "Location point removed successfully", "location_point": serialized_point}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to remove location point: {str(e)}"}), 400
