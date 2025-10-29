import flask
from flask import redirect
from flask_talisman import Talisman
from db import db
from db.print_tracker import PrintTracker, validate_GramsUsed
from db.print_file import PrintFile
from db.user_and_role import User, Role
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from datetime import datetime
from flask_login import LoginManager, current_user, login_required
from werkzeug.security import generate_password_hash
from blueprints.auth import required_role
from dotenv import load_dotenv
import os

from datetime import datetime

app = flask.Flask(__name__)
load_dotenv("instance/.env")


@app.route("/")
def home():
    return flask.render_template("home.html")


def app_factory():
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    with Session(db.create_engine_instance()) as sql_session:
        test_user = User(
            email="test@example.com",
            password=generate_password_hash("password123"),
            date_created=datetime.now(),
            name="testuser",
        )
        test_user_2 = User(
            email="test2@example.com",
            password=generate_password_hash("password123"),
            date_created=datetime.now(),
            name="testuser2",
        )
        role = Role(role="admin")
        role2 = Role(role="user")

        users_to_add = [test_user, test_user_2]
        roles_to_add = [role, role2]

        test_user.roles.append(role)
        test_user_2.roles.append(role2)

        for role in roles_to_add:
            if not sql_session.query(Role).filter_by(role=role.role).first():
                sql_session.add(role)
                sql_session.commit()

        for user in users_to_add:
            if not sql_session.query(User).filter_by(email=user.email).first():
                sql_session.add(user)
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

    app.run(debug=True)
