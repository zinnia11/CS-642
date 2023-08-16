# /usr/bin/env python3

# CS 642 University of Wisconsin
#
# WARNING:
# Do not use this encryption functionality, it has security vulnerabilities!
#
# Your job is to find and understand the problems
#
# usage: python3 badencrypt.py testkeyfile
#

import sys
import os
import Crypto.Cipher.AES
import hashlib

f = open(sys.argv[1], 'r')
key = f.readline()
key = bytes.fromhex(key[:32])
f.close()

message = \
"""AMOUNT: $  12.99
Originating Acct Holder: Alexa
Orgininating Acct #98166-20633

I authorized the above amount to be transferred to the account #51779-31226 
held by a Wisc student at the National Bank of the Cayman Islands.
"""

iv = os.urandom(16)
cipher = Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_CBC, IV=iv)
ciphertext = cipher.encrypt(message.encode()).hex()
tag = hashlib.sha256(message.encode()).hexdigest()
print(iv.hex() + ciphertext + tag)
