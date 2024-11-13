from datetime import datetime, timedelta
from flask import Flask, request, render_template, current_app, Blueprint, jsonify, redirect, url_for, make_response
import hashlib
import jwt

auth_ = Blueprint('auth', __name__)


@auth_.route('/sign_in')
def sign_in():
    return render_template('auth/login.html')

@auth_.route("/sign_in/check", methods=["POST"])
def sign_in_check():
    email = request.form["email"]
    password = request.form["password"]
    pw_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    SECRET_KEY = current_app.config['SECRET_KEY']
    result = current_app.db.users.find_one(
        {
            "email": email,
            "password": pw_hash,
        }
    )
    if result:
        payload = {
            "id": email,
            "exp": datetime.utcnow() + timedelta(hours=8)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return jsonify(
            {
                "result": "success",
                "token": token,
            }
        )
    else:
        return jsonify(
            {
                "result": "fail",
                "msg": "Wrong email or password!",
            }
        )

@auth_.route('/sign_up')
def sign_up():
    myToken = request.cookies.get("mytoken")
    SECRET_KEY = current_app.config['SECRET_KEY']
    try:
        payload = jwt.decode(myToken, SECRET_KEY, algorithms=["HS256"])
        user_info = current_app.db.users.find_one({"email": payload["id"]})
        return render_template('auth/register.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("auth.sign_in", msg="Login time has expired!"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("auth.sign_in", msg="Please login first!"))
    

@auth_.route("/sign_up/save", methods=["POST"])
def sign_up_save():
    
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    doc = {      
        "username": username,    
        "email": email,                
        "password": password_hash,                                  
        "profile" : "",                                       
        "profilePict": "assets/images/profile/profile.jpeg"                                        
    }
    exists = bool(current_app.db.users.find_one({"email": email}))
    if exists == False:
        current_app.db.users.insert_one(doc)
        
    return jsonify({'exists': exists})

@auth_.route("/logout", methods=["DELETE"])
def logout():
    try:
        response = {"message": "Token successfully deleted"}
        resp = make_response(jsonify(response))
        resp.set_cookie("mytoken", "", expires=0, path="/")
        return resp
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        response = {"message": "Invalid token"}
        return jsonify(response), 401