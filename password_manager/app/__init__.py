from flask import Flask
from .config import Config
from .routes.auth_routes import auth_bp
from .routes.password_routes import password_bp
from .routes.main_routes import main_bp
from dotenv import load_dotenv
from datetime import timedelta
from flask_login import LoginManager
from app.utils import get_user_by_id
from flask_talisman import Talisman
from werkzeug.middleware.proxy_fix import ProxyFix

def create_app():

    load_dotenv()  # Read variables from the .env file 

    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Set session lifetime
    app.secret_key = app.config['SECRET_KEY']

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader 
    def load_user(user_id): 
        return get_user_by_id(user_id)
    
    # Customize CSP settings for Talisman 
    csp = { 
        'default-src': ["'self'"], 
        'style-src': ["'self'", 'https://fonts.googleapis.com', 'https://cdn.jsdelivr.net'], 
        'font-src': ["'self'", 'https://fonts.gstatic.com'],
        'script-src': ["'self'", 'https://cdn.jsdelivr.net', "'self' 'unsafe-inline'"], # Allow scripts from static/js 
        'navigate-to': ["'self'"] # Ensure navigation within the site is allowed
    }
    
    # Initialize Talisman for security headers
    Talisman(app, content_security_policy=csp, force_https=False)

    # Apply ProxyFix to respect X-Forwarded-Proto header from load balancer
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # Register blueprints (modular sets of routes)
    app.register_blueprint(auth_bp)
    app.register_blueprint(password_bp)
    app.register_blueprint(main_bp)

    return app
