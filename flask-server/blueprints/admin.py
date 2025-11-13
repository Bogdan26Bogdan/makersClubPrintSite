from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from blueprints.auth import required_role
from flask import request
from sqlalchemy.orm import Session
from db import db
from db.print_tracker import PrintTracker
from db.printer import Printer
from db.printer import STATUS_IDLE

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin")
@login_required
@required_role("admin")
def admin_dashboard():
    printers = []

    with Session(db.create_engine_instance()) as sql_session:
        printers = sql_session.query(Printer).all()

        return render_template("admin_dashboard.html", printers=printers)


@admin_bp.route("/admin/action/<int:print_id>")
@login_required
@required_role("admin")
def admin_action(print_id):
    return render_template("admin_edit_print.html", print_id=print_id)


@admin_bp.route("/start_print/<int:print_id>", methods=["POST"])
@login_required
@required_role("admin")
def start_print(print_id):
    printer = request.form.get("printer", "")

    if printer == "":
        return "Printer not specified", 400

    if printer not in ["1", "2"]:
        return "Invalid printer specified", 400

    printer_id = None
    with Session(db.create_engine_instance()) as sql_session:
        print_tracker = (
            sql_session.query(PrintTracker).filter_by(id=print_id).first()
        )
        if not print_tracker:
            return "Print job not found", 404

        printer_obj = sql_session.query(Printer).filter_by(id=int(printer)).first()
        if not printer_obj:
            return "Printer not found", 404

        # TODO: Add checks to see if printer is available
        printer_obj.Status = "Printing"
        printer_obj.PrintInProgress = print_tracker.id
        printer_id = printer_obj.id
        sql_session.commit()

    return redirect(url_for("admin.admin_dashboard"))


@admin_bp.route("/finish_print/<int:printer_id>", methods=["POST"])
@login_required
@required_role("admin")
def finish_print(printer_id: int):
    printer_obj = None
    with Session(db.create_engine_instance()) as sql_session:
        printer_obj = sql_session.query(Printer).filter_by(id=printer_id).first()
        if not printer_obj:
            return "Printer not found", 404

    printer_obj.finish_print()

    return redirect(url_for("admin.admin_dashboard"))
