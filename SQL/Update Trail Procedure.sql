CREATE PROCEDURE CW2.UpdateTrail
    @TrailID INT,
    @Trail_name VARCHAR(255) = NULL,
    @Trail_Summary VARCHAR(500) = NULL,
    @Trail_Description TEXT = NULL,
    @Difficulty VARCHAR(50) = NULL,
    @Location VARCHAR(255) = NULL,
    @Length DECIMAL(5,2) = NULL,
    @Elevation_gain INT = NULL,
    @Route_type VARCHAR(50) = NULL,
    @OwnerID INT = NULL
AS
BEGIN
    UPDATE CW2.Trail
    SET 
        Trail_name = COALESCE(@Trail_name, Trail_name),
        Trail_Summary = COALESCE(@Trail_Summary, Trail_Summary),
        Trail_Description = COALESCE(@Trail_Description, Trail_Description),
        Difficulty = COALESCE(@Difficulty, Difficulty),
        Location = COALESCE(@Location, Location),
        Length = COALESCE(@Length, Length),
        Elevation_gain = COALESCE(@Elevation_gain, Elevation_gain),
        Route_type = COALESCE(@Route_type, Route_type),
        OwnerID = COALESCE(@OwnerID, OwnerID)
    WHERE TrailID = @TrailID;
END;
