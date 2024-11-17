from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from api.adminlogin_api import AdminLoginAPI
from utilities.swen_344_db_utils import exec_sql_file

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

# Initialize JWT Manager
jwt = JWTManager(app)

api = Api(app)
api.add_resource(AdminLoginAPI, '/admin/login', resource_class_kwargs={'bcrypt': bcrypt})

def setup_database():
    print("Setting up the database...")
    exec_sql_file('data/data.sql')

if __name__ == '__main__':
    setup_database()
    app.run(debug=True)
