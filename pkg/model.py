from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db=SQLAlchemy()

class Contact(db.Model):
    __tablename__='tectonic'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    fullname= db.Column(db.String(255), nullable=False)
    phone=db.Column(db.String(255),nullable=False,unique=True)
    service = db.Column(db.String(255), nullable=False)
    message=db.Column(db.Text)
    booked_time = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return {self.fullname}