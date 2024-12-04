CREATE PROCEDURE CW2.ReadTrailAdministrator
    @TrailID INT = NULL
AS
BEGIN
    IF @TrailID IS NULL
        SELECT * FROM CW2.View_TrailAdministrator;
    ELSE
        SELECT * FROM CW2.View_TrailAdministrator WHERE TrailID = @TrailID;
END;