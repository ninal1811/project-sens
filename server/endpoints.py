"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
import os
from datetime import timedelta
from functools import wraps
# from http import HTTPStatus
import cities.cities_queries as cqry
import countries.country_queries as cntry
import states.states_queries as sqry
import users.users_queries as user_qry

from flask import Flask, request, jsonify, session
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

COUNTRIES_EPS = "/countries"
COUNTRY_RESP = "Countries"

STATES_EPS = "/states"
STATE_RESP = "States"

CITIES_EPS = "/cities"
CITY_RESP = "Cities"

HEALTH_EP = "/health"
VERSION_EP = "/version"
VERSION_NAME = "project-sens"

app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)
app.config['SESSION_COOKIE_SECURE'] = False  # Set True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'


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


@api.route(f'{CITIES_EPS}/add')
class AddCity(Resource):
    def post(self):
        """
        Add or update a city.
        """
        try:
            print(f"AddCity - Request data: {request.get_data(as_text=True)}")

            data = request.get_json()
            print(f"AddCity - Parsed data: {data}")

            if data is None:
                return {ERROR: "Request must be JSON. Check Content-Type header is 'application/json'"}, 400

            city = data.get('city')
            country_code = data.get('country_code')
            state_code = data.get('state_code')
            rec_restaurant = data.get('rec_restaurant')

            missing_fields = []
            if not city:
                missing_fields.append('city')
            if not state_code:
                missing_fields.append('state_code')
            if not country_code:
                missing_fields.append('country_code')
            if not rec_restaurant:
                missing_fields.append('rec_restaurant')

            if missing_fields:
                return {
                    ERROR: f"Missing required fields: {', '.join(missing_fields)}",
                    "received_data": data
                }, 400

            extra_fields = {k: v for k, v in data.items() if k not in ['country_code', 'state_code', 'city', 'rec_restaurant']}

            cqry.add_city(country_code, state_code, city, rec_restaurant, **extra_fields)

            return {
                MESSAGE: "City added/updated successfully",
                CITY_RESP: {
                    "state_code": state_code,
                    "country_code": country_code,
                    "city": city,
                    "rec_restaurant": rec_restaurant,
                    **extra_fields
                }
            }, 201

        except ValueError as e:
            print(f"AddCity - ValueError: {str(e)}")
            return {ERROR: str(e)}, 400
        except Exception as e:
            print(f"AddCity - Unexpected error: {str(e)}")
            return {ERROR: f"Unexpected error: {str(e)}"}, 500


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


@api.route(f"{COUNTRIES_EPS}/add")
class AddCountry(Resource):
    """
    Add or update a state using the add_country method (upsert).
    """
    def post(self):
        """
        Add or update a country.
        """
        try:
            print(f"AddCountry - Request data: {request.get_data(as_text=True)}")

            data = request.get_json()
            print(f"AddCountry - Parsed data: {data}")

            if data is None:
                return {ERROR: "Request must be JSON. Check Content-Type header is 'application/json'"}, 400

            name = data.get('name')
            country_code = data.get('country_code')
            capital = data.get('capital')
            nat_dish = data.get('nat_dish')
            pop_dish_1 = data.get('pop_dish_1')
            pop_dish_2 = data.get('pop_dish_2')

            missing_fields = []
            if not name:
                missing_fields.append('name')
            if not country_code:
                missing_fields.append('country_code')
            if not capital:
                missing_fields.append('capital')
            if not nat_dish:
                missing_fields.append('nat_dish')
            if not pop_dish_1:
                missing_fields.append('pop_dish_1')
            if not pop_dish_2:
                missing_fields.append('pop_dish_2')

            if missing_fields:
                return {
                    ERROR: f"Missing required fields: {', '.join(missing_fields)}",
                    "received_data": data
                }, 400

            extra_fields = {k: v for k, v in data.items() if k not in ['country_code', 'nat_dish', 'capital', 'name', 'pop_dish_1', 'pop_dish_2']}
            # ADD THESE DEBUG PRINTS
            print(f"DEBUG - extra_fields: {extra_fields}")
            print(f"DEBUG - nat_dish_dietary in data: {data.get('nat_dish_dietary')}")
            print(f"DEBUG - pop_dish_1_dietary in data: {data.get('pop_dish_1_dietary')}")
            print(f"DEBUG - pop_dish_2_dietary in data: {data.get('pop_dish_2_dietary')}")
            cntry.add_country(
                country_code,
                name,
                capital,
                nat_dish=nat_dish,
                pop_dish_1=pop_dish_1,
                pop_dish_2=pop_dish_2,
                **extra_fields
            )

            return {
                MESSAGE: "Country added/updated successfully",
                COUNTRY_RESP: {
                    "country_code": country_code,
                    "name": name,
                    "capital": capital,
                    "nat_dish": nat_dish,
                    "pop_dish_1": pop_dish_1,
                    "pop_dish_2": pop_dish_2,
                    **extra_fields
                }
            }, 201

        except ValueError as e:
            print(f"AddCountry - ValueError: {str(e)}")
            return {ERROR: str(e)}, 400
        except Exception as e:
            print(f"AddCountry - Unexpected error: {str(e)}")
            return {ERROR: f"Unexpected error: {str(e)}"}, 500


