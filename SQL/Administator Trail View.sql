CREATE VIEW CW2.View_TrailAdministrator AS
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
    acc.Email_address AS Owner_Email,
    -- Subquery to select all the features associated with a trail
    (SELECT STRING_AGG(feature.Trail_Feature, ', ') 
     FROM CW2.Trail_Feature trail_feat
     JOIN CW2.Feature feature ON trail_feat.Trail_FeatureID = feature.Trail_FeatureID
     WHERE trail_feat.TrailID = trail.TrailID) AS Features,
    -- Subquery to aggregate all location points for the trail
    (SELECT STRING_AGG(CONCAT('(', loc_point.Latitude, ', ', loc_point.Longitude, ') ', loc_point.Description), '; ') 
     FROM CW2.Trail_LocationPt trail_loc
     JOIN CW2.Location_Point loc_point ON trail_loc.Location_Point = loc_point.Location_Point
     WHERE trail_loc.TrailID = trail.TrailID) AS LocationPoints
FROM CW2.Trail trail
JOIN CW2.Account acc ON trail.OwnerID = acc.AccountID;
