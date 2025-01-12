from sqlalchemy.sql import text
from flask import jsonify
from config import db
from models import trail_schema, trails_schema


def read_all_admin():
    try:
        trails = db.session.execute(text("SELECT * FROM CW2.View_TrailAdministrator")).fetchall()
        return jsonify({"trails": trails_schema.dump(trails)}), 200
    except Exception as e:
        print(f"Error in read_all_admin: {str(e)}")
        return jsonify({"error": f"Failed to retrieve administrator trails: {str(e)}"}), 500


def read_all_standard():
    try:
        trails = db.session.execute(text("SELECT * FROM CW2.View_TrailStandard")).fetchall()
        return jsonify({"trails": trails_schema.dump(trails)}), 200
    except Exception as e:
        print(f"Error in read_all_standard: {str(e)}")
        return jsonify({"error": f"Failed to retrieve standard trails: {str(e)}"}), 500


def read_one_admin(trail_id):
    try:
        trail = db.session.execute(
            text("SELECT * FROM CW2.View_TrailAdministrator WHERE TrailID = :TrailID"),
            {"TrailID": trail_id}
        ).fetchone()
        if not trail:
            return jsonify({"error": f"Trail with ID {trail_id} not found"}), 404
        return jsonify({"trail": trail_schema.dump(trail)}), 200
    except Exception as e:
        print(f"Error in read_one_admin: {str(e)}")
        return jsonify({"error": f"Failed to retrieve trail: {str(e)}"}), 500


def read_one_standard(trail_id):
    try:
        trail = db.session.execute(
            text("SELECT * FROM CW2.View_TrailStandard WHERE TrailID = :TrailID"),
            {"TrailID": trail_id}
        ).fetchone()
        if not trail:
            return jsonify({"error": f"Trail with ID {trail_id} not found"}), 404
        return jsonify({"trail": trail_schema.dump(trail)}), 200
    except Exception as e:
        print(f"Error in read_one_standard: {str(e)}")
        return jsonify({"error": f"Failed to retrieve trail: {str(e)}"}), 500


def create(trail_data):
    try:
        required_fields = ["Trail_name", "Trail_Summary", "Trail_Description", "Difficulty", "Location",
                           "Length", "Elevation_gain", "Route_type", "OwnerID"]
        for field in required_fields:
            if field not in trail_data or not trail_data[field]:
                raise ValueError(f"Missing or invalid field: {field}")

        db.session.execute(
            text("EXEC CW2.InsertTrail :Trail_name, :Trail_Summary, :Trail_Description, :Difficulty, "
                 ":Location, :Length, :Elevation_gain, :Route_type, :OwnerID, :LocationPoint1, :LocationPoint2, "
                 ":LocationPoint3, :LocationPoint4, :LocationPoint5"),
            trail_data
        )
        db.session.commit()
        return jsonify({"message": "Trail created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error in create: {str(e)}")
        return jsonify({"error": f"Failed to create trail: {str(e)}"}), 400


def update(trail_id, trail_data):
    try:
        db.session.execute(
            text("EXEC CW2.UpdateTrail :TrailID, :Trail_name, :Trail_Summary, :Trail_Description, :Difficulty, "
                 ":Location, :Length, :Elevation_gain, :Route_type, :OwnerID"),
            {"TrailID": trail_id, **trail_data}
        )
        db.session.commit()
        return jsonify({"message": "Trail updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error in update: {str(e)}")
        return jsonify({"error": f"Failed to update trail: {str(e)}"}), 400


def delete(trail_id):
    try:
        db.session.execute(text("EXEC CW2.DeleteTrail :TrailID"), {"TrailID": trail_id})
        db.session.commit()
        return jsonify({"message": "Trail deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error in delete: {str(e)}")
        return jsonify({"error": f"Failed to delete trail: {str(e)}"}), 400
