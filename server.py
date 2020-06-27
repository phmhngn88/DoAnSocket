import socket 

SERVER = 'localhost'
PORT = 5050

ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

adminPass = 'uname=admin&psw=admin'

def createServer():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        serversocket.bind(ADDR)
        serversocket.listen(5)
        print(f'[LISTENING]: listening at {ADDR}..')
        while True:
            (conn, addr) = serversocket.accept()
            #print(f"[CONNECTION] connected to {addr}")
            rd = conn.recv(1024).decode(FORMAT)
            print(rd)
            pieces = rd.split('\n')
            #if len(pieces) >0:
            #    print(pieces[0])
            
            line = pieces[0].split(' ')
            mode = line[0]
            if mode == 'GET':
                filename = line[1].strip('/')
                fileExtension = filename.split('.')[-1];
                if filename == 'index.html' or filename == '':
                    #print(filename)
                    F = open('index.html', encoding="utf8").read()
                    #print(F)
                    data = "HTTP/1.1 200 OK\r\n"
                    data += "Content-Type: text/html; charset=utf-8\r\n"
                    data += "\r\n"
                    data += F
                elif fileExtension == 'ico':
                    data = "HTTP/1.1 404 Not Found\r\n"
                    data += "\r\n"
                else:
                    F = open(filename, encoding="utf8").read()
                    #print(F)
                    data = "HTTP/1.1 200 OK\r\n"
                    data += "Content-Type: text/html; charset=utf-8\r\n"
                    data += "\r\n"
                    data += F
            elif mode == 'POST':
                if (adminPass == pieces[-1]):
                    print('Login: Success')
                    data = "HTTP/1.1 302 Found\r\n"
                    data += "Location: /member.html\r\n"
                    data += "\r\n"
                else:
                    print('Login: Failed')
                    data = "HTTP/1.1 302 Found\r\n"
                    data += "Location: /404.html\r\n"
                    data += "\r\n"

            conn.sendall(data.encode())


            conn.shutdown(socket.SHUT_WR)
    except KeyboardInterrupt:
        print("\nShutting down...\n")
    except Exception as exc:
        print("Error\n")
        print(exc)

    serversocket.close()

print('Access http://localhost:5050')
createServer()
        
        