from pymongo import MongoClient

# MongoDB Configuration
MONGO_URI = "mongodb+srv://sih:sih@cluster0.bgmt4bj.mongodb.net"  # Change as needed
DATABASE_NAME = "sih"            # Replace with your database name

# Initialize MongoDB Client
client = MongoClient(MONGO_URI)

# Access Database
db = client[DATABASE_NAME]

# Access Collections
users_collection = db["users"]
admins_collection = db["admins"]
applications_collection = db["applications"]
jobs_collection = db["jobs"]
error_logs_collection = db["error_logs"]