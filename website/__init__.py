from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import folium

db = SQLAlchemy()
DB_NAME = "basedonee.db"


def create_app():

    m = folium.Map(location=[36.7958604,10.1805513], zoom_start=12)

    folium.Marker([36.7955925,10.1816146],
                
                tooltip='<strong>ID-Vehicle</strong>',
                icon=folium.Icon(icon='train',prefix='fa')).add_to(m),

    m.save('website/templates/map.html')

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret key'
#    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:qwerty12@localhost/basedonee'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Vehicle, Gps

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
