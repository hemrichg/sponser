from os import makedirs
from uuid import uuid4
from datetime import date

from config.students_conf import students


# students example:
# students = {
#     "jani": {
#         "class": "b12",
#         "pass": "asd1234",
#         "token": "token_for_jani"
#     },
#     "bela": {
#         "class": "a12",
#         "pass": "ddd222",
#         "token": "token_for_bela"
#     }
# }

today = date.today()

def log(cl, username, req, res):
    dir_path = f"logs/{cl}/{username}/"
    makedirs(dir_path, exist_ok = True)

    with open(dir_path + f"{today}_http.log", "a") as l:
        l.write("\n-- req:\n")
        l.write(req)
        l.write("\n\n-- res:\n")
        l.write(res)

def get_user_by_token(token):
    user_data = None

    for k, v in students.items():
        if v["token"] == token:
            user_data = [k, v["class"]]

    return user_data

def get_token_for_user(username, password):
    if username in students \
    and students[username]["pass"] == password:
        token = students[username]["token"]
        return token
    else:
        return None
    