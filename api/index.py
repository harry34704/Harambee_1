
from flask import Flask
from main import app as flask_app

app = flask_app

# For Vercel serverless function
def handler(request, context):
    return app(request.environ, lambda status, headers: [status, headers])
