s = "PyvragFvqrYbtvafNerRnfl@syner-ba.pbz"

arr = []

for c in s:
    arr.append(ord(c))

flag = ''
for i in arr:
    if (i - 13) < 122:
        flag += chr(i - 13)
    else:
        print("-------")

print(flag)