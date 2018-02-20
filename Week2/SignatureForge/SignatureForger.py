#from . import _curve25519
import os
import ed25519
from binascii import hexlify
import sys

def verify(signature, vk, message):
	try:
		vk.verify(signature, message)
		print("good signature")
	except ed25519.BadSignatureError:
		print("bad signature")

def generateNewSignature(signature):
	tmp = bytearray(signature[32:64])
	tmp.reverse() #Не очень понятно, зачем нужен реверс, без него не работает

	modifier = 7237005577332262213973186563042994240829374041602535252466099000494570602496 + 27742317777372353535851937790883648493 #число из википедии по  curve25519

	rightPart = int.from_bytes(tmp, byteorder='big', signed=False) + modifier
	rightPart = bytearray(rightPart.to_bytes((rightPart.bit_length() + 7) // 8, 'big'))
	rightPart.reverse() #Не очень понятно, зачем нужен реверс, без него не работает
	newSignature = bytearray(signature[0:32]) + rightPart
	return bytes(newSignature)

def main():	
	for x in range(0, 10):
		sk,vk = ed25519.create_keypair(entropy=os.urandom)
		vk = sk.get_verifying_key()
		message = bytes(bytearray(os.urandom(1000)))
		signature = sk.sign(message)
		verify(signature, vk, message)
		newSignature = generateNewSignature(signature)
		verify(newSignature, vk, message)

if __name__ == "__main__":
    main()