from datetime import datetime
from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
import re
import uuid

# Setup App
app = Flask(__name__)
app.config.from_object('config')
api = Api(app)
db = SQLAlchemy(app)

class User(db.Model):
    """
    User DB Model
    """
    id = db.Column(db.Integer, primary_key=True)
    user_uuid = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    github_user = db.Column(db.String(200))
    position = db.Column(db.String(255)) # Because people in tech can have fun job titles
    company = db.Column(db.String(255)) # StartUps too
    link = db.Column(db.String(2083)) # Max in IE, not that I think we should support IE
    created = db.Column(db.DateTime)
    updated = db.Column(db.DateTime)
    deleted = db.Column(db.Integer, default=0)
    confirmed = db.Column(db.Integer, default=0)

    def __init__(self, first_name, last_name, github_user):
        """
        Constructor for new rows
        :param first_name: First Name
        :param last_name: Last Name
        """
        self.first_name = first_name
        self.last_name = last_name
        self.github_user = github_user
        self.user_uuid = uuid.uuid4()
        self.created = datetime.utcnow()

    def set_position(self, position):
        """
        Yes I know setters are stupid
        don't judge me haha
        :param position: Position
        """
        self.position = position

    def set_company(self, company):
        """
        Set company for user
        :param company: Company name
        """
        self.company = company

    def set_link(self, link):
        """
        Set link for user
        :param link: URL
        """
        self.link = link

    def set_updated(self):
        """
        Set updated time
        Dev note: Not implemented currently - for future use
        """
        self.updated = datetime.utcnow()

class Users(Resource):
    """
    Handle User Requests
    """

    def get(self):
        """
        Get all users
        """
        return get_users()

    def post(self):
        """
        Create new user
        """
        post_data = request.get_json(force=True)
        return create_user(post_data)

def get_users():
    """
    Retreive a list of all users setup
    """
    return User.query.all()

def create_user(data):
    """
    Create a new user
    :param data: Post Data from Request
    :return: User ID
    """
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    github_user = data.get('github_user')
    position = data.get('position')
    company = data.get('company')
    link = data.get('link')

    # Required
    if not validate_string(first_name):
        return {"error": "Invalid first name"}, 400
    if not validate_string(last_name):
        return {"error": "Invalid last name"}, 400
    if not validate_string(github_user):
        return {"error": "Invalid github user"}, 400

    # Optional
    if position is not None:
        if not validate_string(position):
            return {"error": "Invalid position"}, 400
    if company is not None:
        if not validate_string(company):
            return {"error": "Invalid company"}, 400
    if link is not None:
        if not validate_string(link):
            return {"error": "Invalid string"}, 400

    # Add User to DB
    new_user = User(first_name, last_name, github_user)
    if position is not None:
        new_user.set_position(position)
    if company is not None:
        new_user.set_company(company)
    if link is not None:
        new_user.set_link(link)

    return {"success": str(new_user.user_uuid)}

def validate_string(string, search=re.compile(r'[^a-zA-Z0-9.]').search):
    """
    Simple validation helper func
    :param string: String we are testing
    :param regex: Optional regex
    :return: Bool
    """
    return not bool(search(string))

# Setup Routes
api.add_resource(Users, '/v1/user')

if __name__ == "__main__":

    # Run the App
    app.run(host="0.0.0.0")
