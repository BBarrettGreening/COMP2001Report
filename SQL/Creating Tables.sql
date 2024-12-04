-- Drop existing tables if they exist
IF OBJECT_ID('CW2.Trail_LocationPt', 'U') IS NOT NULL 
  DROP TABLE CW2.Trail_LocationPt;
IF OBJECT_ID('CW2.Location_Point', 'U') IS NOT NULL 
  DROP TABLE CW2.Location_Point;
IF OBJECT_ID('CW2.Trail_Feature', 'U') IS NOT NULL 
  DROP TABLE CW2.Trail_Feature;
IF OBJECT_ID('CW2.Feature', 'U') IS NOT NULL 
  DROP TABLE CW2.Feature;
IF OBJECT_ID('CW2.Trail', 'U') IS NOT NULL 
  DROP TABLE CW2.Trail;
IF OBJECT_ID('CW2.Account', 'U') IS NOT NULL 
  DROP TABLE CW2.Account;


-- Create Account table
CREATE TABLE CW2.Account (
    AccountID INT IDENTITY(1,1) PRIMARY KEY, -- Auto-generated AccountID
    Email_address VARCHAR(255) NOT NULL CHECK (Email_address LIKE '%@%.%'), -- Validates email format
    Role VARCHAR(255) NOT NULL CHECK (Role IN ('Administrator', 'Standard')) -- Specifies allowed roles
);

-- Create Trail table
CREATE TABLE CW2.Trail (
    TrailID INT IDENTITY(1,1) PRIMARY KEY, -- Auto-generated TrailID
    Trail_name VARCHAR(255) NOT NULL, -- Name of the trail
    Trail_Summary VARCHAR(500) NOT NULL, -- Short summary
    Trail_Description TEXT NOT NULL, -- Full description
    Difficulty VARCHAR(50) NOT NULL CHECK (Difficulty IN ('Easy', 'Moderate', 'Hard')), -- Validates difficulty level
    Location VARCHAR(255) NOT NULL, -- Location (e.g., City, Country)
    Length DECIMAL(5,2) NOT NULL, -- Length in KM
    Elevation_gain INT NOT NULL, -- Elevation gain in meters
    Route_type VARCHAR(50) NOT NULL, -- Route type (e.g., Loop, Point-to-point)
    OwnerID INT NOT NULL, -- Foreign key to Account table
    FOREIGN KEY (OwnerID) REFERENCES CW2.Account(AccountID)
);

-- Create Feature table
CREATE TABLE CW2.Feature (
    Trail_FeatureID INT IDENTITY(1,1) PRIMARY KEY, -- Auto-generated FeatureID
    Trail_Feature VARCHAR(50) NOT NULL -- Name of the feature
);

-- Create Trail_Feature relationship table
CREATE TABLE CW2.Trail_Feature (
    TrailID INT NOT NULL, -- Foreign key to Trail
    Trail_FeatureID INT NOT NULL, -- Foreign key to Feature
    PRIMARY KEY (TrailID, Trail_FeatureID),
    FOREIGN KEY (TrailID) REFERENCES CW2.Trail(TrailID),
    FOREIGN KEY (Trail_FeatureID) REFERENCES CW2.Feature(Trail_FeatureID)
);

-- Create Location_Point table
CREATE TABLE CW2.Location_Point (
    Location_Point INT IDENTITY(1,1) PRIMARY KEY, -- Auto-generated Location_Point ID
    Latitude DECIMAL(9,6) NOT NULL CHECK (Latitude BETWEEN -90 AND 90), -- Latitude
    Longitude DECIMAL(9,6) NOT NULL CHECK (Longitude BETWEEN -180 AND 180), -- Longitude
    Description VARCHAR(500) NOT NULL -- Description of the location point
);

-- Create Trail_LocationPt relationship table
CREATE TABLE CW2.Trail_LocationPt (
    TrailID INT NOT NULL, -- Foreign key to Trail
    Location_Point INT NOT NULL, -- Foreign key to Location_Point
    Order_no INT NOT NULL, -- Order of the points in the trail
    PRIMARY KEY (TrailID, Location_Point),
    FOREIGN KEY (TrailID) REFERENCES CW2.Trail(TrailID),
    FOREIGN KEY (Location_Point) REFERENCES CW2.Location_Point(Location_Point)
);

-- Insert example data into Account table
INSERT INTO CW2.Account (Email_address, Role)
VALUES 
('grace@plymouth.ac.uk', 'Administrator'),
('tim@plymouth.ac.uk', 'Administrator'),
('ada@plymouth.ac.uk', 'Standard');

