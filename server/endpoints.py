"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
# from http import HTTPStatus
import cities.queries as cqry

from flask import Flask  # , request
from flask_restx import Resource, Api  # , fields  # Namespace
from flask_cors import CORS

# import werkzeug.exceptions as wz

app = Flask(__name__)
CORS(app)
api = Api(app)

ERROR = "Error"
READ = "read"

ENDPOINT_EP = "/endpoints"
ENDPOINT_RESP = "Available endpoints"

HELLO_EP = "/hello"
HELLO_RESP = "hello"
MESSAGE = "Message"

CITIES_EPS = "/cities"
CITY_RESP = "Cities"

HEALTH_EP = "/health"
VERSION_EP = "/version"
VERSION_NAME = "project-sens"


@api.route(f'{CITIES_EPS}/{READ}')
class Cities(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """

    def get(self):
        """
        A trivial endpoint to see if the server is running.
        """

        try:
            cities = cqry.read()
        # prints out the names and the valies with f string
        except ConnectionError as e:
            return {ERROR: str(e)}
        print(f'{cities=}')
        return {CITY_RESP: cities}


@api.route(HELLO_EP)
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        """
        return {HELLO_RESP: 'world'}


@api.route(ENDPOINT_EP)
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """
    def get(self):
        """
        The `get()` method will return a sorted list of available endpoints.
        """
        endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {"Available endpoints": endpoints}


@api.route(HEALTH_EP)
class Health(Resource):
    """
    An endpoint checking to see if the API is responsive
    """
    def get(self):
        return {"status": "ok"}, 200


@api.route(VERSION_EP)
class Version(Resource):
    """
    An endpoint that returns version information
    """
    def get(self):
        import os
        return {
            "name": os.getenv("APP_NAME", VERSION_NAME),
            "version": os.getenv("APP_VERSION", "0.1.0"),
            "env": os.getenv("APP_ENV", "dev"),
        }, 200
# Helper function for testing raise and enpoint behavior


def parse_limit(raw):
    """
    Parse ?limit= query parameter.
    Returns None if not provided.
    Raises ValueError if invalid.
    """
    if raw is None or raw == "":
        return None
    n = int(raw)  # may raise ValueError
    if n <= 0:

        raise ValueError("limit must be positive")
    return n


@api.route(f'{CITIES_EPS}/<string:city_name>')
class CityDetails(Resource):
    """
    Get details for a specific city
    """
    def get(self, city_name):
        """
        Retrieve details for a single city by name
        """
        try:
            cities = cqry.read()
            if city_name not in cities:
                return {ERROR: f"City '{city_name}' not found"}, 404
            return {
                CITY_RESP: city_name,
                "details": cities[city_name]
            }, 200
        except ConnectionError as e:
            return {ERROR: str(e)}, 500
        except Exception as e:
            return {ERROR: str(e)}, 500
