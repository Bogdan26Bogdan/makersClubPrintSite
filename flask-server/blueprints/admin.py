from flask import Blueprint, render_template
from flask_login import login_required, current_user
from blueprints.auth import required_role
from flask import request
from sqlalchemy.orm import Session
from db import db
from db.print_tracker import PrintTracker
from db.printer import Printer


admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin")
@login_required
@required_role("admin")
def admin_dashboard():
    return render_template("admin_dashboard.html")


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

    return f"Print job {print_id} started on printer {printer_id}."
