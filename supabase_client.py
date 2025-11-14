from supabase import create_client
from dotenv import load_dotenv
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, ".env")

# Load .env file with explicit path
load_dotenv(dotenv_path=env_path)

# Debug: Print if .env file was found
if os.path.exists(env_path):
    print(f"✓ Found .env file at: {env_path}")
else:
    print(f"✗ .env file NOT found at: {env_path}")
    print(f"  Current directory: {os.getcwd()}")
    print(f"  Script directory: {script_dir}")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SERVICE_KEY = os.getenv("SERVICE_KEY")

# Debug: Print what was loaded (hide most of the key)
print(f"SUPABASE_URL loaded: {SUPABASE_URL is not None}")
print(f"SERVICE_KEY loaded: {SERVICE_KEY is not None}")

if not SUPABASE_URL or not SERVICE_KEY:
    print("\n✗ ERROR: Missing environment variables!")
    print(f"  SUPABASE_URL: {SUPABASE_URL or 'NOT SET'}")
    print(f"  SERVICE_KEY: {'SET' if SERVICE_KEY else 'NOT SET'}")
    raise ValueError("Missing SUPABASE_URL or SERVICE_KEY in environment variables")

supabase = create_client(SUPABASE_URL, SERVICE_KEY)
print(f"✓ Supabase client initialized: {SUPABASE_URL}")
