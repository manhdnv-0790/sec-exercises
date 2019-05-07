# Bài 2: Simple Auth
Problem: `http://ksnctf.sweetduet.info/problem/32`

Vào bài chúng ta sẽ thấy một đường dẫn `http://ctfq.sweetduet.info:10080/~q32/auth.php`
và một source code php

```php
<!DOCTYPE html>
<html>
  <head>
    <title>Simple Auth</title>
  </head>
  <body>
    <div>
<?php
$password = 'FLAG_????????????????';
if (isset($_POST['password']))
    if (strcasecmp($_POST['password'], $password) == 0)
        echo "Congratulations! The flag is $password";
    else
        echo "incorrect...";
?>
    </div>
    <form method="POST">
      <input type="password" name="password">
      <input type="submit">
    </form>
  </body>
</html>
```

Trước tiên là mình cứ và link kia và thấy nó hiển thị một form submit, thì mình cũng điền một cái gì đó vớ vẩn và submit xem sao thì tất nhiên là nhận được dòng chữ ` incorrect... ` rồi.

Đến đây mới bắt đầu nhìn vào source code mà bài cho. ok, nhìn đi nhìn lại thì source có vẻ viết khá là ok, php thì viết như thế này thôi.
Đọc logic nó chạy một tý, có vẻ như muốn có được flag thì password nhập vào phải khớp với password trên server. Chính là điểm cần khai thác rồi, cũng không chắc chắn lắm nhưng mình nghĩ là chính cái hàm so sánh ở câu lệnh  `strcasecmp($_POST['password'], $password) == 0` chính là điểm cần để ý ở đây.
Bắt đầu lên google search hàm  `strcasecmp` hoạt động như thế nào. à, thì ra `nó  sẽ so sánh hai chuỗi mà không phân biệt chữ hoa chữ thường, hàm trả về hiệu số giữa chiều dài chuỗi thứ nhất trừ đi chiều dài chuỗi thứ 2`. ok, hàm cũng bình thường mà. Đang tính bỏ cuộc thì search tìm thêm lần nữa để hiểu sâu hơn cách nó hoạt động thì bỗng nhận được 1 đoạn trích trong 1 bài viết về việc hàm này sẽ bị lỗi so sánh một string với một array.
Vậy thì dễ rồi, trong source dùng `$POST['password']` so sách với `$password - là flag chúng ta cần tìm` nếu đúng thì in ra flag.
`$password` chắc chắn là string rồi, vậy thì chỉ cần biến $POST['password'] thành mảng nữa là ok. Vậy thì vào lại trang submit, bấm f12 để show inspect code lên, sửa ô input từ `name='password'` thành  `name='password[]'` là được (kinh nghiệm code web cũng một năm mà :3).
Sửa xong rồi, điền đại một cái gì đó và submit thử. Và kết quả không mấy bất ngờ đó là `Congratulations! The flag is FLAG_VQcTWEK7zZYzvLhX `

=> Flag chính là `FLAG_VQcTWEK7zZYzvLhX`.