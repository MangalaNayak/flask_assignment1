from flask import Flask, request, jsonify
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resource.user import User
from models.user import UserModel
import sendgrid
from sendgrid.helpers.mail import *
from models.u import gen_otp
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # /auth


api.add_resource(User, '/signup')


def check_email_id():
    email_id1 = request.json['email_id']
    user = UserModel.find_by_emailid(email_id1)
    if user is None:
        return jsonify({'message': 'User with that email id not found.'}), 400
    return user

"""
@app.route('/OTP', methods=['GET'])
def otp_compare():
    otp = request.args.get('otp')
    username = request.args.get('name')
    user = UserModel.find_by_username(username)
    if str(user.otp) == otp:
        return jsonify({"message": "OTP matched"})
    return jsonify({"message": "OTP not matched"})
"""


@app.route('/OTP', methods=['GET'])
def otp_compare():
    otp = request.args.get('otp')
    username = request.args.get('name')
    password1 = request.args.get('password')
    user = UserModel.find_by_username(username)
    if str(user.otp) == otp:
        user.password = password1
        user.save_to_db()
    return "Password is RESET"


@app.route('/reset_password', methods=['POST', 'GET'])
def reset_password():
    data = User.parser.parse_args()
    user = UserModel.find_by_emailid(data['email_id'])
    if user.otp == data['otp']:
        user.password = data['password']
        user.save_to_db()
        return jsonify({"message": "Password has been Reset"})
    return jsonify({"message": "OTP is not matching"})


@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    data = User.parser.parse_args()
    user = UserModel.find_by_emailid(data['email_id'])
    if user is None:
        return jsonify({"User of this Email id doesn't exist"})

    otp = gen_otp()
    user.otp = otp
    user.otp_sent_time = datetime.datetime.utcnow()
    user.save_to_db()
    sg = sendgrid.SendGridAPIClient('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')
    from_email = Email("mangala.nayak@robosoftin.com")
    to_email = Email(user.email_id)
    subject = "OTP"
    content = Content("text/plain", str(otp)+" Use this OTP to reset password. Use /reset_password API")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    return jsonify({"message": "OTP has been sent to your mail"})


def resend_otp():
    gen_otp()
    return jsonify({"msg": "OTP is sent to your Email Id"})

"""
@app.route('/resend_OTP', methods = ['POST'])
def resend_otp():
    forgot_password()
"""

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5002, debug=True)
