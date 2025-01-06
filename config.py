from dotenv import load_dotenv
import os

# Load variables from local .env file, force reload
load_dotenv(dotenv_path=".env", override=True)

# Load environment variables
HUGGING_FACE_API_KEY = os.getenv("HUGGING_FACE_API_KEY")
