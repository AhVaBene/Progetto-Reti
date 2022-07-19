import socket as sk
import time
import os

sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
storage_path = os.path.dirname(__file__) + os.path.sep + "storage" + os.path.sep

def getFiles():
    files = ""
    for file in os.scandir(storage_path):
        files += file.name + "\tsize: "+ str(os.path.getsize(storage_path + file.name)/1024) + " KB\n"
    return files

server_address = ('localhost', 10000)
print("Starting connection on ", server_address, "\n")
sock.bind(server_address)

welcome_message = '\r\nCONNECTION ESTABLISHED\r\n\r\nWelcome, please select a command\r\n\r\n1. list -> get all the files available in the server\r\n2. get _filename_ -> download _filename_ from the server\r\n3. put _filename_ -> upload a file to the server\r\n'
while True:
    print("\nWaiting for a client\n")
    
    data, address = sock.recvfrom(4096)
    
    if data:
        time.sleep(1)
        sock.sendto(welcome_message.encode(), address)
        print("Successfully connected to client ", address)
        
        data, address = sock.recvfrom(4096)
        cmd = data.decode("utf8")
        if cmd == "1" or cmd == "list":
            print("Client ", address," chose command 1-list\n")
            ans = getFiles()
            sock.sendto(ans.encode(), address)
            
        elif cmd == "get":
            data, address = sock.recvfrom(4096)
            filename = data.decode("utf8")
            print("Client ", address," chose command 2-get %s\n" % filename)
            if not os.path.exists(storage_path + filename):
                print("File not found\n")
                ans = "False"
                sock.sendto(ans.encode(), address)
            else:
                print("File found...sending")
                ans = "True"
                sock.sendto(ans.encode(), address)
                fin = open(storage_path + filename, 'rb')
                while True:
                    file = fin.read(2048)
                    if file == b'':
                        fin.close()
                        print("File sent\n")
                        ans = b'END'
                        sock.sendto(ans, address)
                        size = str(os.path.getsize(storage_path + filename)/1024)
                        sock.sendto(size.encode(), address)
                        break
                    else:
                        sock.sendto(file, address)
            
        elif cmd == "put":
            print("Client ", address," chose command 3-put\n")
            print("to do")
            
        else:
            print("Client ", address," chose an invalid command\n")
            
        
            