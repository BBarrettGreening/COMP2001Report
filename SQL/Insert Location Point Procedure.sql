CREATE PROCEDURE CW2.InsertLocationPoint
    @Latitude DECIMAL(9,6),
    @Longitude DECIMAL(9,6),
    @Description VARCHAR(500),
    @TrailID INT = NULL, 
    @Order_no INT = NULL 
AS
BEGIN
    BEGIN TRANSACTION;

    BEGIN TRY
        -- Insert the new location point into the Location_Point table
        INSERT INTO CW2.Location_Point (Latitude, Longitude, Description)
        VALUES (@Latitude, @Longitude, @Description);

        -- Get the Location_Point ID of the newly inserted point
        DECLARE @LocationPointID INT = SCOPE_IDENTITY();

        -- If TrailID is provided, associate the new location point with the trail
        IF @TrailID IS NOT NULL AND @Order_no IS NOT NULL
        BEGIN
            INSERT INTO CW2.Trail_LocationPt (TrailID, Location_Point, Order_no)
            VALUES (@TrailID, @LocationPointID, @Order_no);
        END
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        DECLARE @ErrorMessage NVARCHAR(4000) = ERROR_MESSAGE();
        DECLARE @ErrorSeverity INT = ERROR_SEVERITY();
        DECLARE @ErrorState INT = ERROR_STATE();
        RAISERROR(@ErrorMessage, @ErrorSeverity, @ErrorState);
    END CATCH
END;
