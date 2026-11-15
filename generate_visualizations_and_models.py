"""
Visualization & Model Persistence Generator
Creates high-res charts and serializes trained models for the Web Application.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, confusion_matrix
)
from imblearn.over_sampling import SMOTE

# Styling for dark orange fintech aesthetic charts
plt.style.use('dark_background')
palette = ["#ff6b00", "#f59e0b", "#ff8533", "#fbbf24", "#ef4444"]
sns.set_palette(palette)

os.makedirs('models', exist_ok=True)
os.makedirs('static/charts', exist_ok=True)

print("Loading dataset...")
df = pd.read_csv("labeled_transactions.csv")

# Create sample test CSV for user to test upload feature easily
sample_test = pd.concat([
    df[df['Fraud'] == 1].head(15),
    df[df['Fraud'] == 0].head(35)
]).sample(frac=1, random_state=42)
sample_test.to_csv("sample_transactions_for_testing.csv", index=False)
sample_test.to_csv("static/sample_transactions_for_testing.csv", index=False)
print("Saved sample_transactions_for_testing.csv for upload demo testing!")

# Preprocessing
df['TransactionDate'] = pd.to_datetime(df['TransactionDate'], format='mixed')
df['TransactionHour'] = df['TransactionDate'].dt.hour
df['DayOfWeek'] = df['TransactionDate'].dt.dayofweek
df['IsWeekend'] = df['DayOfWeek'].apply(lambda x: 1 if x >= 5 else 0)

cols_to_drop = ['TransactionID', 'AccountID', 'DeviceID', 'IP Address', 'MerchantID', 'TransactionDate', 'Location']
clean_df = df.drop(columns=cols_to_drop)
clean_df = pd.get_dummies(clean_df, columns=['TransactionType', 'Channel', 'CustomerOccupation'], drop_first=True)

X = clean_df.drop(columns=['Fraud'])
y = clean_df['Fraud']
feature_cols = list(X.columns)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

# Apply SMOTE
smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

# Fit Scaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_res)
X_test_scaled = scaler.transform(X_test)

# Save Scaler & Features
joblib.dump(scaler, "models/scaler.joblib")
with open("models/feature_cols.json", "w") as f:
    json.dump(feature_cols, f)

# -------------------------------------------------------------
# CHART 1: Class Imbalance & SMOTE Balancing
# -------------------------------------------------------------
print("Generating Chart 1: Class Imbalance vs SMOTE...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), facecolor='#0d1117')
ax1.set_facecolor('#161b22')
ax2.set_facecolor('#161b22')

# Before SMOTE
counts_before = [sum(y_train == 0), sum(y_train == 1)]
bars1 = ax1.bar(['Legitimate (0)', 'Fraud (1)'], counts_before, color=['#f59e0b', '#ff6b00'], width=0.5)
ax1.set_title("Original Training Set (Severe Imbalance: 98% vs 2%)", fontsize=12, pad=15, color='#e6edf3')
ax1.set_ylabel("Number of Transactions", color='#8b949e')
for bar in bars1:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 500, f"{int(yval):,} ({(yval/sum(counts_before))*100:.1f}%)", ha='center', va='bottom', color='#ffffff', fontweight='bold')

# After SMOTE
counts_after = [sum(y_train_res == 0), sum(y_train_res == 1)]
bars2 = ax2.bar(['Legitimate (0)', 'Fraud (1) [SMOTE]'], counts_after, color=['#f59e0b', '#ff6b00'], width=0.5)
ax2.set_title("Balanced Training Set After SMOTE (50% vs 50%)", fontsize=12, pad=15, color='#e6edf3')
for bar in bars2:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 500, f"{int(yval):,} (50.0%)", ha='center', va='bottom', color='#ffffff', fontweight='bold')

plt.tight_layout()
plt.savefig("static/charts/1_class_imbalance_smote.png", dpi=200)
plt.close()

# -------------------------------------------------------------
# Train Models
# -------------------------------------------------------------
print("Training models...")
models = {
    "Logistic Regression": {
        "model": LogisticRegression(max_iter=1000, random_state=42),
        "train_X": X_train_scaled,
        "test_X": X_test_scaled
    },
    "Decision Tree": {
        "model": DecisionTreeClassifier(max_depth=6, random_state=42),
        "train_X": X_train_res,
        "test_X": X_test
    },
    "Random Forest": {
        "model": RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1),
        "train_X": X_train_res,
        "test_X": X_test
    },
    "Support Vector Machine": {
        "model": CalibratedClassifierCV(LinearSVC(random_state=42, max_iter=2000)),
        "train_X": X_train_scaled,
        "test_X": X_test_scaled
    }
}

metrics_summary = {}
cms = {}
roc_data = {}

for name, cfg in models.items():
    clf = cfg["model"]
    clf.fit(cfg["train_X"], y_train_res)
    preds = clf.predict(cfg["test_X"])
    probs = clf.predict_proba(cfg["test_X"])[:, 1]
    
    acc = accuracy_score(y_test, preds)
    prec = precision_score(y_test, preds, zero_division=0)
    rec = recall_score(y_test, preds)
    f1 = f1_score(y_test, preds)
    auc = roc_auc_score(y_test, probs)
    cm = confusion_matrix(y_test, preds)
    tn, fp, fn, tp = cm.ravel()
    
    metrics_summary[name] = {
        "accuracy": round(acc * 100, 2),
        "precision": round(prec * 100, 2),
        "recall": round(rec * 100, 2),
        "f1": round(f1 * 100, 2),
        "roc_auc": round(auc, 4),
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp)
    }
    cms[name] = cm
    fpr, tpr, _ = roc_curve(y_test, probs)
    roc_data[name] = {"fpr": fpr, "tpr": tpr, "auc": auc}

# Save all 4 models for real-time model comparison switching
joblib.dump(models["Random Forest"]["model"], "models/rf_model.joblib")
joblib.dump(models["Decision Tree"]["model"], "models/dt_model.joblib")
joblib.dump(models["Support Vector Machine"]["model"], "models/svm_model.joblib")
joblib.dump(models["Logistic Regression"]["model"], "models/lr_model.joblib")

# -------------------------------------------------------------
# CHART 2: The Accuracy Paradox
# -------------------------------------------------------------
print("Generating Chart 2: The Accuracy Paradox...")
fig, ax = plt.subplots(figsize=(10, 5), facecolor='#0d1117')
ax.set_facecolor('#161b22')

categories = ['Naive Dummy (Always Legit)', 'Random Forest (Our Model)']
acc_vals = [98.0, metrics_summary['Random Forest']['accuracy']]
rec_vals = [0.0, metrics_summary['Random Forest']['recall']]

x = np.arange(len(categories))
width = 0.35

rects1 = ax.bar(x - width/2, acc_vals, width, label='Accuracy (%)', color='#f59e0b')
rects2 = ax.bar(x + width/2, rec_vals, width, label='Fraud Recall (%) [Catches Fraud]', color='#ff6b00')

ax.set_title("The Accuracy Paradox: Why Accuracy Alone Fails in Banking Fraud", fontsize=14, color='#e6edf3', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(categories, color='#ffffff', fontsize=11)
ax.set_ylabel("Percentage (%)", color='#8b949e')
ax.set_ylim(0, 115)
ax.legend(loc='upper left', framealpha=0.2)

for rect in rects1 + rects2:
    h = rect.get_height()
    ax.annotate(f'{h:.1f}%',
                xy=(rect.get_x() + rect.get_width() / 2, h),
                xytext=(0, 3), textcoords="offset points",
                ha='center', va='bottom', color='white', fontweight='bold')

plt.tight_layout()
plt.savefig("static/charts/2_accuracy_paradox.png", dpi=200)
plt.close()

# -------------------------------------------------------------
# CHART 3: Model Metrics Comparison
# -------------------------------------------------------------
print("Generating Chart 3: Model Benchmark Comparison...")
fig, ax = plt.subplots(figsize=(12, 6), facecolor='#0d1117')
ax.set_facecolor('#161b22')

model_names = list(metrics_summary.keys())
metric_types = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
x = np.arange(len(model_names))
w = 0.2

for i, m in enumerate(metric_types):
    vals = [metrics_summary[k][m.lower().replace('-score', '').replace('-', '')] for k in model_names]
    ax.bar(x + i*w - 0.3, vals, w, label=m, color=palette[i])

ax.set_title("Cross-Model Performance Benchmark (Test Set: 10,000 Transactions)", fontsize=14, color='#e6edf3', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(model_names, color='#ffffff', fontsize=11)
ax.set_ylabel("Score (%)", color='#8b949e')
ax.set_ylim(60, 105)
ax.legend(loc='lower right', framealpha=0.2)

plt.tight_layout()
plt.savefig("static/charts/3_model_comparison.png", dpi=200)
plt.close()

# -------------------------------------------------------------
# CHART 4: Confusion Matrices (4 Models Side-by-Side)
# -------------------------------------------------------------
print("Generating Chart 4: Confusion Matrices Heatmap...")
fig, axes = plt.subplots(2, 2, figsize=(12, 10), facecolor='#0d1117')
axes = axes.flatten()

for idx, (name, cm) in enumerate(cms.items()):
    ax = axes[idx]
    ax.set_facecolor('#161b22')
    sns.heatmap(cm, annot=True, fmt=',d', cmap='Oranges', cbar=False, ax=ax,
                annot_kws={"size": 14, "weight": "bold"},
                xticklabels=['Pred: Legit (0)', 'Pred: Fraud (1)'],
                yticklabels=['Actual: Legit (0)', 'Actual: Fraud (1)'])
    ax.set_title(f"{name}\nFP: {cm[0,1]} | FN: {cm[1,0]}", color='#e6edf3', fontsize=12, pad=10)

plt.suptitle("Confusion Matrices: False Positives (FP) vs False Negatives (FN)", color='#ffffff', fontsize=15, y=0.98)
plt.tight_layout()
plt.savefig("static/charts/4_confusion_matrices.png", dpi=200)
plt.close()

# -------------------------------------------------------------
# CHART 5: ROC Curves
# -------------------------------------------------------------
print("Generating Chart 5: ROC Curves...")
fig, ax = plt.subplots(figsize=(9, 6), facecolor='#0d1117')
ax.set_facecolor('#161b22')

for idx, (name, data) in enumerate(roc_data.items()):
    ax.plot(data['fpr'], data['tpr'], label=f"{name} (AUC = {data['auc']:.4f})", color=palette[idx % len(palette)], lw=2.2)

ax.plot([0, 1], [0, 1], 'r--', label="Random Guess (AUC = 0.5000)", alpha=0.6)
ax.set_title("Receiver Operating Characteristic (ROC) Curves", fontsize=14, color='#e6edf3', pad=15)
ax.set_xlabel("False Positive Rate", color='#8b949e')
ax.set_ylabel("True Positive Rate (Recall)", color='#8b949e')
ax.legend(loc='lower right', framealpha=0.3)

plt.tight_layout()
plt.savefig("static/charts/5_roc_curves.png", dpi=200)
plt.close()

# -------------------------------------------------------------
# CHART 6: Feature Importances
# -------------------------------------------------------------
print("Generating Chart 6: Feature Importances...")
rf_clf = models["Random Forest"]["model"]
imp = rf_clf.feature_importances_
feat_df = pd.DataFrame({"Feature": feature_cols, "Importance": imp * 100}).sort_values(by="Importance", ascending=True)

fig, ax = plt.subplots(figsize=(10, 6), facecolor='#0d1117')
ax.set_facecolor('#161b22')
top_feats = feat_df.tail(10)
bars = ax.barh(top_feats['Feature'], top_feats['Importance'], color='#ff6b00', edgecolor='#161b22')

for bar in bars:
    w = bar.get_width()
    ax.text(w + 0.5, bar.get_y() + bar.get_height()/2.0, f"{w:.2f}%", ha='left', va='center', color='#ffffff', fontweight='bold')

ax.set_title("Top 10 Fraud Predictors (Random Forest Gini Importance)", fontsize=14, color='#e6edf3', pad=15)
ax.set_xlabel("Relative Importance (%)", color='#8b949e')
ax.set_xlim(0, max(top_feats['Importance']) + 8)

plt.tight_layout()
plt.savefig("static/charts/6_feature_importance.png", dpi=200)
plt.close()

# -------------------------------------------------------------
# Save Metadata JSON for API
# -------------------------------------------------------------
metadata = {
    "metrics": metrics_summary,
    "top_features": feat_df.tail(10).to_dict(orient="records"),
    "total_records": len(df),
    "fraud_count": int(sum(df['Fraud'] == 1)),
    "legit_count": int(sum(df['Fraud'] == 0))
}

with open("models/model_metadata.json", "w") as f:
    json.dump(metadata, f, indent=4)

print("\nALL VISUALIZATIONS AND MODEL ARTIFACTS GENERATED SUCCESSFULLY!")
