import os

from dotenv import load_dotenv

load_dotenv()

FLASK_HOST = "localhost"
FLASK_PORT = 5_000

flask_host = str(os.environ.get("HOST") or FLASK_HOST)
flask_port = int(os.environ.get("PORT") or FLASK_PORT)
is_debug_mode = bool(os.environ.get("DEBUG"))

POSTGRES_HOST = "localhost"
POSTGRES_PROVIDER = "postgresql+psycopg"

postgres_host = str(os.environ.get("POSTGRES_HOST") or POSTGRES_HOST)
postgres_db = os.environ["POSTGRES_DB"]
postgres_password = os.environ["POSTGRES_PASSWORD"]
postgres_port = os.environ["POSTGRES_PORT"]
postgres_user = os.environ["POSTGRES_USER"]
postgres_credentials = f"{postgres_user}:{postgres_password}"
postgres_url = f"{postgres_host}:{postgres_port}"
postgres_uri = (
    f"{POSTGRES_PROVIDER}://{postgres_credentials}@{postgres_url}/{postgres_db}"
)
