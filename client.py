from socket import *
import struct
import time


class client:

    def __init__(self, name):
        self.client_name = name
        # self.client_port = 3000
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
            except Exception as e:
                print(str(e))
                time.sleep(1)
                pass

    def get_TCP_socket(self):
        try:
            b_s = socket(AF_INET, SOCK_DGRAM)
        except:
            print(f"{bcolors.FAIL}error - could not listen to broadcast port: {str(self.broadcast_port)}{bcolors.ENDC}")
        else:
            with b_s:
                print(f"{bcolors.OKGREEN}client currently listening to port: {str(self.broadcast_port)}{bcolors.ENDC}")
                b_s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
                while True:
                    b_s.bind(('', self.broadcast_port))
                    pkt, address = b_s.recv(self.max_len)
                    if len(pkt) == self.packet_len:
                        try:
                            print(f"{bcolors.OKGREEN}client received a packet from ip: {str(address[0])}{bcolors.ENDC}")
                            msg = struct.unpack("Ibh", pkt)
                        except:
                            print(f"{bcolors.FAIL}error - could not unpack a server offer{bcolors.ENDC}")
                            time.sleep(1)
                        else:
                            if int(msg[0]) == 0xabcddcba and int(msg[1]) == 0x2:
                                print(f"{bcolors.OKGREEN}client received a good offer{bcolors.ENDC}")
                                self.tcp_port = msg[2]
                                self.server_ip = address[0]
                                return
                            print(f"{bcolors.OKGREEN}client received a bad offer, keep listening {bcolors.ENDC}")

    def open_TCP(self):
        while True:
            try:
                c_s = socket(AF_INET, SOCK_STREAM)
            except:
                print(
                    f"{bcolors.FAIL}error - could not creat tcp socket with server: {str(self.server_ip)} in port: {str(self.tcp_port)} {bcolors.ENDC}")
            else:
                with c_s:
                    conn_flag = False
                    while not conn_flag:
                        try:
                            c_s.connect((self.server_ip, self.tcp_port))
                        except:
                            print(
                                f"{bcolors.FAIL}error - could not connect socket with server: {str(self.server_ip)} in port: {str(self.tcp_port)}{bcolors.ENDC}")
                            # shutdown the connection for read \ write
                            c_s.shutdown(SHUT_RDWR)
                        else:
                            print(f"{bcolors.OKGREEN}client and server are connected via TCP socket{bcolors.ENDC}")
                            encoded_name = str.encode(self.client_name + "\n")
                            while True:
                                try:
                                    c_s.send(encoded_name)
                                except:
                                    print(
                                        f"{bcolors.FAIL}error - could not send client-name to server: {str(self.server_ip)} in port: {str(self.tcp_port)}{bcolors.ENDC}")
                                else:
                                    print(f"{bcolors.OKGREEN}client sent his name to the server{bcolors.ENDC}")
                                    try:
                                        question_from_server = c_s.recv(self.max_len)
                                    except:
                                        print(
                                            f"{bcolors.FAIL}error - could not receive question from server: {str(self.server_ip)} in port: {str(self.tcp_port)}{bcolors.ENDC}")
                                    else:
                                        print(
                                            f"{bcolors.OKCYAN} received question: {question_from_server.decode()}{bcolors.ENDC}")
                                        while True:
                                            self.client_sol = input(
                                                f"{bcolors.OKBLUE}please provide your answer - QUICK! {bcolors.ENDC}")
                                            encoded_sol = str.encode(self.client_sol)
                                            try:
                                                c_s.send(encoded_sol)
                                            except:
                                                print(
                                                    f"{bcolors.FAIL}error - could not send solution to server: {str(self.server_ip)} in port: {str(self.tcp_port)}{bcolors.ENDC}")
                                            else:
                                                print(
                                                    f"{bcolors.OKGREEN}client sent his solution to the server{bcolors.ENDC}")
                                                try:
                                                    server_response = c_s.recv(self.max_len)
                                                except:
                                                    print(
                                                        f"{bcolors.FAIL}error - could not receive the last message from the server: {str(self.server_ip)} in port: {str(self.tcp_port)}{bcolors.ENDC}")
                                                else:
                                                    print(
                                                        f"{bcolors.OKCYAN} received solution from the server: {server_response.decode()}{bcolors.ENDC}")
                                                    return


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


if __name__ == '__main__':
    name = input(f"{bcolors.OKBLUE}Please enter name: {bcolors.ENDC}")
    c = client(name)
    c.begin_game()
