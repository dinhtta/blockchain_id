import Crypto
from Crypto.PublicKey import RSA 
from Crypto.Hash import SHA256
import pickle
from config import *

def gen(nkeys=NUSERS):
	pubkeys = []
	privkeys = {} # map pubkey -> privkey
	hashkeys = {} # map pubkey -> hash(pubkey)
	for i in range(nkeys):
		key = RSA.generate(2048)
		pkey = key.publickey() 
		x = pkey.exportKey("PEM")	
		pubkeys.append(x)
		h = SHA256.new(x)
		hashkeys[x] = h.digest()
		privkeys[x] = key.exportKey("PEM")
	
	pickle.dump(pubkeys, open("pubkeys", "wb"))
	pickle.dump(privkeys, open("privkeys", "wb"))
	pickle.dump(hashkeys, open("hashkeys", "wb"))

