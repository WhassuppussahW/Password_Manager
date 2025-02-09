import cx_Oracle
import os
from dotenv import load_dotenv
import logging


logging.basicConfig(level=logging.ERROR)
# Load environment variables from the .env file
load_dotenv()

# Database connection details from environment variables
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_url = os.getenv('DB_URL')  # TNS name from tnsnames.ora

# Path to the Oracle Instant Client
oracle_client_path = "/opt/oracle/instantclient_19_24"
# Path to the wallet files 
wallet_location = "/home/ubuntu/wallet" # actual path 

cx_Oracle.init_oracle_client(lib_dir=oracle_client_path)

# Function to get a database connection
def get_connection():
    return cx_Oracle.connect(
        user=db_username,
        password=db_password,
        dsn='passwordmanagerdb_medium',
        encoding="UTF-8"
    )

# Function to execute a query
def execute_query(query, params=None):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(query, params or {})
        connection.commit()
    except cx_Oracle.DatabaseError as e:
        logging.error(f"Database error: {e}")
        raise
    finally:
        cursor.close()
        connection.close()

# Function to fetch results from a query
def fetch_query(query, params=None):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(query, params or {})
        result = cursor.fetchall()

        # Add debug logging to check the content of each row
        for row in result:
            logging.debug(f"Fetched row: {row}")

        return result
    except cx_Oracle.DatabaseError as e:
        logging.error(f"Database error: {e}")
        raise
    finally:
        cursor.close()
        connection.close()

