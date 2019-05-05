#!/usr/bin/env python
#*******************************************************************************
#*   Made by Uniris
#********************************************************************************
from ledgerblue.comm import getDongle
from ledgerblue.commException import CommException
from secp256k1 import PublicKey

textToSign = ""
while True:
	data = raw_input("Enter text to sign, end with an empty line : ")
	if len(data) == 0:
		break
	textToSign += data + "\n"

# To get the Public Key
dongle = getDongle(True)
publicKey = dongle.exchange(bytes("8004000000".decode('hex')))
print "publicKey " + str(publicKey).encode('hex')

try:
	offset = 0
	while offset <> len(textToSign):
		if (len(textToSign) - offset) > 255:
			chunk = textToSign[offset : offset + 255] 
		else:
			chunk = textToSign[offset:]
		if (offset + len(chunk)) == len(textToSign):
			p1 = 0x80
		else:
			p1 = 0x00
		#PDU size is limited, so we send the message here over many pdu and depending on the size of the data.
		apdu = bytes("8002".decode('hex')) + chr(p1) + chr(0x00) + chr(len(chunk)) + bytes(chunk)
		signature = dongle.exchange(apdu)
		offset += len(chunk)
	print "signature " + str(signature).encode('hex')
	publicKey = PublicKey(bytes(publicKey), raw=True)
	signature = publicKey.ecdsa_deserialize(bytes(signature))
	print "verified " + str(publicKey.ecdsa_verify(bytes(textToSign), signature))

except CommException as comm:
	if comm.sw == 0x6985:
		print "Aborted by user"
	else:
		print "Invalid status " + comm.sw 

