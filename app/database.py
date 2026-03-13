from pymongo import MongoClient
import certifi
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MongoDB URI from environment variable, default to localhost
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "adaptive_test")

# Create MongoDB client
client = MongoClient(
	MONGODB_URI,
	tls=True,
	tlsCAFile=certifi.where(),
	serverSelectionTimeoutMS=30000,
)

# Get database
db = client[DATABASE_NAME]

# Get collections
questions_collection = db["questions"]
sessions_collection = db["sessions"]
