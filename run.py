from waitress import serve
from app import app

print("Starting Waitress server...")

serve(
    app,
    host="0.0.0.0",
    port=5000
)

print("Server stopped.")