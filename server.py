import socket as sk
import time

sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

server_address = ('localhost', 10000)
print("Starting connection on ", server_address)
sock.bind(server_address)

welcome_message = '\r\nCONNECTION ESTABLISHED\r\n\r\nWelcome, please select a command\r\n\r\n1. list -> get all the files available in the server\r\n2. get _filename_ -> download _filename_ from the server\r\n3. put _filename_ -> upload a file to the server\r\n'
while True:
    print("\nWaiting for a client\n")
    
    data, address = sock.recvfrom(4096)
    
    if data:
        time.sleep(1)
        sent = sock.sendto(welcome_message.encode(), address)
        print("Successfully connected to client ", address)
        
        data, address = sock.recvfrom(4096)
        cmd = data.decode("utf8")
        if cmd == "1" or cmd == "2" or cmd == "3":
            print("Client ",address," chose command %s\n" % cmd)
        else:
            print("%s is an invalid command\n" % cmd)