#!/Python27/python 
import cgi
import cgitb
cgitb.enable()

# HEADERS
print "Content-Type:text/html; charset=UTF-8"
print  # blank line required at end of headers

# CONTENT
print "<html><body>"
print "Content"
print "</body></html>"

form = cgi.FieldStorage()
print form["firstname"]