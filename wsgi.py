
import os
from main import app

# Vercel uses this as the entry point
app.debug = False

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
