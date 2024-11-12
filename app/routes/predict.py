from flask import Flask, jsonify, request, Blueprint
import numpy as np
import pickle
import pandas as pd
from pydantic import BaseModel, Field
from flask_cors import CORS

predict_ = Blueprint('predict', __name__)

# Load variabel yang disimpan
with open('app/./data/Qon.pkl', 'rb') as file:
    Qon = pickle.load(file)

with open('app/./data/C.pkl', 'rb') as file:
    C = pickle.load(file)

with open('app/./data/physpol.pkl', 'rb') as file:
    physpol = pickle.load(file)

# Physician optimal action untuk setiap state
phys_OptimalAction = np.argmax(physpol, axis=1).reshape(-1, 1)

# AI optimal action untuk setiap state
OptimalAction = np.argmax(Qon, axis=1).reshape(-1, 1)

@predict_.route("/predict", methods=["POST"])
def predict():
    try:
        # Dapatkan input JSON dari request
        input_data = request.json
        
        # Konversi input data menjadi DataFrame pandas
        user_input = pd.DataFrame([input_data])

        # Gunakan model untuk memprediksi state saat ini
        current_state = C.predict(user_input)

        # Physician Action
        physician_action = phys_OptimalAction[current_state][0]

        # AI optimal action
        rec_action = OptimalAction[current_state][0]

        return jsonify({
            "Physician_Action": int(physician_action),
            "Recommended_Action": int(rec_action)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400


