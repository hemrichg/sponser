import socket
from flask import Flask, request, render_template

config = {
    "hostname": "localhost",
    "port": "80",
}

app = Flask(__name__)

def netcat(hostname, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, int(port)))
    s.sendall(content.encode())
    s.shutdown(socket.SHUT_WR)

    r_data = ""
    while True:
        data = s.recv(4096)
        if not data:
            break
        r_data += repr(data.decode("utf-8"))
    s.close()

    r_data = r_data[1:][:-1]
    r_data = r_data.replace("\\r\\n", "\n").replace("\\t", "\t")
    return r_data

@app.route("/", methods=["GET", "POST"])
def root():
    if request.method == "POST":
        req = request.form["req"]
        res = netcat(config["hostname"], config["port"], req)
        return render_template("http.html", data={**config,
                                                    "req": req,
                                                    "res": res})
    return render_template("http.html", data={**config,
                                                "req" : "",
                                                "res": ""})

if __name__ == "__main__":
    app.run(debug=True)