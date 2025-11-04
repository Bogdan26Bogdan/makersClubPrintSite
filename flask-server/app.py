import flask
from flask import redirect
from flask_talisman import Talisman
from db import db
from db.print_tracker import PrintTracker, validate_GramsUsed
from db.print_file import PrintFile
from db.user_and_role import User, Role
from db.printer import Printer
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from datetime import datetime
from flask_login import LoginManager, current_user, login_required
from werkzeug.security import generate_password_hash
from blueprints.auth import required_role
from dotenv import load_dotenv, set_key
import os

from datetime import datetime

app = flask.Flask(__name__)
load_dotenv("instance/.env")


@app.route("/")
def home():
    return flask.render_template("home.html")


def initial_setup():
    """This should be run only the first time the app is started and creates the initial admin user."""
    #Create initial roles
    with Session(db.create_engine_instance()) as sql_session:
        # Sanity check
        users = len(sql_session.query(User).all())
        if users > 0:
            print("Users already exist, skipping initial admin setup.")
        else:
            # Create initial admin user
            userName = input("Enter admin username: ")
            email = input("Enter admin email: ")
            password = input("Enter admin password: ")
            hashed_password = generate_password_hash(password)
            with Session(db.create_engine_instance()) as sql_session:
                admin_role = sql_session.query(Role).filter_by(role="admin").first()
                new_admin = User(
                    name=userName,
                    email=email,
                    password=hashed_password,
                    date_created=datetime.now(),
                    roles=[admin_role],
                )
                sql_session.add(new_admin)
                sql_session.commit()

    # Create the printers
    with Session(db.create_engine_instance()) as sql_session:
        printers = sql_session.query(Printer).all()
        if len(printers) == 2:
            print("Printers already exist, skipping printer setup.")
        else:
            printer1 = Printer(
                Name="Printer 1",
                Status="Idle",
                PrintInProgress=None,
            )
            printer2 = Printer(
                Name="Printer 2",
                Status="Idle",
                PrintInProgress=None,
            )
            sql_session.add_all([printer1, printer2])
            sql_session.commit()


    # set the secret key.
    if os.getenv("SECRET_KEY") == "SUPERSECRETKEY":
        print("Generating new secret key...")
        secret_key = os.urandom(24)
        set_key("instance/.env", "SECRET_KEY", secret_key.hex())
        load_dotenv("instance/.env")

    set_key("instance/.env", "FIRST_START", "False")
    print("Initial setup complete.")


def app_factory():
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    with Session(db.create_engine_instance()) as sql_session:

        role = Role(role="admin")
        role2 = Role(role="user")

        roles_to_add = [role, role2]

        for role in roles_to_add:
            if not sql_session.query(Role).filter_by(role=role.role).first():
                sql_session.add(role)
                sql_session.commit()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id: int):
        from db.user_and_role import User

        with Session(
            db.create_engine_instance(), expire_on_commit=False
        ) as sql_session:
            # Eager load the roles of the user, using selectinload so that the .has_role method works without additional queries
            stmt = (
                select(User)
                .where(User.id == user_id)
                .options(selectinload(User.roles))
            )
            return sql_session.scalars(stmt).first()

    from blueprints.auth import auth as auth_blueprint
    from blueprints.print_tracker import print_tracker_bp
    from blueprints.admin import admin_bp

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(print_tracker_bp)
    app.register_blueprint(admin_bp)

    Talisman(app)


app_factory()


if __name__ == "__main__":
    if os.getenv("FIRST_START") != "False":
        initial_setup()
    app.run(debug=True)
