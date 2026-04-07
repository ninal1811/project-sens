from functools import wraps
import data.db_connect as dbc

USERS_COLLECTION = "users"

USERNAME = "username"
PASSWORD = "password"

cache = None

SAMPLE_USER = {
    USERNAME: "foodie",
    PASSWORD: "password123",
}


def needs_cache(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if cache is None:
            load_cache()
        return fn(*args, **kwargs)
    return wrapper


def load_cache():
    """Load the in-memory cache from the DB."""
    global cache
    cache = {}
    
    try:
        users = dbc.read(USERS_COLLECTION)
    except Exception:
        print(f"Error loading users from DB: {Exception}")
        users = []
    
    for user_doc in users:
        username = user_doc.get(USERNAME)
        if username:
            cache[username] = user_doc


@needs_cache
def count() -> int:
    """Return number of users."""
    return len(cache)


@needs_cache
def read() -> dict:
    """Return all users (without passwords)."""
    result = {}
    for username, user_doc in cache.items():
        safe_doc = {k: v for k, v in user_doc.items() if k != PASSWORD}
        result[username] = safe_doc
    return result


def create_user(username: str, password: str) -> str:
    """Create a new user with plain text password (INSECURE!)."""
    if not username or not isinstance(username, str):
        raise ValueError("Username is required")
    
    if not password or not isinstance(password, str):
        raise ValueError("Password is required")
    
    # Check if user already exists
    existing = dbc.read_one(USERS_COLLECTION, {USERNAME: username})
    if existing:
        raise ValueError(f"Username '{username}' already exists")
    
    user_doc = {
        USERNAME: username,
        PASSWORD: password,
    }
    
    result = dbc.create(USERS_COLLECTION, user_doc)
    load_cache()
    return str(result.inserted_id)


def authenticate(username: str, password: str) -> dict:
    if not username or not password:
        raise ValueError("Username and password are required")
    
    user_doc = dbc.read_one(USERS_COLLECTION, {USERNAME: username})
    
    if not user_doc:
        raise ValueError("Invalid username or password")
    
    stored_password = user_doc.get(PASSWORD)
    if not stored_password:
        raise ValueError("User has no password set")
    
    if password != stored_password:
        raise ValueError("Invalid username or password")
    
    safe_user = {k: v for k, v in user_doc.items() if k != PASSWORD}
    return safe_user


@needs_cache
def user_exists(username: str) -> bool:
    return username in cache


def delete_user(username: str) -> bool:
    ret = dbc.delete(USERS_COLLECTION, {USERNAME: username})
    if ret < 1:
        raise ValueError(f"User not found: {username}")
    load_cache()
    return True


def update_password(username: str, new_password: str) -> bool:
    ret = dbc.update(USERS_COLLECTION, {USERNAME: username}, {PASSWORD: new_password})
    
    if ret.modified_count < 1:
        raise ValueError(f"User not found: {username}")
    
    load_cache()
    return True


def main():
    load_cache()
    
    try:
        create_user("foodie", "password123")
        print("✅ Created demo user: foodie / password123")
    except ValueError as e:
        print(f"Demo user already exists: {e}")
    
    print(f"Total users: {count()}")


if __name__ == "__main__":
    main()