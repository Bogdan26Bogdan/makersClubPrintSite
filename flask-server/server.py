from flask import Flask, send_from_directory, request, redirect, url_for, render_template
import os
import sys

# This allows cross-origin-sharing which is needed for Vue.js as the front end
from flask_cors import CORS

# For loading the environement variables
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

load_dotenv()
DB_USERNAME = os.environ.get("username")
DB_PASSWORD = os.environ.get("password")

# adds the classes folder to the path
script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, "classes")
sys.path.append(mymodule_dir)

# adds the mongodb folder to the path
script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, "mongodb")
sys.path.append(mymodule_dir)

#remaining imports
import database
from order import Order, create_order
from file import File


app = Flask(__name__)
# Implements CORS
CORS(app)

# Cap file size at 15MB
app.config["MAX_CONTENT_LENGTH"] = 15 * 1000 * 1000
ALLOWED_EXTENSIONS = {"gcode", "txt"}

# Helper function for file handling


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/flask/submit_form/", methods=["GET", "POST"])
def form_submittion():
    if request.method == "POST":
        failed = []

        # Check that parts of the form are filled out
        if "ID" not in request.form:
            failed.append("ID")
        if "color" not in request.form:
            failed.append("color")

        # Checks if a proper file was uploaded
        if "file" not in request.files:
            failed.append("file")
        else:
            file = request.files["file"]
            if file.filename == "" or not allowed_file(file.filename):
                failed.append("file")

        # If any of the checks failed then we return a list with the parts
        # were not properly supplied
        if len(failed) != 0:
            return failed

        ID = request.form["ID"]  # Holds the ID from the form
        # Holds the chosen color from the form
        filament_color = request.form["color"]

        # grabs the name of the file to use as the print title
        print_title = secure_filename(file.filename)

        # Create the order and get the order number
        order_obj = create_order(filament_color, print_title, ID)

        # Create the file object that we will be uploading to the db
        file_obj = File(ID, order_obj.order_number, file)

        # Create a database object
        db = database.Database(DB_USERNAME, DB_PASSWORD)

        # Upload the order and file to the database
        db.add_value(order_obj)
        db.add_value(file_obj)
    
    #redirects back to the testing page 
    return redirect(url_for("testing_page"))

@app.route("/flask/testing/")
def testing_page(): 
    # Create a database object
    db = database.Database(DB_USERNAME, DB_PASSWORD)

    #Get all the orders
    search = {"data": "Order"}
    returned = {"_id" : 0, "print_title": 1,
                "filament_colour": 1, "order_date": 1}
    orders = db.find_object("Order", search, returned)
    orders = [list(i.values()) for i in orders]

    print(orders)
    return render_template("testing.html", orders=orders)


@app.route("/")
def hello():
    return redirect(url_for("form_submittion"))


if __name__ == "__main__":
    app.run(debug=True)
