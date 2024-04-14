import socket

from config.target_conf import target_host


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

def split_response(response):
    parts = response.split("\r\n\r\n")
    rows = parts[0].split("\r\n")
    
    if len(parts) == 1:
        return {
            "r_line": "",
            "header": "",
            "body": parts[0]
        }

    return {
        "r_line": rows[0],
        "header": "\r\n".join(rows[1:]),
        "body": parts[1] if 1 < len(parts) < 3 else
                parts[1:]if 3 < len(parts) else ""
    }

def get_response_for(request):
    response = netcat(
        target_host["hostname"],
        target_host["port"], 
        request)
        
    return {**split_response(response), "raw": response}
