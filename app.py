#imports
import firebase_admin
import pyrebase
import json
from firebase_admin import credentials, auth
from flask import Flask, request

# Appconfig
app = Flask(__name__)

# Connect app with firebase
credentials = credentials.Certificate('fbAdminConfig.json')
firebase = firebase_admin.initialize_app(credentials)
pb = pyrebase.initialize_app(json.load(open('fbconfig.json')))

@app.route('/')
def index():
    return '<p>works</p>'

# get user info
@app.route('/api/userinfo')
def userinfo():
    return {'data': users}, 200


if __name__ == '__main__':
    app.run(debug = True)
