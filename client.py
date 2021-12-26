from socket import *
import struct
import time

class client:

    def __init__(self, name):
        self.client_name = name
        self.client_port = 3000
        self.client_sol = ''
        self.broadcast_port = 13117
        self.packet_len = 7
        self.max_len = 1024
        self.server_ip = 0
        self.tcp_port = 0


    def begin_game(self):
        while True:
            try:
                self.get_TCP_socket()
                self.open_TCP()
            except:
                time.sleep(1)
                pass

    def get_TCP_socket(self):
        with socket(AF_INET, SOCK_DGRAM) as b_s:
            b_s.setsockopt(SOL_SOCKET, socket.SO_REUSEPORT, 1)
        while True:
            b_s.bind(('', self.broadcast_port))
            pkt, addr = b_s.recv(self.max_len)
            if len(pkt) == self.packet_len:
                with struct.unpack("IBH", pkt) as msg:
                    if int(msg[0]) == 0xabcddcba and int(msg[1]) == 0x2:
                        self.tcp_port = msg[2]
                        self.server_ip = addr[0]
                        return

    def open_TCP(self):
        while True:
            with socket(AF_INET, SOCK_STREAM) as c_s:
                conn_flag = False
                while not conn_flag:
                    with c_s.connect((self.server_ip, self.tcp_port)):
                        encoded_name = str.encode(self.client_name + "\n")
                        while True:
                            with c_s.send(encoded_name):
                                with c_s.recv(self.max_len) as msg_from_server:
                                    print(msg_from_server.decode()+"\n")
                                    while True:
                                        self.client_sol = self.getSol() #need to add getSol function
                                        encoded_sol = str.encode(self.client_sol)
                                        with c_s.send(encoded_sol):
                                            with c_s.recv(self.max_len) as server_response:
                                                print(server_response.decode()+"\n")

    def getSol(self):
        # to be continue
        return "100"

if __name__ == '__main__':
    name=input("Please enter name: ")
    c = client(name)
    c.begin_game()





class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
