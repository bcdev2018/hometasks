import hashlib
import os

class provedData:
	
	def __init__(self, nonce, data):
		self.nonce = nonce
		self.data = data #bytearray

	def toBytes(self):
		return self.nonce.to_bytes((self.nonce.bit_length() + 7) // 8, 'big') + bytes(self.data)	    		

class PowMiner:

	def __init__(self, hash):
		self.MaxTarget = bytearray(b'\xFF'*32)
		self.hashFunc = hash

	def doWork(self, data, difficulty):
		i = 0
		while not(self.validateWork(provedData(i, data), difficulty)):
			i += 1

		return provedData(i, data)

	def validateWork(self, provedData_, difficulty):
		return self.realDifficulty(provedData_) >= difficulty

	def realDifficulty(self, procedData_):
		#h = blake2b(digest_size=32)
		self.h = hashlib.new(self.hashFunc, digest_size=32)
		self.h.update(procedData_.toBytes())
		#print(self.h.hexdigest())
		return int.from_bytes(self.MaxTarget, byteorder='big', signed=False) / int(self.h.hexdigest(), 16)

def main():
	miner = PowMiner("blake2b")
    #difficulty = 2 ** 20
	for difficulty in range(0, 20):
		randData = bytearray(os.urandom(1000))
		proved = miner.doWork(randData, difficulty)
		if not(miner.validateWork(proved, difficulty)):
			print("error: difficulty = " + str(difficulty) + ", provedData = " + str(bytes(proved.data)))
		else:
			print("difficulty passed " + str(difficulty))	

if __name__ == "__main__":
    main()