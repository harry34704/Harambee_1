
from main import app

# This is needed for Vercel serverless functions
app.debug = False

# For Vercel's serverless environment
def handler(request, context):
    return app
