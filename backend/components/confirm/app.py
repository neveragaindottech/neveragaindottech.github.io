from datetime import datetime
from flask import Flask, request
from flask_restful import Resource, Api
import re
import requests
import uuid

# Setup App
app = Flask(__name__)
api = Api(app)

class ConfirmUser(Resource):
    """
    Handle User Requests
    """

    def post(self, github_user):
        """
        Try to confirm the user
        :param github_user: Github username
        """
        post_data = request.get_json(force=True)
        return confirm_user(github_user, post_data)

def confirm_user(github_user, data):
    """
    Try to confirm user based on first
    and last name and github
    :param github_user: Github username
    :param data: Post Request Data
    :return: Bool
    """
    url = 'https://github.com/{github_user}'.format(
        github_user=github_user
    )
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    if not first_name:
        return {"error": "Invalid first name"}, 400
    if not last_name:
        return {"error": "Invalid last name"}, 400

    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        pattern = re.compile(r'<span class="vcard-fullname d-block" itemprop="name">([^.]+)</span>')
        try:
            match = re.search(pattern, html)
            found = match.group(1)
            return True
        except AttributeError as e:
            return {"error": "Unable to confirm user automagically"}, 400
    else:
        return {
            "error": "Invalid response from github: {status_code}".format(
                status_code=response.status_code
            )
        }, response.status_code

# Setup Routes
api.add_resource(ConfirmUser, '/v1/confirm/<github_user>')

if __name__ == "__main__":

    # Run the App
    app.run(host="0.0.0.0")
