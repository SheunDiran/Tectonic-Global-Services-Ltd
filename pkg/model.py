from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone_number = db.Column(db.String(20), nullable=False)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    maxprice = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('services', lazy=True))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    





class EmailNotification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'))
    booking = db.relationship('Booking', backref=db.backref('email_notifications', lazy=True))
    notification_type = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)  # Add this line
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)




class Testimonials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(50), default='pending')

class State(db.Model):
     state_id = db.Column(db.Integer, primary_key=True)
     state_name = db.Column(db.String(80), nullable=False)

class Lga(db.Model):
     lga_id = db.Column(db.Integer, primary_key=True)
     state_id = db.Column(db.Integer, db.ForeignKey('state.state_id'))
     state = db.relationship('State', backref=db.backref('lgas', lazy=True))
     lga_name = db.Column(db.String(50), nullable=False)     

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    booking_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(100), nullable=False)
    user = db.relationship('Users', backref=db.backref('bookings', lazy=True))
    lga_id = db.Column(db.Integer, db.ForeignKey('lga.lga_id'))
    state_id = db.Column(db.Integer, db.ForeignKey('state.state_id'))
    service = db.relationship('Service', backref=db.backref('bookings', lazy=True))     