from functools import wraps
import data.db_connect as dbc

USERS_COLLECTION = "users"

EMAIL = "email"
PASSWORD = "password"
IS_DEVELOPER = "is_developer"

cache = None

SAMPLE_USER = {
    EMAIL: "foodie@example.com",
    PASSWORD: "password123",
    IS_DEVELOPER: False,
}

SAMPLE_DEVELOPER = {
    EMAIL: "dev@projectsens.com",
    PASSWORD: "devpass123",
    IS_DEVELOPER: True,
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
        email = user_doc.get(EMAIL)
        if email:
            cache[email] = user_doc


@needs_cache
def count() -> int:
    """Return number of users."""
    return len(cache)


@needs_cache
def read() -> dict:
    """Return all users (without passwords)."""
    result = {}
    for email, user_doc in cache.items():
        safe_doc = {k: v for k, v in user_doc.items() if k != PASSWORD}
        result[email] = safe_doc
    return result


def create_user(email: str, password: str, is_developer: bool = False) -> str:
    """Create a new user with plain text password (INSECURE!)."""
    if not email or not isinstance(email, str):
        raise ValueError("Email is required")

    if not password or not isinstance(password, str):
        raise ValueError("Password is required")

    # Basic email validation
    if '@' not in email:
        raise ValueError("Invalid email format")

    # Check if user already exists
    existing = dbc.read_one(USERS_COLLECTION, {EMAIL: email})
    if existing:
        raise ValueError(f"Email '{email}' already exists")

    # Create user document
    user_doc = {
        EMAIL: email,
        PASSWORD: password, 
        IS_DEVELOPER: is_developer,
    }

    result = dbc.create(USERS_COLLECTION, user_doc)
    load_cache()
    return str(result.inserted_id)


def authenticate(email: str, password: str) -> dict:
    if not email or not password:
        raise ValueError("Email and password are required")

    user_doc = dbc.read_one(USERS_COLLECTION, {EMAIL: email})

    if not user_doc:
        raise ValueError("Invalid email or password")

    stored_password = user_doc.get(PASSWORD)
    if not stored_password:
        raise ValueError("User has no password set")

    if password != stored_password:
        raise ValueError("Invalid email or password")

    safe_user = {k: v for k, v in user_doc.items() if k != PASSWORD}
    return safe_user


@needs_cache
def user_exists(email: str) -> bool:
    return email in cache


@needs_cache
def is_user_developer(email: str) -> bool:
    user = cache.get(email)
    if not user:
        return False
    return user.get(IS_DEVELOPER, False)


def delete_user(email: str) -> bool:
    ret = dbc.delete(USERS_COLLECTION, {EMAIL: email})
    if ret < 1:
        raise ValueError(f"User not found: {email}")
    load_cache()
    return True


def update_password(email: str, new_password: str) -> bool:
    ret = dbc.update(USERS_COLLECTION, {EMAIL: email}, {PASSWORD: new_password})

    if ret.modified_count < 1:
        raise ValueError(f"User not found: {email}")

    load_cache()
    return True


def main():
    # Create demo users
    load_cache()

    try:
        create_user("foodie@example.com", "password123", is_developer=False)
        print("✅ Created demo user: foodie@example.com / password123")
    except ValueError as e:
        print(f"Demo user already exists: {e}")

    try:
        create_user("dev@projectsens.com", "devpass123", is_developer=True)
        print("✅ Created developer user: dev@projectsens.com / devpass123")
    except ValueError as e:
        print(f"Developer user already exists: {e}")

    print(f"Total users: {count()}")


if __name__ == "__main__":
    main()