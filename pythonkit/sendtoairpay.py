#!/Python27/python 
import cgi
import cgitb
import config
import sys
import datetime
from pprint import pprint
from checksum import Checksum

cgitb.enable()

# HEADERS
print "Content-Type:text/html; charset=UTF-8"
print  # blank line required at end of headers

today = datetime.datetime.now().strftime ("%Y-%m-%d")

form = cgi.FieldStorage()
chk = Checksum()

errorAction = 'error.py'

buyerEmail = form.getvalue('buyerEmail')
buyerEmail =  form.getvalue('buyerEmail')
buyerPhone = form.getvalue('buyerPhone')
buyerFirstName = form.getvalue('buyerFirstName')
buyerLastName = form.getvalue('buyerLastName')
buyerAddress = form.getvalue('buyerAddress')
amount = form.getvalue('amount')
buyerCity = form.getvalue('buyerCity')
buyerState = form.getvalue('buyerState')
buyerPinCode = form.getvalue('buyerPinCode')
buyerCountry = form.getvalue('buyerCountry')
orderid = form.getvalue('orderid')

#validation starts here

import re
import sys


def createsendBack( action,sendBack,error=''):
	print "<!DOCTYPE HTML>"
	print "<html lang='en'>"
	print "<head>"
	print "<meta charset='utf-8' />"
	print "</head>"
	print "<body onLoad='javascript:document.errorform.submit();'>"
	print "<form name='errorform' id='errorform' method='post' action='error.py'>"
	print "<input type='hidden' id='bac' name='bac' value='"+sendBack+"'>"
	print "<input type='hidden' id='status' name='status' value='"+error+"'>"
	print "</form>"
	print "</body>"
	print "</html>"
	sys.exit()
	
# if not buyerEmail  and not buyerPhone  and not buyerFirstName  and not buyerLastName  and not amount:
# 	createsendBack(errorAction,sendBack='',error='ALL')

if not buyerFirstName  and not buyerLastName  and not amount:
	createsendBack(errorAction,sendBack='',error='ALL')

# if not buyerEmail:
# 	createsendBack(errorAction,sendBack='',error='E')
# else:
# 	match = re.search(r'[\w.-]+@[\w.-]+.\w+', buyerEmail)
# 	if not match:
# 		createsendBack(errorAction,sendBack='',error='VE')

if buyerEmail:
	match = re.search(r'[\w.-]+@[\w.-]+.\w+', buyerEmail)
	if not match:
		createsendBack(errorAction,sendBack='',error='VE')


# if not buyerPhone:
# 	createsendBack(errorAction,sendBack='',error='BP')
# else:
# 	match = re.search(r'^[789]\d{9}$', buyerPhone)
# 	if not match:
# 		createsendBack(errorAction,sendBack='',error='VBP')

if buyerPhone:
	match = re.search(r'^[789]\d{9}$', buyerPhone)
	if not match:
		createsendBack(errorAction,sendBack='',error='VBP')

if not buyerEmail  and not buyerPhone:
	createsendBack(errorAction,sendBack='',error='EP')

if not buyerFirstName:
	createsendBack(errorAction,sendBack='',error='FN')	
else:
	match = re.search(r'^[A-Za-z\d\s]+$', buyerFirstName)
	if not match:
		createsendBack(errorAction,sendBack='',error='VFN')	

if not buyerLastName:
	createsendBack(errorAction,sendBack='',error='LN')	
else:
	match = re.search(r'^[A-Za-z\d\s]+$', buyerLastName)
	if not match:
		createsendBack(errorAction,sendBack='',error='VLN')	

if buyerAddress:
	match = re.search(r'^[A-Za-z. ,;#$\/()-_]*$', buyerAddress)
	if not match:
		createsendBack('error.py?a='+buyerAddress,sendBack='',error='VADD')	

if buyerCity:
	match = re.search(r'^[A-Za-z \d]{2,50}$', buyerCity)
	if not match:
		createsendBack(errorAction,sendBack='',error='VCIT')

if buyerState:
	match = re.search(r'^[a-z \d]{2,50}$', buyerState)
	if not match:
		createsendBack(errorAction,sendBack='',error='VSTA')	

if buyerCountry:
	match = re.search(r'^[a-z \d]{2,50}$', buyerCountry)
	if not match:
		createsendBack(errorAction,sendBack='',error='VCON')	
	
if buyerPinCode:
	match = re.search(r'^[a-z\d]{4,8}$', buyerPinCode)
	if not match:
		createsendBack(errorAction,sendBack='',error='VPIN')	


if not amount:
	createsendBack(errorAction,sendBack='',error='A')	
else:
	match = re.search(r'^[0-9]{1,6}\.[0-9]{2,2}$', amount)
	if not match:
		createsendBack(errorAction,sendBack='',error='VA')	
	

#validation ends here

if not buyerEmail:
	buyerEmail = '';

if buyerAddress  and  buyerCity and  buyerState and  buyerCountry:
	alldata = buyerEmail + buyerFirstName + buyerLastName + buyerAddress + buyerCity + buyerState + buyerCountry + amount + orderid
else:
	alldata = buyerEmail + buyerFirstName + buyerLastName + amount + orderid

privatekey = chk.encrypt(config.username + ":|:" + config.password, config.secret)
checksum = chk.calculateChecksum(alldata + today, privatekey)

print "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">"
print "<html xmlns=\"http://www.w3.org/1999/xhtml\">"
print "<head>"
print "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />"
print "<title>Airpay</title>"
print "<script type=\"text/javascript\">"
print "function submitForm() {"
print "var form = document.forms[0];"
print "form.submit();"
print " }"
print "</script>"
print "</head>"
print "<body onload=\"javascript:submitForm()\">"
print "<center>"
print "<table width=\"500px;\">"
print "<tr>"
print "<td align=\"center\" valign=\"middle\">Do Not Refresh or Press Back <br/> Redirecting to Airpay</td>"
print "</tr>"	
print "<tr>"
print "<td align=\"center\" valign=\"middle\">"
print "<form action=\"https://payments.airpay.co.in/pay/index.php\" method=\"post\">"
print '<input type="hidden" name="privatekey" value="'+privatekey+'">'
print '<input type="hidden" name="mercid" value="'+config.mercid+'">'
print '<input type="hidden" name="orderid" value="'+orderid+'">'
print "<input type=\"hidden\" name=\"currency\" value=\"356\">"
print "<input type=\"hidden\" name=\"isocurrency\" value=\"INR\">"

chk.outputForm(checksum,form)

print "</form>"
print "</tr>"
print "</table>"
print "</center>"
print "</html>"





