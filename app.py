from flask import Flask, jsonify, render_template

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")


@app.route("/version", methods=["GET", "POST"])
def version():
    version = "0.0.0"
    with open("version.txt") as f:
        version = f.read()
    output = {"APP": "Medusa", "Version": version.strip()}
    return jsonify(output)


if __name__ == "__main__":
    app.run(debug=True)