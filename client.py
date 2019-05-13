#!/usr/bin/env python
#*******************************************************************************
#*   Made by Uniris
#********************************************************************************
import time
import sys
from ledgerblue.comm import getDongle
from ledgerblue.commException import CommException
from secp256k1 import PublicKey



textToSign = sys.argv[1]

# To get the Public Key
start = time.time()
dongle = getDongle(True)
publicKey = dongle.exchange(bytes("8004000000".decode('hex')))
end = time.time()
print "publicKey " + str(publicKey).encode('hex')
print "Getting the public key takes:" , (end - start)

try:
	start = time.time()
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
		apdu = bytes("8008".decode('hex')) + chr(p1) + chr(0x00) + chr(len(chunk)) + bytes(chunk)
		signature = dongle.exchange(apdu)
		offset += len(chunk)
	end = time.time()
	print "signature " + str(signature).encode('hex')
	print "Signing the message takes:" , (end - start)
	publicKey = PublicKey(bytes(publicKey), raw=True)
	signature = publicKey.ecdsa_deserialize(bytes(signature))
	print "verified " + str(publicKey.ecdsa_verify(bytes(textToSign), signature))

except CommException as comm:
	if comm.sw == 0x6985:
		print "Aborted by user"
	else:
		print "Invalid status " + comm.sw 

