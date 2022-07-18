import socket as sk
import time

sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

server_address = ('localhost', 10000)
print("Starting connection on ", server_address)
sock.bind(server_address)

while True:
    print("\nWaiting for a client\n")
    
    data, address = sock.recvfrom(4096)
    
    if data:
        data1 = "CONNECTION ESTABLISHED"
        time.sleep(1)
        sent = sock.sendto(data1.encode(), address)
        print("Successfully connected to client ", address)