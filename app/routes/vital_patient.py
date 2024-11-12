from flask import Flask, request, render_template, current_app, Blueprint, jsonify, redirect, url_for
import pandas as pd
import jwt

vital_patient_ = Blueprint('vital_patient', __name__)

@vital_patient_.route('/vital_patient/<bed_id>')
def summary(bed_id):
    myToken = request.cookies.get("mytoken")
    SECRET_KEY = current_app.config['SECRET_KEY']
    try:
        payload = jwt.decode(myToken, SECRET_KEY, algorithms=["HS256"])
        user_info = current_app.db.users.find_one({"email": payload["id"]})
        return render_template('dashboard/vital-patient.html', user_info=user_info, bed_id=bed_id, active="active", text="text-white", title="Vital Patient")
    except jwt.ExpiredSignatureError:
        return redirect(url_for("auth.sign_in", msg="Login time has expired!"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("auth.sign_in", msg="Please login first!"))
    
@vital_patient_.route('/get_vital_data/<bed_id>', methods=['GET'])
def get_vital_data(bed_id):
    data = pd.read_csv('app/./data/df_with_readable_charttime.csv')
    filtered_data = data[data['icustayid'] == float(bed_id)]
    data_vital = filtered_data.to_dict(orient='records')
    return jsonify(data_vital)
