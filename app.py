from flask import render_template, request, redirect, url_for, session
import requests
from sqlalchemy.sql import text
import config
from models import Person

# App instance
app = config.connex_app
app.add_api(config.basedir / "swagger.yml")

# Set the secret key on the inner Flask app
flask_app = app.app
flask_app.secret_key = "c6dd213a199731bfbb8484b6d6b538a9836d6307bf0b9c34cac74639426354ba"

# Authenticator API URL
AUTH_URL = 'https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users'


@app.route("/", methods=["GET"])
def home():
    if session.get("authenticated"):
        user_role = session.get("user_role")
        if user_role == "Standard":
            people = Person.query.all()
            return render_template("home.html", people=people, role=user_role)
        elif user_role == "Administrator":
            return render_template("home.html", role=user_role)
    return render_template("home.html")


@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    # Validate email and password using Authenticator API
    credentials = {"email": email, "password": password}
    response = requests.post(AUTH_URL, json=credentials)

    if response.status_code == 200:
        response_data = response.json()

        # Check API response is correct for authorised user
        if response_data == ['Verified', 'True']:
            # Get user role from database
            query = text("SELECT AccountID, Role FROM CW2.Account WHERE Email_address = :email")
            user = config.db.session.execute(query, {"email": email}).fetchone()

            if user:
                # Set session data
                session["authenticated"] = True
                session["user_id"] = user.AccountID
                session["user_role"] = user.Role
                session["user_email"] = email
                return redirect(url_for("home"))
            else:
                error_message = "Username or Password Incorrect. Please try again."
                return render_template("home.html", error=error_message)
        else:
            error_message = "Username or Password Incorrect. Please try again."
            return render_template("home.html", error=error_message)
    else:
        error_message = "Authentication API failed. Please try again later."
        return render_template("home.html", error=error_message)


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
