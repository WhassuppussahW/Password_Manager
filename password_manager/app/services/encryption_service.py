import hashlib
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet, InvalidToken
import logging
import base64
from cryptography.hazmat.backends import default_backend


# Configure logging to display debug messages
logging.basicConfig(level=logging.DEBUG)

def hash_password(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashlib.sha256(),
        length=32,
        salt=salt,
        iterations=200000
    )
    return kdf.derive(password.encode()) # Output in bytes, 32b


def encrypt_data(data, key):
    try:
        fernet = Fernet(key)
        if isinstance(data, str):
            encoded_data = data.encode()  # Convert to bytes if it's a string
        else:
            encoded_data = data  # Assume it's already bytes
        logging.debug(f"Data before encryption (bytes): {encoded_data}")
        encrypted_data = fernet.encrypt(encoded_data)
        logging.debug(f"Encrypted data: {encrypted_data}")
        return encrypted_data
    except Exception as e:
        print(f"Encryption error: {e}")
        return None

    

def decrypt_data(token, key):
    try:
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(token)
        logging.debug(f"Data after decryption (bytes): {decrypted_data}")
        
        # Decode the decrypted data back to a string
        decoded_data = decrypted_data.decode('utf-8')
        logging.debug(f"Data after decoding (string): {decoded_data}")

        return decoded_data  # Return the decoded string
    except InvalidToken:
        print("Invalid token. Decryption failed.")
        return None
    except Exception as e:
        print(f"Decryption error: {e}")
        return None


def decrypt_salt(token, key):
    try:
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(token)
        logging.debug(f"Salt after decryption (bytes): {decrypted_data}")
        
        return decrypted_data  # Return raw bytes without decoding
    except InvalidToken:
        logging.error("Invalid token. Decryption of salt failed.")
        return None
    except Exception as e:
        logging.error(f"Decryption error: {e}")
        return None


    
def validate_password(provided_password, stored_password): 
    return provided_password == stored_password

# Example of generating a random salt
def generate_salt():
    return os.urandom(16)  # Generates a random 16-byte salt


def derive_key(master_password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256,
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return key

