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