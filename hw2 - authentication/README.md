# cs642-hw2

Prerequisites
You will need to set up and use a specified Python environment for this homework. Please refer to the instructions below:

We recommend using Python 3.10. However, you must use version 3.8 or later. The code in the assignment won't work with earlier versions of Python.

There are subtle differences between versions of Python, and between versions of Python packages. We need to make sure we’re all using the same versions. Otherwise, your code may run differently while the TAs are grading it.

In the following instructions, we assume you have access to a computer with the following programs installed on it.

python3
pip
virtualenv
Note: the CS lab Linux computers satisfy this requirement.

We’re going to do the following:

create a virtual environment for running your cs642 hw2 code
install specific version of crypto library for that virtual environment.
Open a bash terminal and run the following commands:

Make a directory where you can keep your virtual environments (if you don’t already have one)
```
$ mkdir ~/envs
```
Install virtualenv
```
$ pip3 install --user virtualenv
```
Make a virtual environment called ’cs642hw2’
```
$ python3 -m virtualenv --python=python3.10 ~/envs/cs642hw2
```
Activate the virtual environment
```
$ source ~/envs/cs642hw2/bin/activate
```
Install the allowed packages for your environment (You will need the “requirements.txt” file located in HW2.zip)
```
(cs642hw2) $ pip install -r requirements.txt
```
You now have a virtual environment identical to the one used by the TAs. You’ll know the virtual environment is active because its name will appear in parentheses to the left of the bash prompt, so run code files by:
```
(cs642hw2) $ python your_code.py
```
When you don’t need the virtual environment, just ‘deactivate’ it
```
(cs642hw2) $ deactivate
```
Packages in the virtual environment should be sufficient for HW2. If you want to use a Python package that isn’t included in the official virtual environment, contact the TAs for approval.

# Part A: Password Cracking (20 pts)
A colleague has built a password hashing mechanism. It applies SHA-256 to a string of the form "username,password,salt", where salt is a randomly chosen value. For example, the stored value for username user, password 12345 and salt 999999 is c50603be4fedef7a260ef9181a605c27d44fe0f37b3a8c7e8dbe63b9515b8e96. The Python code to generate this is:
```
import hashlib
print(hashlib.sha256("user,12345,999999".encode()).hexdigest())
```
The same process was used to generate the following challenge hashes: 

a) ffa2dcdd84a45582b17d4f535cda63887273f34a679eded10428b480999c3a8b for user bjacobsen and salt 980166.

b) 41db4f70c8ce1c866462b4c0636aef38c1ea5ef36809bf099165c826bc3a8881 for user ceccio and salt 547750.

## Tasks:

1. Recover the password for both challenge hashes above. Hint: Both the passwords are an ASCII string consisting only of numeric digits up to 8 digits.
2. Give a pseudocode description of your algorithm and the worst-case running time for it.
3. Discuss the merits of your colleague’s proposal. Suggest how your attack might be made intractable.
4. Put your solutions under the correct section in the file solutions.txt. Also, upload the pwcrack.py containing the code to crack the hashes, with clear instructions about how to run it.

# Part B: Encryption (40 pts)
Another colleague decided to build a symmetric encryption scheme. These are implemented in badencrypt.py and baddecrypt.py (see attached .zip file) and are designed to encrypt a sample message to demonstrate the encryption scheme. To use these demo programs, run:
```
  CT=$(python3 badencrypt.py testkeyfile)
  echo $CT
  python3 baddecrypt.py testkeyfile $CT
```
Your job is to assess the security of this encryption scheme. Your solution will be a Python program attack.py that takes as input a ciphertext and modifies the ciphertext so that the decrypted message has a different (and more lucrative to the recipient) TOTAL field and still passes the verification in baddecrypt.py. The file attack.py must do this without access to the key file or knowledge of the key. You can assume the ciphertext contains the sample message hardcoded in badencrypt.py.

We will test your solution with original versions of badencrypt.py and baddecrypt.py and with different encryption keys than the test key provided. To ensure that attack.py produces the correct formatted output, you can run from the command line:
```
 CT=$(python3 badencrypt.py testkeyfile) 
 MODCT=$(python3 attack.py $CT) 
 python3 baddecrypt.py testkeyfile $MODCT
```
## Tasks:

1. Complete the attack program attack.py (feel free to make modifications to the pre-filled content. The skeleton is provided just to help you out)
2. In solutions.txt, describe what is wrong with your colleague's scheme and how it should be fixed so that it will be more secure.

