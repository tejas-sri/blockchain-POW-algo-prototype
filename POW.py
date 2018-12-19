import pickle
import hashlib
import binascii
import base64
import time

salt = "saltyboi"
blockchain_file = "blockchain"
powfactor = 4

def hashstr(string):
    return binascii.hexlify(hashlib.scrypt(string.encode('utf-8'), salt=salt.encode('utf-8'), n=1024, r=1, p=1))

def mine(string, i):
    bstring = string+':'
    pstring = bstring+base64.b64encode(str(i).encode('utf-8')).decode('utf-8')
    shash = hashstr(pstring).decode('utf-8')
    if shash.startswith('0'*powfactor):
        return ([pstring, shash])
    else:
        return 0

def proofOfWork(string, blockchain_file):
    start = time.time()
    i = 0
    while True:
        test = mine(string, i)
        if test != 0:
            t = time.time()-start
            with open(blockchain_file, 'rb') as bchain:
                bchaindata = pickle.load(bchain)
            phash = hashlib.sha3_512(str(bchaindata[-1]).encode('utf-8')).hexdigest()
            block = [phash, test[0], test[1]]
            bchaindata.append(block)
            with open(blockchain_file, 'wb') as bchain:
                pickle.dump(bchaindata, bchain)
            return [i, t]
        i += 1

if __name__ == '__main__':    
    while True:
        print('----- New Transaction -----')
        details = input("Enter Transaction Details: ")
        print('mining..')
        hashesChecked, timer = proofOfWork(details, blockchain_file)
        print('Done! '+str(hashesChecked)+' hashes were checked in ' + str(timer)+ ' seconds for a rate of ' + str(hashesChecked/timer) + ' hashes/second.')
