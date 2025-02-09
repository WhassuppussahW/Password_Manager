# app/models/user_model.py
from flask_login import UserMixin
from typing import Union, Dict

class User(UserMixin):
    def __init__(self, id: Union[str, bytes], username: str, hashed_password: str, encrypted_salt: str):
        self.id = id.hex() if isinstance(id, bytes) else id  # Convert bytes to hex for readability
        self.username = username
        self.hashed_password = hashed_password
        self.encrypted_salt = encrypted_salt

    @classmethod
    def from_db_row(cls, row: Union[tuple, Dict[str, Union[str, bytes]]]):
        return cls(
            id=row[0],  # Index-based access for tuples
            username=row[1],
            hashed_password=row[2],
            encrypted_salt=row[3],
        )
