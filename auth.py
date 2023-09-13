import config
from flask_httpauth import HTTPBasicAuth

def setup_auth():
    if config.AUTHENTICATION is not None:
        auth = HTTPBasicAuth()

        @auth.verify_password
        def verify_password(username, password):
            if config.AUTHENTICATION == (username, password):
                return username
            return None

        auth_dec = auth.login_required
    else:
        auth_dec = lambda x: x

    return auth_dec
