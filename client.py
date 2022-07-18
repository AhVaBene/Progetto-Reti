import socket as sk
import time

sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

server_address = ('localhost', 10000)
data = "Connection"

try:
    print("Trying to connect to server ",server_address)
    time.sleep((1))
    sent = sock.sendto(data.encode(), server_address)
    
    data, server = sock.recvfrom(4096)
    print(data.decode('utf8'))
except Exception as info:
    print (info)
finally:
    print("Closing socket")
    sock.close()
