CREATE VIEW CW2.View_TrailStandard AS
SELECT 
    trail.TrailID,
    trail.Trail_name,
    trail.Trail_Summary,
    trail.Trail_Description,
    trail.Difficulty,
    trail.Location,
    trail.Length,
    trail.Elevation_gain,
    trail.Route_type,
    -- Subquery to select all the features associated with a trail
    (SELECT STRING_AGG(feature.Trail_Feature, ', ') 
     FROM CW2.Trail_Feature trail_feat
     JOIN CW2.Feature feature ON trail_feat.Trail_FeatureID = feature.Trail_FeatureID
     WHERE trail_feat.TrailID = trail.TrailID) AS Features
FROM CW2.Trail trail
