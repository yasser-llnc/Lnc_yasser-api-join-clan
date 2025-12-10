from flask import Flask, jsonify
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

app = Flask(__name__)

# ضع هنا جميع دوالك:
# Encrypt_ID()
# encrypt_api()
# get_jwt()
# join_clan()
# exit_clan()

@app.route("/")
def home():
    return {"status": "API ON"}

# 🚫 لا تضيف app.run()
