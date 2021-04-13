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

# Global variables
response = ''

def check_token(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if not request.headers.get('authorization'):
            return {'message': 'No token provided'},400
        try:
            user = auth.verify_id_token(request.headers['authorization'])
            request.user = user
        except:
            return {'message':'Invalid token provided.'},400
        return f(*args, **kwargs)
    return wrap

# sign up as a new user (NOT DONE YET!)
@app.route('/api/signup')
def signup():
    
    global response

    # user sends {username, email, and password} data to register.
    if request.method == 'POST':
        
        #aquire data & parse
        user_data = request.data
        user_data = json.loads(request.decode('UTF-8'))

        username = user_data['username']
        email = user_data['email']
        password = user_data['password']

        # check how to store the data in firebase. if it will be hashed or we should hash before sending the password.
        if email is None or password is None:
            return {'message': 'Error: email or password missing'}, 400
            try: 
                user = auth.create_user(
                    email = email,
                    password = password
                )
                return {'message': f'Account successfully created. {user.uid}'}, 200
            except:
                return {'message': 'Error creating user'},400


# Route to get new token for a valid user (FIREBASE AUTH TO BE CHECKED)
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    global response

    # user sends a post request from flutter to login
    if(request.method == 'POST'):
        # aquire the data
        request_data = request.data
        # decode json data using json.loads() -- [json.load() does not work as it needs an object compared to string in json.loads()]
        request_data = json.loads(request_data.decode('UTF-8'))
        
        # email and password.
        email = request_data['email']
        password = request_data['password']

        #debug response to terminal
        response = f'Hello {email}!, {password}'
        print(response)
        return ''
    # works with firebase    
    # try:
    #     user = pb.auth().sign_in_with_email_and_password(email, password)
    #     # Json web token: jwt
    #     jwt = user['idToken']
    #     return {'token': jwt}, 200
    # except:
    #     return {'message': 'Error logging in.'}, 400

# # GET USER BALANCE
# @app.route('/balance', methods=['GET', 'POST'])
# def get_balance():

# # GET USER TRANSACTIONS
# @app.route('/transactions', methods=['GET', 'POST'])
# def get_transactions():

# # ADD NEW TRANSACTION
# @app.route('/newtransaction', methods=['GET', 'POST'])
# def new_transaction():

# # GET TRANSACTION REPORTS
# @app.route('/reports', methods=['GET', 'POST'])
# def reports():


# # TALK TO CHATBOT (this method should all chatbot_response)
# @app.route('/chatbot_request', methods=['GET', 'POST'])
# def chatbot_request():

# # GET FEEDBACK FROM CHATBOT
# @app.route('/chatbot_response', methods=['GET', 'POST'])
# def chatbot_response():


@app.route('/')
def index():
    return 'works'

# get user info
@app.route('/api/userinfo')
def userinfo():
    return {'data': users}, 200


if __name__ == '__main__':
    app.run(debug = True)