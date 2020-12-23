import hashlib
import datetime
from pythonkit.checksum import Checksum
import requests

import config

buyerEmail = 'sachin@gmail.com'

buyerFirstName = 'sachin'

buyerLastName = 'kumar'

amount = "10.00"
currency = 356
isocurrency = "INR"
customvar = "fee"

orderid = 'order1'
today = datetime.datetime.now().strftime ("%Y-%m-%d")
url = "https://payments.airpay.co.in/pay/index.php"

chk = Checksum()

alldata = buyerEmail + buyerFirstName + buyerLastName + amount + orderid

privatekey = chk.encrypt(config.username + ":|:" + config.password, config.secret)
checksum = chk.calculateChecksum(alldata + today, privatekey)

print("privatekey",privatekey,"checksum",checksum)

myobj = {'buyerEmail': buyerEmail, 'buyerFirstName': buyerFirstName, 'buyerLastName': buyerLastName, \
		'amount': amount, 'currency': currency, 'isocurrency': isocurrency, 'customvar': customvar, \
		'orderid': orderid, 'privatekey': privatekey, 'mercid': config.mercid, 'checksum': checksum
}

x = requests.post(url, data = myobj)

print(x.text)
