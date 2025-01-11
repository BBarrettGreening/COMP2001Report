import secrets

# Generate a secure random JWT secret key
jwt_secret_key = secrets.token_hex(32)  # Generates a 64-character hex string
print(f"Your JWT Secret Key: {jwt_secret_key}")
