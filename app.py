from config import create_connexion_app, db
from routes import routes_blueprint

# Create Connexion app
connexion_app = create_connexion_app()

# Get the Flask app instance from Connexion
app = connexion_app.app

# Register the Blueprint
app.register_blueprint(routes_blueprint)

# Ensure database tables are created if necessary
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    import os

    # Use the FLASK_DEBUG value from environment variables
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"

    # Run the Connexion app (serves Swagger UI at /api/ui/)
    connexion_app.run(host="0.0.0.0", port=8000, debug=debug)
