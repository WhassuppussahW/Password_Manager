from app.models.user_model import User
import string
import secrets
from app.services.encryption_service import encrypt_data, decrypt_data, derive_key, decrypt_salt  
from app.services.db_services import execute_query, fetch_query  
from flask import current_app
import logging
import base64

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def generate_random_password(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))


def add_password(user_id, master_password, website, password):
    # Fetch the encrypted salt from the database
    result = fetch_query(
        "SELECT encrypted_salt FROM users WHERE user_id = :user_id",
        {"user_id": user_id},
    )
    if not result:
        raise ValueError("User not found.")
    
    
    encoded_encrypted_salt = result[0][0]
    encrypted_salt = base64.b64decode(encoded_encrypted_salt)  # Decode the base64-encoded salt

    # Get the key used to encrypt the salt from the configuration
    key_for_salt = current_app.config['ENCRYPTION_KEY']

    # Decrypt the salt using Fernet
    salt = decrypt_salt(encrypted_salt, key_for_salt)
    if not salt:
        raise RuntimeError("Failed to decrypt the salt.")

    # Derive the key using the master password and the decrypted salt
    key = derive_key(master_password, salt)
    logging.debug(f"Derived key for user_id '{user_id}': {key}")

    if not website or not password:
        raise ValueError("Website and password are required.")

    try:
        # Encrypt the password
        encrypted_password = encrypt_data(password, key)
        if not encrypted_password:
            raise RuntimeError("Password encryption failed.")
        
        # Encode the encrypted password in base64 for textual storage
        encoded_encrypted_password = base64.b64encode(encrypted_password).decode('utf-8')

        # Insert the data into the database
        execute_query(
            """
            INSERT INTO passwords (user_id, website, encrypted_password)
            VALUES (:user_id, :website, :encrypted_password)
            """,
            {"user_id": user_id, "website": website, "encrypted_password": encoded_encrypted_password},
        )
        logging.info(f"Password for user_id '{user_id}' and website '{website}' added successfully.")
    except Exception as e:
        raise RuntimeError(f"Failed to add password: {e}")




def retrieve_password(user_id, website, master_password):
    try:
        result = fetch_query(
            """
            SELECT encrypted_password, encrypted_salt FROM passwords 
            JOIN users ON passwords.user_id = users.user_id 
            WHERE passwords.user_id = :user_id AND website = :website
            """,
            {"user_id": user_id, "website": website},
        )
        if not result:
            logging.error("Password not found in the database.")
            return None

        encrypted_password = result[0][0]
        encoded_encrypted_salt = result[0][1]

        logging.debug(f"Fetched encrypted_password: {encrypted_password}")
        logging.debug(f"Fetched encoded_encrypted_salt: {encoded_encrypted_salt}")

        # Decode and decrypt the salt
        encrypted_salt = base64.b64decode(encoded_encrypted_salt)
        key_for_salt = current_app.config['ENCRYPTION_KEY']
        salt = decrypt_salt(encrypted_salt, key_for_salt)
        logging.debug(f"Salt after decryption (bytes): {salt}")
        
        if not salt:
            logging.error("Failed to decrypt the salt.")
            return None

        # Derive the key using the master password and the decrypted salt
        key = derive_key(master_password, salt)
        logging.debug(f"Derived key: {key}")

        # Decode the encrypted password from Base64
        encrypted_password_bytes = base64.b64decode(encrypted_password)
        logging.debug(f"Decoded encrypted_password (bytes): {encrypted_password_bytes}")

        # Decrypt the password
        password = decrypt_data(encrypted_password_bytes, key)
        if password:
            logging.debug(f"Decrypted password: {password}")
        else:
            logging.error("Password decryption failed.")
        
        return password
    except Exception as e:
        logging.exception("Exception occurred while retrieving password")
        return None



def delete_password(user_id, website):
    try:
        execute_query(
            """
            DELETE FROM passwords WHERE user_id = :user_id AND website = :website
            """,
            {"user_id": user_id, "website": website},
        )
    except Exception as e:
        raise RuntimeError(f"Failed to delete password: {e}")


    
def retrieve_all_websites(user_id):
    try:
        result = fetch_query(
            """
            SELECT website FROM passwords
            WHERE user_id = :user_id
            """,
            {"user_id": user_id},
        )
        websites = [row[0] for row in result]  # Extract websites from the result
        return websites
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve websites: {e}")
