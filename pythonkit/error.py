#!/Python27/python 
import cgi

# HEADERS
print "Content-Type:text/html; charset=UTF-8"
print  # blank line required at end of headers

print "<div align = 'center'><a href= 'transaction.html'>Back</a></div>"
form = cgi.FieldStorage()
status = form.getvalue('status')

if status == 'ALL':
	print "All fields are mendatory."
if status == 'E':
	print "Please enter email address."
if status == 'VE':
	print "Please enter valid email."
if status == 'BP':
	print "Please enter phone number."
if status == 'VBP':
	print "Please enter valid phone number."
if status == 'FN':
	print "Please enter first name."
if status == 'VFN':
	print "Please enter valid first name."
if status == 'LN':
	print "Please enter last name."
if status == 'VLN':
	print "Please enter valid last name."
if status == 'VADD':
	print "Please enter valid address."
if status == 'VCIT':
	print "Please enter valid City Name."
if status == 'VSTA':
	print 'Please enter valid State'
if status == 'VCON':
	print "Please enter valid Country Name."
if status == 'VADD':
	print "Please enter valid address."
if status == 'VPIN':
	print "Please enter valid PIN."
if status == 'A':
	print "Please enter amount."
if status == 'VA':
	print "Please enter valid amount."
if status == 'EP':
	print "Please enter email or phone number."
