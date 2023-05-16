from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from os import path
from flask_login import LoginManager
import folium
import redis

db = SQLAlchemy()
DB_NAME = "baseD.db"


def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret key'
#    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:11111111@localhost/baseD'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # r = redis.Redis(host='localhost', port=6379, db=0)

    from .models import User, Vehicle, Gps

    # create_database(app)


    
    with app.app_context():
        db.create_all()
        subquery = db.session.query(
            Gps.vehicle_id,
            func.max(Gps.time).label('max_time')
        ).group_by(Gps.vehicle_id).subquery()

        vehicles = db.session.query(
            Gps
        ).join(
            subquery,
            db.and_(
                Gps.vehicle_id == subquery.c.vehicle_id,
                Gps.time == subquery.c.max_time
            )
        ).all()

    if len(vehicles) > 0:
        map = folium.Map(location=[vehicles[0].lat, vehicles[0].lon], zoom_start=15)
    else:
        map = folium.Map(location=[36.7958604, 10.1805513], zoom_start=15)

    for Gps in vehicles:
        folium.Marker([Gps.lat, Gps.lon],
                      tooltip=f"<b>ID: {Gps.vehicle_id}</b><br><b>Latitude:</b> {Gps.lat}<br><b>Longitude:</b> {Gps.lon}<br><b>Altitude:</b> {Gps.alt} m<br><b>Speed:</b> {Gps.speed} km/h<br><b>Time:</b> {Gps.time}",
                      icon=folium.Icon(icon='train',prefix='fa')).add_to(map),

    map.save('website/templates/map.html')


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


# def create_database(app):
#     if not path.exists('website/' + DB_NAME):
#         db.create_all(app=app)
#         print('Created Database!')
