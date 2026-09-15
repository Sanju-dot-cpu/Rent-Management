from flask import Flask, render_template, session, redirect, url_for
from config import Config

from routes.auth_routes import auth_bp
from routes.owner_routes import owner_bp
from routes.renter_routes import renter_bp
from routes.room_routes import room_bp
from routes.audit_routes import audit_bp
from routes.electricity_routes import electricity_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY

    app.register_blueprint(owner_bp, url_prefix="/owner")
    app.register_blueprint(renter_bp, url_prefix="/renter")
    app.register_blueprint(room_bp, url_prefix="/owner/room")
    app.register_blueprint(audit_bp, url_prefix="/owner/audit")
    app.register_blueprint(electricity_bp, url_prefix="/owner/electricity")
    app.register_blueprint(auth_bp) 

    @app.route("/", methods=["GET"])
    def index():
        if session.get("token"):
            role = session.get("role")
            if role == "owner":
                return redirect(url_for("owner.dashboard"))
            elif role == "renter":
                return redirect(url_for("renter.view"))
        return render_template("auth/login.html")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)