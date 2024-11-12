from flask import Flask, request, render_template, current_app, Blueprint, jsonify, redirect, url_for
import hashlib
import jwt

sofa_ = Blueprint('sofa', __name__)

@sofa_.route('/sofa/<bed_id>')
def summary(bed_id):
    myToken = request.cookies.get("mytoken")
    SECRET_KEY = current_app.config['SECRET_KEY']
    try:
        payload = jwt.decode(myToken, SECRET_KEY, algorithms=["HS256"])
        user_info = current_app.db.users.find_one({"email": payload["id"]})
        return render_template('dashboard/sofa.html', user_info=user_info, bed_id=bed_id, active_sofa="active", text_sofa="text-white", title="SOFA Score")
    except jwt.ExpiredSignatureError:
        return redirect(url_for("auth.sign_in", msg="Login time has expired!"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("auth.sign_in", msg="Please login first!"))
