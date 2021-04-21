import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = 'fsnd-practice1.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'movie'

## AuthError Exception
'''
AuthError Exception
    A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

## Auth Header

'''
get_token_auth_header()
    returns the token authorization header to ensure it is of the 'bearer' type
    raises AuthError otherwise
'''
def get_token_auth_header():
    if 'Authorization' not in request.headers:
        raise AuthError({
            'code': 'Unathorized',
            'description': 'Permission Not Allowed' 
    }, 401)
    auth_header = request.headers.get('Authorization', None)
    auth_parts = auth_header.split()
    if len(auth_parts) != 2:
        raise AuthError({
            'code': 'Unathorized',
            'description': 'Permission Not Allowed' 
    }, 401)
    elif auth_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'Unathorized',
            'description': 'Permission Not Allowed' 
    }, 401)
    return auth_parts[1]

'''
check_permissions(permission, payload)
        permission: a specific Auth0 permission(get:actors) (string) 
        payload: decoded JWT token along with the rsa_key, ALGORITHMS, API_AUDIENCE, and issuer variable    
    returns True if given permission is in the payload, raises AuthError otherwise
'''

def check_permissions(permission, payload):
    if 'permissions' not in payload:
        abort(400)
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'Unathorized',
            'description': 'Permission Not Allowed' 
    }, 401)
    return True

'''
verify_decode_jwt(token)
        token: a json web token (string)
    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload, raises AuthError otherwise
'''
def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed' 
    }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'hello',
                'description': 'Unable to find the appropriate key.'
            }, 400)

'''
requires_auth('')
    checks if JWT token and permission is valid with 
    get_token_auth_header(), verify_decode_jwt(), and check_permissions() functions
    returns requires_auth_decorator if JWT token and permission is valid
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator