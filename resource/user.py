from flask_restful import Resource, reqparse
from models.user import UserModel
from reusable import gen_send_otp
import datetime


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        )
    parser.add_argument('email_id',
                        type=str,
                        required=False,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=False,
                        )
    parser.add_argument('otp',
                        type=str,
                        required=False,
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400
        confirm = True
        user = UserModel(**data)

        user.otp = gen_send_otp(user, confirm)
        print(user.otp)
        user.otp_sent_time = datetime.datetime.utcnow()
        user.save_to_db()
        return {"message": "Confirmation OTP has been sent your email"}, 201


class UserList(Resource):
    def get(self):
        return {'users': list(map(lambda x: x.json(), UserModel.query.all()))}
