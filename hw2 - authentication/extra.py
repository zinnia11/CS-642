'''
Scrypt is a password-based key derivation function that is designed to be computationally intensive (slow). 
This is because legitimate users only need to perform the function once per operation (e.g., during authentication), 
and so the computational overhead and the time required is not noticeable.
However, a brute-force attacker would likely need to perform the operation billions of times, 
at which point the time computational requirements become significant and, ideally, prohibitive.
For example, the input 'batman,password', and salt '84829348943' processed with scrypt produces the following hash
'594b32011f597e921b07be213b469a94492ddcdeea84ffea27e2e0392e77f6c59690f1f85b22b8fcb9f551f6613880ef1dc1cc855d600165b8a285c9a342ad8f'

While using the same technique, for the 
username 'bucky' with salt '0719173488' (and also keeping n = 16, r = 32, p = 1) the challenge hash is
'fdd2a52969ff2cab2c2653e5cc7129a70b0cad398ea3ff44bf700bb0cd168d8b5c080c90b9281f04993b05895705229c3a5261e20f8a453369b81efd4f9040b6'
'''
import hashlib

def crack_it_extra(username, salt, hash, passwords):
    #password is ASCII string with numeric digits
    for passw in passwords:
        passw=passw.strip()
        if (len(passw)<6): # length of password is too short
            continue
        if (not any(c.isalpha() for c in passw)): # if there are no letters, then remove the password
            continue
        if (passw.isalpha()): # only letters
            continue
        #format input correctly
        test_input = "{uname},{password}".format(uname=username, password=passw)
        #hash it
        output = hashlib.scrypt(password=test_input.encode(), salt=str(salt).encode(), n=16, r=32, p=1).hex()
        if (output == hash):
            print(passw)
            return passw


if __name__ == "__main__":
    file1 = open('crackstation-human-only.txt', 'r', encoding='latin-1')
    lines = file1.readlines()

    crack_it_extra('bucky', '0719173488', 'fdd2a52969ff2cab2c2653e5cc7129a70b0cad398ea3ff44bf700bb0cd168d8b5c080c90b9281f04993b05895705229c3a5261e20f8a453369b81efd4f9040b6', lines)
    
    '''
    numthreads = 8
    threads = []
    for i in range(numthreads):
        t = threading.Thread(target=crack_it_extra, args=('bucky', '0719173488', 'fdd2a52969ff2cab2c2653e5cc7129a70b0cad398ea3ff44bf700bb0cd168d8b5c080c90b9281f04993b05895705229c3a5261e20f8a453369b81efd4f9040b6', splitted[i],))
        t.start()
        threads.append(t)

    # wait until they finish
    for t in threads:
        t.join()

    '''
    