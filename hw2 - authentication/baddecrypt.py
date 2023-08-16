# /usr/bin/env python3

# CS 642 University of Wisconsin
#
# WARNING:
# Do not use this encryption functionality, it has security vulnerabilities!
#
# Your job is to find and understand the problems
#
# usage: python3 baddecrypt.py testkeyfile ciphertext
#

import sys
import Crypto.Cipher.AES
import hashlib

f = open(sys.argv[1], 'r')
key = f.readline()
key = bytes.fromhex(key[:32])
f.close()

# Grab ciphertext from first argument
ciphertextWithTag = bytes.fromhex(sys.argv[2]) # bytes.fromhex($CT)

if len(ciphertextWithTag) < 16+16+32:
  print("Ciphertext is too short!")
  sys.exit(0)

iv = ciphertextWithTag[:16]
ciphertext = ciphertextWithTag[:len(ciphertextWithTag)-32]  # with iv
tag = ciphertextWithTag[len(ciphertextWithTag)-32:]
cipher = Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_CBC, IV=iv)
plaintext = cipher.decrypt(ciphertext[16:]) # here [16:] has spare apart iv

# Check the tag
if tag.hex() != hashlib.sha256(plaintext).hexdigest():
   print("Invalid tag!")
else:
   print("Verified message")
   print(plaintext.decode())
