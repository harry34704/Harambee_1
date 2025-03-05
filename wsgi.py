
import os
from main import app

# Set Flask to production mode
app.debug = False
app.config['ENV'] = 'production'

# Vercel uses this as the serverless function entry point
def handler(request, context):
    return app(request, context)

# For local development
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
