from flask import Flask, send_from_directory


app= Flask(__name__)
#Cap file size at 15MB 
app.config['MAX_CONTENT_LENGTH'] = 15 * 1000 * 1000


@app.route("/")
def hello():
    return "Hello"

if __name__ == "__main__":
    app.run(debug=True)
