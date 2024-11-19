from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from datetime import timedelta
from utilities.swen_344_db_utils import exec_sql_file

# Import API resources
from api.adminlogin_api import AdminLoginAPI
from api.adminsignout_api import AdminSignoutAPI
from api.adminaddEvents import AdminAddEventsAPI, AdminEventDetailIDsAPI
from api.userlogin_api import UserLoginAPI
from api.userregister_api import UserRegisterAPI
from api.userviewevent_api import UserViewEventsAPI, UserViewEventDetailsAPI
from api.useraddtobucket_api import UserAddToBucketAPI
from api.usersignout_api import UserSignoutAPI
app = Flask(__name__)
CORS(app)

# App configuration
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30) 
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Initialize API
api = Api(app)

# Add resources with endpoints
api.add_resource(AdminLoginAPI, '/admin/login', resource_class_kwargs={'bcrypt': bcrypt})
api.add_resource(AdminSignoutAPI, '/admin/signout')
api.add_resource(AdminAddEventsAPI, '/admin/addevent')
api.add_resource(UserLoginAPI, '/login', resource_class_kwargs={'bcrypt': bcrypt})
api.add_resource(UserRegisterAPI, '/register', resource_class_kwargs={'bcrypt': bcrypt})
api.add_resource(AdminEventDetailIDsAPI, '/admin/eventdetails/<int:event_id>')
api.add_resource(UserViewEventsAPI, '/viewevents')
api.add_resource(UserViewEventDetailsAPI, '/vieweventdetails/<int:event_id>')
api.add_resource(UserAddToBucketAPI, '/addtobucket')
api.add_resource(UserSignoutAPI, '/signout')

# Function to set up the database
def setup_database():
    print("Setting up the database...")
    exec_sql_file('data/data.sql')

if __name__ == '__main__':
    setup_database()
    app.run(debug=True)
