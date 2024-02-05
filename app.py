# setting up flask app
import os
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from apis import *


app = Flask(__name__)
api = Api(app)

# setting up the api's
api = Api(app)
api.add_resource(UserAPI, '/user', '/user/<string:email>', '/user/<int:id>')
api.add_resource(HotelAPI, '/hotel', '/hotel/<string:name>' , '/hotel/<int:id>')
api.add_resource(BookingAPI, '/booking', '/booking/<int:id>')
if __name__ == '__main__':
    app.run(debug=True)