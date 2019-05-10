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
Đây vẫn là bắt gói tin TCP và HTTP.
