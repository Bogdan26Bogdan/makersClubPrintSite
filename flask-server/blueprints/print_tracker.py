from datetime import datetime
import flask
from flask import Blueprint, current_app, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy.orm import Session
from db import db
from db.print_tracker import PrintTracker, validate_GramsUsed
from db.print_file import PrintFile
from blueprints.auth import required_role
import io


print_tracker_bp = Blueprint("print_tracker", __name__)


@print_tracker_bp.route("/submit", methods=["GET", "POST"])
def submit_print():
    # TODO: Add form validation and error handling
    if flask.request.method == "POST":
        # Handle file submission logic here

        new_print = PrintTracker(
            Name=flask.request.form.get("name"),
            PrintName=flask.request.form.get("print_name"),
            Printer="",
            GramsUsed=validate_GramsUsed(flask.request.form.get("grams_used"))[1],
            Duration=int(flask.request.form.get("duration")),
            Color=flask.request.form.get("color"),
            Completed=False,
            Submitted=datetime.now(),
        )

        file_obj = flask.request.files.get("print_file")
        new_file = PrintFile(
            file_name=file_obj.filename,
            file_data=file_obj.read(),
            print_tracker_id=-1,  # Placeholder, will set after adding PrintTracker
        )

        with Session(db.create_engine_instance()) as sql_session:
            sql_session.add(new_print)
            sql_session.commit()
            new_file.print_tracker_id = new_print.id
            sql_session.add(new_file)
            sql_session.commit()

        return "File submitted successfully!"
    elif flask.request.method == "GET":
        return flask.render_template("submit_print.html")

    # If not a valid method it should give an error saying that the method is not allowed.... but in case it doesn't + this removes the linter error
    return redirect("/")


@print_tracker_bp.route("/prints")
@login_required
@required_role("admin")
def view_prints():
    with Session(db.create_engine_instance()) as sql_session:
        prints = sql_session.query(PrintTracker).all()
        return flask.render_template("print_tracker.html", prints=prints)

@print_tracker_bp.route("/download/<int:print_id>")
@login_required
@required_role("admin")
def download_print_file(print_id):
    with Session(db.create_engine_instance()) as sql_session:
        print_file = sql_session.query(PrintFile).filter_by(print_tracker_id=print_id).first()
        if print_file:
            return flask.send_file(
                io.BytesIO(print_file.file_data),
                download_name=print_file.file_name,
                as_attachment=True,
            )
        else:
            return "File not found", 404
