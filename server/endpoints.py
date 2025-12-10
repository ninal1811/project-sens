"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
# from http import HTTPStatus
import cities.queries as cqry
import countries as cntry
import states.queries as sqry

from flask import Flask  # , request
from flask_restx import Resource, Api  # , fields  # Namespace
from flask_cors import CORS
from flask import request

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

STATES_EPS = "/states"
STATE_RESP = "States"

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

    def delete(self, city_name):
        """
        Delete a specific city by name
        """
        try:
            result = cqry.delete(city_name)
            if not result:
                return {ERROR: f"City '{city_name}' not found"}, 404
            return {MESSAGE: f"City '{city_name}' deleted successfully"}, 200
        except ConnectionError as e:
            return {ERROR: str(e)}, 500


@api.route(f'{CITIES_EPS}/create')
class CreateCity(Resource):
    def post(self):
        """
        Create a new city
        """
        try:
            data = request.get_json()
            if not data or 'name' not in data:
                return {ERROR: "City name required"}, 400
            # Add validation
            if not isinstance(data['name'], str) or not data['name'].strip():
                return {ERROR: "City name must be a non-empty string"}, 400

            result = cqry.create(data['name'], data.get('details', {}))
            return {MESSAGE: "City created", CITY_RESP: result}, 201
        except Exception as e:
            return {ERROR: str(e)}, 500


@api.route(f"{CITIES_EPS}/state/<string:state_code>")
class CitiesByState(Resource):
    def get(self, state_code):
        """
        Retrieve all cities for a specific state.
        """
        try:
            cities = cqry.get_cities_by_state(state_code)
            if not cities:
                msg = f"No cities found for state '{state_code}'"
                return {ERROR: msg}, 404
            return {CITY_RESP: cities}, 200

        except Exception as e:
            return {ERROR: str(e)}, 500


@api.route("/countries")
class Countries(Resource):
    def get(self):
        """
        Retrieve all countries (cached).
        """
        try:
            countries = cntry.read_all()
            return {"countries": countries}, 200
        except Exception as e:
            return {ERROR: str(e)}, 500


@api.route(f"{STATES_EPS}/{READ}")
class States(Resource):
    """
    Retrieve all states from the states cache or database.
    """

    def get(self):
        """
        Return a list of all stored states.
        """
        try:
            # sqry.read() returns a dict keyed by (code, country_code),
            # so we just return the values as a list of state records.
            states = sqry.read()
            return {STATE_RESP: list(states.values())}, 200
        except ConnectionError as e:
            return {ERROR: str(e)}, 500


@api.route(f"{STATES_EPS}/count")
class StateCount(Resource):
    """
    Return the total number of states currently stored.
    """

    def get(self):
        """
        Return the number of state records.
        """
        try:
            count = sqry.count()
            return {"count": count}, 200
        except ConnectionError as e:
            return {ERROR: str(e)}, 500


@api.route(f"{STATES_EPS}/<string:state_code>/<string:country_code>")
class StateDetails(Resource):
    """
    Retrieve or delete a specific state using its code and country code.
    """

    def get(self, state_code, country_code):
        """
        Retrieve details for a single state by code and country code.
        """
        try:
            state = sqry.read_one(state_code, country_code)
            return {
                STATE_RESP: {
                    "code": state_code,
                    "country_code": country_code,
                    "details": state,
                }
            }, 200
        except ValueError:
            return {ERROR: f"State '{state_code}', '{country_code}' not found"}, 404
        except ConnectionError as e:
            return {ERROR: str(e)}, 500
        except Exception as e:
            return {ERROR: str(e)}, 500

    def delete(self, state_code, country_code):
        """
        Delete a specific state by code and country code.
        """
        try:
            result = sqry.delete(state_code, country_code)
            if not result:
                return {
                    ERROR: f"State '{state_code}', '{country_code}' not found"
                }, 404
            return {
                MESSAGE: f"State '{state_code}', '{country_code}' deleted successfully"
            }, 200
        except ValueError:
            return {ERROR: f"State '{state_code}', '{country_code}' not found"}, 404
        except ConnectionError as e:
            return {ERROR: str(e)}, 500