(Your attack script will not have direct access to the key file and should not attempt to gain access to the process memory of baddecrypt or any other files to steal the key directly.)

# Part C: Diffie-Hellman Key Exchange (40 pts)
In this part of the assignment you will receive a secret code from a secret server. However, the code is very sensitive and the server does not want any network sniffer to be able to read the code intended for you. So the server encrypts the message with a DH exchanged key before sending. You have to establish a shared secret key using DH key exchange protocol using HTTP messages.

The APIs the server provides are:

1. ```/dh?gx=<gx_str>``` which takes one parameter ```gx```. This is the client-side part of the the DH key (g^x). In response, the server will send a json object with the following fields:
```
{
  'gy': <gy>,
  'c':  <ciphertext encrypted with the k = SHA256(gxy)
}
```
2. ```/verify?code=<code_value>``` which takes a code and returns if the code is valid or not.

To access these APIs, send HTTP GET requests to the server at the IP address 128.105.19.18:8080. The server is only available from inside the CS network. There are several ways to access the network:

1. Go to a lab and work directly from a CS machine.
2. Use ssh: In the terminal, type ssh [YOUR_CS_USERNAME]@best-linux.cs.wisc.edu . You will be prompted to enter your password and to use Duo multi-factor auth. If you need to transfer files to the CS machines, go into the directory where the file is located on your personal machine and enter scp [FILENAME] [YOUR_CS_USERNAME]@best-linux.cs.wisc.edu:~/ .
3. Use the department VPN: See this webpage for information on how to use GlobalProtect.

In cryptography, "strings" are strings of bytes, and not of ASCII characters. For ease of sending them over network, and writing to files, we encode them into base64 format. See hereLinks to an external site. for more on base64 encoding. In this part of the assignment, all strings are urlsafe_base64 encoded. In Python you can do so using base64Links to an external site. library: base64.urlsafe_b64encode(gx) for encoding a bytestring into a base64 string, and base64.urlsafe_b64decode(gx_str) for decoding a base64 string back into a bytestring.

This assignment uses the [cryptography.io](https://cryptography.io/en/latest/) library.

## Tasks:

1. For this part of the assignment, you must complete dh_sol.py so that it retrieves and decrypts the secret code from the secret server. Starter code is provided for you.

2. In solutions.txt, write down the secret code and briefly explain how your solution works.

# Extra credit: More password cracking (10 pts)
Yet another colleague, to make the password cracking hard, uses a slow hash function named scrypt. Scrypt is a password-based key derivation function that is designed to be computationally intensive (slow). This is because legitimate users only need to perform the function once per operation (e.g., during authentication), and so the computational overhead and the time required is not noticeable.
However, a brute-force attacker would likely need to perform the operation billions of times, at which point the time computational requirements become significant and, ideally, prohibitive.

For example, the input ```batman,password```, and salt ```84829348943``` processed with scrypt produces the following hash
```594b32011f597e921b07be213b469a94492ddcdeea84ffea27e2e0392e77f6c59690f1f85b22b8fcb9f551f6613880ef1dc1cc855d600165b8a285c9a342ad8f```

While using the same technique, for the username bucky with salt 0719173488 (and also keeping n = 16, r = 32, p = 1) the challenge hash is

```fdd2a52969ff2cab2c2653e5cc7129a70b0cad398ea3ff44bf700bb0cd168d8b5c080c90b9281f04993b05895705229c3a5261e20f8a453369b81efd4f9040b6```

The password is representative of real-world passwords: something complex enough that the person that selected this password would consider using it for a website login, but easy enough to be memorable. 

## Tasks:

Find the password used to produce the challenge hash. Give a pseudocode description of your algorithm and the correct password in solutions.txt.

## Hints for Extra Credit:
The website has a password policy that requires that the password must have at least 6 characters and at least three of the four character classes: uppercase letters (A-Z), lower case letters (a-z), symbols (~`!@#$%^&*()+=_-{}[]\|:;”’?/<>,.), and digits (0-9).
You can look at [CrackStation's password cracking dictionaries](https://crackstation.net/crackstation-wordlist-password-cracking-dictionary.htm) for some help.
Note: the password is human-chosen, so you should use the smaller "human password" dataset.
It is wise to estimate the running time of your solution before starting it.
