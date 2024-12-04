CREATE PROCEDURE CW2.InsertTrailFeatures
    @TrailID INT, -- ID of the trail to which features are being assigned
    @FeatureJSON NVARCHAR(MAX) -- JSON array of feature names
AS
BEGIN
    BEGIN TRANSACTION;

    BEGIN TRY
        -- Validate that the provided TrailID exists
        IF NOT EXISTS (SELECT 1 FROM CW2.Trail WHERE TrailID = @TrailID)
        BEGIN
            RAISERROR('Invalid TrailID. No trail exists with the given ID.', 16, 1);
            RETURN;
        END

        -- Parse the JSON array into a temporary table
        DECLARE @ParsedFeatures TABLE (FeatureName NVARCHAR(50));
        INSERT INTO @ParsedFeatures (FeatureName)
        SELECT value
        FROM OPENJSON(@FeatureJSON);

        -- Loop through each feature in the parsed table
        DECLARE @FeatureName NVARCHAR(50);
        DECLARE @FeatureID INT;

        DECLARE FeatureCursor CURSOR FOR
        SELECT FeatureName FROM @ParsedFeatures;

        OPEN FeatureCursor;
        FETCH NEXT FROM FeatureCursor INTO @FeatureName;

        WHILE @@FETCH_STATUS = 0
        BEGIN
            -- Check if the feature exists
            SELECT @FeatureID = Trail_FeatureID
            FROM CW2.Feature
            WHERE Trail_Feature = @FeatureName;

            -- If it doesn't exist, insert it and get the new FeatureID
            IF @FeatureID IS NULL
            BEGIN
                INSERT INTO CW2.Feature (Trail_Feature)
                VALUES (@FeatureName);

                SET @FeatureID = SCOPE_IDENTITY();
            END

            -- Link the feature to the TrailID in the Trail_Feature table
            IF NOT EXISTS (
                SELECT 1 FROM CW2.Trail_Feature
                WHERE TrailID = @TrailID AND Trail_FeatureID = @FeatureID
            )
            BEGIN
                INSERT INTO CW2.Trail_Feature (TrailID, Trail_FeatureID)
                VALUES (@TrailID, @FeatureID);
            END

            FETCH NEXT FROM FeatureCursor INTO @FeatureName;
        END;

        CLOSE FeatureCursor;
        DEALLOCATE FeatureCursor;
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
