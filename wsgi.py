
from flask import Flask
from main import app

# For Vercel serverless function
def handler(request, context):
    # The request object is a WSGI object
    return app

# For local development
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
