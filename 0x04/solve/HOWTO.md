# Bài 1

Problem: `nc 125.235.240.166 11223`

Ban đầu vào bài dùng netcat connect tới `nc 125.235.240.166 11223` thì nhận được đề bài tương tự vầy
![Alt text](images/netcat.png?raw=true "Netcat")

Đọc đề thì hiểu đại loại là có 2 chai nước và muốn đong làm sao cho ra lượng nước bằng với `z`. Cũng chưa biết thế nào, nên search thuật toán đong nước, hóa ra nó có thuật toán đó thật :v

Ý tưởng thuật toán thì cũng tuận thủ 3 luật cơ bản:
```txt
/********************************************************
 *   Luat 1: Neu VX day thi do VX di                    *
 *   Luat 2: Neu VY rong thi do day nuoc cho binh 2     *
 *   Luat 3: Neu VX khong day va VY khong rong thi      *
 *   trut nuoc tu VY sang VX cho den khi VX day         *
 *                                                      *
*********************************************************/
```
Thế này thì cũng không có gì phức tạp lắm, dựa trên 3 luật mà code thôi :D

```python
def dong_nuoc(Vx, Vy, Vz):
    results = ''
    x = 0
    y = 0
    while x != Vz and y != Vz:
        # print("dang dong x = {}, y = {}".format(x, y))
        if x == Vx:
            x = 0
            # print("1:e_", end="")
            results += "1:e_"
        
        if y == 0:
            y = Vy
            results += "2:f_"
            # print("2:f_", end="")

        if x != Vx and y > 0:
            sl_nc_trut_sang_x = min(Vx - x, y)
            x += sl_nc_trut_sang_x
            y -= sl_nc_trut_sang_x
            results += "2:o_"
            # print("2:o_", end="")
    return results[0: len(results) - 1] + "\n"
    # print("x={}, y={}".format(x, y))
```
Code xong lấy thông số trong đề bài điền vào chạy thử xem thuật toán code chính xác chưa, thì nhận được đề bài round 2. Tức là thuật toán đã ok. Đề round 2
```txt
Round 1
1: 63 
2: 153 
z: 108
```

Vậy là đề sẽ có chung 1 cấu trúc là dong 1 tên round, dòng 2 giá trị 1, dòng 3 giá trị 2, dòng 4 giá trị z.
Code thêm đoạn để lấy được từng giá trị

```py
data_round_n += s.recv(10240).decode()

arr_data_round_n = data_round_n.split("\n")
Vx = arr_data_round_n[arr_data_round_n.index("Round {}".format(_round)) + 1].split(": ")[1]
Vy = arr_data_round_n[arr_data_round_n.index("Round {}".format(_round)) + 2].split(": ")[1]
Vz = arr_data_round_n[arr_data_round_n.index("Round {}".format(_round)) + 3].split(": ")[1]
```

Đơn giản chỉ việc đẩy Vx, Vy, Vz vào cho hàm `dong_nuoc()` xử lý là ra kết quả thôi.

Đây là code đầy đủ:
```py
import socket, sys

def dong_nuoc(Vx, Vy, Vz):
    results = ''
    x = 0
    y = 0
    while x != Vz and y != Vz:
        # print("dang dong x = {}, y = {}".format(x, y))
        if x == Vx:
            x = 0
            # print("1:e_", end="")
            results += "1:e_"
        
        if y == 0:
            y = Vy
            results += "2:f_"
            # print("2:f_", end="")

        if x != Vx and y > 0:
            sl_nc_trut_sang_x = min(Vx - x, y)
            x += sl_nc_trut_sang_x
            y -= sl_nc_trut_sang_x
            results += "2:o_"
            # print("2:o_", end="")
    return results[0: len(results) - 1] + "\n"
    # print("x={}, y={}".format(x, y))

host = '125.235.240.166'
port = 11223

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

data_round_1 = s.recv(1024).decode()
data_round_1 += s.recv(1024).decode()
_round = 0

# # tach du dieu
arr_data_round_1 = data_round_1.split("\n")
Vx = arr_data_round_1[arr_data_round_1.index("Round {}".format(_round)) + 1].split(": ")[1]
Vy = arr_data_round_1[arr_data_round_1.index("Round {}".format(_round)) + 2].split(": ")[1]
Vz = arr_data_round_1[arr_data_round_1.index("Round {}".format(_round)) + 3].split(": ")[1]
# print("VX = {}, VY={}, VZ={}".format(int(Vx), int(Vy), int(Vz)))
msg = dong_nuoc(int(Vx), int(Vy), int(Vz))
# import pdb; pdb.set_trace()

# print(msg)
s.send(msg.encode())
while True:
    data_round_n = s.recv(10240).decode()
    data_round_n += s.recv(10240).decode()

    _round += 1
    if data_round_n.find("Round {}".format(_round)) == -1:
        print(data_round_n)
        break
    print("Đang chơi round {}".format(_round))
    
    arr_data_round_n = data_round_n.split("\n")
    Vx = arr_data_round_n[arr_data_round_n.index("Round {}".format(_round)) + 1].split(": ")[1]
    Vy = arr_data_round_n[arr_data_round_n.index("Round {}".format(_round)) + 2].split(": ")[1]
    Vz = arr_data_round_n[arr_data_round_n.index("Round {}".format(_round)) + 3].split(": ")[1]
    msg = dong_nuoc(int(Vx), int(Vy), int(Vz))
    s.send(msg.encode())

s.close()
```

Sau khi chạy hết chương trình chúng ta sẽ thu được kết quả là

```txt
Dang choi round 1
Dang choi round 2
Dang choi round 3
Dang choi round 4
1: 1677118 2: 1886090
Correct!
Congrats, here is your flag
matesctf{f1ll_d4t_b0ttl3!}
```

=> Vậy chắc chắn flag chính là: `matesctf{f1ll_d4t_b0ttl3!}`
