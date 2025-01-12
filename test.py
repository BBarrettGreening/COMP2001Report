import requests
import pytest

# Base URL of the micro-service
BASE_URL = "http://127.0.0.1:8000/api"

# Example user credentials
ADMIN_CREDENTIALS = {
    "username": "grace@plymouth.ac.uk",
    "password": "ISAD123!"
}

STANDARD_CREDENTIALS = {
    "username": "ada@plymouth.ac.uk",
    "password": "insecurePassword"
}

# Global variables for tokens
admin_token = None
standard_token = None

# Helper function to login and retrieve token
def login_and_get_token(credentials):
    response = requests.post(f"{BASE_URL}/login", json=credentials)
    assert response.status_code == 200, f"Login failed: {response.text}"
    data = response.json()
    assert "token" in data, "Token not returned in response"
    return data["token"]

# Test login for admin and standard users
def test_login():
    global admin_token, standard_token

    # Login as admin
    admin_token = login_and_get_token(ADMIN_CREDENTIALS)
    assert admin_token is not None, "Admin login failed"

    # Login as standard user
    standard_token = login_and_get_token(STANDARD_CREDENTIALS)
    assert standard_token is not None, "Standard user login failed"

# Test fetching all trails for admin
def test_get_admin_trails():
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = requests.get(f"{BASE_URL}/trails/admin", headers=headers)
    assert response.status_code == 200, f"Failed to get admin trails: {response.text}"
    trails = response.json()
    assert "trails" in trails
    assert isinstance(trails["trails"], list)

# Test fetching all trails for standard user
def test_get_standard_trails():
    headers = {"Authorization": f"Bearer {standard_token}"}
    response = requests.get(f"{BASE_URL}/trails/standard", headers=headers)
    assert response.status_code == 200, f"Failed to get standard trails: {response.text}"
    trails = response.json()
    assert "trails" in trails
    assert isinstance(trails["trails"], list)

# Test adding a new trail (admin only)
def test_add_trail():
    headers = {"Authorization": f"Bearer {admin_token}"}
    new_trail = {
        "Trail_name": "New Test Trail",
        "Trail_Summary": "Test Summary",
        "Trail_Description": "Test Description",
        "Difficulty": "Medium",
        "Location": "Test Location",
        "Length": 10.5,
        "Elevation_gain": 500,
        "Route_type": "Loop",
        "OwnerID": 1,
        "LocationPoint1": None,
        "LocationPoint2": None,
        "LocationPoint3": None,
        "LocationPoint4": None,
        "LocationPoint5": None,
    }
    response = requests.post(f"{BASE_URL}/trails/add", json=new_trail, headers=headers)
    assert response.status_code == 201, f"Failed to add trail: {response.text}"

# Test updating a trail (admin only)
def test_update_trail():
    headers = {"Authorization": f"Bearer {admin_token}"}
    trail_id = 3
    updated_trail = {
        "Trail_name": "Updated Trail Name",
        "Trail_Summary": "Updated Summary",
        "Trail_Description": "Updated Description",
        "Difficulty": "Hard",
        "Location": "Updated Location",
        "Length": 12.5,
        "Elevation_gain": 600,
        "Route_type": "Out and Back",
        "OwnerID": 1,
    }
    response = requests.put(f"{BASE_URL}/trails/update/{trail_id}", json=updated_trail, headers=headers)
    assert response.status_code in [200, 404], f"Failed to update trail: {response.text}"

# Test deleting a trail (admin only)
def test_delete_trail():
    headers = {"Authorization": f"Bearer {admin_token}"}
    trail_id = 3
    response = requests.delete(f"{BASE_URL}/trails/delete/{trail_id}", headers=headers)
    assert response.status_code in [200, 404], f"Failed to delete trail: {response.text}"

# Test adding features to a trail (admin only)
def test_add_features():
    headers = {"Authorization": f"Bearer {admin_token}"}
    trail_id = 2
    features = ["Waterfall", "Viewpoint"]
    response = requests.post(f"{BASE_URL}/trails/{trail_id}/features", json=features, headers=headers)
    assert response.status_code == 200, f"Failed to add features: {response.text}"

# Test removing a feature from a trail (admin only)
def test_remove_feature():
    headers = {"Authorization": f"Bearer {admin_token}"}
    trail_id = 1
    feature_id = 1
    response = requests.delete(f"{BASE_URL}/trails/{trail_id}/features/{feature_id}", headers=headers)
    assert response.status_code in [200, 404], f"Failed to remove feature: {response.text}"

# Test updating location points (admin only)
def test_update_location_points():
    headers = {"Authorization": f"Bearer {admin_token}"}
    trail_id = 1
    location_points = [
        {"Latitude": 51.5074, "Longitude": -0.1278, "Description": "Point 1"},
        {"Latitude": 51.5075, "Longitude": -0.1279, "Description": "Point 2"}
    ]
    response = requests.put(f"{BASE_URL}/trails/{trail_id}/location-points", json=location_points, headers=headers)
    assert response.status_code == 200, f"Failed to update location points: {response.text}"

# Test removing a location point (admin only)
def test_remove_location_point():
    headers = {"Authorization": f"Bearer {admin_token}"}
    trail_id = 1
    location_point_id = 1
    response = requests.delete(f"{BASE_URL}/trails/{trail_id}/location-points/{location_point_id}", headers=headers)
    assert response.status_code in [200, 404], f"Failed to remove location point: {response.text}"

# Run tests
if __name__ == "__main__":
    pytest.main(["-v", "--disable-warnings"])
