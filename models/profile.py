from db import db


class ProfileModel(db.Model):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), db.ForeignKey('users.username'))
    place = db.Column(db.String(80))

    def __init__(self, name, place):
        self.name = name
        self.place = place

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_place(cls, place):
        return cls.query.filter_by(place=place).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'name': self.name, 'place':self.place}

