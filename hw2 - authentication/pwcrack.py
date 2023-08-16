'''
Password hashing: Applies SHA-256 to a string of the form "username,password,salt", 
                  where salt is a randomly chosen value.

Python code to do it:
import hashlib
print(hashlib.sha256("user,12345,999999".encode()).hexdigest())

Challenge hashes: 
a) ffa2dcdd84a45582b17d4f535cda63887273f34a679eded10428b480999c3a8b for user bjacobsen and salt 980166.
b) 41db4f70c8ce1c866462b4c0636aef38c1ea5ef36809bf099165c826bc3a8881 for user ceccio and salt 547750.
'''
import hashlib

def crack_it(username, salt, hash, length):
    #password is ASCII string with numeric digits
    counter = 0
    while (1):
        #numeric password to test
        test_pass = str(counter).zfill(length)
        #format input correctly
        test_input = "{uname},{password},{salt}".format(uname=username, password=test_pass, salt=salt)
        #hash it
        output = hashlib.sha256(test_input.encode()).hexdigest()
        if (output == hash):
            return test_pass
        if (len(str(counter)) > length): #99999999 is the last possible password of length 8
            return "Password not found"
        #next password to test
        counter+=1

if __name__ == "__main__":
    print(crack_it("bjacobsen", "980166", "ffa2dcdd84a45582b17d4f535cda63887273f34a679eded10428b480999c3a8b", 8))
    print(crack_it("ceccio", "547750", "41db4f70c8ce1c866462b4c0636aef38c1ea5ef36809bf099165c826bc3a8881", 8))
