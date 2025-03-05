import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import create_app

app = create_app()

# Use the Render PostgreSQL database URL from environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
