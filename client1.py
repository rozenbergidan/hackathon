from socket import *
import struct
import time
# import scapy


class Client:

    def __init__(self, name="Illuminati"):
        self.broadcast_port = 13117
        # self.client_ip = "132.73.199.2"
        # self.client_ip_test = scapy.get_if_addr("eth2")
        # self.client_ip_dev = scapy.get_if_addr("eth1")
        self.pack_len = 7
        self.server_port = 0
        self.server_ip = 0
        self.buff = 1024
        self.name = name

    def run(self):
        while True:
            try:
                print(f"Client started, listening for offer requests...")
                self.receive_game_port()
                self.create_tcp_sock()
                self.clear()
            except Exception as e:
                print(1)
                print(str(e))
                time.sleep(1)

    def receive_game_port(self):
        # creating new broadcast socket
        broadcast_sock = socket(AF_INET, SOCK_DGRAM)
        broadcast_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        try:
            # binding to broadcast to receive packets
            broadcast_sock.bind(('', self.broadcast_port))
        except Exception as e:
            print(2)
            print(str(e))
        # receive offer packet
        pkt, addr = broadcast_sock.recvfrom(self.buff)
        if len(pkt) == self.pack_len:
            try:
                print(f"client received a packet from ip: {str(addr[0])}")
                msg = struct.unpack("!IBH", pkt)
            except Exception as e:
                print(3)
                print(str(e))
            if int(msg[0]) == 0xabcddcba and int(msg[1]) == 0x2:
                print(f"client received a good offer")
                self.server_port = msg[2]
                self.server_ip = addr[0]
                print(f"server ip is: {self.server_ip}, server port is: {self.server_port}")
            else:
                print(f"client received a bad offer, keep listening")

    def create_tcp_sock(self):
        tcp_sock = socket(AF_INET, SOCK_STREAM)
        tcp_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        connected = False

        while not connected:
            try:
                tcp_sock.connect((self.server_ip, self.server_port))
                connected = True
            except Exception as e:
                print(4)
                print(str(e))

        self.send_massage_to_server(tcp_sock, self.name)
        self.receive_massage_from_server(tcp_sock)
        solution = input("please type your solution")
        self.send_massage_to_server(tcp_sock, solution)
        self.receive_massage_from_server(tcp_sock)

    def receive_massage_from_server(self, conn):
        massage = ""
        try:
            massage = conn.recv(self.buff).decode()
        except Exception as e:
            print(5)
            print(str(e))
        print(f"the server sent you: \n {massage}")

    def send_massage_to_server(self, conn, massage):
        massage = str.encode(massage)
        try:
            conn.sendto(massage, (self.server_ip, self.server_port))
        except Exception as e:
            print(6)
            print(str(e))

    def clear(self):
        self.server_port = 0
        self.server_ip = 0

if __name__ == '__main__':
    c = Client()
    c.run()