from flask import (
    Flask,
    send_from_directory,
    send_file,
    request,
    redirect,
    url_for,
    render_template,
)
import os
import sys

DOWNLOAD_FOLDER = "flask-server/Downloads"

# This allows cross-origin-sharing which is needed for Vue.js as the front end
from flask_cors import CORS

# For loading the environement variables
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

load_dotenv()
DB_USERNAME = os.environ.get("db_username")
DB_PASSWORD = os.environ.get("db_password")

# adds the classes folder to the path
script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, "classes")
sys.path.append(mymodule_dir)

# adds the mongodb folder to the path
script_dir = os.path.dirname(__file__)
mymodule_dir = os.path.join(script_dir, "mongodb")
sys.path.append(mymodule_dir)

# remaining imports
import database
from order import Order, create_order
from file import File
import printer
from filament import Filament


app = Flask(__name__)
# Implements CORS
CORS(app)

# Cap file size at 15MB
app.config["MAX_CONTENT_LENGTH"] = 15 * 1000 * 1000
ALLOWED_EXTENSIONS = {"gcode", "txt", "stl"}

# Helper function for file handling


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/flask/submit_form/", methods=["GET", "POST"])
def file_submittion():
    if request.method == "POST":
        failed = []

        # Check that parts of the form are filled out
        if "ID" not in request.form or request.form["ID"] == "":
            failed.append("ID")
        if "color" not in request.form or request.form["color"] == "":
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

    # redirects back to the testing page
    return redirect(url_for("testing_page"))


@app.route("/flask/testing/")
def testing_page():
    # Create a database object
    db = database.Database(DB_USERNAME, DB_PASSWORD)

    # Get all the orders
    search = {"data": "Order"}
    returned = {"_id": 0, "print_title": 1, "filament_colour": 1, "order_date": 1}
    orders = db.find_object("Order", search, returned)
    orders = [list(i.values()) for i in orders]

    print(orders)
    return render_template("testing.html", orders=orders)


@app.route("/")
def hello():
    return redirect(url_for("home"))


@app.route("/index")
def home():
    # Create a database object
    db = database.Database(DB_USERNAME, DB_PASSWORD)

    # Get all the orders
    search = {"data": "Printer"}
    returned = {"_id": 0, "ID": 1, "status": 1}
    printers = db.find_object("Printer", search, returned)
    printers = [list(i.values()) for i in printers]

    print(printers)
    return render_template("index.html", printers=printers)


@app.route("/file_upload")
def file_upload():
    return render_template("fileSubmittion.html")


@app.route("/updatePrinterStatus")
def update_printer_status():
    db = database.Database(DB_USERNAME, DB_PASSWORD)
    search = {"data": "Printer"}
    printers = db.find_object("Printer", search)
    printers = [i["ID"] for i in printers]

    # Get all the orders
    search = {"data": "Order"}
    returned = {
        "_id": 0,
        "order_number": 1,
        "print_title": 1,
        "filament_colour": 1,
        "student_ID": 1,
    }
    orders = db.find_object("Order", search, returned)
    orders = [list(i.values()) for i in orders]  # Get all values
    orders = [
        [i[:1], i[1:]] for i in orders
    ]  # Split the order number from the rest of the values

    return render_template(
        "updatePrinterStatus.html",
        printers=printers,
        orders=orders,
        statuses=printer.STATUSES,
    )


@app.route("/printerUpdateSubmission", methods=["GET", "POST"])
def printerUpdateSubmission():
    if request.method == "POST":
        pass
    return redirect(url_for("update_printer_status"))


@app.route("/filament_upload", methods=["GET", "POST"])
def addFilament():
    if request.method == "POST":
        print(request.form)

        if "colour" not in request.form:
            return "Colour not supplied"

        # Create the filament object and then add it to the database
        fil = Filament(
            request.form["colour"],
            (
                float(request.form["cost_per_gram"])
                if "cost_per_gram" in request.form
                else 0.03
            ),
            request.form["material"] if "material" in request.form else "PLA",
        )
        db = database.Database(DB_USERNAME, DB_PASSWORD)
        db.add_value(fil)

    return redirect(url_for("update_printer_status"))


@app.route("/fileDownload")
def file_download():
    db = database.Database(DB_USERNAME, DB_PASSWORD)
    search = {"data": "File"}
    returned = {"_id": 0, "order_number": 1}
    files = db.find_object("File", search, returned)
    files = [list(i.values()) for i in files]

    for i in files:
        search = {"data": "Order", "order_number": i[0]}
        returned = {"_id": 0, "print_title": 1}
        print_title = db.find_object("Order", search, returned)
        i.append(print_title[0]["print_title"])

    return render_template("fileDownload.html", files=files)


@app.route("/download/<order_number>")
def download_file(order_number):
    db = database.Database(DB_USERNAME, DB_PASSWORD)
    search = {"data": "File", "order_number": order_number}
    returned = {"_id": 0, "file": 1}
    file = db.find_object("File", search, returned)
    file = file[0]["file"]

    search = {"data": "Order", "order_number": order_number}
    returned = {"_id": 0, "print_title": 1}
    print_title = db.find_object("Order", search, returned)
    print_title = print_title[0]["print_title"]

    # Create a file in the Downloads folder
    if not os.path.exists(f"{DOWNLOAD_FOLDER}/{print_title}"):
        f = open(f"{DOWNLOAD_FOLDER}/{print_title}", "x")
        f.close()

    # Write the file
    if ".txt" in print_title:
        # txt file
        with open(f"{DOWNLOAD_FOLDER}/{print_title}", "w+") as f:
            f.write(file.decode())
    else:
        # gcode or stl file
        with open(f"{DOWNLOAD_FOLDER}/{print_title}", "wb") as f:
            f.write(file)

    return send_file(f"Downloads/{print_title}", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
