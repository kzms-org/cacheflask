# imports
import json
from flask import Flask, request, render_template

# Appconfig
app = Flask(__name__)

# Routes and their functions

# default route just to test the connection
@app.route('/')
def index():
    return '<p>works</p>'

# CSV preprocessing route that will return a json object with all transactions
@app.route('/csvPreProcessing', methods= ['GET', 'POST'])
def momosFunction():
    return None

# get user info (TEST)
@app.route('/api/userinfo')
def userinfo():
    return {'data': "Abdur Rahman"}, 200

# routes to this page if an incorrect url is entered
@app.errorhandler(404)
def page_not_found(e):
    return {'message': "ERROR 404"}, 404

if __name__ == '__main__':
    app.run(debug = True)
