#!/Python27/python 
import config
import cgi
import cgitb
import binascii
import sys
import zlib
import pprint

cgitb.enable()
print "Content-Type:text/html; charset=UTF-8\r\n"

form = cgi.FieldStorage()

#pprint.pprint(form)

TRANSACTIONID = form.getvalue('TRANSACTIONID')
APTRANSACTIONID  = form.getvalue('APTRANSACTIONID')
AMOUNT  = form.getvalue('AMOUNT')
TRANSACTIONSTATUS  = form.getvalue('TRANSACTIONSTATUS')
MESSAGE  = form.getvalue('MESSAGE')
ap_SecureHash = form.getvalue('ap_SecureHash')
CUSTOMVAR  = form.getvalue('CUSTOMVAR')



error_msg = ''

if not TRANSACTIONID or not APTRANSACTIONID or not AMOUNT or not TRANSACTIONSTATUS or not ap_SecureHash:
	if not TRANSACTIONID:
		error_msg += 'TRANSACTIONID' 
	
	if not APTRANSACTIONID:
		error_msg +=  ' APTRANSACTIONID'
	
	if not AMOUNT:
		error_msg +=  ' AMOUNT'
	
	if not TRANSACTIONSTATUS:
		error_msg +=  ' TRANSACTIONSTATUS'
					
	if not ap_SecureHash:
		error_msg +=  ' ap_SecureHash'

	error_msg += '<tr><td>Variable(s) '+ error_msg+' is/are empty.</td></tr>'

crcdata = str(TRANSACTIONID) +':'+ str(APTRANSACTIONID) +':'+ str(AMOUNT) +':'+ str(TRANSACTIONSTATUS) +':'+ str(MESSAGE)+':'+ str(config.mercid) +':'+ str(config.username)

mer_sec_hsh = zlib.crc32(crcdata) & 0xffffffff
merchant_secure_hash = "%u" %  mer_sec_hsh

#comparing Secure Hash with Hash sent by Airpay
if ap_SecureHash != merchant_secure_hash:
	error_msg += '<tr><td>AP Secure Hash '+ap_SecureHash+'</td></tr>';
	error_msg += '<tr><td>Merchant Secure Hash '+merchant_secure_hash+'</td></tr>';
	error_msg += '<tr><td>Secure Hash mismatch.</td></tr>';
	error_msg += '<tr><td>CRCdata.'+crcdata+'</td></tr>';


if error_msg:
	print "<table><font color=\"red\"><b>ERROR:</b> "+error_msg+"</font></table>"
	print "<table>"
	print "<tr><td>Variable Name</td><td> Value</td></tr>"
	print "<tr><td>TRANSACTIONID:</td><td> "+TRANSACTIONID+"</td></tr>"
	print "<tr><td>APTRANSACTIONID:</td><td> "+APTRANSACTIONID+"</td></tr>"
	print "<tr><td>AMOUNT:</td><td> "+AMOUNT+"</td></tr>"
	print "<tr><td>TRANSACTIONSTATUS:</td><td> "+TRANSACTIONSTATUS+"</td></tr>"
	print "<tr><td>CUSTOMVAR:</td><td> "+CUSTOMVAR+"</td></tr>"
	print "</table>"
	sys.exit()


if TRANSACTIONSTATUS == '200':
	print "<table><tr><td>Success Transaction</td></tr></table>"
	print "<table>"
	print "<tr><td>Variable Name</td><td> Value</td></tr>"
	print "<tr><td>TRANSACTIONID:</td><td> "+TRANSACTIONID+"</td></tr>"
	print "<tr><td>APTRANSACTIONID:</td><td> "+APTRANSACTIONID+"</td></tr>"
	print "<tr><td>AMOUNT:</td><td> "+AMOUNT+"</td></tr>"
	print "<tr><td>TRANSACTIONSTATUS:</td><td> "+TRANSACTIONSTATUS+"</td></tr>"
	print "<tr><td>MESSAGE:</td><td> "+MESSAGE+"</td></tr>"
	#print "<tr><td>CUSTOMVAR:</td><td> "+CUSTOMVAR+"</td></tr>"
	print "</table>"
else:
	print "<table><tr><td>Failed Transaction</td></tr></table>"
	print "<table>"
	print "<tr><td>Variable Name</td><td> Value</td></tr>"
	print "<tr><td>TRANSACTIONID:</td><td> "+TRANSACTIONID+"</td></tr>"
	print "<tr><td>APTRANSACTIONID:</td><td> "+APTRANSACTIONID+"</td></tr>"
	print "<tr><td>AMOUNT:</td><td> "+AMOUNT+"</td></tr>"
	print "<tr><td>TRANSACTIONSTATUS:</td><td> "+TRANSACTIONSTATUS+"</td></tr>"
	print "<tr><td>MESSAGE:</td><td> "+MESSAGE+"</td></tr>"
	#print "<tr><td>CUSTOMVAR:</td><td> "+CUSTOMVAR+"</td></tr>"
	print "</table>"
# Process Failed Transaction
