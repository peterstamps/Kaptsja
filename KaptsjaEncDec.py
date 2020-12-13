###################################################################################################
#  KaptsjaEncDec uses AES Encryption to encrypt / decrypr ANY data string or file 
#  Kaptsja is the Dutch phonetic pronunciation of the English word Captcha.
#  In Kaptsja it encrypts/decrypts the controlvalue send with the Kaptsja page.
#  This encryption/ decryption module can be used universally in many projects!
#
#  WARNING: BEFORE CHANGING ANYTHING IN THIS FILE MAKE A BACKUP SO YOU CAN RESTORE !
#  Read the comments in this file as they contain valuable information to understand the effects 
###################################################################################################

from Crypto.Cipher import AES
from Crypto import Random
import base64
import hashlib
import os
import random

key_filename = "secret_key.txt"

def get_create_save_key(self):
    if os.path.exists(key_filename) == True:
        kfile = open(key_filename,"rb")
        key = kfile.readline()
        kfile.close()
        # logging.info(r'Get key: Encryption key: %s' % secret_key)
    else:
        kfile = open(key_filename,"wb") 
        # os.urandom generates a random value of 32 bytes long using key_size
        # the key size may be 128, 192, or 256 bits long.
        # 256 bits equals to 32 bytes 
        # 128 bits equals to 16 bytes 
        key_size = 32
        key = os.urandom(key_size)
        kfile.write(key)
        kfile.close() 
        # logging.info(r'Create & Save Key: Encryption key: %s' % key)
    return key


