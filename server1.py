import threading

import scapy
import time
from socket import *
import struct


class server:

    def __init__(self):
        self.broadcast_port = 13117
        self.server_ip = "132.73.199.2"
        # self.server_ip_test = scapy.get_if_addr("eth2")
        # self.server_ip_dev = scapy.get_if_addr("eth1")
        self.server_port = 2070
        self.buff = 1024
        self.qeustions = {"2 + 2": 4,
                          "10 - 6*2 + 4": 2,
                          "10*100/100 + 1 - 7": 4
                          }
        self.connected = 0
        self.thread1_name = ""
        self.thread2_name = ""
        self.welcome_msg = msg = f"Welcome to our game \n player 1: {self.thread1_name} \n player 2: {self.thread2_name} \n the question is: {self.qeustions.keys()[0]}"

    def run(self):
        try:
            offer_thread = threading.Thread(target=self.send_offers, args=[])
            offer_thread.start()
            self.start_listen()
            self.clear()
        except Exception as e:
            print(str(e))

    def start_listen(self):
        print(f"Server started, listening on IP address {self.server_ip}")

        server_sock = socket(AF_INET, SOCK_DGRAM)
        server_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        server_sock.bind((self.server_ip, self.server_port))

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

        p1_thread = threading.Thread(target=self.playtime, args=[conn1, addr1, 1])
        p2_thread = threading.Thread(target=self.playtime, args=[conn2, addr2, 2])

        p1_thread.start()
        p2_thread.start()

        self.start_game()

        p1_thread.join()
        p2_thread.join()

    def send_offers(self):
        broadcast_sock = socket(AF_INET, SOCK_DGRAM)
        broadcast_sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        for i in range(10):
            if self.connected == 2:
                pass
            else:
                offer = (0xabcddcba).to_bytes(4, "little") + (0x2).to_bytes(1, "little") + (
                    self.server_port).to_bytes(2, "little")
                broadcast_sock.sendto(offer, ("255.255.255.255", self.server_port))
                time.sleep(1)

    def playtime(self, conn, addr, number):
        name = conn.recv(self.buff)
        name = name.decode()


if __name__ == '__main__':
    s = server()
    s.run()
