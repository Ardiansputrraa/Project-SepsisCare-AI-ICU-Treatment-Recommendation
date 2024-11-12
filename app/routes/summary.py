from flask import Flask, request, render_template, current_app, Blueprint, jsonify, redirect, url_for
import json
import jwt

summary_ = Blueprint('summary', __name__)

@summary_.route('/summary/<stay_id>')
def summary(stay_id):
    myToken = request.cookies.get("mytoken")
    SECRET_KEY = current_app.config['SECRET_KEY']
    try:
        payload = jwt.decode(myToken, SECRET_KEY, algorithms=["HS256"])
        user_info = current_app.db.users.find_one({"email": payload["id"]})
        return render_template('dashboard/summary.html', user_info=user_info, stay_id=stay_id, title="Summary")
    except jwt.ExpiredSignatureError:
        return redirect(url_for("auth.sign_in", msg="Login time has expired!"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("auth.sign_in", msg="Please login first!"))
 
@summary_.route('/get_summary/<stay_id>', methods=["GET"])
def get_summary(stay_id):
    with open('app/./data/similarity.json') as f:
        data_summary = json.load(f) 
    return jsonify({"data_summary": data_summary, "stay_id":stay_id})