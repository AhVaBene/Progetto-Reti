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
    
    command = input()
    cmd = command.split()[0]
    sent = sock.sendto(cmd.encode(), server_address)
    
    if cmd == "1" or cmd == "list":
        data, server = sock.recvfrom(4096)
        list = data.decode('utf8')
        if list == "":
            print("An error has occured")
        else:
            print(list)
        
    elif cmd == "get":
        filename = command.split()[1]
        print("to do")
        
    elif cmd == "put":
        filename = command.split()[1]
        print("to do")
        
    else:
        print("You chose an invalid command")


except Exception as info:
    print (info)
finally:
    print("Ending connection")
    sock.close()
