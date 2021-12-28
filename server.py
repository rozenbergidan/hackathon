import threading
import time
from socket import *
import struct
from _thread import *

class server:

    def __init__(self):
        self.host_ip = '127.0.0.1'
        self.game_port = 2070
        self.broadcast_port = 13117
        self.question = {"2 + 2": 4,
                         "10 - 6*2 + 4": 2,
                         "10*100/100 + 1 - 7": 4
                         }
        self.buff = 1024
        self.thread_cnt=0
        self.threads=[]
        self.threads_name = {}

    def send_broadcast_offers(self):
        try:
            s_s = socket(AF_INET, SOCK_DGRAM)
        except:
            print("error - could not create udp socket")
        else:
            with s_s:
                s_s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
                for i in range(10):
                    print(f"server sending offers for {i+1} sec")
                    offer = struct.pack("IBH", 0xabcddcba, 0x2, self.game_port)
                    s_s.sendto(offer, ('<broadcast>',self.broadcast_port))
                    time.sleep(1)
                print(f"server started, listening on IP address {self.host_ip}")

    def listen_to_clients(self):
        s_s = socket(AF_INET, SOCK_STREAM)
        s_s.setblocking(True)
        s_s.bind(('',self.game_port))
        s_s.listen(2)
        while True:
            try:
                c_s, address = s_s.accept()
            except:
                print("error")
            else:
                print(f"Connected to client ip: {str(address[0])} in port: {str(address[1])}")
                a_thread = threading.(self.accept_client, (c_s,))
                self.thread_cnt += 1
                # if self.thread_cnt <= 2: maybe not needed because of listen(2)
                print(f"Thread Number: {str(self.thread_cnt)}")
                self.threads.append(a_thread)
                a_thread.start()


    def accept_client(self, conn):
        msg = conn.recv(self.buff)
        self.threads_name[self] = msg.decode()

        while len(self.threads_name) != 2:
            time.sleep(1)
        conn.send()






