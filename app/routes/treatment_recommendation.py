from flask import Flask, request, render_template, current_app, Blueprint, jsonify, redirect, url_for
import pandas as pd
import jwt

treatment_recommendation_ = Blueprint('treatment_recommendation', __name__)

@treatment_recommendation_.route('/treatment_recommendation/<bed_id>')
def treatment_recommend(bed_id):
    
    myToken = request.cookies.get("mytoken")
    SECRET_KEY = current_app.config['SECRET_KEY']
    try:
        payload = jwt.decode(myToken, SECRET_KEY, algorithms=["HS256"])
        user_info = current_app.db.users.find_one({"email": payload["id"]})
        return render_template('dashboard/treatment-recommendation.html', user_info=user_info, bed_id=bed_id, active_treatment="active", text_treatment="text-white", title="Treatment Recommendation")
    except jwt.ExpiredSignatureError:
        return redirect(url_for("auth.sign_in", msg="Login time has expired!"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("auth.sign_in", msg="Please login first!"))
    
@treatment_recommendation_.route('/get_treatment_recommendation_data/<bed_id>', methods=['GET'])
def get_treatment_recommendation_data(bed_id):
    data = pd.read_csv('app/./data/df_with_readable_charttime.csv')
    filtered_data = data[data['icustayid'] == float(bed_id)]
    data_vital = filtered_data.to_dict(orient='records')
    return jsonify(data_vital)
