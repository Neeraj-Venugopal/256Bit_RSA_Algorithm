#!/usr/bin/env python

############################################################################################
#    Python code to implement a 256-bit RSA algorithm for encryption and decryption.       #
############################################################################################

## Importing the programming requirements.
import sys
import PrimeGenerator as pGen
import BitVector as BV

## The Following function, computes the GCD of 2 Numbers by Euclids Method. ##
def getGCD (a, b):

    while (b != 0):
        temp_a = a
        a = b
        b = temp_a % b
    return a


## The Following function, computes the value of P and Q. It stores it in a file for  ##
## the purpose of Decryption.                                                         ##
def findPandQ():

    ## To get all the requirements for the Encryption and Decryption. ##
    generator = pGen.PrimeGenerator( bits = 128, debug = 0,emod = 65537)

    while (True):
        p = generator.findPrime()
        q = generator.findPrime()
        
        tempVar = getGCD(e, p - 1)
        if (tempVar == 1):
            tempVar = getGCD(e, q - 1)
            
        if (p != q and tempVar == 1):
            break
    
    ## The Following Logic is to Store the values of P and Q for the Decryption usage. ##
    filePQ = open ('PQValue.txt', 'w')
    filePQ.write(str(p)+"\n")
    filePQ.write(str(q))
    filePQ.close()

    return p * q


## The Following Function Encrypts the data in the input file and stores it ##
## in the new File name provided by the command.                            ##
## Encryption Formula, C = (M power e ) mod N, N = p * q                    ##
def encryptData (blockMessage, e, N, outputFile):
    
    counter = 16
    fileWrite = open (outputFile, 'w')
    for char in blockMessage:
        if(counter == 16):
            ## Logic for Prepending 128 Leading Zeros.. 16 * 8 = 128 bit of Zeros. 
            ## For Each Block Size.
            while (counter != 0):
                cypherText = pow(ord('0'), e, N)
                print >> fileWrite, cypherText
                counter -= 1
        
        counter += 1
        cypherText = pow(ord(char), e, N);     ## ord() Function will change the character to ASCII Number. ##
        print >> fileWrite, cypherText
    
    newLineCount = 16 - counter
    while( newLineCount != 0):
        char = "\n"
        cypherText = pow(ord(char), e, N)
        print >> fileWrite, cypherText
        newLineCount -= 1

    fileWrite.close()


## Calculate the Value of d, using Multiplicative Inverse Logic..                                               ##
def calculateDVal (e, p, q):

    phi = (p - 1) * (q - 1)
    mod = BV.BitVector(intVal = phi)
    bitVector = BV.BitVector(intVal = e)
    d = int(bitVector.multiplicative_inverse(mod))
    return d

    ## The below code Snippet can be used instead of Bit Vector                                                 ##
    ## https://www.youtube.com/watch?v=shaQZg8bqUM&t=184s, the following video was taken as refernce.           ##
    #d = 0
    #x1 = 0
    #x2 = 1
    #y1 = 1

    #while (e > 0):                 ## as temp2 Approaches 0 the more closer we are getting to d= value of d ##
        #temp1 = phi / e
        #temp2 = phi - temp1 * e
        #phi = e
        #e = temp2

        #x = x2 - temp1 * x1
        #y = d - temp1 * y1

        #x2 = x1
        #x1 = x
        #d = y1
        #y1 = y

    #if phi == 1:
        #return d + ((p - 1) * (q - 1)); ## The end value of d will be Negative, Hence a value of phi is added ##
    ## calculateDVal ends ##


## The Following function is used to decrypt the Message from the provided Encrypted File ##
## The Formula for Decryption is, M = (C power d) mod N                                   ##
def decryptData(d, N, encryptedFile, decryptedFile):

    #print d;
    fileRead = open ( encryptedFile, 'r');     ## File Opened to read the Encrypted data ##
    fileWrite = open ( decryptedFile, 'w');    ## File Opened to write the Decrypted data ##

    encryptMsg = [int(line) for line in fileRead]

    dec = [chr(pow(char, d, N)) for char in encryptMsg]   ## chr() function is used to convert ASCII to char ##

    dec = ''.join(dec)
    
    decryptedMessage = ""
    counter = 1

    ## To remove the Appended Zero's ##
    for char in dec:

        if (counter % 32 <= 16 and counter % 32 != 0):
            counter += 1
        else:
            counter += 1
            decryptedMessage += char
    
    ## Removing all new Line Character at the end and adding one at the end of the message. ##
    decryptedMessage = decryptedMessage.rstrip("\n")
    #decryptedMessage += "\n"

    fileWrite.write(decryptedMessage)
    fileRead.close()
    fileWrite.close()

## Main Program Executes here ##
if __name__ == '__main__':
    
    ## Given value ##
    e = 65537

    arguments = len(sys.argv)

    if (arguments == 4):
        
        ## Encryption Logic Begins ##
        if (sys.argv[1] == '-e'):

            messageFile = sys.argv[2]
            outputFile = sys.argv[3]
        
            fileOpen = open (messageFile, 'r')
            plainText = fileOpen.read()
            fileOpen.close()
            
            N = findPandQ()
            encryptData (plainText, e, N, outputFile)             ## Encryption Function Called ##
        ## Encryption Logic Ends ##

        ## Decryption Logic Begins ## 
        elif (sys.argv[1] == '-d'):

            encryptedFile = sys.argv[2]
            decryptedFile = sys.argv[3]

            filePQOpen = open ('PQValue.txt', 'r')
            arr = [int(line) for line in filePQOpen]
            p = arr[0]
            q = arr[1]
            filePQOpen.close()

            d = calculateDVal(e, p, q)
            N = p * q

            decryptData(d, N, encryptedFile, decryptedFile)       ## Decryption Function Called ##
        ## Decryption Logic Ends ##

        else:

            print "Format is Wrong. Enter the Correct Format."
    else:

        print "Please perform Encryption first and then do Decryption"
        print "Follow the below Formats"
        print "python hw03.py -e message.txt output.txt"
        print "python hw03.py -d output.txt decrypted.txt"
    
    ## Program End ##