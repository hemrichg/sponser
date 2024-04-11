import socket

def netcat(hostname, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, int(port)))
    b_content = content.encode("utf-8")
    
    totalsent = 0
    while totalsent < len(b_content):
        sent = s.send(b_content[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent
    s.shutdown(socket.SHUT_WR)

    b_data = bytearray()
    while True:
        data = s.recv(4096)
        if not data:
            break
        b_data = b_data + data
    s.close()

    str_data = b_data.decode("utf-8")
    return str_data