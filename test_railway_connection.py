# test_railway_connection.py
from dotenv import load_dotenv
import os

load_dotenv()

print("Testing Railway connection variables:")
print(f"DB_HOST: {os.getenv('DB_HOST')}")
print(f"DB_PORT: {os.getenv('DB_PORT')}")
print(f"DB_USER: {os.getenv('DB_USER')}")
print(f"DB_PASSWORD: {'***' if os.getenv('DB_PASSWORD') else 'NOT SET'}")
print(f"DB_NAME: {os.getenv('DB_NAME')}")

# Now test actual connection
from db_config import DatabaseConfig

try:
    DatabaseConfig.initialize_pool()
    print("\n✅ Successfully connected to Railway MySQL!")
except Exception as e:
    print(f"\n❌ Connection failed: {e}")