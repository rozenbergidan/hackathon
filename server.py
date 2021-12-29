import threading
from threading import Thread
import time
from socket import *
import struct



class server:
    def __init__(self):
        self.dev = "eth1"
        self.test = "eth2"
        # self.host_ip = scapy.get_if_addr(self.dev)
        self.host_ip = "132.73.199.2"
        self.game_port = 2000
        self.broadcast_port = 13117
        self.question = {"2 + 2": 4,
                         "10 - 6*2 + 4": 2,
                         "10*100/100 + 1 - 7": 4
                         }
        self.buff = 1024
        self.thread_cnt = 0
        self.threads = []
        self.threads_name = {}
        self.winner = ""

    def send_broadcast_offers(self):
        try:
            s_s = socket(AF_INET, SOCK_DGRAM)
        except:
            print("error - could not create udp socket")
        s_s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s_s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        for i in range(10):
            print(f"server sending offers for {i + 1} sec")
            offer = struct.pack("Ibh", 0xabcddcba, 0x2, self.game_port)
            # print(f"server sending to port {self.broadcast_port}")
            s_s.sendto(offer, ('255.255.255.255', self.broadcast_port))
            time.sleep(1)

    def listen_to_clients(self):
        print(f"server started, listening on IP address {self.host_ip}")
        s_s = socket(AF_INET, SOCK_STREAM)
        s_s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s_s.bind((self.host_ip, self.game_port))
        s_s.listen(2)
        while True:
            try:
                c_s, address = s_s.accept()
                print("catch")
            except:
                print("error")
            else:
                print(f"Connected to client ip: {str(address[0])} in port: {str(address[1])}")
                a_thread = Thread(target=self.accept_client, args=(c_s, address))
                self.thread_cnt += 1
                # if self.thread_cnt <= 2: maybe not needed because of listen(2)
                print(f"Thread Number: {str(self.thread_cnt)}")
                self.threads.append(a_thread)
                a_thread.start()

    def accept_client(self, conn):
        msg = conn.recv(self.buff)
        self.threads_name[threading.get_ident()] = msg.decode()

        while len(self.threads_name) != 2:
            time.sleep(1)

        msg = f"Welcome to our game \n player 1: {self.threads_name.keys()[0]} \n player 1: {self.threads_name.keys()[1]} \n the question is: {self.question.keys()[0]}"
        try:
            conn.sendto(str.encode(msg))
        except:
            print("err")
        else:
            end_time = time.time() + 10
            while time.time() < end_time:
                try:
                    msg = conn.recv(self.buff)
                except:
                    print("err")
                else:
                    msg = msg.decode()
                    msg = int(msg)
                    if msg == self.question.values()[0]:
                        print(f"the server received {msg} from player {self.threads_name[threading.get_ident()]}")
                        if self.winner == "":
                            self.winner = self.threads_name[threading.get_ident()]
                        break
                    else:
                        if self.winner == "":
                            if self.threads_name[threading.get_ident()] == self.threads_name.values()[0]:
                                self.winner = self.threads_name[1]
                            else:
                                self.winner = self.threads_name[0]
                        break

            if self.winner != "":
                msg = f"the winner is {self.winner}"
            else:
                msg = f"no winner"
            msg = str.encode(msg)
            conn.sendto(msg)
            return

    def start(self):
        while True:
            try:
                offer_thread = threading.Thread(target=self.send_broadcast_offers,args=[])
                offer_thread.start()
                # accept_thread = threading.Thread(target=self.listen_to_clients, args=[])
                # accept_thread.start()
                self.listen_to_clients()
                offer_thread.join()
                # accept_thread.join()

                self.clear()
            except Exception as e:
                print(str(e))
                time.sleep(1)
                pass

    def clear(self):
        self.winner = ""
        self.threads_name = {}
        self.threads = []
        self.thread_cnt = 0


if __name__ == '__main__':
    s = server()
    s.start()
