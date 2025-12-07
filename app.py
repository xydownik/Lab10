from flask import Flask
import os
import json

app = Flask(__name__)

@app.route("/")
def index():
    secret_env = os.getenv("APP_SECRET", "NOT_SET")
    secret_file = "NOT_SET"

    if os.path.exists("config.json"):
        with open("config.json") as f:
            secret_file = json.load(f).get("file_secret", "NOT_SET")

    return {
        "secret_from_env": secret_env,
        "secret_from_file": secret_file
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