class Cripto(object): #  a variant of Crypto :-)
    def __init__(self, key_filename): 
        self.key_filename = key_filename
        # get the key from the key file
        if os.path.exists(self.key_filename) == True:
            kfile = open(self.key_filename,"rb")
            self.key = kfile.readline()
            kfile.close()
            # logging.info(r'Get key: Encryption key: %s' % secret_key)
        else:
            kfile = open(self.key_filename,"wb") 
            # os.urandom generates a random value of 32 bytes long using key_size
            # the key size may be 128, 192, or 256 bits long.
            # 256 bits equals to 32 bytes 
            # 128 bits equals to 16 bytes 
            key_size = 32
            self.key = os.urandom(key_size)
            kfile.write(self.key)
            kfile.close() 
            # logging.info(r'Create & Save Key: Encryption key: %s' % key)
        #A block cipher works on units of a fixed size (known as a block size), but messages come in a variety of lengths. 
         # block size MUST be equal to 16 which is the value of AES.block_size. 
        # Do not change this!
        self.block_size = AES.block_size
        # MODE_CBC: Ciphertext Block Chaining is a mode of operation where each
        # plaintext block gets XOR-ed with the previous ciphertext block prior to encryption.
        # XOR-ed is an exclusive or, or exclusive disjunction and is a logical operation 
        # that outputs true only when inputs differ (one is true, the other is false).
        self.mode_cbc = AES.MODE_CBC
        
    #################################### ENCRYPTION METHODS ##################################### 
    
    def encryption(self, data):  # all encryption steps in one go
        ''' 
        The correct sequence of processing for encryption, 
        For easy following the flow, all intermediate data results are numbered and deleted at the end. 
        This is not per se needed and all data1,data2,.. may be called just data)
        Input data is a default Python 3 string of type str which is by default encoded with utf-8
        Steps for encription:
         A. Encode the still readable data (of Python type str) into bytes; a "bytes literal"), 
            this will ensure correct length calculation when double-byte or multiple bytes characters (sets) have been used like Chinese characters.
         B. Add padding characters to data (of Python type bytes)) till a length of a multiple of 16 bytes has been reached.
         C. Encrypt with cipher the encoded data to a encrypted bytes data object using default encoding set 'utf-8'
         D. Concatenate the initiation vector and the encrypted bytes data object together to a single data value in bytes.
            This concatenated data (iv_and_enc) is the bytes (of Python type bytes) representation of the encrypted end result. 
            The encryption output can be written into a binary file (write/read file with open(name, mode="wb") or open(name, "wb")
         G. Encode with library Base64 the concatenated initiation vector and encrypted bytes object to a "readable" string 
            This Base64 encode output is a string (of Python type str) representation of the encrypted end result as is printable and transferrable (e.g. via http).
        '''
        data1 = self.encode_string(data)                # encode the still readable input string of of Python 3 type str which defaults to utf-8.
        data2 = self.pad_bytes(data1)                   # pad the encoded bytes  - when needed - with extra bytes till a multiple of 16 bytes has been reached 
        data3 = self.encrypt_string(data2)              # encrypt the encoded bytes literal (a multiple of 16 bytes)  
        self.iv_and_enc = self.iv + data3               # concatenate initiation vector (bytes) + encrypted bytes literal to a bytes literal (= the bytes Encrypted end result)
        data4 = self.base64encode_string(self.iv_and_enc) # create with based64 encode a printable/transferrable string version of it in Python 3 type str which defaults to utf-8.
        encryption_result = data4                       # return encryption result as string
        del data, data1, data2, data3, data4            # delete all intermediate data to quickly save memory 
        return encryption_result   
        
    def encode_string(self, data):  # in: an normal string of Python 3 type str which defaults to utf-8. may contain double/multiple bytes characters like 一個長句子，外加一些額外的單詞。
        # encode printable characters to bytes
        return data.encode()  #out: encoded bytes literal of Python 3 type bytes
 
    def pad_bytes(self, data): # in: should always be an encoded byte string (not to be confused with base64 encoded!!)
        extra = len(data) % self.block_size
        if extra > 0:
            data = data + b"\0" * (self.block_size - extra)
        return data # out: a padded encoded byte string of a multiple of 16 bytes length ready for encryption!

    def encrypt_string(self, data):  # in: encoded padded bytes literal
        # if following error occurs it means that the input is NOT properly padded: ValueError: Input strings must be a multiple of 16 in length
        #  Usually this happens when data of type(data) == str has been padded BEFORE encoding, which is wrong
        #  Always pad and unpad on bytes not on strings! 
        #   -  There is only one exception and that is when all characters in the original input string are single byte characters!  
        #   -  Then padding of original input string after the encode would also result in a multiple of 16 bytes length. Avoid this method!   
        #   
        # create initiation vector for encryption in Python 3 format bytes
        self.iv = Random.new().read(self.block_size)
        # create cipher for encryption and decription
        self.cipher = AES.new(self.key, self.mode_cbc, self.iv)
        encrypted_string =  self.cipher.encrypt(data) # use cipher to encrypt the bytes
        return encrypted_string   # out: encrypted bytes literal 

    def base64encode_string(self, iv_and_enc):  # in: concatenated iv and encrypted bytes literal (Note: the input here is NOT only the output of self.function encrypt_string()!
        # encode concatenated iv and the encrypted bytes literal to a printable/transferrable string of Python 3 type str
        # The iv and the encryted data in bytes MUST be kept together else decryption will always fail (therefore concatenation is the preferred method) 
        return base64.b64encode(iv_and_enc) # out: base64 encoded string literal of Python 3 type str
    
    # SOME HELPER FUNCTIONS

    def get_iv(self):  # returns no value (None) when not set
        if self.iv: return self.iv
        
    def get_cipher(self): # returns no value (None) when not set
        if self.cipher: return self.cipher



    #################################### DECRYPTION METHODS ##################################### 
    
    def decryption(self, data): # all decryption steps in one go
        ''' 
        The correct sequence of processing for decryption, 
        For easy following the flow, all intermediate data results are numbered and deleted at the end. 
        This is not per se needed and all data1,data2,.. may be called just data)
        Input is a printable and transferrable (e.g. via http) representation of the encrypted text string (equals to the output of encryption process as defined above).
        Steps for decription:
         A. Decode with library Base64 the concatenated initiation vector and encrypted string to bytes
         B. Decrypt with cipher the Base64 decoded result to a bytes object (still padded)
         C. Remove padding characters to decypted bytes.
         D. Decode the unpadded bytes into a readable string (original text)
        '''
        data1 = self.base64decode_string(data)    # input is a printable/transferrable base64 encoded str, which must be decoded to bytes first
        data2 = self.decrypt_string(data1)           # decrypt decoded bytes literal to decrypted bytes
        data3 = self.unpad_bytes(data2)              # remove all padding characters from decrypted bytes         
        data4 = self.decode_string(data3)            # decode the unpadded bytes to original string
        decryption_result = data4                    # return encryption result
        del data, data1, data2, data3, data4              # delete all intermediate strings to quickly save memory 
        return decryption_result

    def base64decode_string(self, data): #in: base64encoded string of Python 3 type str. This contains the concatenated iv and encrypted data
        # decode the printable/tranferrable characters from string Python 3 type str into Python 3 type bytes
        return base64.b64decode(data)  #out: decoded bytes literal

    def decrypt_string(self, data): # in: base64decoded bytes literal, which when originally correctly created is already a multiple of 16 bytes length
        iv = data[:self.block_size] # first 16 bytes of the bytes literal contains the initiation vector, which together with the key is needed for decryption
        cipher = AES.new(self.key, self.mode_cbc, iv) # determine the cipher based on key and iv and encryption mode
        enc = data[self.block_size:]  # After the first 16 bytes of the initiation vector, the encryted data follows
        encoded_string = cipher.decrypt(enc)   # decrypt the encryted data
        return encoded_string    # return the decripted but still padded data as bytes
    
    def unpad_bytes(self, data):                # in: decrypted but still padded data as bytes
        unpadded_string =  data.rstrip(b"\0")   # get rid of all padding characters (which were added before)
        return unpadded_string                  # out decrypted unpadded data as bytes

    def decode_string(self, data):   #in: encoded and unpadded data in bytes
        # decode printable ASCII characters to bytes
        return data.decode('utf-8')  #out: decoded string of data in Python type str, which should be equal to the original input for encryption!


    #################################### HELPER AND FILE METHODS ##################################### 
        
    def str2bytes(self, data):        # in: a  string
        return bytes(data, 'utf-8')   # out : a bytes literal
        
    def bytes2str(self, data):        # in : a bytes literal
        return str(data)     # out : a  string

    def encrypt_file(self, file_name):
        with open(file_name, 'r', encoding="utf8") as fo:
            text_from_file = fo.read()
        encrypted_text = self.encryption(text_from_file)
        with open(file_name[:-4] + "_enc.txt", 'wb') as fo:
            fo.write(encrypted_text)

    def decrypt_file(self, file_name):
        with open(file_name[:-4] + "_enc.txt", 'rb') as fo:
            encrypted_text_from_file = fo.read()
        decrypted_text = self.decryption(encrypted_text_from_file)
        with open(file_name[:-4] + "_dec.txt", 'w', encoding="utf-8") as fo:
            fo.write(decrypted_text)

