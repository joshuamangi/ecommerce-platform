import socket
import time

from utils.config import settings
DB_HOST = settings.DB_HOST
DB_PORT = settings.DB_PORT

MAX_RETRIES = 30
RETRY_DELAY = 2


def wait_for_db():
    retries = 0
    while retries < MAX_RETRIES:
        try:
            print(f"Attempting to connect to {DB_HOST}:{DB_PORT}...")
            with socket.create_connection((DB_HOST, DB_PORT), timeout=5):
                print("Database is available")
                return
        except OSError:
            retries += 1
            print(f"Database not ready. Retrying ({retries}/{MAX_RETRIES})...")
            time.sleep(RETRY_DELAY)

    raise Exception(
        "Could not connect to the database after multiple attempts.")


if __name__ == "__main__":
    wait_for_db()