@api.route(f'{COUNTRIES_EPS}/<string:country_name>')
class CountryDetails(Resource):
    """
    Get details for a specific country
    """
    def get(self, country_name):
        """
        Retrieve details for a single country by name
        """
        try:
            countries = cntry.read_all()
            if country_name not in countries:
                return {ERROR: f"Country '{country_name}' not found"}, 404
            return {
                COUNTRY_RESP: country_name,
                "details": countries[country_name]
            }, 200
        except ConnectionError as e:
            return {ERROR: str(e)}, 500
        except Exception as e:
            return {ERROR: str(e)}, 500

    def delete(self, country_name):
        """
        Delete a specific country by name
        """
        try:
            result = cntry.delete_country(country_name)
            if not result:
                return {ERROR: f"Country '{country_name}' not found"}, 404
            return {MESSAGE: f"Country '{country_name}' deleted successfully"}, 200
        except ConnectionError as e:
            return {ERROR: str(e)}, 500


@api.route(f"{STATES_EPS}/{READ}")
class States(Resource):
    """
    Retrieve all states from the states cache or database.
    """

    def get(self):
        """
        Return all stored states.
        """
        try:
            states = sqry.read()

            # If sqry.read() returns the cache dict (like your test_queries),
            # return the values as a list. If it already returns a list,
            # just send it back directly.
            if isinstance(states, dict):
                data = list(states.values())
            else:
                data = states

            return {STATE_RESP: data}, 200
        except Exception as e:
            # Catch any error and surface the message instead of a generic 500.
            return {ERROR: str(e)}, 500


@api.route(f"{STATES_EPS}/country/<string:country_code>")
class StatesByCountry(Resource):
    def get(self, country_code):
        try:
            all_states = sqry.read()
            filtered_states = []
            if isinstance(all_states, dict):
                for state_code, state_data in all_states.items():
                    if state_data.get('country_code') == country_code:
                        filtered_states.append({
                            'state_code': state_code,
                            **state_data
                        })
            elif isinstance(all_states. list):
                filtered_states = [
                    state for state in all_states
                    if state.get('country_code') == country_code
                ]

            if not filtered_states:
                return {
                    ERROR: f"No states found for country code '{country_code}'",
                    "country_code": country_code
                }, 404

            return {
                "success": True,
                "country_code": country_code,
                "count": len(filtered_states),
                "states": filtered_states
            }, 200
        except Exception as e:
            print(f"StatesByCountry - Error: {str(e)}")
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