if __name__ == '__main__':
    import sys

###################################################################
#    Start Encryption and Decryption in ONE GO             
###################################################################
    cript = Cripto(key_filename)
    text ="A long sentence with some extra words. 一個長句子，外加一些額外的單詞。"
    # direct one go encryption
    encrypted_result = cript.encryption(text)
    print ("\nEncrypted result\n", encrypted_result , "\n")

    # direct one go decryption
    decrypted_result = cript.decryption(encrypted_result)
    print ("\nDecrypted result\n", decrypted_result, "\n")

###################################################################
#    Encryption and Decryption in a Step by Step approach             
###################################################################
#    ENCRYPTION - Step by Step           
###################################################################

    print ("*"*20, "ENCRYPTION STARTED step by step", "*"*20)    
  
    text ="A 一個長句子 long NEW sentence with some extra words. 一個長句子，外加一些額外的單詞。"
    print("\nInput: original text (str)\n", text, "\n")
    
    # Show initiation vector and corresponding chiper
    print("\nOutput: inition vector (bytes)\n", cript.get_iv() )
    print("Output: chiper (bytes)", cript.get_cipher(), "\n")
    
    text1 = cript.encode_string(text)          # encode the text from string to bytes
    print("\nOutput: encoded text (bytes)\n", text1, "\n")

    text2 = cript.pad_bytes(text1)              # pad the encoded bytes text 
    print("\nOutput: padded text (bytes)\n", text2, "\n")
       
    text3 = cript.encrypt_string(text2)         # encrypt encoded bytes literal
    print("\nOutput: encrypted text (bytes), excluded initiaton vector!\n", text3, "\n")

    iv_and_enc = cript.iv + text3               # concatenate initiation vector + encrypted bytes literal
    print("\nOutput: encryption result (bytes) equals to initiaton vector+encrypted text \n", iv_and_enc, "\n")

    text4 = cript.base64encode_string(iv_and_enc) # create a printable/transferrable version of it
    encryption_output = text4                  # keep encryption_output for decryption process

    print("\nOutput: encryption result (str in base64 format) equals to initiaton vector+encrypted text\n", encryption_output, "\n")
    del text1, text2, text3, text4             # delete all intermediate strings saving memory 

###################################################################
#    DECRYPTION - Step by Step          
###################################################################

    print ("*"*20, "DECRYPTION STARTED  step by step", "*"*20)    

    text5 = encryption_output
    print("\nInput: encryption result (str in base64 format) equals to initiaton vector+encrypted text\n", text5, "\n")

    text6 = cript.base64decode_string(text5)   # input is string: printable/transferrable  
    print("\nOutput: base64 decoded text (bytes)\n", text6, "\n")

    text7 = cript.decrypt_string(text6)       # decrypt encoded bytes to padded bytes
    print("\nOutput: decrypted text (bytes)\n", text7, "\n")

    text8 = cript.unpad_bytes(text7)         # delete padding characters to get original text
    print("\nOutput: unpadded text (bytes)\n", text8, "\n")
 
    text9 = cript.decode_string(text8)        # decode padded bytes to padded string    
    decryption_result = text9      
           # return encryption result
    del text5, text6, text7, text8             # delete all intermediate strings saving memory 
    print("\nOutput: decoded text = decryption result, should be equal as original text (str)\n", decryption_result, "\n") 


###################################################################
#    Encryption and Decryption of a File Content in ONE GO             
###################################################################

    # Create a file with some text to be encrypted 
    # Prefix "Z__" is used to find file easyly back when sorting.
    # Files created with prefix "Z__" can be deleted after reviewing test results
    
    cript = Cripto(key_filename)

# -----------------------------------------------------------------
#    Create the input file in text mode  (mode="w")
#    The input file  cannot be a binary file!
#    It must be created with: open(<filename>, 'w', encoding="utf8")  <! mandatory for text with certain language characters    
#                         or: open(<filename>, 'w')                   <! 
#   The default encoding is platform dependent (whatever import locale; locale.getpreferredencoding() returns
# -----------------------------------------------------------------    
    test_filename = 'Z__input.txt'
    text ="A long NEW FILE sentence with some extra words. 一個長句子，外加一些額外的單詞。"
    with open(test_filename, 'w', encoding="utf8") as fo:
        fo.write(text)
              
    cript.encrypt_file( test_filename)
    cript.decrypt_file( test_filename) 
    print ("\nTest: input text file and corresponding encryption and decryption result files are created in the run directory.\n")
