CREATE PROCEDURE CW2.InsertTrail
    @Trail_name VARCHAR(255),
    @Trail_Summary VARCHAR(500),
    @Trail_Description TEXT,
    @Difficulty VARCHAR(50),
    @Location VARCHAR(255),
    @Length DECIMAL(5,2),
    @Elevation_gain INT,
    @Route_type VARCHAR(50),
    @OwnerID INT,
    @LocationPoint1 INT,
    @LocationPoint2 INT,
    @LocationPoint3 INT,
    @LocationPoint4 INT,
    @LocationPoint5 INT
AS
BEGIN
    BEGIN TRANSACTION;

    BEGIN TRY
        -- Validate that the provided location points are unique
        IF @LocationPoint1 = @LocationPoint2 OR @LocationPoint1 = @LocationPoint3 OR 
           @LocationPoint1 = @LocationPoint4 OR @LocationPoint1 = @LocationPoint5 OR 
           @LocationPoint2 = @LocationPoint3 OR @LocationPoint2 = @LocationPoint4 OR 
           @LocationPoint2 = @LocationPoint5 OR 
           @LocationPoint3 = @LocationPoint4 OR @LocationPoint3 = @LocationPoint5 OR 
           @LocationPoint4 = @LocationPoint5
        BEGIN
            RAISERROR('All location points must be unique.', 16, 1);
            RETURN;
        END

        -- Insert the trail into the Trail table
        INSERT INTO CW2.Trail (Trail_name, Trail_Summary, Trail_Description, Difficulty, Location, Length, Elevation_gain, Route_type, OwnerID)
        VALUES (@Trail_name, @Trail_Summary, @Trail_Description, @Difficulty, @Location, @Length, @Elevation_gain, @Route_type, @OwnerID);

        -- Retrieve the TrailID of the newly inserted trail
        DECLARE @TrailID INT = SCOPE_IDENTITY();

        -- Insert the 5 location points into the Trail_LocationPt table
        INSERT INTO CW2.Trail_LocationPt (TrailID, Location_Point, Order_no)
        VALUES 
            (@TrailID, @LocationPoint1, 1),
            (@TrailID, @LocationPoint2, 2),
            (@TrailID, @LocationPoint3, 3),
            (@TrailID, @LocationPoint4, 4),
            (@TrailID, @LocationPoint5, 5);

        -- Commit the transaction if all operations succeed
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        -- Rollback the transaction on error
        ROLLBACK TRANSACTION;

        -- Capture error details
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        DECLARE @ErrorSeverity INT = ERROR_SEVERITY();
        DECLARE @ErrorState INT = ERROR_STATE();

        -- Re-raise the error with the captured details
        RAISERROR(@ErrorMessage, @ErrorSeverity, @ErrorState);
    END CATCH
END;
