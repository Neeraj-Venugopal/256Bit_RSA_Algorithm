# 256Bit_RSA_Algorithm

The Following is a 256 Bit RSA Algorithm written in Python.
The Message Block is encrypted with 128 bit if data and 128 bit of padded zero's making it 256 bit Encyption.

The inputs to the program would be the Message File and the output file wherein the Encrypted message should be stored.
For Decryption the encrypted file acts as an input and the end data is stored in the decrypted file.

Encryption Format
python 256Bit_RSA_Algorithm -e message.txt encrypted.txt

Decrytion Format
python 256Bit_RSA_Algorithm -d encrypted.txt decrypted.txt
