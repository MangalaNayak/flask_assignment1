from db import db
import datetime
#from passlib.apps import custom_app_context as pwd_context


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email_id = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80))
    otp = db.Column(db.Integer)
    otp_sent_time = db.Column(db.DateTime)

    def __init__(self, username, email_id, password):
        self.username = username
        self.email_id = email_id
        self.password = password
        self.otp = 0

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



"""
@classmethod
def hash_password(self, password):
    self.password = pwd_context.encrypt(password)


@classmethod
def verify_password(self, password):
    return pwd_context.verify(password, self.password_hash)

class Login(Resource):
    def get(self):
        email = request.json['emailId']
        password = request.json['password']
        if db.users.find({'emailId': email}).count() == 0:
            abort(400, message='User is not found.')
        user = db.users.find_one({'email': email})
        if not check_password_hash(user['password'], password):
            abort(400, message='Password is incorrect.')
        exp = datetime.datetime.utcnow() + datetime.timedelta(hours=app.config['TOKEN_EXPIRE_HOURS'])
        encoded = jwt.encode({'email': email, 'exp': exp},
                             app.config['KEY'], algorithm='HS256')
    return {'email': email, 'token': encoded.decode('utf-8')}
"""