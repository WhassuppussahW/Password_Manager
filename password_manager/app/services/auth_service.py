from flask import current_app
from app.models.user_model import User
from app.services.encryption_service import (
    hash_password,
    generate_salt,
    encrypt_data,
    decrypt_data,
    validate_password,
    decrypt_salt
)
from app.services.db_services import execute_query, fetch_query
from werkzeug.security import check_password_hash, safe_str_cmp
import logging
import base64
from app.utils import get_user_by_id

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def sign_in_user(username, password):
    """
    Register a new user by storing their credentials securely.
    """
    try:
        if len(username) < 4 or len(username) > 25:
            raise ValueError("Username must be between 4 and 25 characters.")
        
        # Get the encryption key from the configuration
        key = current_app.config['ENCRYPTION_KEY']
        logging.debug(f"Encryption key for sign-in: {key}")

        # Generate hashed password and encrypted salt
        salt = generate_salt()
        logging.debug(f"Salt before encryption (bytes): {salt}")

        hashed_password = hash_password(password, salt)
        # Encode hashed password in base64 for textual storage
        encoded_hashed_password = base64.b64encode(hashed_password).decode('utf-8')

        encrypted_salt = encrypt_data(salt, key)  # Encrypt salt (in bytes)
        # Encode encrypted salt in base64 for textual storage
        encoded_encrypted_salt = base64.b64encode(encrypted_salt).decode('utf-8')

        logging.debug(f"Encrypted salt before storing (base64): {encoded_encrypted_salt}")

        execute_query(
            """
            INSERT INTO users (username, hashed_password, encrypted_salt)
            VALUES (:username, :hashed_password, :encrypted_salt)
            """,
            {
                "username": username,
                "hashed_password": encoded_hashed_password,
                "encrypted_salt": encoded_encrypted_salt,
            },
        )
        logging.info(f"User '{username}' signed up successfully.")
        return True
    except Exception as e:
        logging.error(f"Error during sign-in for user '{username}': {e}")
        return False



def login_user(username, password):
    """
    Log in a user by verifying their credentials.
    """
    try:
        # Fetch user from the database
        result = fetch_query(
            "SELECT user_id, hashed_password, encrypted_salt FROM users WHERE username = :username",
            {"username": username},
        )
        if not result:
            logging.warning(f"Login failed: User '{username}' not found.")
            return None

        # Get the encryption key from the configuration
        key = current_app.config['ENCRYPTION_KEY']
        logging.debug(f"Encryption key for login: {key}")

        user_id = result[0][0]
        encoded_hashed_password = result[0][1]
        encoded_encrypted_salt = result[0][2]

        # Decode Base64-encoded hashed password and encrypted salt
        hashed_password = base64.b64decode(encoded_hashed_password)  # Converts to bytes
        encrypted_salt = base64.b64decode(encoded_encrypted_salt)  # Converts to bytes

        # Decrypt the salt using Fernet (requires bytes input)
        salt = decrypt_salt(encrypted_salt, key)
        if salt is None:
            logging.error("Failed to decrypt the salt.")
            return None

        logging.debug(f"Decrypted salt (bytes): {salt}")

        # Hash the input password using the retrieved salt
        input_hashed_password = hash_password(password, salt)
        logging.debug(f"Input hashed password: {input_hashed_password}")


        # Validate hashed passwords
        if safe_str_cmp(input_hashed_password, hashed_password):
            logging.info(f"User '{username}' logged in successfully.")
            return User(user_id, username, hashed_password, encrypted_salt) # Return User object
            # return {"id": user_id, "username": username}
        else:
            logging.warning(f"Login failed: Invalid password for user '{username}'.")
            return None
    except Exception as e:
        logging.error(f"Error during login for user '{username}': {e}")
        return None





def get_user_by_id(user_id):
    """
    Retrieve a user by their ID from the database.
    """
    try:
        result = fetch_query(
            "SELECT user_id, username, hashed_password, encrypted_salt FROM users WHERE user_id = :user_id",
            {"user_id": user_id},
        )
        if not result:
            logging.warning(f"User with ID '{user_id}' not found.")
            return None
        return User.from_db_row(result[0])
    except Exception as e:
        logging.error(f"Error fetching user with ID '{user_id}': {e}")
        return None


"""
def authenticate_user(username, password):
    
    Authenticate a user using database credentials.
    
    try:
        # Input validation
        if not username or not password:
            raise ValueError("Username and password cannot be empty.")

        # Query the database for the stored password hash
        query = "SELECT hashed_password FROM users WHERE username = :username"
        result = fetch_query(query, {"username": username})
        if not result:
            logging.warning(f"Authentication failed: User '{username}' not found.")
            return False

        # Use Werkzeug's `check_password_hash` to securely compare the hashes
        stored_password_hash = result[0][0]
        is_authenticated = check_password_hash(stored_password_hash, password)
        if is_authenticated:
            logging.info(f"User '{username}' authenticated successfully.")
        else:
            logging.warning(f"Authentication failed: Invalid password for user '{username}'.")
        return is_authenticated
    except Exception as e:
        logging.error(f"Error during authentication for user '{username}': {e}")
        return False
"""