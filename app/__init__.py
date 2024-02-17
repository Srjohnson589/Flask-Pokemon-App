from flask import Flask
from config import Config
from flask_login import LoginManager
from app.models import db, User
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager()

login_manager.init_app(app)
db.init_app(app)
migrate = Migrate(app, db)

#login manager messages
login_manager.login_view = 'auth.login'
login_manager.login_message = 'You must be logged in to access this page.'
login_manager.login_message_category = 'warning'

#import blueprint into app
from app.blueprints.auth import auth
from app.blueprints.pokesearch import pokesearch

#register blueprint
app.register_blueprint(auth)
app.register_blueprint(pokesearch)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
