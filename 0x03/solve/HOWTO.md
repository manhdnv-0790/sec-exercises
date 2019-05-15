# Bài 1: Basic is secure?

Problem: `https://ksnctf.sweetduet.info/problem/8`

Vào bài chúng ta sẽ được cho một file `q8.pcap`. Tải về thôi.
Theo kinh nghiệm vọc vạch thì file .pcap là file của wireshark.
Tải wireshark lên, mở file ra và đọc.
Khi mở file.
![Alt text](images/http.png?raw=true "File có")
Vậy là có 2 giao thức đã được bắt gói tin ở đây: `TCP` và `HTTP`. Với một thằng từng code web thì mình vẫn thích nhìn `HTTP` trước, mà cụ thể là nhìn vào gói tin nào trả về 200 (ông nào code web cũng thích 200).
Vậy thì khi mở HTTP Stream follow của gói tin tin có trả về 200.
![Alt text](images/basic.png?raw=true "Basic authen")
Ơn trời, Sử dụng Basic Authentication lại còn không dùng `HTTPS` mà lại đi dùng `HTTP` thì xác định rồi. Để ý header của gói tin có dòng `Authentication: Basic cTg6RkxBR181dXg3eksyTktTSDhmU0dB`. Đoạn mã Authentication chắc là base64 rồi, decode nó ra thôi nào.
Sau khi decode ta thu được `q8:FLAG_5ux7zK2NKSH8fSGA`.
=>> Vậy Flag là `FLAG_5ux7zK2NKSH8fSGA` chứ còn gì nữa :3

Nhưng sau khi decode các kiểu ảo lòi ra, lượn lờ vài gói tin HTTP nữa mới phát hiện ra là mình ngủ, là quên đọc dòng chữ dưới phần nội dung của gói tin 200 là `The flag is q8's password.`. Thì để có được đoạn token authentication trên thì nó phải gửi xác thực chứ, nó phải gửi password lên và với việc không có HTTPS thì đọc đơn giản rồi. đó chính là gói tin:
![Alt text](images/password.png?raw=true "Basic authen")
Có header kèm theo Credentials là user và password là `q8:FLAG_5ux7zK2NKSH8fSGA`. Flag đây chứ đâu nữa :( 

=> Bài học rút ra, hãy cứ nhìn tổng quan qua một lượt mọi thứ khi động vào cái gì đó nếu không muốn `thân lừa ưa nặng`.

# Bài 2: Digest is secure!
Problem: `https://ksnctf.sweetduet.info/problem/9`

Lại là một file pcap nữa. Mở bằng wireshark lên và moi móc nó thôi nào.
![Alt text](images/q9_wireshark.png?raw=true "Basic authen")
Đây vẫn là bắt gói tin TCP và HTTP. Phân tích gói tin một lúc thì cũng nhận dạng được nó dùng Digest Authentication.
Bên trong có một gói tin có trả về `q9:secret:c627e19450db746b739f41b64097d449`. Và đường dẫn cần đọc là `http://ksnctf.sweetduet.info:10080/~q9/flag.html`. Mình sẽ dựa vào đó để code.

Đầu tiên khai báo các biến chứa giá trị mà đọc được từ pcap

```py
#URI cần đi tới
uri = "/~q9/flag.html"
#METHOD được sử dụng
method = "GET"
# Mã ha1 là chuỗi secret trong q9:secret:c627e19450db746b739f41b64097d449
ha1 = "c627e19450db746b739f41b64097d449"
# ha2 là chuỗi hash md5 tính được dựa vào methos và uri 
ha2 = hashlib.md5("{}:{}".format(method, uri).encode('utf-8')).hexdigest()
# mình tự định nghĩa
cnonce = "9691c24"
# Số lượng request gửi tới server 
nc = "00000001"
# một số thứ khác đọc được từ file pcap
realm = "secret"
qop = "auth"
algorithm = "MD5"
username ="q9"
```

Trước tiên phải đi tới URL cần vào để server trả về yêu cầu xác thực, mục đích lấy được nonce

```py
url = "http://ksnctf.sweetduet.info:10080/~q9/flag.html"
auth_header = requests.get(url).headers["WWW-Authenticate"]
auth_arr = auth_header.split(" ")
nonce = auth_arr[2][7:-2]
```

Dùng nonce lấy được kết hợp một số thông tin ở trên để tạo chuỗi reponse

```py
before_reponse = "{}:{}:{}:{}:{}:{}".format(ha1,nonce,nc,cnonce,qop, ha2)
response = hashlib.md5(before_reponse.encode("utf-8")).hexdigest()
# print(response)
```

Tạo lại headers có chuỗi reponse vừa tạo ở trên để đi tới trang `flag.html`. Đọc nội dung và in ra.

```py
headers  = {
    "Authorization":"Digest username=\"{}\", realm=\"{}\", nonce=\"{}\", uri=\"{}\", algorithm=\"{}\", response=\"{}\", qop={}, nc={}, cnonce=\"{}\"".format(username, realm, nonce, uri, algorithm, response, qop, nc, cnonce)
}

# print(headers)

results =  requests.get(url, headers=headers)

print(results.text)
```

Kết quả sau khi chạy sẽ là

```html
<!DOCTYPE html>
  <head>
    <meta charset="utf-8">
    <title>Q9</title>
  </head>
  <body>
    <p>FLAG_YBLyivV4WEvC4pp3</p>
  </body>
</html>
```

=>> Vậy ta có được flag là `FLAG_YBLyivV4WEvC4pp3`

source code: [Code](code_digest.py)