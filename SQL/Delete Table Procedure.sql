CREATE PROCEDURE CW2.DeleteTrail
    @TrailID INT
AS
BEGIN
    -- Delete references from Trail_LocationPt and Trail_Feature
    DELETE FROM CW2.Trail_LocationPt WHERE TrailID = @TrailID;
    DELETE FROM CW2.Trail_Feature WHERE TrailID = @TrailID;
    -- Delete the trail
    DELETE FROM CW2.Trail WHERE TrailID = @TrailID;
END;
