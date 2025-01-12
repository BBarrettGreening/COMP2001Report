from sqlalchemy.sql import text
from config import db
from flask import jsonify

def update_location_points(trail_id, location_points):
    try:
        for i, point in enumerate(location_points, start=1):
            db.session.execute(
                text(
                    "EXEC CW2.InsertLocationPoint @Latitude = :Latitude, @Longitude = :Longitude, "
                    "@Description = :Description, @TrailID = :TrailID, @Order_no = :Order_no"
                ),
                {"Latitude": point["Latitude"], "Longitude": point["Longitude"], "Description": point["Description"], "TrailID": trail_id, "Order_no": i}
            )
        db.session.commit()
        return {"message": "Location points updated successfully"}
    except Exception as e:
        db.session.rollback()
        print(f"Error in update_location_points: {str(e)}")
        return jsonify({"error": f"Failed to update location points: {str(e)}"}), 400

def remove_location_point(trail_id, location_point_id):
    try:
        db.session.execute(
            text("EXEC CW2.DeleteTrailLocationPoint @TrailID = :TrailID, @LocationPointID = :LocationPointID"),
            {"TrailID": trail_id, "LocationPointID": location_point_id}
        )
        db.session.commit()
        return {"message": f"Location point {location_point_id} removed successfully"}
    except Exception as e:
        db.session.rollback()
        print(f"Error in remove_location_point: {str(e)}")
        return jsonify({"error": f"Failed to remove location point: {str(e)}"}), 400
