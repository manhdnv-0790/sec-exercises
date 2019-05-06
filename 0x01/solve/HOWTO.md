# SOLVE

## Bài 2: Easy cipher

`problem: https://ksnctf.sweetduet.info/problem/2`

- Chúng ta nhận được một chuỗi:

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