-- Insert example data into Trail table
INSERT INTO CW2.Trail (Trail_name, Trail_Summary, Trail_Description, Difficulty, Location, Length, Elevation_gain, Route_type, OwnerID)
VALUES 
('Plymouth Circular', 'A circular walk through oak woodlands', 'This is a gentle circular walk through ancient oak woodlands, beside the beautiful River Plym...', 
 'Easy', 'Plymouth, Devon, England', 5.0, 147, 'Loop', 
 (SELECT AccountID FROM CW2.Account WHERE Email_address = 'grace@plymouth.ac.uk')),
('Exmouth and Dawlish Warren', 'A route between Exmouth and Dawlish', 'This stretch of the Exe Estuary Trail is a cycling and walking route between Exmouth and Dawlish...', 
 'Moderate', 'Exmouth, Devon, England', 26.2, 181, 'Point-to-point', 
 (SELECT AccountID FROM CW2.Account WHERE Email_address = 'tim@plymouth.ac.uk'));

-- Insert example data into Feature table
INSERT INTO CW2.Feature (Trail_Feature) 
VALUES ('Dog-friendly'), ('Kid-friendly'), ('Partially paved'), ('Caves'), ('Forests'),
       ('Birding'), ('Beaches'), ('Rivers'), ('Hiking'), ('Mountain biking'), ('Walking');

-- Insert example data into Trail_Feature relationship table
INSERT INTO CW2.Trail_Feature (TrailID, Trail_FeatureID)
VALUES 
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), 
(2, 3), (2, 7), (2, 8), (2, 9), (2, 10), (2, 11);

-- Insert location points for Plymouth Circular
INSERT INTO CW2.Location_Point (Latitude, Longitude, Description)
VALUES
    (50.3690, -4.1362, 'Plymouth Hoe starting and ending point'), -- Start and end point
    (50.3705, -4.1427, 'Royal Citadel viewpoint'),
    (50.3740, -4.1480, 'Barbican historic area'),
    (50.3765, -4.1420, 'Sutton Harbour marina'),
    (50.3715, -4.1385, 'Plymouth Mayflower Steps'); -- Intermediate point

-- Retrieve the last inserted Location_Point IDs for Plymouth Circular
DECLARE @PlymouthCircularPoint1 INT = SCOPE_IDENTITY() - 4;
DECLARE @PlymouthCircularPoint2 INT = SCOPE_IDENTITY() - 3;
DECLARE @PlymouthCircularPoint3 INT = SCOPE_IDENTITY() - 2;
DECLARE @PlymouthCircularPoint4 INT = SCOPE_IDENTITY() - 1;
DECLARE @PlymouthCircularPoint5 INT = SCOPE_IDENTITY();

-- Associate location points with Plymouth Circular trail
INSERT INTO CW2.Trail_LocationPt (TrailID, Location_Point, Order_no)
VALUES
    (1, @PlymouthCircularPoint1, 1), -- Start point
    (1, @PlymouthCircularPoint2, 2),
    (1, @PlymouthCircularPoint3, 3),
    (1, @PlymouthCircularPoint4, 4),
    (1, @PlymouthCircularPoint5, 5); -- End point (same as start)

-- Insert location points for Exmouth and Dawlish Warren
INSERT INTO CW2.Location_Point (Latitude, Longitude, Description)
VALUES
    (50.6174, -3.4066, 'Exmouth Marina starting point'),
    (50.6210, -3.4375, 'Lympstone Village'),
    (50.6265, -3.4630, 'Topsham Town'),
    (50.6290, -3.4855, 'Powderham Castle viewpoint'),
    (50.5980, -3.4460, 'Dawlish Warren Nature Reserve'); -- Ending point

-- Retrieve the last inserted Location_Point IDs for Exmouth and Dawlish Warren
DECLARE @ExmouthPoint1 INT = SCOPE_IDENTITY() - 4;
DECLARE @ExmouthPoint2 INT = SCOPE_IDENTITY() - 3;
DECLARE @ExmouthPoint3 INT = SCOPE_IDENTITY() - 2;
DECLARE @ExmouthPoint4 INT = SCOPE_IDENTITY() - 1;
DECLARE @ExmouthPoint5 INT = SCOPE_IDENTITY();

-- Associate location points with Exmouth and Dawlish Warren trail
INSERT INTO CW2.Trail_LocationPt (TrailID, Location_Point, Order_no)
VALUES
    (2, @ExmouthPoint1, 1), -- Start point
    (2, @ExmouthPoint2, 2),
    (2, @ExmouthPoint3, 3),
    (2, @ExmouthPoint4, 4),
    (2, @ExmouthPoint5, 5); -- End point


-- Display created tables with example data
SELECT * FROM CW2.Account;
SELECT * FROM CW2.Trail;
SELECT * FROM CW2.Feature;
SELECT * FROM CW2.Trail_Feature;
SELECT * FROM CW2.Location_Point;
SELECT * FROM CW2.Trail_LocationPt;
