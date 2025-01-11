# Trail Application Micro-Service

## Overview
This repository contains the micro-service implementation for managing trail-related data in a Trail Application. This micro-service performs CRUD operations for trails, ensuring secure and efficient data management.

## Features
- RESTful API to manage trails and related data.
- Database schema implementation under the `CW2` schema.
- Deployed and tested on a live server.
- Supports modular and scalable design.

## File Structure
- **`app.py`**: The main Flask application entry point. Initializes the app and sets up routes.
- **`config.py`**: Configuration file for application settings (e.g., database connection, secret keys).
- **`decorators.py`**: Custom decorators for reusable operations like authentication and logging.
- **`generate_key.py`**: Script to generate secure API keys.
- **`models.py`**: Defines the database models and relationships for the micro-service.
- **`routes.py`**: Contains all the API endpoint definitions.
- **`swagger.yml`**: OpenAPI 3.0 specification file for documenting and testing the API.
- **`test.py`**: Unit tests and integration tests for validating the micro-service functionality.
- **`requirements.txt`**: Dependencies for the application can be installed using `pip install -r requirements.txt`.
- **`templates/`**: HTML templates used for the frontend views.
  - **`home.html`**: A basic homepage for the application linking the swagger UI.
- **`SQL/`**: SQL scripts for setting up the database.
  - `schema.sql`: Creates the database structure under the `CW2` schema.

## Deployment
### Prerequisites
- Python 3.9+ installed on the server.
- Access to an SQL database with the listed tables created.
- Flask and other dependencies installed via `requirements.txt`.

### Steps to Deploy Locally
1. Clone this repository:
   ```bash
   git clone https://github.com/BBarrettGreening/TrailMicroService.git
   cd TrailMicroService
