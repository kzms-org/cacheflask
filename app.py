# #imports
# import firebase_admin
# import pyrebase
import json
# from firebase_admin import credentials, auth
from flask import Flask, request, render_template

# Appconfig
app = Flask(__name__)

# Connect app with firebase
# credentials = credentials.Certificate('fbAdminConfig.json')
# firebase = firebase_admin.initialize_app(credentials)
#pb = pyrebase.initialize_app(json.load(open('fbconfig.json')))

@app.route('/')
def index():
    return '<p>works</p>'

# get user info
@app.route('/api/userinfo')
def userinfo():
    return {'data': "Abdur Rahman"}, 200

@app.errorhandler(404)
def page_not_found(e):
    return {'message': "ERROR 404"}, 404

if __name__ == '__main__':
    app.run(debug = True)
