import base64
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "a2811575-a229-4c95-9995-e995f26098a0"
BARCODE_SCAN_URL = "https://api.cloudmersive.com/barcode/scan/image/file"

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/scan", methods=["GET", "POST"])
def scan():
    result = None
    if request.method == "POST":
        file = request.files.get("barcode_image")
        if file:
            headers = {
                "Apikey": API_KEY
            }
            files = {
                "imageFile": file.read()
            }

            response = requests.post(BARCODE_SCAN_URL, headers=headers, files=files)

            if response.status_code == 200:
                data = response.json()
                if data["Barcodes"]:
                    result = data["Barcodes"][0]["RawText"]
                else:
                    result = "No barcode found."
            else:
                result = f"Error: {response.status_code}"

    return render_template("scan.html", result=result)

@app.route("/generate", methods=["GET", "POST"])
def generate():
    barcode_image = None

    if request.method == "POST":
        text = request.form["barcode_text"]

        url = "https://api.cloudmersive.com/barcode/generate/code128"
        headers = {
            "Apikey": API_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "Value": text
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            barcode_image = base64.b64encode(response.content).decode("utf-8")

    return render_template("generate.html", barcode_image=barcode_image)

if __name__ == "__main__":
    app.run(debug=True)
