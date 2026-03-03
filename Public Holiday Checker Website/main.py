from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    holidays = None
    error_message = None
    if request.method == "POST":
        year = request.form.get("year");
        country_code = request.form.get("country_code")

        if year and country_code:
            api_url = f"https://date.nager.at/api/v3/publicholidays/{year}/{country_code}"

            request_answer = requests.get(api_url);

            if request_answer.status_code == 200:
                holidays = request_answer.json()
            elif request_answer.status_code == 404:
                error_message = "There isn't any data for this year or the country"
            else:
                error_message = "Error in API"

    return render_template("home_page.html", holidays = holidays, error = error_message)

if __name__ == "__main__":
    app.run(debug=True)