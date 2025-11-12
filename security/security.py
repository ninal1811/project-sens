from functools import wraps

# import data.db_connect as dbc

"""
Our record format to meet our requirements (see security.md) will be:

{
    feature_name1: {
        create: {
            user_list: [],
            checks: {
                login: True,
                ip_address: False,
                dual_factor: False,
                # etc.
            },
        },
        read: {
            user_list: [],
            checks: {
                login: True,
                ip_address: False,
                dual_factor: False,
                # etc.
            },
        },
        update: {
            user_list: [],
            checks: {
                login: True,
                ip_address: False,
                dual_factor: False,
                # etc.
            },
        },
        delete: {
            user_list: [],
            checks: {
                login: True,
                ip_address: False,
                dual_factor: False,
                # etc.
            },
        },
    },
    feature_name2: # etc.
}
"""

COLLECT_NAME = 'security'
CREATE = 'create'
READ = 'read'
UPDATE = 'update'
DELETE = 'delete'
USER_LIST = 'user_list'
CHECKS = 'checks'
LOGIN = 'login'

# Features:
PEOPLE = 'people'

security_recs = None
# These will come from the DB soon:
temp_recs = {
    PEOPLE: {
        CREATE: {
            USER_LIST: ['ejc369@nyu.edu'],
            CHECKS: {
                LOGIN: True,
            },
        },
    },
}


def read() -> dict:
    global security_recs
    # dbc.read()
    security_recs = temp_recs
    return security_recs


def needs_recs(fn):
    """
    Should be used to decorate any function that directly accesses sec recs.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        global security_recs
        if not security_recs:
            security_recs = read()
        return fn(*args, **kwargs)
    return wrapper


@needs_recs
def read_feature(feature_name: str) -> dict:
    if feature_name in security_recs:
        return security_recs[feature_name]
    else:
        return None


@needs_recs
def validate_security_record(record: dict) -> bool:
    """
    Validate that a security record has the correct structure.
    Args:
        record: The security record to validate
    Returns:
        True if valid, False otherwise
    """
    required_ops = [CREATE, READ, UPDATE, DELETE]
    for feature_name, feature_data in record.items():
        for op in feature_data.keys():
            if op not in required_ops:
                return False
            if USER_LIST not in feature_data[op]:
                return False
            if CHECKS not in feature_data[op]:
                return False
    return True
