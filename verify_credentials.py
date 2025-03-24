import os

# Check if the environment variable is set
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

if credentials_path:
    print(f"✅ GOOGLE_APPLICATION_CREDENTIALS is set to: {credentials_path}")
else:
    print("❌ GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.")
