"""
Sentinel AI - Next-Gen Banking Fraud Intelligence & Prevention Engine
Flask Backend API with Multi-Model Switching and Real-time Auditing
"""

import os
import io
import json
import random
import warnings
warnings.filterwarnings('ignore')
import joblib
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify, send_file

app = Flask(__name__)

# Load trained models & artifacts
MODEL_DIR = "models"
MODELS = {
    "Random Forest": joblib.load(os.path.join(MODEL_DIR, "rf_model.joblib")),
    "Decision Tree": joblib.load(os.path.join(MODEL_DIR, "dt_model.joblib")),
    "Support Vector Machine": joblib.load(os.path.join(MODEL_DIR, "svm_model.joblib")),
    "Logistic Regression": joblib.load(os.path.join(MODEL_DIR, "lr_model.joblib"))
}
scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.joblib"))

with open(os.path.join(MODEL_DIR, "feature_cols.json"), "r") as f:
    FEATURE_COLS = json.load(f)

with open(os.path.join(MODEL_DIR, "model_metadata.json"), "r") as f:
    MODEL_METADATA = json.load(f)


def prepare_features(input_dict):
    """
    Transforms transaction inputs, extracts temporal features, encodes categoricals,
    and aligns with model training columns.
    """
    row_df = pd.DataFrame([input_dict])
    
    # Date parsing
    if 'TransactionDate' in row_df.columns and pd.notnull(row_df['TransactionDate'].iloc[0]):
        dt = pd.to_datetime(row_df['TransactionDate'].iloc[0], format='mixed')
        row_df['TransactionHour'] = dt.hour
        row_df['DayOfWeek'] = dt.dayofweek
        row_df['IsWeekend'] = 1 if dt.dayofweek >= 5 else 0
    else:
        row_df['TransactionHour'] = int(input_dict.get('TransactionHour', 14))
        row_df['DayOfWeek'] = int(input_dict.get('DayOfWeek', 2))
        row_df['IsWeekend'] = int(input_dict.get('IsWeekend', 0))

    # Clean non-predictive IDs
    drop_cols = ['TransactionID', 'AccountID', 'DeviceID', 'IP Address', 'MerchantID', 'TransactionDate', 'Location', 'Fraud']
    row_df = row_df.drop(columns=[c for c in drop_cols if c in row_df.columns], errors='ignore')
    
    # Dummy encoding
    row_df = pd.get_dummies(row_df, columns=[c for c in ['TransactionType', 'Channel', 'CustomerOccupation'] if c in row_df.columns], drop_first=True)
    
    # Align columns
    aligned_df = row_df.reindex(columns=FEATURE_COLS, fill_value=0)
    for col in aligned_df.columns:
        aligned_df[col] = pd.to_numeric(aligned_df[col], errors='coerce').fillna(0)
        
    return aligned_df


def predict_probability(model_name, features_df):
    """
    Safely computes probability for any of the 4 supported models.
    Applies scaler to Logistic Regression and SVM.
    """
    clf = MODELS.get(model_name, MODELS["Random Forest"])
    if model_name in ["Support Vector Machine", "Logistic Regression"]:
        scaled_feat = scaler.transform(features_df)
        if hasattr(clf, "predict_proba"):
            return float(clf.predict_proba(scaled_feat)[0, 1])
        else:
            return float(1 / (1 + np.exp(-clf.decision_function(scaled_feat)[0])))
    else:
        return float(clf.predict_proba(features_df)[0, 1])


def determine_prevention_tier(prob, risk_score, login_attempts, low_thresh=0.25, high_thresh=0.65):
    """
    Multi-tier proactive fraud prevention strategy logic.
    """
    if prob >= high_thresh or (login_attempts >= 3 and risk_score >= 65):
        return {
            "tier": "Tier 3: High Risk",
            "action": "AUTO-BLOCK & FREEZE",
            "badge_color": "danger",
            "severity": "CRITICAL",
            "description": "Transaction halted. Account credentials locked. Alert dispatched to Fraud Operations & Cardholder."
        }
    elif prob >= low_thresh or login_attempts >= 2 or risk_score >= 60:
        return {
            "tier": "Tier 2: Medium Risk",
            "action": "CHALLENGE 2FA / OTP",
            "badge_color": "warning",
            "severity": "ELEVATED",
            "description": "Out-of-band Step-up Challenge (SMS OTP / Biometric FaceID) required before authorization."
        }
    else:
        return {
            "tier": "Tier 1: Low Risk",
            "action": "AUTO-APPROVE",
            "badge_color": "success",
            "severity": "NORMAL",
            "description": "Instant cryptographic verification (<15ms). Authorized and logged seamlessly."
        }


