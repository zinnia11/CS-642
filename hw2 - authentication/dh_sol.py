"""
## Diffie-Hellman (DH) key exchange over HTTP

In this part of the assignment you will receive a secret code from a secret
server. However the code is very sensitive and the server does not want any
network sniffer to be able to read the code inteded for you. So the server
encrypts the message with a DH exchanged key before sending. You have to
establish a shared secret key using DH key exchange protocol using HTTP
messages.

The API server provides are: 
1. `/dh?gx=<gx_str>` which takes one parameter `gx`. This is the client-side part of the the DH key (g^x).
In response, the server will send a json object with the following fields:
{
  'gy': <g^y>
  'c':  <ciphertext encrypted with the k = HMAC(g^{xy})
}

 
2. `/verify?code=<code_value>` which takes a code and returns if the code is valid or not. 


In cryptography we regularly "strings" are string of bytes, and not ascii
characters. For ease of sending them over network, and writing to filees, we
encode them into `base64` format. (See <....> for more on base64 encoding.  In
this part of the assignment, all strings are urlsafe_base64 encoded. In Python
you can do so using `base64` library: `base64.urlsafe_b64encode(gx)` for
encoding a bytestring, and `base64.urlsafe_b64decode(gx_str)` for decoding into
a bytestring.

You will be using [cryptography.io](https://cryptography.io/en/latest/) library.
Below all the functions that you might need are already imported.

"""
import requests
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
import json

URL = "http://128.105.19.18:8080"  ## Update this URL to match the IP given in the instructions.

EC_CURVE = ec.SECP384R1()
ENCODING = Encoding.X962
FORMAT = PublicFormat.CompressedPoint

#### Your code starts here #####

#generating random x and secret key
x = ec.generate_private_key(EC_CURVE)
#gx is public key to be sent in base64
gx = x.public_key()
gx_str = base64.urlsafe_b64encode(gx.public_bytes(ENCODING, FORMAT))

#send the base64 gx
r = requests.get("{url}/dh".format(url=URL), params={'gx': gx_str}) #HTTP GET request
server_info = r.json()
#get JSON object with c and base 64 gy back
c = server_info['c']
gy_str = server_info['gy']
#decode the gy
gy_bin = base64.urlsafe_b64decode(gy_str)
gy = ec.EllipticCurvePublicKey.from_encoded_point(EC_CURVE, gy_bin)
#get the shared gxy key to decrypt the message
gxy = x.exchange(ec.ECDH(), gy)

#### Don't change the code below ####
k = base64.urlsafe_b64encode(HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b'handshake data'
).derive(gxy)) # gxy = <g^xy>

m = Fernet(k).decrypt(c.encode('ascii'))
print(m)
                      
sc = m.split(b'=', 1)[1]

r = requests.get(URL + '/verify', params={
    'code': sc
})

print(r.content)
