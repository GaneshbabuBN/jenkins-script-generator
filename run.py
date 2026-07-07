from waitress import serve
from app import app
import logging
import sys


logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO
)


print("Starting Waitress server...", flush=True)


serve(
    app,
    host="0.0.0.0",
    port=5000
)


print("Server stopped.", flush=True)
