from supabase import create_client
from dotenv import load_dotenv
import os

# load .env file in app package
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "app", ".env"))

SUPABASE_URL = os.getenv("SUPABASE_URL")
SERVICE_KEY = os.getenv("SERVICE_KEY")
supabase = create_client(SUPABASE_URL, SERVICE_KEY)
