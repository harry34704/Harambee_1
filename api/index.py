
from flask import Flask
from main import app as flask_app

app = flask_app

# Handle Vercel serverless function requests
def handler(request, context):
    return app
