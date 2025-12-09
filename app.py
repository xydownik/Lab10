from flask import Flask
import os
import json
import hvac

app = Flask(__name__)

def get_vault_secret():
    vault_addr = os.getenv("VAULT_ADDR", "http://127.0.0.1:8200")
    vault_token = os.getenv("VAULT_TOKEN")

    if not vault_token:
        return "NO_VAULT_TOKEN"

    client = hvac.Client(url=vault_addr, token=vault_token)

    if not client.is_authenticated():
        return "VAULT_AUTH_FAILED"

    try:
        response = client.secrets.kv.v2.read_secret_version(
            mount_point="secret",
            path="app",
        )
        data = response["data"]["data"]
        return data.get("vault_secret", "NO_VAULT_KEY")
    except Exception as e:
        return f"VAULT_ERROR: {e}"

@app.route("/")
def index():
    secret_env = os.getenv("APP_SECRET", "NOT_SET")
    secret_file = "NOT_SET"
    vault_secret = get_vault_secret()

    if os.path.exists("config.json"):
        with open("config.json") as f:
            secret_file = json.load(f).get("file_secret", "NOT_SET")

    return {
        "secret_from_env": secret_env,
        "secret_from_file": secret_file,
        "secret_from_vault": vault_secret,
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
