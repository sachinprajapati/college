#!/Python27/python 
import re
import sys

def createsendBack( id, value, action,sendBack,err='',):
	print "<!DOCTYPE HTML>"
	print "<html lang=\"en\">"
	print "<head>"
	print "<meta charset=\"utf-8\" />"
	print "</head>"
	print "<body onLoad=\"javascript:document.errorform.submit();\">"
	print "<form name=\"errorform\" id=\"errorform\" method=\"post\" action=\"'.$action.'\">"
	print "<input type=\"hidden\" id=\"bac\" name=\"bac\" value=\"'.htmlspecialchars($sendBack).'\">"
	print "<input type=\"hidden\" id=\"status\" name=\"status\" value=\"'.$err.'\">"
	print "<input type=\"hidden\" id=\"statusmsg\" name=\"statusmsg\" value=\"'.$statusmsg.'\">"
	print "<input type=\"hidden\" id=\"'.$id.'\" name=\"'.$id.'\" value=\"'.$value.'\">"
	print "</form>"
	print "</body>"
	print "</html>"
	sys.exit()
	
# if not buyerEmail  and not buyerPhone  and not buyerFirstName  and not buyerLastName  and not amount:
# 	createsendBack(id,value,'error.py',sendBack='',error='ALL')

if not buyerFirstName  and not buyerLastName  and not amount:
	createsendBack(id,value,'error.py',sendBack='',error='ALL')

if not buyerEmail:
	#createsendBack(id,value,'error.py',sendBack='',error='ALL')
else:
	match = re.search(r'[\w.-]+@[\w.-]+.\w+', email)
	if not match:
		createsendBack(id,value,'error.py',sendBack='',error='VE')

if not buyerPhone:
	#createsendBack(id,value,'error.py',sendBack='',error='ALL')
else:
	match = re.search(r'/^[0-9- ]{8,15}$/i', buyerPhone)
	if not match:
		createsendBack(id,value,'error.py',sendBack='',error='VBP')

if not buyerEmail  and not buyerPhone:
	createsendBack(id,value,'error.py',sendBack='',error='EP')

if not buyerFirstName:
	createsendBack(id,value,'error.py',sendBack='',error='FN')	
else:
	match = re.search(r'/^[a-z \d]{1,50}$/i', buyerFirstName)
	if not match:
		createsendBack(id,value,'error.py',sendBack='',error='VFN');	

if not buyerLastName:
	createsendBack(id,value,'error.py',sendBack='',error='LN');	
else:
	match = re.search(r'/^[a-z \d]{1,50}$/i', buyerLastName)
	if not match:
		createsendBack(id,value,'error.py',sendBack='',error='VLN')	

if buyerAddress:
	match = re.search(r'/^[a-z ,;.#$\/( )-_\d]{4,255}$/i', buyerAddress)
	if not match:
		createsendBack(id,value,'error.py?a='+buyerAddress,sendBack='',error='VADD')	

if buyerCity:
	match = re.search(r'/^[a-z \d]{2,50}$/i', buyerCity)
	if not match:
		createsendBack(id,value,'error.py',sendBack='',error='VCIT')

if buyerState:
	match = re.search(r'/^[a-z \d]{2,50}$/i', buyerState)
	if not match:
		createsendBack(id,value,'error.py',sendBack='',error='VSTA')	

if buyerCountry:
	match = re.search(r'/^[a-z \d]{2,50}$/i', buyerCountry)
	if not match:
		createsendBack(id,value,'error.py',sendBack='',error='VCON')	
	
if buyerPinCode:
	match = re.search(r'/^[a-z\d]{4,8}$/i', buyerCountry)
	if not match:
		createsendBack(id,value,'error.py',sendBack='',error='VPIN')	


if not amount:
	createsendBack(id,value,'error.py',sendBack='',error='A')	
else:
	match = re.search(r'/^[0-9]{1,6}\.[0-9]{2,2}$/', amount)
	if not match:
		createsendBack(id,value,'error.py',sendBack='',error='VA')	
	



