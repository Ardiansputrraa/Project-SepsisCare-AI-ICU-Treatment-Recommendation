from flask import Flask, request, render_template, current_app, Blueprint, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import jwt
import os

profile_ = Blueprint('profile', __name__)

@profile_.route('/profile')
def profile():
    myToken = request.cookies.get("mytoken")
    SECRET_KEY = current_app.config['SECRET_KEY']
    try:
        payload = jwt.decode(myToken, SECRET_KEY, algorithms=["HS256"])
        user_info = current_app.db.users.find_one({"email": payload["id"]})
        return render_template('profile/profile.html', user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("/"))
    
@profile_.route('/update_profile', methods=["POST"])
def update_profile():
    SECRET_KEY = current_app.config['SECRET_KEY']
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
        username = request.form["username"]
        email = payload["id"]
        newDoc = {"username": username}
        if "filePict" in request.files:
            file = request.files["filePict"]
            filename = secure_filename(file.filename)
            extension = filename.split(".")[-1]
            file_path = f"assets/images/profile/{email}.{extension}"
            file.save("app/./static/" + file_path)
            newDoc["profile"] = filename
            newDoc["profilePict"] = file_path
        current_app.db.users.update_one({"email": payload["id"]}, {"$set": newDoc})
        return jsonify({"msg": "Profile successfully updated!"})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("dashboard"))
    
    