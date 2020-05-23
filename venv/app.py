from flask_restful import Resource, Api
from flask import Flask, Response, json, jsonify, request, abort
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/kampus'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)


@app.route('/')
def hello_world():
    return 'Selamat Datang'

@app.route('/admin')
def admin():
    return 'Ini Adalah Admin'



class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/helloworld')



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    @staticmethod
    def get_all_users():
        return User.query.all()


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'username', 'email')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route("/user/", methods=["GET"])
def get_user():
    all_users = User.get_all_users()
    result = users_schema.dump(all_users)
    return jsonify(result)

if __name__ == '__main__':
    app.run()
