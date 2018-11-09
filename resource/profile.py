from flask_restful import Resource, reqparse
from models.profile import ProfileModel


class Profile(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id',
                            type=str,
                            required=False,
                            )
    parser.add_argument('name',
                            type=str,
                            required=False,
                            help="This field cannot be blank."
                            )
    parser.add_argument('place',
                            type=str,
                            required=False,
                            )

    def get(self, name):
        store = ProfileModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if ProfileModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400

        store = ProfileModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred creating the store."}, 500

        return store.json(), 201

    def delete(self, name):
        store = ProfileModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}


class StoreList(Resource):
    def get(self):
        return {'stores': list(map(lambda x: x.json(), ProfileModel.query.all()))}
