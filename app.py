from flask import Flask
app = Flask(__name__)

@app.route("/")
@app.route("/Home")

def hello():
    return "<h1> Welcome to RocDoc </h1>"

if __name__ == "__main__":
    app.run(debug=True)
