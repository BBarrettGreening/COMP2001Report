CREATE PROCEDURE CW2.DeleteTrailFeature
    @TrailID INT,
    @FeatureID INT
AS
BEGIN
    DELETE FROM CW2.Trail_Feature
    WHERE TrailID = @TrailID AND Trail_FeatureID = @FeatureID;
END;
