import threading
from select import select

# import scapy
import time
from socket import *
import struct


class server:

    def __init__(self):
        self.broadcast_port = 13117
        # self.server_ip = "132.73.199.2"
        # self.server_ip_test = scapy.get_if_addr("eth2")
        # self.server_ip_dev = scapy.get_if_addr("eth1")
        self.server_port = 2070
        self.buff = 1024
        self.questions = ["2+4 = ?"]
        self.answers = [6]
            # {"2 + 2": 4,
            #               "10 - 6*2 + 4": 2,
            #               "10*100/100 + 1 - 7": 4
            #               }
        self.connected = 0
        self.thread1_name = ""
        self.thread2_name = ""

    def run(self):
        while True:
            try:
                offer_thread = threading.Thread(target=self.send_offers, args=[])
                offer_thread.start()
                self.start_listen()
                self.clear()
                offer_thread.join()
            except Exception as e:
                print(str(e))

    def start_listen(self):
        print(f"Server started, listening on IP address ")

        conn1, addr1, conn2, addr2 = None, None, None, None
        server_sock = socket(AF_INET, SOCK_STREAM)
        server_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        server_sock.bind(('', self.server_port))

        server_sock.listen(2)
        connected = False
        while not connected:
            if self.connected == 0:
                conn1, addr1 = server_sock.accept()
                self.connected = self.connected + 1
                pass
            elif self.connected == 1:
                conn2, addr2 = server_sock.accept()
                self.connected = self.connected + 1
                connected = True

        name1 = conn1.recv(self.buff).decode()
        name2 = conn2.recv(self.buff).decode()

        time.sleep(10)
        msg = f"Welcome to our game  \nplayer 1: {name1} \nplayer 2: {name2} \nthe question is: {self.questions[0]}"
        msg = msg.encode()
        conn1.send(msg)
        conn2.send(msg)

        lst, _, _ = select([conn1, conn2], [], [], 10)

        if(len(lst)==0):
            msg=f"time out, draw! the solution is {self.answers[0]}"
        elif lst[0]==conn1:
            sol = conn1.recv(self.buff).decode()
            if sol == str(self.answers[0]):
                msg = f"the winner is {name1}"
            else:
                msg = f"the winner is {name2}"
        else:
            sol = conn2.recv(self.buff).decode()
            if sol == str(self.answers[0]):
                msg = f"the winner is {name2}"
            else:
                msg = f"the winner is {name1}"
        msg = msg.encode()
        conn1.send(msg)
        conn2.send(msg)


    def send_offers(self):
        broadcast_sock = socket(AF_INET, SOCK_DGRAM)
        broadcast_sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        broadcast_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)
        for i in range(10):
            if self.connected == 2:
                break
            else:
                offer = struct.pack("!IBH", 0xabcddcba, 0x2, self.server_port)
                broadcast_sock.sendto(offer, ("<broadcast>", self.broadcast_port))
                time.sleep(1)

    def playtime(self, conn, addr, number):
        name = conn.recv(self.buff).decode()

    def clear(self):
        self.connected = 0
        self.thread1_name = ""
        self.thread2_name = ""


if __name__ == '__main__':
    s = server()
    s.run()
