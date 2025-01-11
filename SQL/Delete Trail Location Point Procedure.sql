CREATE PROCEDURE CW2.DeleteTrailLocationPoint
    @TrailID INT,
    @LocationPointID INT
AS
BEGIN
    DELETE FROM CW2.Trail_LocationPt
    WHERE TrailID = @TrailID AND Location_Point = @LocationPointID;
END;