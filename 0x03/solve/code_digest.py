import hashlib
import requests

uri = "/~q9/flag.html"
method = "GET"
ha1 = "c627e19450db746b739f41b64097d449"
ha2 = hashlib.md5("{}:{}".format(method, uri).encode('utf-8')).hexdigest()
cnonce = "9691c24"
nc = "00000001"
realm = "secret"
qop = "auth"
algorithm = "MD5"
username ="q9"

url = "http://ksnctf.sweetduet.info:10080/~q9/flag.html"
auth_header = requests.get(url).headers["WWW-Authenticate"]
auth_arr = auth_header.split(" ")
nonce = auth_arr[2][7:-2]

before_reponse = "{}:{}:{}:{}:{}:{}".format(ha1,nonce,nc,cnonce,qop, ha2)
response = hashlib.md5(before_reponse.encode("utf-8")).hexdigest()
# print(response)

headers  = {
    "Authorization":"Digest username=\"{}\", realm=\"{}\", nonce=\"{}\", uri=\"{}\", algorithm=\"{}\", response=\"{}\", qop={}, nc={}, cnonce=\"{}\"".format(username, realm, nonce, uri, algorithm, response, qop, nc, cnonce)
}

# print(headers)

results =  requests.get(url, headers=headers)

print(results.text)
