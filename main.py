from app import app

if __name__ == "__main__":
    # ALWAYS serve the app on port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)