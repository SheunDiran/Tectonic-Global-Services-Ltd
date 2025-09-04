from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()



class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
class Shipment(db.Model):
    __tablename__ = 'shipments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Sender Info
    sender_name = db.Column(db.String(150), nullable=False)
    sender_phone = db.Column(db.String(20), nullable=False)
    sender_email = db.Column(db.String(150), nullable=False)
    sender_address = db.Column(db.String(255), nullable=False)
    sender_city = db.Column(db.String(100))
    sender_state = db.Column(db.Integer, db.ForeignKey('state.state_id'))
    sender_lga = db.Column(db.Integer, db.ForeignKey('lga.lga_id'))

    # Receiver Info
    receiver_name = db.Column(db.String(150), nullable=False)
    receiver_phone = db.Column(db.String(20), nullable=False)
    receiver_email = db.Column(db.String(150))
    receiver_address = db.Column(db.String(255), nullable=False)
    receiver_city = db.Column(db.String(100))
    receiver_state = db.Column(db.Integer, db.ForeignKey('state.state_id'))
    receiver_lga = db.Column(db.Integer, db.ForeignKey('lga.lga_id'))

    # Package Info
    package_type = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    pickup_date = db.Column(db.Date, nullable=False)
    delivery_date = db.Column(db.Date)  # optional for future use
    notes = db.Column(db.Text)
    voucher_code = db.Column(db.String(50))
    status = db.Column(db.String(50), default='Pending')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("Users", backref="shipments")
    sender_state_rel = db.relationship("State", foreign_keys=[sender_state])
    sender_lga_rel = db.relationship("Lga", foreign_keys=[sender_lga])
    receiver_state_rel = db.relationship("State", foreign_keys=[receiver_state])
    receiver_lga_rel = db.relationship("Lga", foreign_keys=[receiver_lga])



class State(db.Model):
     state_id = db.Column(db.Integer, primary_key=True)
     state_name = db.Column(db.String(80), nullable=False)

class Lga(db.Model):
     lga_id = db.Column(db.Integer, primary_key=True)
     state_id = db.Column(db.Integer, db.ForeignKey('state.state_id'))
     state = db.relationship('State', backref=db.backref('lgas', lazy=True))
     lga_name = db.Column(db.String(50), nullable=False)     


