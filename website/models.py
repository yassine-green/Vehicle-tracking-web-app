from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Gps(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    alt = db.Column(db.Float)
    speed = db.Column(db.Float)
    time = db.Column(db.DateTime, nullable=False)
    vehicle_id = db.Column(db.String(45), db.ForeignKey('vehicle.reg'))
    
# # Retrieve the latest location for each vehicle
# subquery = db.session.query(
#     Gps.vehicle_id,
#     func.max(Gps.time).label('max_time')
# ).group_by(Gps.vehicle_id).subquery()

# latest_locations = db.session.query(
#     Gps
# ).join(
#     subquery,
#     db.and_(
#         Gps.vehicle_id == subquery.c.vehicle_id,
#         Gps.time == subquery.c.max_time
#     )
# ).all()

class Vehicle(db.Model):
    reg = db.Column(db.String(45),primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(45), unique=True, nullable=False)
    brand = db.Column(db.String(45), nullable=False)
    color = db.Column(db.String(45))
    seats = db.Column(db.Integer, nullable=False)
    inServ = db.Column(db.Date)
    outServ = db.Column(db.Date)
    gpss = db.relationship('Gps')

def __init__(self, reg, brand, color, seats, inServ, outServ):
    self.reg = reg
    self.brand = brand
    self.color = color
    self.seats = seats
    self.inServ = inServ
    self.outServ = outServ

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

