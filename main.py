
import random
import string

import json

from flask import Flask, render_template, redirect, request

app= Flask(__name__)
shortened_url = {}

def _generate_short_url(length=6):
    chars = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(chars) for _ in range(length))
    return short_url
 


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        long_url = request.form["long_url"]
        short_url = _generate_short_url()
        while short_url in shortened_url:
            short_url = _generate_short_url()
        shortened_url[short_url] = long_url
        with open("urls.json", "w") as f:
            json.dump(shortened_url, f)
        return render_template("index.html", short_url=f"{request.url_root}{short_url}")

    return render_template("index.html")


@app.route("/<short_url>")
def redirect_url(short_url):
    long_url = shortened_url.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return "URL not found", 404
    

if __name__ == "__main__":
    app.run(debug=True)