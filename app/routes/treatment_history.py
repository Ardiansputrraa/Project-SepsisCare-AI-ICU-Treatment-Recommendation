from flask import Flask, request, render_template, current_app, Blueprint, jsonify, redirect, url_for
import pandas as pd
import jwt

treatment_history_ = Blueprint('treatment_history', __name__)

@treatment_history_.route('/treatment_history')
def summary():
    myToken = request.cookies.get("mytoken")
    SECRET_KEY = current_app.config['SECRET_KEY']
    try:
        payload = jwt.decode(myToken, SECRET_KEY, algorithms=["HS256"])
        user_info = current_app.db.users.find_one({"email": payload["id"]})
        return render_template('dashboard/treatment-history.html', user_info=user_info, title="Treatment History")
    except jwt.ExpiredSignatureError:
        return redirect(url_for("auth.sign_in", msg="Login time has expired!"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("auth.sign_in", msg="Please login first!"))

@treatment_history_.route('/get_treatment_history', methods=['GET'])
def get_vital_data():
    data = pd.read_csv('app/./data/history_treatment.csv')
    data_history = data.to_dict(orient='records')
    return jsonify(data_history)