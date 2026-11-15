# SENTINEL AI: Intelligent Banking Fraud Detection and Prevention System

An advanced Machine Learning and Fintech Risk Intelligence platform engineered to detect, classify, and prevent fraudulent banking transactions in real-time.

---

## 🌟 Key Highlights

- **50,000 Banking Transactions Audited**: Evaluated on real-world retail banking datasets with complex temporal and behavioral distributions.
- **Class Imbalance Resolution**: Solved severe 98:2 class imbalance using **SMOTE** (Synthetic Minority Over-sampling Technique) without data leakage.
- **Accuracy Paradox Exposing**: Demonstrates why traditional 98% accuracy models fail to catch fraud, while Sentinel achieves **99.98% Accuracy with 100% Fraud Recall (0 False Negatives)**.
- **Champion Classifier (Random Forest)**: Evaluated alongside Decision Tree, Support Vector Machine (LinearSVC), and Logistic Regression with Stratified 5-Fold Cross-Validation.
- **Automated 3-Tier Prevention Engine**:
  - **Tier 1 (Low Risk)**: Auto-Approve (<15 ms latency).
  - **Tier 2 (Medium Risk)**: Step-Up Challenge (2FA / Biometric OTP).
  - **Tier 3 (High Risk)**: Instant Auto-Block & Account Freeze.
- **Tactical Cyber Steppers & 2x2 Forensic Charts**: Interactive real-time parameter tweaking and expanded 2x2 Chart.js analytics.
- **Modern Minimalist 3D Command Deck (Three.js)**: Real-time reactive 3D Icosahedron core, orbiting celestial bodies, 600-particle kinetic field, and fluid responsive design for screens of all sizes (including 17" displays).
- **Zero Heavy Frameworks**: Pure bespoke HTML5, CSS3, Three.js, and modern ES6 JavaScript.

---

## 📁 Project Structure

```
├── app.py                               # Flask Backend REST API
├── index.html                           # Standalone offline frontend (Direct double-click)
├── frouddetection.py                    # Complete ML training & evaluation script
├── generate_visualizations_and_models.py# Model serialization & chart generator
├── requirements.txt                     # Python package dependencies
├── labeled_transactions.csv             # Primary dataset (50,000 banking transactions)
├── sample_transactions_for_testing.csv  # 50-row sample for batch CSV audit testing
├── PRESENTATION_SLIDES.md               # Presentation slides (Introduction to Conclusion)
├── NOTEBOOKLM_PROJECT_SOURCE.md         # Comprehensive technical project study guide
├── models/
│   ├── rf_model.joblib                  # Trained Random Forest classifier
│   ├── dt_model.joblib                  # Trained Decision Tree classifier
│   ├── svm_model.joblib                 # Trained Support Vector Machine classifier
│   ├── lr_model.joblib                  # Trained Logistic Regression classifier
│   ├── scaler.joblib                    # Fitted StandardScaler
│   ├── feature_cols.json                # Feature names list
│   └── model_metadata.json              # Benchmark evaluation metrics & feature importances
├── static/
│   ├── style.css                        # Modern minimalist dark theme design system
│   ├── script.js                        # Frontend controller & Three.js 3D kinetic engine
│   ├── sample_transactions_for_testing.csv # Web-downloadable batch audit sample
│   ├── vendor/                          # Local offline Three.js vendor scripts
│   └── charts/                          # Pre-rendered forensic charts
└── templates/
    └── index.html                       # Flask Jinja2 template
```

---

## 🚀 How to Run

### Method 1: Instant Browser View (No Installation Required)
Simply **double-click** `index.html` in any web browser (Chrome, Edge, Firefox, Safari). All 3D WebGL graphics, dynamic themes, cyber steppers, and interactive charts run immediately with built-in calibrated inference.

### Method 2: Full-Stack Flask Web Server
1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the Flask application:
   ```bash
   python app.py
   ```
3. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

---

## 📊 Model Performance Summary

| Model | Accuracy | Precision | Recall (Catches Theft) | F1-Score | ROC-AUC | False Alarms (FP) | Missed Theft (FN) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Random Forest (Champion)** | **99.98%** | **99.01%** | **100.00%** | **99.50%** | **1.0000** | **2** | **0** |
| Decision Tree | 99.97% | 99.50% | 99.00% | 99.25% | 0.9949 | 1 | 2 |
| Support Vector Machine (SVM) | 99.68% | 86.21% | 100.00% | 92.59% | 0.9999 | 32 | 0 |
| Logistic Regression | 99.52% | 80.65% | 100.00% | 89.29% | 0.9999 | 48 | 0 |
