import flask
from flask import request
import string
import base64
import binascii
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
import os


app = flask.Flask(__name__)

EC_CURVE = ec.SECP384R1()
ENCODING = Encoding.X962
FORMAT = PublicFormat.CompressedPoint
HASH = hashes.SHA256()

HMAC_KEY = b"nevertryagreatpwforyou!"  # Deployed server will have a different password

def _random_sample(n, k):
    """Randomly samples k values between [0, n]"""
    assert n>0 and k>0, "n and k must be > 0"
    return [int(b) % n
            for b in os.urandom(k)]

mlen = 8
hlen = 8

def generate_secret_code():
    # generate a 4-char string
    s = ''.join([string.hexdigits[i] for i in _random_sample(len(string.hexdigits), 8)])
    m = mac(HMAC_KEY, s)
    return s + '-' + m[:hlen//2].hex()

def verify_secret_code(code):
    if isinstance(code, bytes):
        code = code.encode('utf-8')
    s, m = code.split('-')
    mprime = mac(HMAC_KEY, s)
    return mprime[:hlen//2].hex() == m

    
def encrypt(k, m):
    f = Fernet(k)
    return f.encrypt(m)

def decrypt(k, c):
    f = Fernet(k)
    return f.decrypt(c)
    
def mac(k, s):
    h = hmac.HMAC(k, hashes.SHA256())
    d = h.update(s.encode('ascii'))
    return h.finalize()

@app.route("/verify", methods=["GET"])
def verify():
    code = request.args.get('code', None)
    if verify_secret_code(code):
        return "The code is valid!"
    else:
        return "Sorry the code is wrong. :( Good luck forging!"
    
@app.route("/dh", methods=['GET'])
def dh():
    gx_str = request.args.get('gx', None)
    if gx_str is None:
        print(request.args)
        return "You must provide 'gx'", 400
    try:
        gx_bin = base64.urlsafe_b64decode(gx_str)
        gx = ec.EllipticCurvePublicKey.from_encoded_point(EC_CURVE, gx_bin)
    except Exception as ex:
        print(ex)
        return "Could not parse 'gx' properly.<br/>"\
            f"This error might help you debug: {ex!r}", 400
    y = ec.generate_private_key(EC_CURVE)
    gy = y.public_key()
    gy_str = base64.urlsafe_b64encode(gy.public_bytes(ENCODING, FORMAT))
    gxy = y.exchange(ec.ECDH(), gx)
    k = base64.urlsafe_b64encode(HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data'
    ).derive(gxy))
    code = generate_secret_code()
    c = encrypt(k, f"Congrats! Your Secret_Code={code}".encode('ascii'))
    print(f"c={c}\ngy_str={gy_str}")
    return flask.jsonify(
        c=c.decode('utf-8'),
        gy=gy_str.decode('utf-8')
    )


@app.route("/")
def index():
    return "Running!"

PORT = os.getenv('PORT', 5000)
DEBUG = int(os.getenv('DEBUG', 0))
if __name__ == "__main__":
    app.run("0.0.0.0", port=PORT, debug=DEBUG)
