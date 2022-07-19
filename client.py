import socket as sk
import time
import os

sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
download_path = os.path.dirname(__file__) + os.path.sep + "client_storage" + os.path.sep
if not os.path.exists(download_path):
    os.mkdir(download_path)

server_address = ('localhost', 10000)
data = "Connection"

try:
    print("Trying to connect to server ",server_address)
    time.sleep((1))
    sock.sendto(data.encode(), server_address)
    
    data, server = sock.recvfrom(4096)
    print(data.decode('utf8'))
    
    command = input()
    cmd = command.split()[0]
    sock.sendto(cmd.encode(), server_address)
    
    if cmd == "1" or cmd == "list":
        data, server = sock.recvfrom(4096)
        list = data.decode('utf8')
        if list == "":
            print("An error has occured")
        else:
            print(list)
        
    elif cmd == "get":
        filename = command.split()[1]
        sock.sendto(filename.encode(), server_address)
        data, server = sock.recvfrom(4096)
        if data.decode("utf8") == "True":
            print("Starting download")
            file = open(download_path + filename, 'wb')
            while True:
                data, server = sock.recvfrom(2048)
                if data == b'END':
                    file.close()
                    print("File received")
                    data, server = sock.recvfrom(4096)
                    expected_size = data.decode('utf8')
                    actual_size = str(os.path.getsize(download_path + filename)/1024)
                    if expected_size == actual_size:
                        print("Download succesful\n")
                    else:
                        print("Download not succesful\n")
                    break
                else:
                    file.write(data)
        else:
            print("The file does not exist")
        
    elif cmd == "put":
        filename = command.split()[1]
        sock.sendto(filename.encode(), server_address)
        if not os.path.exists(download_path + filename):
            print("File not found\n")
            ans = "False"
            sock.sendto(ans.encode(), server_address)
        else:
            ans = "True"
            sock.sendto(ans.encode(), server_address)
            print("Starting upload")
            fin = open(download_path + filename, 'rb')
            while True:
                file = fin.read(2048)
                if file == b'':
                    fin.close()
                    print("File sent\n")
                    ans = b'END'
                    sock.sendto(ans, server_address)
                    size = str(os.path.getsize(download_path + filename)/1024)
                    sock.sendto(size.encode(), server_address)
                    break
                else:
                    sock.sendto(file, server_address)
        
    else:
        print("You have chosen an invalid command")

except Exception as info:
    print (info)
finally:
    print("Ending connection")
    sock.close()
