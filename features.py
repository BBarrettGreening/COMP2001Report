# Add features to a trail
from sqlalchemy.sql import text
from config import db
from flask import jsonify

# Add features to a trail
def add_features(trail_id, features):
    try:
        # Validate that features is a list of strings (feature names)
        if not isinstance(features, list) or not all(isinstance(f, str) for f in features):
            return jsonify({"error": "Invalid features format. Must be a list of feature names (strings)."}), 400

        for feature_name in features:
            db.session.execute(
                text("EXEC CW2.InsertTrailFeatures @TrailID = :TrailID, @FeatureJSON = :FeatureJSON"),
                {
                    "TrailID": trail_id,
                    "FeatureJSON": feature_name
                }
            )
        db.session.commit()
        return {"message": "Features added successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to add features: {str(e)}"}), 400

# Remove a feature from a trail
def remove_feature(trail_id, feature_id):
    try:
        db.session.execute(
            text("EXEC CW2.DeleteTrailFeature @TrailID = :TrailID, @FeatureID = :FeatureID"),
            {"TrailID": trail_id, "FeatureID": feature_id}
        )
        db.session.commit()
        return {"message": f"Feature {feature_id} removed successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to remove feature: {str(e)}"}), 400
