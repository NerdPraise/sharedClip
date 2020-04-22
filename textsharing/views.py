from django.shortcuts import render, redirect
from django.contrib import auth as ath
from django.contrib.auth.views import logout_then_login
from datetime import datetime, timezone
import pytz
import pyrebase
import time


config = {
    "apiKey": "AIzaSyDlAUF_7PmkLo7fO357IO-Y8n7CJVvZATw",
    "authDomain": "shared-clipboard-a312e.firebaseapp.com",
    "databaseURL": "https://shared-clipboard-a312e.firebaseio.com",
    "projectId": "shared-clipboard-a312e",
    "storageBucket": "shared-clipboard-a312e.appspot.com",
    "messagingSenderId": "151654450292",
    "appId": "1:151654450292:web:8007db457c2b17f8573d21",
    "measurementId": "G-QM9K6T6K8Y",
    
    }
firebase = pyrebase.initialize_app(config)
db = firebase.database()
auth = firebase.auth()

def get_uid(request):
    id_token = request.session["uid"]
    user_id = auth.get_account_info(id_token)
    uid = user_id["users"][0]["localId"]
    return (uid, id_token)


def index(request):
    if auth.current_user:
        try:
            user = auth.current_user
            uid, id_token = get_uid(request)
            path = db.child("users").child(uid)
            name = path.child("name").get(id_token).val()
            uuidstamps = db.child("users").child(uid).child("saved clips").shallow().get(id_token).val()
            if uuidstamps:
                list_uuid = list(uuidstamps)
                # obj = [path.child("users").child(uid).child("saved clips").child(uuid).shallow().get().val() for uuid in list_uuid]
                # for i in obj:
                #     print(i)

                """
                check if object can be stored in local storage, then compared if there is any new change 
                check if obj is stored and compare the obj
                """
                unix_time = []
                content = []
                for clip_id in list_uuid:
                    unix_time.append(db.child("users").child(uid).child("saved clips").child(clip_id).child("unix time").get(id_token).val())
                    content.append(db.child("users").child(uid).child("saved clips").child(clip_id).child("content").get(id_token).val())
                date = [datetime.fromtimestamp(time).strftime("%H:%M %d/%m") for time in unix_time]
                comb_list = list(zip(date, content)) 
                comb_list.sort(reverse=True, key=lambda comb: comb[0])
                
            else:
                comb_list = ""
            context = {"name": name, "profile": user, "content":comb_list}
            return render(request, "main/index.html", context)
        except (ConnectionAbortedError, ConnectionError):
            return redirect("/404.html")
    else:
        return render(request, "main/index.html")


def signIn(request):
    return render(request, "registration/signin.html")


def postsign(request):
    email = request.POST.get("email")
    password = request.POST.get("password")
    try:
        user = auth.sign_in_with_email_and_password(email, password)
    except (ConnectionAbortedError, ConnectionError):
        return redirect("/404.html")
    except:
        message = "invalid credentials" 
        return render(request, "registration/signin.html", {"message": message})
    session_id = user["idToken"]
    request.session["uid"] = str(session_id)
    return redirect("/")


def logout(request):
    auth.current_user = None
    try:
        del request.session["uid"]
    except KeyError:
        pass
    return redirect("/")
    # return logout_then_login(request)


def signup(request):
    if request.POST:       
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password==password2: 
            try:
                user = auth.create_user_with_email_and_password(email, password)
                uid = str(user["localId"])
                data = {"name": name, "email": email}
                db.child("users").child(uid).set(data, user["idToken"])
                
                """
                key error for uid, check today // INTEGRATE GOOGLE LOGIN
                """
                request.session["uid"] = str(user["idToken"])
                auth.sign_in_with_email_and_password(email, password)
                return redirect("/")
            except:
                error = "Something wrong went wrong. It couldn't go wronger"
                
        else:
            error = "Passwords are not alike"
        return render(request, "registration/signup.html", {"error": error})

    else:
        return render(request, "registration/signup.html")


def createClip(request):
    if request.POST and auth.current_user != None:
        import uuid
        
        tz = pytz.timezone("GMT")
        time_now = datetime.now(timezone.utc).astimezone(tz)
        UUID = str(uuid.uuid4())        
        millis = int(time.mktime(time_now.timetuple()))
        clip = request.POST.get("clip")
        uid, id_token = get_uid(request)
        try:
            data = {
                "title": clip,
                "content": clip,
                "unix time": millis,
            }
            path = db.child("users").child(uid)
            path.child("saved clips").child(UUID).set(data, id_token)
            return redirect("/")
        except KeyError:
            error = "Oops, you are not logged in"
            return render(request, "registration/signin.html", {"error":error})
    else:
        return render(request, "main/index.html", {})
