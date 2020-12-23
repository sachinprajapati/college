#!/Python27/python 
import hashlib
import cgi
import sys
from pprint import pprint
class Checksum:
    
    def test(self):
        print("hello")

    def calculateChecksum(self,data, secret_key):
    	checksum = hashlib.md5((data+secret_key).encode('utf-8')).hexdigest()
    	return checksum

    def encrypt(self,data, salt):
        ke = (salt+'@'+data).encode('utf-8')
        encryptedkey = hashlib.sha256(ke).hexdigest()
        return encryptedkey
    	

    def outputForm(self,checksum,form):
        frm = form.keys()
        #frm = ['buyerCountry', 'orderid', 'buyerState', 'buyerCity', 'buyerEmail', 'buyerPinCode', 'buyerLastName', 'amount', 'buyerFirstName', 'buyerAddress', 'buyerPhone']
        params = {}
        for k in frm:
        	params[k] = form[k].value

        

        for key,value in params.iteritems():
        	print ('<input type="hidden" name="'+key+'" value="'+value+'" />')
		
		


        print ('<input type="hidden" name="checksum" value="'+checksum+'" />')

	

    def verifyChecksum(self,checksum, all, secret):
        cal_checksum = self.calculateChecksum(secret, all)
        bool = 0;

        if checksum == cal_checksum:
        	bool = 1

        return bool;


	
