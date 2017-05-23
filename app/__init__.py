from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from config import config
from flask_login import LoginManager
from markdown import markdown
import bleach
# from flask_pagedown import PageDown

allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                'h1', 'h2', 'h3', 'p']

def email_hide(args):
    end = args.find('@')
    return args[:end-3]+'***'+args[end:]

def to_html(text):
    return bleach.linkify(bleach.clean(markdown(text, output_format='html'), tags=allowed_tags, strip=True))



bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
# pagedown = PageDown()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    # pagedown.init_app(app)

    env = app.jinja_env
    env.filters['email_hide'] = email_hide
    env.filters['to_html'] = to_html


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    return app