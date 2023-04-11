from flask import Flask
from flask_login import LoginManager
from .config import Configuration
from .models import db, Employee
from .routes import orders
from .routes import session

app = Flask(__name__)

app.config.from_object(Configuration)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.db'
db.init_app(app)
app.register_blueprint(orders.bp)
app.register_blueprint(session.bp)


login = LoginManager(app)
login.login_view = 'session.login'


@login.user_loader
def load_user(id):
    return Employee.query.get(int(id))
