from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Define a default value for SQLALCHEMY_DATABASE_URL in case it's not set in the environment
default_db_url = "sqlite:///./sql_app.db"

# Get the SQLALCHEMY_DATABASE_URL from the environment, using the default value if it's not set
SQLALCHEMY_DATABASE_URL = os.environ.get("SQLALCHEMY_DATABASE_URL", default_db_url)
print(SQLALCHEMY_DATABASE_URL)
# SQLALCHEMY_DATABASE_URL = os.environ.get("SQLALCHEMY_DATABASE_URL_LOCAL", default_db_url)


SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24