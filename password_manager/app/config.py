import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv() #Read variables from the .env file 

class Config:
    AUTH_TOKEN= os.getenv("AUTH_TOKEN") #Oracle auth token 
    ENCRYPTION_KEY= os.getenv ("ENCRYPTION_KEY") #In order to encrypt the salt
    SECRET_KEY= os.getenv("FLASK_SECRET_KEY") #Flask key
    DB_URL= os.getenv("DB_URL") #DB related
    DB_USERNAME= os.getenv("DB_USERNAME") #DB related
    DB_PASSWORD= os.getenv("DB_PASSWORD") #DB related
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)  # Set session lifetime
    SESSION_COOKIE_SECURE = False # Ensure cookies are only sent over HTTPS but http with the load balancer
    SESSION_COOKIE_HTTPONLY = True # Prevent JavaScript access to cookies
    SESSION_COOKIE_SAMESITE = 'Lax'  # Set SameSite attribute to Lax or Strict
