from flask import Flask
from app.database import init_db

app = Flask(__name__)

# Initialize database on startup
init_db()

from app import routes  # Import routes after app initialization
