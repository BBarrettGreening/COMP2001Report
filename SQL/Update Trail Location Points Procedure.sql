CREATE PROCEDURE CW2.UpdateTrailLocationPoints
    @TrailID INT,
    @LocationPoints NVARCHAR(MAX) -- JSON array of location points
AS
BEGIN
    BEGIN TRY
        BEGIN TRANSACTION;

        -- Parse and process the input JSON
        DECLARE @Latitude DECIMAL(9,6), @Longitude DECIMAL(9,6), @Description VARCHAR(500), @OrderNo INT;
        DECLARE @LocationID INT;

        -- Cursor to handle mutliple location point updates
        DECLARE LocationCursor CURSOR FOR
        SELECT 
            JSON_VALUE(value, '$.Latitude') AS Latitude,
            JSON_VALUE(value, '$.Longitude') AS Longitude,
            JSON_VALUE(value, '$.Description') AS Description,
            JSON_VALUE(value, '$.OrderNo') AS OrderNo
        FROM OPENJSON(@LocationPoints);

        OPEN LocationCursor;
        FETCH NEXT FROM LocationCursor INTO @Latitude, @Longitude, @Description, @OrderNo;

        WHILE @@FETCH_STATUS = 0
        BEGIN
            -- Check if the location point exists in Trail_LocationPt
            SELECT @LocationID = Location_Point
            FROM CW2.Trail_LocationPt
            WHERE TrailID = @TrailID AND Order_no = @OrderNo;

            IF @LocationID IS NOT NULL
            BEGIN
                -- Update if it exists
                UPDATE CW2.Location_Point
                SET Latitude = @Latitude, Longitude = @Longitude, Description = @Description
                WHERE Location_Point = @LocationID;
            END
            ELSE
            BEGIN
                -- Insert a new point if it doesn't exist
                INSERT INTO CW2.Location_Point (Latitude, Longitude, Description)
                VALUES (@Latitude, @Longitude, @Description);

                SET @LocationID = SCOPE_IDENTITY();
                INSERT INTO CW2.Trail_LocationPt (TrailID, Location_Point, Order_no)
                VALUES (@TrailID, @LocationID, @OrderNo);
            END;

            FETCH NEXT FROM LocationCursor INTO @Latitude, @Longitude, @Description, @OrderNo;
        END;

        CLOSE LocationCursor;
        DEALLOCATE LocationCursor;
        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;
    END CATCH;
END;
