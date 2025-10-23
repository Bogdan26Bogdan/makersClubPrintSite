from functools import wraps
from flask_login import current_user, login_user, logout_user, login_required
from flask import Blueprint, current_app, redirect, url_for
from flask import render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Session
from db import user_and_role, db
from db.db import create_engine_instance
import secrets
from db.magic_value import MagicValue
from datetime import datetime

auth = Blueprint("auth", __name__)


def required_role(role: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check that the role exists
            role_to_check_against = None
            with Session(
                db.create_engine_instance(), expire_on_commit=False
            ) as db_session:
                role_to_check_against = (
                    db_session.query(user_and_role.Role).filter_by(role=role).first()
                )

            if role_to_check_against is None:
                raise ValueError("Role does not exist")

            """
            This needs to work with flask, so stealing the way that
            flask_login does it.
            """
            has_role = False
            with Session(db.create_engine_instance()) as db_session:
                user = db_session.get(user_and_role.User, current_user.id)
                has_role = role_to_check_against in user.roles
            # Check that the user has the roles
            if current_user.is_authenticated and has_role:
                if callable(getattr(current_app, "ensure_sync", None)):
                    return current_app.ensure_sync(func)(*args, **kwargs)
                return func(*args, **kwargs)
            else:
                return redirect(url_for("auth.unauthorized_page"))

        return wrapper

    return decorator


def login_failed():
    session["failed_login"] = True
    return redirect(url_for("auth.login_page"))


def signup_failed():
    session["failed_signup"] = True
    return redirect(url_for("auth.signup"))


def login_successful(user, next=None):
    login_user(user)
    return redirect(next or url_for("home"))


@auth.route("/login")
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    failed_login = session.pop("failed_login", False)
    return render_template(
        "login.html", failed_login=failed_login, next=request.args.get("next")
    )


@auth.route("/login", methods=["POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    email = request.form.get("email", "")
    password = request.form.get("password", "")
    user = None

    if email == "" or password == "":
        return login_failed()

    with Session(db.create_engine_instance(echo=True)) as sql_session:
        user = sql_session.query(user_and_role.User).filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return login_failed()

    return login_successful(user, next=request.form.get("next"))


@auth.route("/logout")
@auth.route("/signout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@auth.route("/unauthorized")
def unauthorized_page():
    return render_template("unauthorized.html")


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        email = request.form.get("email", "")
        name = request.form.get("name", "")
        password = request.form.get("password", "")
        magic_value = request.form.get("magic_value", "")

        if email == "" or name == "" or password == "" or magic_value == "":
            return signup_failed()

        if not MagicValue.is_magic_value_valid(magic_value):
            return signup_failed()

        with Session(db.create_engine_instance(echo=True)) as sql_session:
            existing_user = (
                sql_session.query(user_and_role.User).filter_by(email=email).first()
            )
            if existing_user:
                # TODO: Create a way to differentiate that the user already exists
                return signup_failed()

            new_user = user_and_role.User(
                email=email,
                name=name,
                password=generate_password_hash(password),
                date_created=datetime.now().isoformat(),
            )
            user_role = (
                sql_session.query(user_and_role.Role).filter_by(role="user").first()
            )

            if not user_role:
                # TODO: THis is more of a sanity check but this does need to be improved
                return signup_failed()

            new_user.roles.append(user_role)
            sql_session.add(new_user)
            sql_session.commit()

            return login_successful(new_user)
    else:
        failed_signup = session.pop("failed_signup", False)
        return render_template("signup.html", failed_signup=failed_signup)


@auth.route("/generate-magic-value")
@login_required
@required_role("admin")
def generate_magic_value():
    magic_value = MagicValue.generate_magic_value()
    return {"magic_value": magic_value}
