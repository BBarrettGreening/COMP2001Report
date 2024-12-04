from functools import wraps
from flask import session, flash, redirect, url_for

def role_required(required_role):
    """Decorator for role-based access control."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if session.get("user_role") != required_role:
                flash("Access denied. You do not have the required permissions.", "danger")
                return redirect(url_for("home"))
            return func(*args, **kwargs)
        return wrapper
    return decorator
