from flask import Flask, send_from_directory
#This allows cross-origin-sharing which is needed for Vue.js as the front end
from flask_cors import CORS


app= Flask(__name__)
CORS(app) #Implements CORS

@app.route("/")
def hello():
    return "Hello"

if __name__ == "__main__":
    app.run(debug=True)
