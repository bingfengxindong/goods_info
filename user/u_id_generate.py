from .models import *

def u_id():
    users = User.objects.filter().order_by("-pk")
    if len(users) == 0:
        uid = "u111111"
    else:
        before_uid = users[0].u_login_name
        uid = int(before_uid.strip("u")) + 1
        uid = "%s%s"%("u",uid)
    return uid