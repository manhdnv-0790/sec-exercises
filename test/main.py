import requests

jar = requests.cookies.RequestsCookieJar()
jar.set('ship', '3%80%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%b0,10', domain='ctfq.sweetduet.info', path='	/~q31')
jar.set('signature', '8d536a3a911e0578cb301e1fbe4e0a42aa8bc8e1a0a3baeba11339ee0f006743b58c669e11a1583795e69e231af20a6411f2727541eaf5586c3ec5943e579659', domain='ctfq.sweetduet.info', path='/~q31')
# jar.set('gross_cookie', 'blech', domain='httpbin.org', path='/elsewhere')

url = "http://ctfq.sweetduet.info:10080/~q31/kangacha.php"
# 
# 
cookies = {
    'ship': '3%80%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%00%b0,10',
    'signature': '8d536a3a911e0578cb301e1fbe4e0a42aa8bc8e1a0a3baeba11339ee0f006743b58c669e11a1583795e69e231af20a6411f2727541eaf5586c3ec5943e579659'
}
data = {
    'submit': 'Gacha'
}

cookies = {}

res = requests.post(url, data=data, cookies=jar)

# import pdb; pdb.set_trace()

print(res.text)