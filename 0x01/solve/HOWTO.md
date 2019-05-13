# SOLVE

## Bài 1

* Viết biểu diễn của số `1234` sang:
    * base-2 => 10011010010
    * base-8 => 2322
    * base-16 => 4D2
    * base-36 => YA
    * base-58 => 2PM
    * base-64 => MTIzNA==

## Bài 2: Base64

Problem: Tự viết hàm `my_base64_encode` và `my_base64_decode` bằng ngôn ngữ tự chọn, sử dụng alphabet: `A-Za-z0-9=~.`

```py
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
```

## Bài 3: Easy cipher

`problem: https://ksnctf.sweetduet.info/problem/2`

* Chúng ta nhận được một chuỗi:

    `EBG KVVV vf n fvzcyr yrggre fhofgvghgvba pvcure gung ercynprf n yrggre jvgu gur yrggre KVVV yrggref nsgre vg va gur nycunorg. EBG KVVV vf na rknzcyr bs gur Pnrfne pvcure, qrirybcrq va napvrag Ebzr. Synt vf SYNTFjmtkOWFNZdjkkNH. Vafreg na haqrefpber vzzrqvngryl nsgre SYNT.`

    Ban đầu nghĩ trong đầu, cái gì đây thế này, chỉ vứt cho mỗi chuỗi loằng ngoằng kia và tiêu đề `easy cipher`, khó phết mà kêu easy.

    Rồi một lúc mình tĩnh lại thì bỗng để ý rằng, chuỗi đó chia thành từng cụm và mỗi cụm phân cách bởi khoảng trắng, rồi xong ok, có vẻ nó chả phải mã hóa gì cao siêu cả.

    Hack thời gian một tý, nhớ về những ngày còn ngồi học ở trường, nhớ là cô giáo có bảo có cái mã hóa gì đó mà nó xoay vòng trong bảng chữ cái. Đến đây là đủ rồi, xoay vòng bảng chữ cái thì không cần biết là xoay như thế nào, bắt đầu thử thôi, nó xoay thì mình xoay ngược nó lại :D . bảng chữ cái tiếng anh có mỗi 26 ký tự thôi mà :D

    Thôi xong, 26 ký tự với một chuỗi dài ngoằng, xoay khi nào cho xong :D , thôi thì mình lười thì mình viết tool vậy.

    Ý tưởng của cái mã hóa mà mình nghĩ tới trong problem này là thay thế một ký tự ở bản rõ bằng 1 ký tự ở một vị trí cách vị trí của ký tự đó 1 khoảng ( gọi là khóa k) trong bảng chữ cái tiếng anh:
    `VD: chữ a mà có khóa bằng 2 thì thay thế bằng chữ c`

    => Đến đây lại gặp vấn đề là nó có tận 26 ký tự thì nó sẽ dùng khóa K nào đây, ngồi chuyển thủ công tận 1 -> 25 cũng chết.
    vì mình nhớ là có công thứ:

    ```shell
    Mã hóa: MH(i) = (i + k) mod N
    Giải mã: GM(i) = (i - k) mod N
    ```

    Bắt đầu viết tool nhỏ dựa trên công thức đó:

    ```py
    import string


    def decode(x, k):
        # danh sach chu cai tieng anh viet thuong
        abc_lowercase = string.ascii_lowercase
        # danh sach chu cai tieng anh viet hoa
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
    ```

    * x là chuỗi cần giải mã
    * k là khóa

    Rồi chỉ việc copy chuỗi kia và và chạy hàm, với khóa k từ 1 cho tới 25. Nên là viết thêm đoạn nữa để khỏi copy đi copy lại mệt mỏi:
    ```python
    str_x = "EBG KVVV vf n fvzcyr yrggre fhofgvghgvba pvcure gung ercynprf n yrggre jvgu gur yrggre KVVV yrggref nsgre vg va gur nycunorg. EBG KVVV vf na rknzcyr bs gur Pnrfne pvcure, qrirybcrq va napvrag Ebzr. Synt vf SYNTFjmtkOWFNZdjkkNH. Vafreg na haqrefpber vzzrqvngryl nsgre SYNT."
    for i in range(1, 26):
        print("----------K-{}------------------".format(i))
        print(decode_rot(str_x, i))
        print("---------------------------------------")
    ```

    * Tại sao chạy từ 1? Vì nếu K bằng 0 chả có ý nghĩa gì cả, khi thay thế chữ cái bằng khóa K=0 tức là chính nó thì chả có gì gọi là mã hóa cả, nên chúng ta phải chạy từ 1.
    Và chạy tới 25 cũng là lý do đó, nếu vị trí 1 mã hóa với khóa k = 26, thì công thức ( 1 + 26 ) mod 26 chính là bằng 1 => trở về chính nó :3 Nên chạy từ 1 đến 25 là hợp lý rồi.

    Bây giờ cho code trên vào 1 file và chạy lên thì tìm được ở K = 13 thì chuỗi giải mã ra được có nghĩa
    `ROT XIII is a simple letter substitution cipher that replaces a letter with the letter XIII letters after it in the alphabetm ROT XIII is an example of the Caesar cipherm developed in ancient Romem Flag is FLAGSwzgxBJSAMqwxxAUm Insert an underscore immediately after FLAGm`
    và có chứa flag là `FLAGSwzgxBJSAMqwxxAUm`.

    Nhưng cấu trúc flag của trang `ksnctf` là `FLAG_xxxxxxx`. Nên ta chơi ảo thuật một chút, chuyển `FLAGSwzgxBJSAMqwxxAUm` về thành `FLAG_SwzgxBJSAMqwxxAUm`, và ok submit thành công!

    => Nhưng có điều là sau khi làm xong thì search nghịch google thì mới biết nó là rot :D , và cụ thể hơn là rot-13 cho problem này.

