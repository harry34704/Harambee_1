import os
from flask import Flask
from app import app
from flask_sqlalchemy import SQLAlchemy
# app = Flask(__name__) # Remove this line
# Use the Render PostgreSQL database URL from environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

if __name__ == "__main__":
    # ALWAYS serve the app on port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
