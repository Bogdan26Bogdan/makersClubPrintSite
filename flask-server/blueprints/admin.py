from flask import Blueprint, render_template
from flask_login import login_required, current_user
from blueprints.auth import required_role


admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin")
@login_required
@required_role("admin")
def admin_dashboard():
    return render_template("admin_dashboard.html")

