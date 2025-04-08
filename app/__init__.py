from flask import Flask, jsonify, send_from_directory
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint
from app.config import Config
from app.extensions import db  
from app.routes.auth import auth_bp

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    migrate = Migrate(app, db)

    from app.routes.main import main_bp
    from app.routes.classes import classes_bp
    from app.routes.schedule import schedule_bp

    swaggerui_blueprint = get_swaggerui_blueprint(
        app.config["SWAGGER_URL"],
        app.config["API_URL"]
    )

    app.register_blueprint(main_bp)
    app.register_blueprint(classes_bp, url_prefix='/api')
    app.register_blueprint(schedule_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(swaggerui_blueprint, url_prefix=app.config["SWAGGER_URL"])

    with app.app_context():
        from app import models  

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found. Please check your URL."}), 404
    
    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory('static', path)

    return app
    
