import string


def decode(x, k):
    # danh sach chu cai tieng anh viet thuong
    abc_lowercase = string.ascii_lowercase
    abc_uppercase = string.ascii_uppercase
    # chuoi sau khi decode
    str_decode = ""
    # chay het chuoi x
    for c in x:
        # neu khong phai dau cach thi di chuyen theo khoa k
        if c != " ":
            if c.isupper():
                str_decode += "".join([abc_uppercase[(abc_uppercase.find(c)-k)%26]])
            else:
                str_decode += "".join([abc_lowercase[(abc_lowercase.find(c)-k)%26]])
        else:
            # gap dau cach thi be nguyen dau cach vao chuoi decode
            str_decode += " "
    return str_decode

if __name__ == "__main__":
    str_x = "EBG KVVV vf n fvzcyr yrggre fhofgvghgvba pvcure gung ercynprf n yrggre jvgu gur yrggre KVVV yrggref nsgre vg va gur nycunorg. EBG KVVV vf na rknzcyr bs gur Pnrfne pvcure, qrirybcrq va napvrag Ebzr. Synt vf SYNTFjmtkOWFNZdjkkNH. Vafreg na haqrefpber vzzrqvngryl nsgre SYNT."
    for i in range(1, 26):
        print("----------ROT-{}------------------".format(i))
        print(decode(str_x, i))
        print("---------------------------------------")