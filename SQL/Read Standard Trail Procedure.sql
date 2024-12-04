CREATE PROCEDURE CW2.ReadTrailStandard
    @TrailID INT = NULL
AS
BEGIN
    IF @TrailID IS NULL
        SELECT * FROM CW2.View_TrailStandard;
    ELSE
        SELECT * FROM CW2.View_TrailStandard WHERE TrailID = @TrailID;
END;