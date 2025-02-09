# app/utils.py
import logging
from app.models.user_model import User
from app.services.db_services import fetch_query

def get_user_by_id(user_id):
    """
    Retrieve a user by their ID from the database.
    """
    try:
        # Convert hex string to bytes if needed
        if isinstance(user_id, str):
            user_id = bytes.fromhex(user_id)

        result = fetch_query(
            "SELECT user_id, username, hashed_password, encrypted_salt FROM users WHERE user_id = :user_id",
            {"user_id": user_id},
        )
        if not result:
            logging.warning(f"User with ID '{user_id}' not found.")
            return None
        logging.debug(f"Fetched user data: {result[0]}")  # Log fetched user data
        user_data = result[0]
        return User(
            id=user_data[0],
            username=user_data[1],
            hashed_password=user_data[2],
            encrypted_salt=user_data[3]
        )
    except Exception as e:
        logging.error(f"Error fetching user with ID '{user_id}': {e}")
        return None
