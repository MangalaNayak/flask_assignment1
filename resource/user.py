#Temporary

from flask_restful import Resource, reqparse
from models.user import UserModel
import sendgrid
from sendgrid.helpers.mail import *


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=False,
                        )
    parser.add_argument('email_id',
                        type=str,
                        required=True,
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
    parser.add_argument('otp_sent_time',
                        type=str,
                        required=False,
                        )

    def post(self):
        data = User.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        if UserModel.find_by_emailid(data['email_id']):
            return {"message": "A user with that email Id already exists"}

        user = UserModel(data['username'], data['email_id'], data['password'])
        user.save_to_db()

        sg = sendgrid.SendGridAPIClient('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')
        from_email = Email("mangala.nayak@robosoftin.com")
        to_email = Email(data['email_id'])
        subject = "Confirmation Email"
        content = Content("text/plain", "User Registered")
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        #print(response.body)
        #print(response.headers)

        return {"message": "User created successfully. "}, 201