@api.route(f"{STATES_EPS}/add")
class AddState(Resource):
    """
    Add or update a state using the add_state method (upsert).
    """
    def post(self):
        """
        Add or update a state.
        """
        try:
            print(f"AddState - Request data: {request.get_data(as_text=True)}")

            data = request.get_json()
            print(f"AddState - Parsed data: {data}")

            if data is None:
                return {ERROR: "Request must be JSON. Check Content-Type header is 'application/json'"}, 400

            name = data.get('name')
            country_code = data.get('country_code')
            state_code = data.get('state_code')

            missing_fields = []
            if not name:
                missing_fields.append('name')
            if not state_code:
                missing_fields.append('state_code')
            if not country_code:
                missing_fields.append('country_code')

            if missing_fields:
                return {
                    ERROR: f"Missing required fields: {', '.join(missing_fields)}",
                    "received_data": data
                }, 400

            extra_fields = {k: v for k, v in data.items() if k not in ['country_code', 'state_code', 'name']}

            sqry.add_state(country_code, state_code, name, **extra_fields)

            return {
                MESSAGE: "State added/updated successfully",
                STATE_RESP: {
                    "state_code": state_code,
                    "country_code": country_code,
                    "name": name,
                    **extra_fields
                }
            }, 201

        except ValueError as e:
            print(f"AddState - ValueError: {str(e)}")
            return {ERROR: str(e)}, 400
        except Exception as e:
            print(f"AddState - Unexpected error: {str(e)}")
            return {ERROR: f"Unexpected error: {str(e)}"}, 500


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


# ============= AUTHENTICATION ENDPOINTS =============


def login_required(f):
    """Decorator to require authentication for endpoints."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function


@api.route('/auth/login')
class Login(Resource):
    """Login endpoint"""
    def post(self):
        """
        Login with username and password.
        Expects JSON: {"username": "...", "password": "..."}
        """
        try:
            data = request.get_json()

            if not data:
                return {'error': 'No data provided'}, 400

            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return {'error': 'Username and password are required'}, 400

            # Authenticate user
            user = user_qry.authenticate(username, password)

            # Store username in session
            session['username'] = username
            session.permanent = True

            return {
                'success': True,
                'user': user
            }, 200

        except ValueError as e:
            return {'error': str(e)}, 401
        except Exception as e:
            print(f"Login error: {e}")
            return {'error': 'Login failed'}, 500


@api.route('/auth/logout')
class Logout(Resource):
    """Logout endpoint"""
    def post(self):
        """Logout - clears session"""
        session.clear()
        return {'success': True, 'message': 'Logged out'}, 200


@api.route('/auth/session')
class CheckSession(Resource):
    """Check if user is logged in"""
    def get(self):
        """Check current session status"""
        if 'username' in session:
            username = session['username']
            users = user_qry.read()
            user = users.get(username)

            if user:
                return {
                    'loggedIn': True,
                    'user': user
                }, 200

        return {'loggedIn': False}, 200


@api.route('/auth/user')
class CurrentUser(Resource):
    """Get current authenticated user"""
    def get(self):
        """Get current user information"""
        if 'username' not in session:
            return {'error': 'Not authenticated'}, 401

        username = session['username']
        users = user_qry.read()
        user = users.get(username)

        if user:
            return {'user': user}, 200

        return {'error': 'User not found'}, 404


@api.route('/auth/register')
class Register(Resource):
    """User registration endpoint"""
    def post(self):
        """
        Register a new user.
        Expects JSON: {"username": "...", "password": "..."}
        """
        try:
            data = request.get_json()

            if not data:
                return {'error': 'No data provided'}, 400

            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return {'error': 'Username and password are required'}, 400

            user_id = user_qry.create_user(username, password)

            return {
                'success': True,
                'message': 'User created successfully',
                'user_id': user_id
            }, 201

        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            print(f"Registration error: {e}")
            return {'error': 'Registration failed'}, 500
