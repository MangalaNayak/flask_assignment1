from db import db
import datetime
#from passlib.apps import custom_app_context as pwd_context


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email_id = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80))
    otp = db.Column(db.String(80))
    otp_sent_time = db.Column(db.DateTime)

    def __init__(self, username, email_id, password, otp):
        self.username = username
        self.email_id = email_id
        self.password = password
        self.otp = otp

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_emailid(cls, email_id):
        return cls.query.filter_by(email_id=email_id).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()


