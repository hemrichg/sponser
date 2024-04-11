from datetime import datetime, timedelta
from flask import Flask, request, render_template, redirect, make_response

from config.target_conf import target_host
from utils.nc import netcat
from utils.other import log, get_user_by_token, get_token_for_user

# target_host example:
# target_host = {
#     "hostname": "localhost",
#     "port": "8080",
# }

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def root():
    token = request.cookies.get("token")
    
    if not token:
        return redirect("login")
    
    u_name, cl = get_user_by_token(token)
    # u_name, cl = "test", "class"

    if request.method == "POST":
        req = request.form["req"]
        res = netcat(target_host["hostname"], target_host["port"], req)

        log(cl, u_name, req, res)

        return render_template("http.html", data={**target_host,
                                                    "req": req,
                                                    "res": res,
                                                    "user": u_name,
                                                    "cl": cl})
    return render_template("http.html", data={**target_host,
                                                "req" : "",
                                                "res": "",
                                                "user": u_name,
                                                "cl": cl})

@app.route("/login", methods=["GET", "POST"])
def login():
    token = request.cookies.get("token")

    if get_user_by_token(token):
        return redirect("/")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username and password:
            token = get_token_for_user(username, password)
            if token:
                res = make_response(redirect("/"))
                res.set_cookie(
                    "token",
                    token,
                    expires=datetime.now() + timedelta(weeks=1))
                    
                return res

    return app.send_static_file("login.html")

if __name__ == "__main__":
    app.run(debug=True)