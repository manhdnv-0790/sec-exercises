import base64

STAND_TABLE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
MY_TABLE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789=~.'

ENCODE = str.maketrans(STAND_TABLE, MY_TABLE)
DECODE = str.maketrans(MY_TABLE, STAND_TABLE)

def my_base64_encode(str_s):
    return base64.b64encode(str_s.encode()).decode().translate(ENCODE)

def my_base64_decode(str_s):
    return base64.b64decode(str_s.translate(DECODE)).decode()

if __name__ == "__main__":
    print("--------------------MY BASE64 ENCODE -------------")
    s = my_base64_encode("N9uy3nM@nhS2n0tf0und")
    print(s)
    print("--------------------MY BASE64 DECODE -------------")
    s2 = my_base64_decode(s)
    print(s2)