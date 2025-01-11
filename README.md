
# TrailService Micro-Service

## Overview
This repository contains the TrailService micro-service implementation for managing trail-related data in a Trail Application. The service provides secure, modular, and efficient CRUD operations for trails.

## Features
- RESTful API to manage trails and related data.
- Database schema implementation under the `CW2` schema.
- Deployed and tested using a Docker image for portability.
- Designed for scalability and modularity.

## File Structure

### Root Directory
- **`.env`**: Defines environment variables for configuration.
- **`app.py`**: Main Flask application entry point.
- **`config.py`**: Configuration settings (e.g., database connection, secret keys).
- **`generate_key.py`**: Script to generate a JWT key.
- **`models.py`**: Database models and relationships.
- **`routes.py`**: Defines RESTful API endpoints.
- **`swagger.yml`**: API documentation in OpenAPI 3.0 format.
- **`requirements.txt`**: Lists project dependencies.
- **`Dockerfile`**: Defines the Docker image for containerization.
- **`templates/home.html`**: Basic homepage linking to Swagger UI.
- **`SQL/`**: SQL scripts for database setup and management.

### SQL Directory
The `SQL` directory includes:
- Scripts for creating, reading, updating and deleting database records.
- Views and procedures for trail management.
- Supporting documentation and sample result files.

## Deployment

### Prerequisites
- Python 3.9+ installed.
- Access to an SQL database with the `CW2` schema.
- Flask and other dependencies installed via:
  ```bash
  pip install -r requirements.txt
  ```

### Deploy Locally
1. Clone this repository:
   ```bash
   git clone https://github.com/BBarrettGreening/COMP2001Report.git
   cd COMP2001Report
   ```
2. Create a `.env` file in the root directory as described in the [Environment Variables](#environment-variables) section.
3. Run the application:
   ```bash
   python app.py
   ```

### Deploy Using Docker
1. Build the Docker image:
   ```bash
   docker build -t trailservice .
   ```
2. Tag the Docker image:
    ```bash
    docker tag trailservice <username>/trailservice
   ```
3. Run the Docker container:
   ```bash
   docker run -p 8000:8000 <username>/trailservice
   ```

4. Verify the application is running by accessing:
   ```
   http://localhost:8000
   ```

### Environment Variables
Create a `.env` file in the root directory with the following configuration:
```plaintext
SQLALCHEMY_DATABASE_URI=mssql+pyodbc://<username>:<password>@<server>?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes&Encrypt=yes
SECRET_KEY=<your_secret_key>
JWT_SECRET=<your_secret_key>
FLASK_DEBUG=False
```

- **`DATABASE_URL`**: Connection string to your SQL database.
- **`SECRET_KEY`**: Secret key for sessions, allows for secure integration with other services.
- **`JWT_SECRET`**: A secure key for JWT token generation.
- **`FLASK_DEBUG`**: Set to `False` for deployment or `True` for testing.

## Example Usage
Test API endpoints using `curl` or Postman:
```bash
curl -X GET http://localhost:8000/api/trails
```

## Notes
- Ensure that the database is properly initialized with the `CW2` schema before running the service.
- The service has been tested on a live server and is containerized for scalability.
