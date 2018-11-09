from random import randint


def gen_otp():
    otp = randint(100000, 999999)
    return otp

"""
def send_email():
    user = check_email_id()
    sg = sendgrid.SendGridAPIClient('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')
    from_email = Email("mangala.nayak@robosoftin.com")
    to_email = Email(user.email_id)
    subject = "OTP"
    otp = gen_otp()
    user.otp = otp
    user.otp_sent_time = datetime.datetime.utcnow()
    user.save_to_db()
"""