## Bài 4: Onion

Problem: `https://ksnctf.sweetduet.info/problem/5`

Vào bài được cho một chuỗi dài ngoằng

```txt
Vm0wd2QyUXlVWGxWV0d4V1YwZDRWMVl3WkRSV01WbDNXa1JTV0ZKdGVGWlZNakExVmpBeFYySkVU
bGhoTWsweFZtcEdZV015U2tWVQpiR2....................
```

Nhìn có vẻ giống base64 nhưng sao dài thế này. Quyết định là lên trang decode base64 online test thử.
Thì thấy vẫn decode được, nhưng vẫn là chuỗi loằng ngoằng. Bây giờ thì nghĩ đến trường hợp là nó có thể encode nhiều lần thì sao.
Làm một chương trình nho nhỏ check xem sao.
**Ý tưởng**: cho chạy liên tục đến khi không decode được nữa thì thôi.

```py
import base64

str_s = """Vm0wd2QyUXlVWGxWV0d4V1YwZDRWMVl3WkRSV01WbDNXa1JTV0ZKdGVGWlZNakExVmpBeFYySkVU
bGhoTWsweFZtcEdZV015U2tWVQpiR2hvVFZWd1ZWWnRjRWRUTWxKSVZtdFdVZ3BpVlZwWVZtMTRj
MDB4V25GUmJVWlVUV3hLU1ZadGRHdFhRWEJwVW01Q1VGZFhNSGhpCk1WWlhWMjVHVW1KVldtRldh
a0Y0VGxaVmVXUkdaRmRWV0VKd1ZXcEtiMlJzV2tkWGJHUnJDazFXY0ZoV01qVlRZV3hLV0ZWdFJs
ZGgKYTFwTVZURmFZV1JIVWtkYVJscGhUVEJLZDFadGVHRmtNV1JYVjI1U1RsWkdTbkZEYXpGRlVX
cFNWMDFxVmxSWlYzaExWMFpXYzFacwpWbGNLVFRKb1RWWlVSbUZaVjFKSVZXdHNWV0pYYUZkV01G
WkxWbFprV0dWSGRHbE5iRXA2VmpKMGExbFdUa2xSYmtwRVlYcEdlbFl5CmRHOVdNREZ4Vm14U1Yx
SXphR2hWYWtaUFl6RmFjd3BXYkdOTFZGUkJNRTFHV2toa1IwWm9UV3MxTUZWdGRHdFpWa2w1WVVa
T1YwMUcKV2t4V2JGcHJWMGRTU0U5V1NrNVdiSEJKVmpKMFlXSXhVbk5VYTJob1UwVktSVmxZY0Vk
WFJsbDVDbVZIT1ZkTlJFWjRWbTE0VTFZeApTWHBoUjJoV1lXdGFVRmw2Um1GamQzQlhZa2RPVEZa
R1VrdGlNVkpYVjJ4V1UySlZXbUZXYWtaTFUxWmFXR1JIT1doTlZXdzFXVlZhCmExWXdNVWNLVjJ0
NFYySkdjR2hWYWtaaFpFWktkR1JGTlZkTlZYQmFWbTF3U2sxV1ZYbFNiazVVWWtkNFYxbHRkRXRT
Vm14WlkwVmsKV0ZKc1ZqVkRiVlpJVDFab1UwMUdXVEJYVkVKdldWWmtjd3BYYTFwWVlUTlNhRlZy
Vm1GamJIQkdWMnQwYW1RelFtaFZha3ByVkVaawpWMVZyVGxkTlJGWklWMnRvVDFkSFNsWlhiR1JW
VmpOT05GUnJXbXRqYlVaSFZHMW9UbFpZUVhoV1ZtUTBDbUV4V1hkTlZXTkxWakowCk5GWXlTa2Rq
U0VwWFRVZFNXRlV3V2t0ak1WWnlUbFprVGxaWVFtRldiVEYzVXpBeFNGSllhRmhpYkVwVVZqQmtV
MVZHV25SbFIwWlQKVm0xNFdsa3dWbXNLVjBaS2RHUkVUa1JpUjFJd1ZERmFiMVV3TVVkWFZFSllW
a1ZLZGxWNlJscGxVWEJUWW10d2NWVnNhRzlXTVd4WQpaRWhrVmxKc1ZqUldNbmhQWVcxUmVsRnNi
RnBpUjFGM1ZrVmFZUXBrUjFKSFdrWndWMkpJUWxsV2FrbzBWakZWZVZOc1dsaGlWVnBZCldWZDBZ
VlJHVlhoWGJVWllVakZLU1ZReFpHOVViRnBZWkhwR1dGWnNXbkpEYlVsNFYyeGtXR0V4YkV4V1ZF
b3dDazVHV1hsVGEyUnEKVTBWd1dGUlZaRk5YUmxWM1YydDBhazFXV25sVWJGcHJWR3hhV1ZGdFJs
ZGlXRUpNVkZWa1NtVkdWbGxoUjJ4VFlsWktWbGRXVWtkawpNVnBYWWtoT1YySlZXbFFLVm0weE5H
VldXWGxPVjNOTFZtcEtTMUl4WkhGUmExSm9aV3hhWVZZeWRHRmhNVkp6VTJ0YVdHRnNTbGhaCmJG
SkdUVVpXVlZKc2NHdGtNMEpQVm14a2IxWXhiRlZVYlRsWVVtMTRlZ3BaVldNMVlXMUtTVkZyYUZk
TmJrMHhXVmN4VW1Wc1JuVlMKYkZwb1lUSTVNMVpyVm1GWlVYQllVbFJHUmxWdGVFdFViVVY1Wkhw
Q1YyRnJhM2hXVkVwSFl6Rk9jMkZHV21sU01VcG9DbGRYZEdGawpNa1pIVmxoa1dHSklRbk5XYkZK
WFYwWmtjbGR0ZEZkTlJFWktWVmQ0ZDFkR1duTlhiV2hFWWtaR05GWXhhR3RVYkZwWVZHdDRWMkZy
CmIzZERhelZIVjFoc1ZHRXlVbkVLVlRCV2QxZEdVbFphUms1WFVteFdNMVl5ZERCaE1VbDRVMnRr
VldKR2NISldSM2hoVjFaR2RGSnMKWkdsWFJVcE5Wa1pXWVdNeFpFZFViR3hwVW1zMVdWVnFTbTlX
YkZweFVXMTBWZ3BOVjFKWVdXdG9VMkV4VGtoVmJGRkxWbTB3ZUU1RwpaSE5oTTJSWFlsaE9URlpx
UW1GVE1sSklWV3RXVldFeFNuQlZha1pLWkRGYVJWSnRSbWhOVmtwNlZUSjBZVmRIUm5OVGJHaGFD
bUpHClNrZFVWVnBYVmxaS2RHUkdUbXROTUVwYVYxY3hlazFYVGxkV2JrNW9VbnBzV0ZSV1pEUmxa
M0JhVmxkTk1WWnRlRXRrVmtaeVlVWmsKVG1Kc1JqTlhWbU40VlcxV2MxSnVUbWdLVW01Q2IxUlhl
RXRWVmxweVZtMUdhR1F6UWxsVmFrWkxVMVpSZUZkcmRHaFdiSEI2V1RCUwpZVll5Um5KaE0yaFdZ
V3RhV0ZwRldrOWpNV1J6WVVkc1UwMXRhRzlEYkdSWVpFZEdhd3BOYTFwSVZqSTFSMVV5U2taT1dF
WlZWbTFTClZGUlZXbGRrUjFaSVVteGFUbUV6UWt0V1ZscHZZVEZrUjFkdVRsaGlWMmhGV1d0YVIw
NUdXWGhoUjNSVllrWndXVlpIZERSV01rWnkKQ21JelpFUmhlbFpJV1d0YWExWkhSWGhqUm10TFYx
ZDRhMkl4WkVkVmJGcGhVbXMxVjFWdGVHRk5SbXQ2WTBaa1dGSnJiRE5aTUZacgpWbGRLUjJOSVNs
ZFNNMmhvVmpGYVIyTnRVa2NLV2tkc1YxSldiRFpXYkdoM1VXMVdSMVJyWkZSaVIzaHZWV3BDWVZa
R1duRlRiVGxYCllrZFNXVnBGWkRCVWQzQlRZa2QzTUZkWGRHOVZNa1owVm01S1dHSkdSa3hXYlRC
M1pVVTFTQXBXYms1WVlteEtVRlpxVGs5VVJscHgKVVcxR1ZFMXJNVFZWTW5SWFZqSkZlRk51UWxk
aVdGSXpWVEo0WVZKV1NuUlNiV2hPVm10d05sWlVTakJaVm1SSFdrVm9hRkp0YUdGRApiVVY1Q2xW
ck9XRldWbkJ5Vm1wR2EyUkhVa2hqUjNST1RVVndZVll4V2xOU01sRjRXa1prYVZKc1dsWlphMVV4
WWpGV2RHVkhSbXhWCldFSllXV3hTUjFOR2JGaE5WWFJVVWpGSk1sVXllR0VLWVZaa1NHRkliRmhX
YlU0MFZsY3hWMk14U25WVWJXZExWVzAxUTJJeFVsaGwKUlhSV1ZteHdlVlp0TVVkaFIxRjZVV3hz
Vm1GcldreFZNVnBYWkVkV1NHUkdWbWxTV0VKSlZtcEtNQXBqTVZsNVVtNUthV1ZyU21GWgpWM1Iz
VTBac05sSnJPV3BOYTFwSVZqSXhjMVV3TVZaalJtaEVZa1p3TUZrd1ZUVldVWEJPVWtaYVNWWnNZ
ekZUTVdSSVUydHNVbUpyCk5WaFphMXBMQ2xkR1duRlNiRXBzVW0xU01GcEZXbXRVYkVwR1YydDBW
MVp0VVhkYVJFWmFaVlpPY21GR1dsZFNWWEJHVjFkNFYxWXcKTlVkWFdHaG9Vak5TVmxsclduZFhW
bHBJWkVSU1YwMXJXbmtLUTIxSmVscEZVbWhsYkZwSlZtcEdiMkV4VW5OYVJXUllZbFJvVEZacwpa
SGRUTWtsNFdrVmtWbUpHY0ZsWmEyUlRWVVpXZEdWSVpHeGlSbXcxV2tWa01HRkZNVlppUkZKV1RX
NVNjZ3BXYkdSTFVqSk9TVk5zCmNGZGlTRUpSVmxjeE5GUXlUblJWYTJOTFYydGtjMWRHU2xaalJU
VlhZVEZ3V0ZsVVJrOWtSbHB5V2taa2FWSXphSFpXVjNCRFdWWmEKVjFadVRtaFNWVFZYQ2xWdGVI
ZFdiRlpZVFZSQ1ZXUXpRbFJaYTJRelRVWmtXR1JIT1ZSTlZtdzFWV3hvZDFadFNrZFNhM2hYWWxS
QwpNMXBWVlRGVFFYQlhZa2RTV1ZsdGVFdFZSbHB6VlcwNVZWSnNjSGtLVmxkMGExWkZNWEpOVkZK
WVlUSm9TRlpYTVVabFJrNTFVV3hrCmFWSnJjRmxXVkVaaFdWZE9jMk5GVmxaaVYyaFBWbTEwZDA1
c1duRlRhbEpwVFZaYVNGWkhkRzlpUmtwMFlVZEdSQXBpVlhCSVEyeE8KY2xwR1ZsZFdia0paVm0x
NFlWTXlUWGxVYTJoc1VteHdXVlZzVm5kV01WbDRXa1JDV2xadGVGaFdNblJyWVZaS2MxZHNXbHBp
UmtwNgpWakZhVjJSSFZrWmtSbWhTQ2xkRlNsbFdSbVIzVmpKT2MxZHVTbGhoTTFKeVZXcEdTazFz
VlhsbFIwVkxXVlphYTFJeFRuVmlSbWhYCllsVTBNRlpzWTNoV01rMTRVMjVXVm1KWFpFeFdWekUw
WkRKSmVHSkdWbFFLVmtaYVQxUldXbmRsVmxwMFRWVmtXR0pHV2xwVlYzaHoKVm0xS1IxTnJhRmRp
V0doWVZqQlZlRlpXUm5OV2JXeFRZbXRHTkZac1dtdE9RWEJxVFZac05WVnROVXRoVlRCNVZXMUdW
d3BoTVZwbwpXVlZhZDFKc1pISmtSbWhYVFVoQ1NWWnFTWGhqTWtaR1RWWnNVbUpIYUVWWmExcDNU
VVpTVm1GSE9WZGFNMEpQVm0wMVExTldXbkZTCmJUbHBUVmRTU1ZVeWVHRlhSMHBIQ2xkc1pGcFdN
MUpvUTJ4U1IxWllhRmhpUjFKeVZXcEdZVk5XVm5SbFIwWlZZbFZXTmxWWGREQlcKTVZwMFZXcE9X
RlpzY0dGYVZscExaRlpPZEdGRk5VNWlWMmhIVmpGa01GWnRWa1lLVGxWa1dGZEhlSE5WYWs1VFYx
WldjVkZzWkU5UwpiWGg1Vm0xd1UxWXdNVmRqUldOTFVUSXhTbVZzY0VaVmJXaHNZa1p3U2xadGNF
ZGlNazE0Vmxob1lWSlhhRzlWTUZaWFZFWmFjd3BhClNHUlVUV3RzTkZZeGFHOWhWa3AwWVVoS1Zt
RnJTbWhaTVZwelkyeHdSVlJyTldsU2JHOTNWa2Q0YTAxR1dYaFRia3BwVWtaS1YxUlgKTlZOaloz
QlhZa2RTVEZWcVNrOVRWazV6Q2xwRk5WTmlhMHBPVm0wd2QyVkdVWGhUYmxKV1lUSk9URll5ZEd0
ak1WbDRVMnhrYVZKRwpjRmhaYTFwTFZFWndXRTFXWkZOTlYxSmFXVlZhYjJGV1NYcGhTR1JYVm5w
Rk1GVjZTa29LWlVaV2MyRkhlRk5YUmtwWlEyeHNjbHBHClRsaFdia0pIVjJ0U1EyRkdWbGxSYXps
WFlsUkZlbFJWV210WFIxSklUMVphVG1FeFdUQldhMlF3WWpGYWRGTnJaRk5oTTJoWVdXeFMKUXdw
Tk1YQldWbFJHVkZGWVFsaFpiWE14VjFac2RHVkZkRlpTYkhCNFZrZHpOVlpXU25OalJFRkxWMnRX
YTFJeFpITlhXR1JPVmtaSwpWMVJYY0ZkVFJscDBUVlZhYkZKck5URlZWM2hoQ21GV1pFaGFNM0JY
VWpOb2FGZFdXa3RXTVU1MVZXeE9hVll5YUZCV2JURXdaREExCmMxZHVSbFJoYkVwd1ZGWmFZVk5H
V2toa1J6bHBVbXR3TUZsVlpFZFNRWEJwVmxoQ1NWRXllRThLWTJ4d1IxWnNaRmRpYTBwMlZtMHgK
TkZsV1RYbFVXR3hWWVRKb2MxVnRlSGRYVmxaelZtNWtWMkpHYkRSWFZFNXZWR3hKZUZKcVZsZFNN
Mmh5Vm1wS1MyTnJOVmhQVmxwcApZbXRLTmdwV01WcGhXVmRTUms1V1dsVmlSMmhYUTJ4a1JsTnRP
VmRXTTJoeVZsUkdUMUl5U2tkaFJUVlhWMFpLVmxadE1UQlpWMVpYCldraEtXR0pVYUV4WFZsWlda
VVpaZVZScmJHbFNiVkp3Q2xWdGRIZFVWbHB6V1ROb1YwMXJNVFJWTWpWWFZsZEtXR1JGZUZkV2Vr
RjQKVlZSS1NtVkdWbk5oUjNkTFZXeG9VMVl4V25SbFNHUnNWbXh3TUZSV1ZtdGhSa2w0VW1wYVZs
WXphSG9LVm0weFIyTnNaSFJoUmxwTwpVbTVDYUZkc1dsWmxSbHBYVW01T1YySlhlRmhXTUZaTFUx
WmFkR05GWkZaa00wSlRWRlphYzA1V1ZuUk9WWFJvVmxSQ05WWlhlRzlYClozQlhUVEZLYndwV2JY
QkhaREZaZUZwSVNsQldNMEp3Vm14YWQxTldXbkZUV0docVRWWldOVlV5TlV0V1IwcElZVVZXV21F
eGNETlUKVlZweVpERmFWVlpzWkdGTk1FcFFWbGQwVjFOck1VZGFSbFpTQ21KVlduQlVWM1IzVTBa
VmVVNVdUbGRpVlhCSlEyMVdSMXBHY0ZkTgpNVXB2VVRJeFIxSXhXbGxhUm1ocFYwWktlRmRYZEd0
Vk1sWnpXa2hLWVZKNmJGaFVWM1JYVG14V1dFMVZaRmNLVFZad01GWkhjRk5XCmJVWnlWMjFHWVZa
c2NFeFdNV1JMVWpGa2MyRkdUazVXV0VKSVZtcEdZV0l5VVhoWFdHZExWa2QwYTFZeFpFaGxTRXBX
WVdzMVZGbHEKUm5OamJGcDFXa1pTVXdwaVdHZzFWbTB4ZDFVeFdYZE5WbHBxVTBjNVRGVlVTalJo
TWsxNFZtNUtWbUpYZUZoV2ExWldaREZhYzFWcgpkRTVTTUZZMVZXMDFUMVpIUlhsVmJrWldZa1pL
ZGxaRldtRmpkM0JoQ2xKRlNtOVVWVkpYVTBaVmVXVkhkRnBXYXpWSVZqSTFRMVpXCldrWmpSbEpY
Vm14d2FGbDZSbUZXVmtwMFpFWmthVkp1UWtwV2JYaGhZakpGZUZkcmFGWlhSM2hSVld0a05GSlda
SFVLWWpOa1VGVlkKUWtWWGJtOTNUMVZPYmxCVU1Fc0sK"""

# decode = base64.b64decode(str_s)

while True:
    try:
        str_s = base64.b64decode(str_s).decode()
        # print(decode)
    except:
        break

print(str_s)
```

Sau khi chạy một lúc thì thấy ra được kết quả như thế này.

```txt
begin 666 <data>
51DQ!1U]&94QG4#-3:4%797I74$AU
 
end
```

Ủa vậy `begin 666 ` là gì? Lên google search thôi.
Hóa ra là `UUencode`. Tìm trang nào online decode thử thì có ngay flag `FLAG_FeLgP3SiAWezWPHu`

=> Vậy flag là `FLAG_FeLgP3SiAWezWPHu`.

## Bài 5: Source: `Mates CTF 2019`

Problem: Giải mã chuỗi sau: `NVQXIZLTMN2GM63XGNWGGMDNGNPXI327ORUDGX3GGFXDI3C7OIYHK3TEPU`

Nhìn chuỗi mã hóa chỉ gồm số và chữ cái in hoa. ok, mạnh dạn đoán base32.

Tìm trang online decode base32 được flag: `matesctf{w3lc0m3_to_th3_f1n4l_r0und}`

Easy!

=> Vậy flag là 'matesctf{w3lc0m3_to_th3_f1n4l_r0und}'
