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

@treatment_recommendation_.route('/get_treatment_recommendation_data_hourly/<bed_id>', methods=['GET'])
def get_treatment_recommendation_data_hourly(bed_id):
    # Baca file CSV dengan separator '|'
    df = pd.read_csv('app/./data/hourly_data.csv', sep='|', header=None)

    # Tambahkan nama kolom agar lebih mudah diakses
    df.columns = ['icustay_id', 'itemid', 'charttime', 'Parameter', 'Value']

    # Inisialisasi variabel sebagai list kosong untuk menghindari error jika kondisi tidak terpenuhi
    heart_rate = []
    systolic = []
    diastolic = []
    mean = []
    respiratory_rate = []
    gcs = []
    sp = []

    # Pastikan `bed_id` sesuai tipe data, misalnya sebagai string
    if float(bed_id) == 11.0:
        # Filter `icustay_id` untuk nilai spesifik
        icustay_data = df[df['icustay_id'] == '200011']
        if not icustay_data.empty:
            # Ambil data berdasarkan parameter yang diperlukan
            heart_rate = icustay_data[icustay_data['Parameter'] == 'Heart Rate'].to_dict(orient='records')
            systolic = icustay_data[icustay_data['Parameter'] == 'Systolic Blood Preassure Non Invasive'].to_dict(orient='records')
            diastolic = icustay_data[icustay_data['Parameter'] == 'Diastolic Blood Preassure Non Invasive'].to_dict(orient='records')
            mean = icustay_data[icustay_data['Parameter'] == 'Mean Blood Preassure Non Invasive'].to_dict(orient='records')
            respiratory_rate = icustay_data[icustay_data['Parameter'] == 'Respiratory Rate'].to_dict(orient='records')
            gcs = icustay_data[icustay_data['Parameter'] == 'GCS Verbal Response'].to_dict(orient='records')
            sp = icustay_data[icustay_data['Parameter'] == 'SpO2'].to_dict(orient='records')

    # Buat dictionary dengan data yang sudah difilter
    data = {
        "heart_rate": heart_rate,
        "systolic": systolic,
        "diastolic": diastolic,
        "mean": mean,
        "respiratory_rate": respiratory_rate,
        "gcs": gcs,
        "sp": sp
    }

    # Kembalikan data dalam format JSON
    return jsonify(data)