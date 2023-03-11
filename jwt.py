import json
import hmac
import hashlib
import base64


JWT_SECRET_KEY = "8a6519af467ffc7ab0d583f922eb0620".encode()


def generate_jwt(d: dict) -> str:
    data = base64.b64encode(json.dumps(d).encode())
    return f'{data.decode()}.{base64.b64encode(hmac.new(JWT_SECRET_KEY, data, hashlib.sha256).digest()).decode()}'


def validate_jwt(jwt: str) -> None:
    strs = jwt.split('.')
    return strs[1] == base64.b64encode(hmac.new(JWT_SECRET_KEY, strs[0].encode(), hashlib.sha256).digest()).decode()


def get_user_info(jwt: str) -> dict:
    return json.loads(base64.b64decode(jwt.split('.')[0]))


# print(generate_jwt({'name': 'PalaniyappanOL'}))
# print(get_user_info(
#     'eyJuYW1lIjogIlBhbGFuaXlhcHBhbk9MIn0=.ES1k54x+QX9o817SPru+WI5RoY6Ib06BUdaWLmi7XWQ='))
# print(validate_jwt(
#     'eyJuYW1lIjogIlBhbGFuaXlhcHBhbk9MIn0=.ES1k54x+QX9o817SPru+WI5RoY6Ib06BUdaWLmi7XWQ='))
