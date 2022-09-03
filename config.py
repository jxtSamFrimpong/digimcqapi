# importing libraries
from flask import Flask, request, Response, jsonify
# creating an instance of the flask app
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