@app.route('/')
def index():
    return render_template('index.html', metadata=MODEL_METADATA)


@app.route('/favicon.ico')
def favicon():
    return ('', 204)


@app.route('/api/metadata')
def get_metadata():
    return jsonify(MODEL_METADATA)


@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        model_name = data.get('model_choice', 'Random Forest')
        low_thresh = float(data.get('low_threshold', 0.25))
        high_thresh = float(data.get('high_threshold', 0.65))

        processed_features = prepare_features(data)
        prob = predict_probability(model_name, processed_features)
        prediction = int(prob >= 0.5)
        
        risk_score = float(data.get('RiskScore', 50.0))
        login_attempts = int(data.get('LoginAttempts', 1))
        prevention = determine_prevention_tier(prob, risk_score, login_attempts, low_thresh, high_thresh)
        
        return jsonify({
            "status": "success",
            "active_model": model_name,
            "is_fraud": prediction,
            "fraud_probability": round(prob * 100, 2),
            "confidence": round((prob if prediction == 1 else 1 - prob) * 100, 2),
            "prevention": prevention
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route('/api/upload', methods=['POST'])
def upload_csv():
    try:
        if 'file' not in request.files:
            return jsonify({"status": "error", "message": "No file uploaded"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"status": "error", "message": "No file selected"}), 400
            
        model_name = request.form.get('model_choice', 'Random Forest')
        low_thresh = float(request.form.get('low_threshold', 0.25))
        high_thresh = float(request.form.get('high_threshold', 0.65))

        df_upload = pd.read_csv(file)
        if len(df_upload) == 0:
            return jsonify({"status": "error", "message": "CSV file is empty"}), 400
            
        results = []
        fraud_count = 0
        
        sample_batch = df_upload.head(200).copy()
        
        for idx, row in sample_batch.iterrows():
            row_dict = row.to_dict()
            processed_row = prepare_features(row_dict)
            prob = predict_probability(model_name, processed_row)
            is_fraud = int(prob >= 0.5)
            if is_fraud:
                fraud_count += 1
                
            risk_score = float(row.get('RiskScore', 50.0)) if pd.notnull(row.get('RiskScore', None)) else 50.0
            login_attempts = int(row.get('LoginAttempts', 1)) if pd.notnull(row.get('LoginAttempts', None)) else 1
            prevention = determine_prevention_tier(prob, risk_score, login_attempts, low_thresh, high_thresh)
            
            results.append({
                "id": str(row.get('TransactionID', f'TX_{idx+1:05d}')),
                "amount": f"${float(row.get('TransactionAmount', 0)):.2f}",
                "channel": str(row.get('Channel', 'Online')),
                "type": str(row.get('TransactionType', 'Debit')),
                "risk_score": round(risk_score, 1),
                "login_attempts": login_attempts,
                "fraud_probability": f"{prob * 100:.1f}%",
                "is_fraud": is_fraud,
                "action": prevention['action'],
                "tier": prevention['tier'],
                "badge": prevention['badge_color']
            })
            
        total = len(results)
        fraud_rate = round((fraud_count / total) * 100, 2) if total > 0 else 0
        
        return jsonify({
            "status": "success",
            "active_model": model_name,
            "total_processed": total,
            "total_in_file": len(df_upload),
            "fraud_detected": fraud_count,
            "legitimate_count": total - fraud_count,
            "fraud_rate": fraud_rate,
            "records": results
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route('/download_sample')
def download_sample():
    sample_path = os.path.join("static", "sample_transactions_for_testing.csv")
    return send_file(sample_path, as_attachment=True, download_name="sample_banking_transactions.csv")


if __name__ == '__main__':
    print("Sentinel AI Fraud Prevention Engine running on port 5000...")
    app.run(debug=True, port=5000, host='127.0.0.1')
