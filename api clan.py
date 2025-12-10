from flask import Flask, jsonify
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

app = Flask(__name__)

# ===========================
# مفاتيح اللعبة
# ===========================

KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
IV = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

def encrypt_api(hex_data):
    data = bytes.fromhex(hex_data)
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    encrypted = cipher.encrypt(pad(data, AES.block_size))
    return encrypted.hex()

def Encrypt_ID(num):
    num = int(num)
    encoded = []
    while True:
        b = num & 0x7F
        num >>= 7
        if num:
            b |= 0x80
        encoded.append(b)
        if not num:
            break
    return bytes(encoded).hex()

# ===========================
# جلب JWT
# ===========================

def get_jwt(uid, password):
    try:
        url = f"https://jwt-tmk.vercel.app/GeneRate-Jwt?uid={uid}&password={password}"
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            return res.text.strip()
        return None
    except:
        return None

# ===========================
# JOIN CLAN
# ===========================

@app.route("/join/<clan>/<uid>/<password>")
def join(clan, uid, password):

    token = get_jwt(uid, password)
    if not token:
        return jsonify({"error": "JWT FAILED"}), 400

    enc = Encrypt_ID(clan)
    payload = f"08{enc}1007"
    encrypted_payload = encrypt_api(payload)

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "deflate, gzip",
        "Authorization": f"Bearer {token}",
        "Content-Length": str(len(encrypted_payload) // 2),
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "clientbp.ggblueshark.com",
        "ReleaseVersion": "OB51",
        "User-Agent": "UnityPlayer/2022.3.47f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
        "X-GA": "v1 1",
        "X-Unity-Version": "2022.3.47f1"
    }

    try:
        res = requests.post(
            "https://clientbp.ggblueshark.com/RequestJoinClan",
            headers=headers,
            data=bytes.fromhex(encrypted_payload)
        )

        return {
            "status": res.status_code,
            "jwt_used": token,
            "response": res.text
        }

    except Exception as e:
        return {"error": str(e)}

# ===========================
# EXIT CLAN
# ===========================

@app.route("/exit/<clan>/<uid>/<password>")
def exit_clan(clan, uid, password):

    token = get_jwt(uid, password)
    if not token:
        return jsonify({"error": "JWT FAILED"}), 400

    enc = Encrypt_ID(clan)
    payload = f"08{enc}1007"
    encrypted_payload = encrypt_api(payload)

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "deflate, gzip",
        "Authorization": f"Bearer {token}",
        "Content-Length": str(len(encrypted_payload) // 2),
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "clientbp.ggblueshark.com",
        "ReleaseVersion": "OB51",
        "User-Agent": "UnityPlayer/2022.3.47f1 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
        "X-GA": "v1 1",
        "X-Unity-Version": "2022.3.47f1"
    }

    try:
        res = requests.post(
            "https://clientbp.ggblueshark.com/QuitClan",
            headers=headers,
            data=bytes.fromhex(encrypted_payload)
        )

        return {
            "status": res.status_code,
            "jwt_used": token,
            "response": res.text
        }

    except Exception as e:
        return {"error": str(e)}

@app.route("/")
def home():
    return {"status": "API READY 🔥"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

