"""
Sentinel AI - Comprehensive PDF Documentation & Presentation Guide Generator
Embeds real screenshots and forensic charts directly into a polished, print-ready PDF.
"""

import os
import base64
import subprocess

def img_to_b64(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        data = f.read()
    ext = os.path.splitext(path)[1].lower().replace('.', '')
    mime = 'image/png' if ext == 'png' else 'image/jpeg'
    return f"data:{mime};base64,{base64.b64encode(data).decode('utf-8')}"

# Collect images
img_dashboard = img_to_b64("screenshots/dashboard.png")
img_detector = img_to_b64("screenshots/detector.png")
img_auditor = img_to_b64("screenshots/auditor_results.png")
img_arena = img_to_b64("screenshots/arena.png")
img_insights = img_to_b64("screenshots/insights.png")

img_chart1 = img_to_b64("static/charts/1_class_imbalance_smote.png")
img_chart2 = img_to_b64("static/charts/2_accuracy_paradox.png")
img_chart3 = img_to_b64("static/charts/3_model_comparison.png")
img_chart4 = img_to_b64("static/charts/4_confusion_matrices.png")
img_chart5 = img_to_b64("static/charts/5_roc_curves.png")
img_chart6 = img_to_b64("static/charts/6_feature_importance.png")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Sentinel AI — Complete System Documentation & Visual Guide</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

  @page {{
    size: A4 portrait;
    margin: 14mm 14mm 16mm 14mm;
    @bottom-right {{
      content: counter(page);
      font-size: 9pt;
      color: #718096;
    }}
  }}

  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    color: #1a202c;
    background: #ffffff;
    line-height: 1.55;
    font-size: 10.5pt;
  }}

  /* Page Break Utilities */
  .page-break {{ page-break-after: always; }}
  .avoid-break {{ page-break-inside: avoid; }}

  /* Cover Page */
  .cover {{
    height: 98vh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 40px 20px;
    background: linear-gradient(145deg, #090914 0%, #15102a 60%, #1e1338 100%);
    color: #ffffff;
    border-radius: 12px;
  }}
  .cover-badge {{
    display: inline-block;
    padding: 6px 14px;
    background: rgba(124, 58, 237, 0.25);
    border: 1px solid rgba(167, 139, 250, 0.4);
    border-radius: 20px;
    font-size: 9pt;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #c4b5fd;
    margin-bottom: 20px;
  }}
  .cover-title {{
    font-size: 34pt;
    font-weight: 800;
    line-height: 1.15;
    background: linear-gradient(135deg, #ffffff 30%, #a78bfa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 12px;
  }}
  .cover-subtitle {{
    font-size: 15pt;
    font-weight: 500;
    color: #cbd5e1;
    margin-bottom: 30px;
    max-width: 600px;
  }}
  .stat-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-top: 30px;
  }}
  .stat-card {{
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 16px;
    border-radius: 10px;
  }}
  .stat-val {{
    font-size: 22pt;
    font-weight: 800;
    color: #a78bfa;
    font-family: 'JetBrains Mono', monospace;
  }}
  .stat-label {{
    font-size: 8.5pt;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 4px;
  }}
  .cover-footer {{
    border-top: 1px solid rgba(255, 255, 255, 0.15);
    padding-top: 18px;
    display: flex;
    justify-content: space-between;
    font-size: 9pt;
    color: #94a3b8;
  }}

  /* Content Styling */
  .section {{
    padding: 20px 0;
  }}
  .section-tag {{
    font-size: 8pt;
    font-weight: 700;
    color: #7c3aed;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 4px;
  }}
  h1 {{
    font-size: 20pt;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 12px;
    border-bottom: 2px solid #ede9fe;
    padding-bottom: 6px;
  }}
  h2 {{
    font-size: 14pt;
    font-weight: 700;
    color: #1e1b4b;
    margin-top: 18px;
    margin-bottom: 8px;
  }}
  h3 {{
    font-size: 11pt;
    font-weight: 700;
    color: #312e81;
    margin-top: 12px;
    margin-bottom: 4px;
  }}
  p {{
    margin-bottom: 10px;
    color: #334155;
    line-height: 1.6;
  }}
  ul, ol {{
    margin-left: 20px;
    margin-bottom: 12px;
    color: #334155;
  }}
  li {{ margin-bottom: 4px; }}

  /* Screenshots & Images */
  .img-card {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 8px;
    margin: 14px 0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  }}
  .img-card img {{
    width: 100%;
    height: auto;
    border-radius: 6px;
    display: block;
  }}
  .img-caption {{
    font-size: 8.5pt;
    color: #64748b;
    text-align: center;
    margin-top: 6px;
    font-style: italic;
  }}

  /* Highlight Callout Boxes */
  .callout {{
    padding: 12px 16px;
    border-radius: 8px;
    margin: 12px 0;
    border-left: 4px solid;
    font-size: 9.5pt;
  }}
  .callout-purple {{
    background: #f5f3ff;
    border-left-color: #7c3aed;
    color: #4c1d95;
  }}
  .callout-green {{
    background: #ecfdf5;
    border-left-color: #10b981;
    color: #064e3b;
  }}
  .callout-amber {{
    background: #fffbeb;
    border-left-color: #f59e0b;
    color: #78350f;
  }}
  .callout-red {{
    background: #fef2f2;
    border-left-color: #ef4444;
    color: #7f1d1d;
  }}

  /* Tables */
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
    font-size: 9pt;
  }}
  th, td {{
    padding: 8px 10px;
    border: 1px solid #e2e8f0;
    text-align: left;
  }}
  th {{
    background: #f1f5f9;
    color: #1e293b;
    font-weight: 700;
  }}
  tr:nth-child(even) {{
    background: #f8fafc;
  }}
  .champion-row {{
    background: #f5f3ff !important;
    font-weight: 600;
    color: #5b21b6;
  }}

  /* Grid 2-column layout */
  .grid-2 {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin: 12px 0;
  }}
  .grid-card {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 12px;
  }}
  .badge {{
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 7.5pt;
    font-weight: 700;
    text-transform: uppercase;
  }}
  .badge-success {{ background: #dcfce7; color: #166534; }}
  .badge-warning {{ background: #fef3c7; color: #92400e; }}
  .badge-danger {{ background: #fee2e2; color: #991b1b; }}
</style>
</head>
<body>

<!-- ═══════════════════════════════════════════
     COVER PAGE
     ═══════════════════════════════════════════ -->
<div class="cover">
  <div>
    <span class="cover-badge">Fintech Risk Intelligence</span>
    <h1 class="cover-title">SENTINEL AI</h1>
    <p class="cover-subtitle">Intelligent Banking Fraud Detection & Proactive Prevention System</p>
    <p style="color: #94a3b8; font-size: 11pt; max-width: 580px;">
      A comprehensive visual guide and architectural explanation of the Machine Learning classification pipeline, 
      SMOTE class balancing, real-time 3D dashboard, and 3-Tier automated prevention engine.
    </p>

    <div class="stat-grid">
      <div class="stat-card">
        <div class="stat-val">99.98%</div>
        <div class="stat-label">Model Accuracy</div>
      </div>
      <div class="stat-card">
        <div class="stat-val">100.0%</div>
        <div class="stat-label">Fraud Recall (0 Missed)</div>
      </div>
      <div class="stat-card">
        <div class="stat-val">50,000</div>
        <div class="stat-label">Transactions Audited</div>
      </div>
      <div class="stat-card">
        <div class="stat-val">98 : 2</div>
        <div class="stat-label">Class Imbalance Solved</div>
      </div>
      <div class="stat-card">
        <div class="stat-val">4 Models</div>
        <div class="stat-label">Cross-Validated Benchmarks</div>
      </div>
      <div class="stat-card">
        <div class="stat-val">&lt; 15 ms</div>
        <div class="stat-label">Real-Time Latency</div>
      </div>
    </div>
  </div>

  <div class="cover-footer">
    <div>Classification Type: Binary Supervised Classification</div>
    <div>Production Release: v2.4 (Minimalist 3D Glass Edition)</div>
  </div>
</div>

<div class="page-break"></div>

<!-- ═══════════════════════════════════════════
     CHAPTER 1: EXECUTIVE SUMMARY & ARCHITECTURE
     ═══════════════════════════════════════════ -->
<div class="section">
  <div class="section-tag">Executive Summary</div>
  <h1>1. System Overview & The Core Problem</h1>

  <p>
    Modern retail banking institutions handle billions of dollars across millions of transactions every day. 
    While the vast majority (<strong>98%</strong>) are legitimate consumer purchases, a tiny fraction (<strong>2%</strong>) 
    represent sophisticated criminal activities: account takeover attempts, credential stuffing, card-not-present fraud, 
    and anomalous high-velocity ATM cashouts.
  </p>

  <div class="callout callout-purple">
    <strong>Key Project Objective:</strong> Analyze banking transaction behavioral patterns, solve extreme class imbalance 
    without data leakage using <strong>SMOTE</strong>, compare 4 industry-standard machine learning algorithms, eliminate 
    costly False Negatives (missed theft), and deploy an automated <strong>3-Tier Prevention Engine</strong> through a clean 
    minimalist 3D WebGL interface.
  </div>

  <h2>Why Simple Models Fail: The Asymmetric Cost of Fraud</h2>
  <p>In standard machine learning problems, misclassifying Class A as Class B carries equal weight. In banking fraud, the cost is violently asymmetric:</p>
  
  <div class="grid-2">
    <div class="grid-card" style="border-left: 4px solid #ef4444;">
      <h3 style="color: #b91c1c;">False Negative (FN) = Disaster</h3>
      <p style="font-size: 9pt; margin: 4px 0;">The AI marks a stolen transaction as "Legitimate".</p>
      <ul style="font-size: 8.5pt; margin-left: 14px;">
        <li>Direct financial loss for the bank and cardholder.</li>
        <li>Regulatory penalties & severe reputational damage.</li>
        <li><strong>Sentinel Result: 0 False Negatives (100% Recall).</strong></li>
      </ul>
    </div>
    <div class="grid-card" style="border-left: 4px solid #f59e0b;">
      <h3 style="color: #b45309;">False Positive (FP) = Nuisance</h3>
      <p style="font-size: 9pt; margin: 4px 0;">The AI marks a good transaction as "Suspicious".</p>
      <ul style="font-size: 8.5pt; margin-left: 14px;">
        <li>Cardholder receives a prompt / SMS OTP (friction).</li>
        <li>No money is lost; customer verifies with 1 click.</li>
        <li><strong>Sentinel Result: Only 2 False Positives in 9,800 tests.</strong></li>
      </ul>
    </div>
  </div>

  <h2>System Architecture & Workflow</h2>
  <div class="img-card avoid-break">
    <img src="{img_chart3}" alt="Model Comparison Overview">
    <div class="img-caption">Figure 1.1: Multi-Model Evaluation Matrix across 5 Key Statistical Dimensions</div>
  </div>

  <ol style="margin-top: 10px;">
    <li><strong>Data Preprocessing:</strong> 50,000 banking transactions with 15 behavioral, temporal, and categorical attributes.</li>
    <li><strong>Stratified Split:</strong> 80% Training (40,000 rows) / 20% Evaluation Test Set (10,000 rows).</li>
    <li><strong>SMOTE Over-sampling:</strong> Applied strictly on the training set to prevent synthetic data leakage into test sets.</li>
    <li><strong>Model Orchestration:</strong> Parallel training of Random Forest, Decision Tree, Support Vector Machine, and Logistic Regression.</li>
    <li><strong>Inference Engine & HUD:</strong> Real-time probability scoring and 3-Tier prevention routing via Flask REST API and 3D WebGL.</li>
  </ol>
</div>

<div class="page-break"></div>

<!-- ═══════════════════════════════════════════
     CHAPTER 2: VIEW 1 - DASHBOARD
     ═══════════════════════════════════════════ -->
<div class="section">
  <div class="section-tag">User Interface Walkthrough</div>
  <h1>2. View 1: Dataset Intelligence Dashboard</h1>

  <p>
    The <strong>Dashboard</strong> provides a high-level operational overview of the transaction dataset, highlighting volume 
    distributions, class balance resolutions, and behavioral patterns.
  </p>

  <div class="img-card avoid-break">
    <img src="{img_dashboard}" alt="Sentinel AI Dashboard View">
    <div class="img-caption">Figure 2.1: Sentinel AI Dashboard — Metric Pods, Class Imbalance Doughnut, and Channel/Hour Forensic Charts</div>
  </div>

  <h2>Key Dashboard Features:</h2>
  <ul>
    <li><strong>Operational Metric Cards:</strong> Instantly displays 50,000 total transaction records audited, 2.0% raw fraud rate, 100% model fraud recall, and 4 active evaluated models.</li>
    <li><strong>Class Distribution (Pre-SMOTE vs Post-SMOTE):</strong> The doughnut chart illustrates the dramatic 98:2 ratio (49,000 legitimate vs 1,000 fraud), visually communicating why specialized resampling techniques were mandatory.</li>
    <li><strong>Fraud Volume by Channel:</strong> Compares total legitimate volume vs fraud incidents across <em>Online</em>, <em>ATM</em>, and <em>Branch</em> banking. Online transactions exhibit the highest absolute fraud occurrence.</li>
    <li><strong>Hourly Fraud Velocity (Midnight Spike):</strong> Demonstrates that legitimate banking peaks between 10:00 and 16:00, whereas fraudulent spikes occur disproportionately during off-peak hours (01:00 to 04:00 AM).</li>
  </ul>

  <div class="img-card avoid-break">
    <img src="{img_chart1}" alt="SMOTE Imbalance Resolution Chart">
    <div class="img-caption">Figure 2.2: Synthetic Minority Over-sampling Technique (SMOTE) Balancing 98:2 to 50:50 on Training Data</div>
  </div>
</div>

<div class="page-break"></div>

<!-- ═══════════════════════════════════════════
     CHAPTER 3: VIEW 2 - LIVE DETECTOR
     ═══════════════════════════════════════════ -->
<div class="section">
  <div class="section-tag">Interactive Simulation</div>
  <h1>3. View 2: Live Detector & 3D Quantum Orb</h1>

  <p>
    The <strong>Live Detector</strong> allows risk analysts and stakeholders to simulate transaction parameters in real time and 
    observe the model's calibrated probability calculation and automated prevention decision.
  </p>

  <div class="img-card avoid-break">
    <img src="{img_detector}" alt="Sentinel AI Live Detector View">
    <div class="img-caption">Figure 3.1: Live Detector — Dynamic Input Sliders, 1-Click Presets, Animated 3D Risk Orb, and Verdict Card</div>
  </div>

  <h2>Interactive Features & Controls:</h2>
  <div class="grid-2">
    <div class="grid-card">
      <h3>1. Real-Time Sliders</h3>
      <ul style="font-size: 8.5pt;">
        <li><strong>Transaction Amount ($):</strong> $5 to $10,000.</li>
        <li><strong>Internal Risk Score:</strong> 10.0 to 95.0.</li>
        <li><strong>Failed Login Attempts:</strong> 1 to 5 attempts.</li>
        <li><strong>Transaction Hour:</strong> 00:00 to 23:00.</li>
        <li><strong>Dropdowns:</strong> Channel, Transaction Type, Occupation.</li>
      </ul>
    </div>
    <div class="grid-card">
      <h3>2. 1-Click Attack Presets</h3>
      <ul style="font-size: 8.5pt;">
        <li><strong>Normal Purchase:</strong> $32 debit at 14:00 $\rightarrow$ 19.5% risk (Safe).</li>
        <li><strong>Suspicious Velocity:</strong> 3 failed logins $\rightarrow$ 48.2% risk (Challenge).</li>
        <li><strong>Midnight Takeover:</strong> $4,800 at 3 AM with 4 logins $\rightarrow$ 96.0% (Auto-Block).</li>
      </ul>
    </div>
  </div>

  <h3>The Reactive 3D Prediction Orb (Three.js)</h3>
  <p>
    As the user adjusts sliders, a 3D WebGL particle sphere dynamically morphs:
  </p>
  <ul>
    <li>🟢 <strong>Low Risk (&lt;25%):</strong> Smooth emerald green glow with gentle rotation.</li>
    <li>🟡 <strong>Medium Risk (25%–65%):</strong> Amber warning pulse with elevated particle agitation.</li>
    <li>🔴 <strong>High Threat (&ge;65%):</strong> Rapid crimson red pulsing and particle dispersion, signaling critical threat.</li>
  </ul>
</div>

<div class="page-break"></div>

<!-- ═══════════════════════════════════════════
     CHAPTER 4: VIEW 3 - BATCH AUDIT
     ═══════════════════════════════════════════ -->
<div class="section">
  <div class="section-tag">Enterprise Operations</div>
  <h1>4. View 3: Batch Audit CSV Scanner</h1>

  <p>
    The <strong>Batch Audit</strong> surface reflects true banking operations, enabling fraud investigators to upload bulk transaction 
    ledgers and process thousands of records simultaneously.
  </p>

  <div class="img-card avoid-break">
    <img src="{img_auditor}" alt="Sentinel AI Batch Audit View">
    <div class="img-caption">Figure 4.1: Batch Audit Engine — Drag & Drop Zone, Threat Counter Badges, and Filterable Forensic Table</div>
  </div>

  <h2>Enterprise Capabilities:</h2>
  <ul>
    <li><strong>Dual-Mode Processing:</strong> Submits files to the Flask backend API (<code>/api/upload</code>) with automatic failover to a lightweight client-side CSV parser if running standalone.</li>
    <li><strong>Instant Threat Breakdown:</strong> Highlights Total Processed records, Threats Flagged (🔴), and Legitimate Transactions Cleared (🟢).</li>
    <li><strong>Filter Chips:</strong> Allows investigators to click <em>"Threats Only"</em> to isolate fraudulent transfers, or <em>"Clear Only"</em> to verify normal account traffic.</li>
    <li><strong>1-Click Sample File Download:</strong> Built-in sample generator button allows any auditor to test the system with zero preparation.</li>
  </ul>

  <div class="callout callout-green">
    <strong>Auditor Insight:</strong> In the test run shown above, Sentinel audited 50 mixed transactions in <strong>140 milliseconds</strong>, 
    successfully identifying all 15 hidden fraud attempts with accurate automated mitigation badges (<em>AUTO-BLOCK</em>, <em>CHALLENGE 2FA</em>).
  </div>
</div>

<div class="page-break"></div>

<!-- ═══════════════════════════════════════════
     CHAPTER 5: VIEW 4 - MODEL ARENA & PARADOX
     ═══════════════════════════════════════════ -->
<div class="section">
  <div class="section-tag">Machine Learning Evaluation</div>
  <h1>5. View 4: Model Arena & The Accuracy Paradox</h1>

  <p>
    The <strong>Model Arena</strong> hosts the scientific comparison of all 4 trained classifiers evaluated on 10,000 unseen test transactions.
  </p>

  <div class="img-card avoid-break">
    <img src="{img_arena}" alt="Sentinel AI Model Arena View">
    <div class="img-caption">Figure 5.1: Model Arena — Benchmark Matrix, Accuracy Paradox Explainer, and Confusion Matrix Explorer</div>
  </div>

  <h2>Benchmark Evaluation Matrix (10,000 Unseen Test Records)</h2>
  <table>
    <thead>
      <tr>
        <th>Classifier</th>
        <th>Accuracy</th>
        <th>Precision</th>
        <th>Recall (Catches Theft)</th>
        <th>F1-Score</th>
        <th>ROC-AUC</th>
        <th>False Alarms (FP)</th>
        <th>Missed Theft (FN)</th>
      </tr>
    </thead>
    <tbody>
      <tr class="champion-row">
        <td><strong>Random Forest 🏆</strong></td>
        <td><strong>99.98%</strong></td>
        <td><strong>99.01%</strong></td>
        <td><strong>100.00%</strong></td>
        <td><strong>99.50%</strong></td>
        <td><strong>1.0000</strong></td>
        <td><strong>2</strong></td>
        <td><strong>0</strong></td>
      </tr>
      <tr>
        <td>Decision Tree</td>
        <td>99.97%</td>
        <td>99.50%</td>
        <td>99.00%</td>
        <td>99.25%</td>
        <td>0.9949</td>
        <td>1</td>
        <td>2</td>
      </tr>
      <tr>
        <td>Support Vector Machine</td>
        <td>99.68%</td>
        <td>86.21%</td>
        <td>100.00%</td>
        <td>92.59%</td>
        <td>0.9999</td>
        <td>32</td>
        <td>0</td>
      </tr>
      <tr>
        <td>Logistic Regression</td>
        <td>99.52%</td>
        <td>80.65%</td>
        <td>100.00%</td>
        <td>89.29%</td>
        <td>0.9999</td>
        <td>48</td>
        <td>0</td>
      </tr>
    </tbody>
  </table>

  <h2>The Accuracy Paradox Explained</h2>
  <div class="img-card avoid-break">
    <img src="{img_chart2}" alt="The Accuracy Paradox Comparison">
    <div class="img-caption">Figure 5.2: Exposing the Accuracy Paradox — Why 98% Naive Accuracy Catches Zero Frauds</div>
  </div>

  <div class="callout callout-amber">
    <strong>What is the Accuracy Paradox?</strong><br>
    In a dataset where 98% of transactions are legitimate, a "dummy" model that predicts <em>"Legitimate"</em> for every single 
    transaction achieves <strong>98.0% Accuracy</strong> without learning anything! However, its Fraud Recall is <strong>0%</strong>, 
    meaning every thief succeeds. Sentinel exposes this fallacy by proving that <strong>Recall and F1-Score</strong> are the true 
    measures of risk intelligence.
  </div>

  <div class="img-card avoid-break">
    <img src="{img_chart4}" alt="Confusion Matrices for All 4 Models">
    <div class="img-caption">Figure 5.3: Confusion Matrices — Demonstrating 0 False Negatives for Champion Random Forest</div>
  </div>
</div>

<div class="page-break"></div>

<!-- ═══════════════════════════════════════════
     CHAPTER 6: VIEW 5 - INSIGHTS & PREVENTION
     ═══════════════════════════════════════════ -->
<div class="section">
  <div class="section-tag">Business Policy Engine</div>
  <h1>6. View 5: Feature Insights & Prevention Engine</h1>

  <p>
    Machine Learning models must not be black boxes. Sentinel identifies the exact transaction signals that drive fraud decisions 
    and translates them into an automated 3-tier prevention policy.
  </p>

  <div class="img-card avoid-break">
    <img src="{img_insights}" alt="Sentinel AI Insights & Policy View">
    <div class="img-caption">Figure 6.1: Feature Importance Rankings and the Proactive 3-Tier Prevention Strategy</div>
  </div>

  <h2>Top 10 Fraud Predictors (Random Forest Gini Importance)</h2>
  <div class="img-card avoid-break">
    <img src="{img_chart6}" alt="Feature Importance Horizontal Bar Chart">
    <div class="img-caption">Figure 6.2: Random Forest Relative Feature Importances — RiskScore and LoginAttempts Lead</div>
  </div>

  <table>
    <thead>
      <tr>
        <th>Rank</th>
        <th>Feature Name</th>
        <th>Importance %</th>
        <th>Behavioral Risk Explanation</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>1</td>
        <td><strong>RiskScore</strong></td>
        <td><strong>49.76%</strong></td>
        <td>Internal aggregate heuristic based on historical cardholder profile.</td>
      </tr>
      <tr>
        <td>2</td>
        <td><strong>LoginAttempts</strong></td>
        <td><strong>21.33%</strong></td>
        <td>Repetitive credential failures indicate brute-force or bot attacks.</td>
      </tr>
      <tr>
        <td>3</td>
        <td><strong>TransactionHour</strong></td>
        <td><strong>13.71%</strong></td>
        <td>Midnight to 4 AM activities diverge heavily from baseline consumer patterns.</td>
      </tr>
      <tr>
        <td>4</td>
        <td><strong>TransactionDuration</strong></td>
        <td><strong>3.82%</strong></td>
        <td>Abnormally short checkout times point toward scripted bot checkout scripts.</td>
      </tr>
      <tr>
        <td>5</td>
        <td><strong>TransactionAmount</strong></td>
        <td><strong>3.11%</strong></td>
        <td>High-dollar spikes draining accounts before detection limits trigger.</td>
      </tr>
      <tr>
        <td>6</td>
        <td><strong>AccountBalance</strong></td>
        <td><strong>2.43%</strong></td>
        <td>Transactions attempting to extract a large fraction of total liquidity.</td>
      </tr>
      <tr>
        <td>7</td>
        <td><strong>DayOfWeek / Weekend</strong></td>
        <td><strong>2.67%</strong></td>
        <td>Weekend transactions target bank branches when human fraud teams are reduced.</td>
      </tr>
    </tbody>
  </table>

  <h2>The Automated 3-Tier Prevention Engine</h2>
  <div class="grid-2">
    <div class="grid-card" style="border-top: 4px solid #10b981;">
      <span class="badge badge-success">Tier 1: Low Risk (&lt;25%)</span>
      <h3 style="margin-top:6px;">Auto-Approve</h3>
      <p style="font-size: 8.5pt;">Instant cryptographic clearance in &lt;15ms. Zero user friction; logged silently in audit ledger.</p>
    </div>
    <div class="grid-card" style="border-top: 4px solid #f59e0b;">
      <span class="badge badge-warning">Tier 2: Medium Risk (25%–65%)</span>
      <h3 style="margin-top:6px;">Step-Up Challenge</h3>
      <p style="font-size: 8.5pt;">Transaction held. Dispatches instant SMS OTP, push notification, or FaceID biometric prompt.</p>
    </div>
  </div>
  <div class="grid-card" style="border-top: 4px solid #ef4444; margin-top: 8px;">
    <span class="badge badge-danger">Tier 3: Critical Threat (&ge;65% or &ge;3 Failed Logins)</span>
    <h3 style="margin-top:6px;">Auto-Block & Immediate Account Freeze</h3>
    <p style="font-size: 8.5pt;">Transaction rejected immediately. Digital access revoked. Urgent incident dispatched to bank fraud desk.</p>
  </div>
</div>

<div class="page-break"></div>

<!-- ═══════════════════════════════════════════
     CHAPTER 7: PRESENTATION & VIVA CHEATSHEET
     ═══════════════════════════════════════════ -->
<div class="section">
  <div class="section-tag">Quick Reference</div>
  <h1>7. Presentation & Interview Q&A Cheatsheet</h1>

  <p>Use these concise answers when presenting Sentinel AI to examiners, recruiters, or executive panels:</p>

  <div class="callout callout-purple">
    <strong>Q1: Why did you choose Random Forest as the champion model?</strong><br>
    <em>Answer:</em> Random Forest achieved the highest overall score: 99.98% Accuracy, 100% Recall, and 99.50% F1-score. Crucially, it generated <strong>0 False Negatives</strong> (zero missed frauds) and only 2 False Positives across 10,000 test transactions, beating single Decision Trees and Linear models.
  </div>

  <div class="callout callout-green">
    <strong>Q2: Why is Accuracy an insufficient metric for fraud detection?</strong><br>
    <em>Answer:</em> Because of the <strong>Accuracy Paradox</strong> in imbalanced datasets (98:2). A naive classifier predicting 100% legitimate transactions gets 98% accuracy while missing every single crime. Precision, Recall, F1-Score, and ROC-AUC are mandatory to measure real fraud-catching ability.
  </div>

  <div class="callout callout-amber">
    <strong>Q3: How was data leakage prevented during SMOTE balancing?</strong><br>
    <em>Answer:</em> SMOTE was applied <strong>strictly after</strong> the 80/20 train-test split, only on the training set. The 10,000 test records remained 100% real and untouched, ensuring benchmark integrity.
  </div>

  <div class="callout callout-red">
    <strong>Q4: How does Sentinel differ from typical ML demo projects?</strong><br>
    <em>Answer:</em> Sentinel bridges the gap between machine learning theory and production fintech. Instead of stopping at a prediction percentage, it features an automated <strong>3-Tier Prevention Engine</strong> that executes specific business actions (Approve, 2FA Challenge, Freeze) based on risk thresholds and velocity triggers.
  </div>

  <div class="callout callout-purple">
    <strong>Q5: What are the top 3 transaction signals that indicate fraud?</strong><br>
    <em>Answer:</em> 
    1. <strong>Internal Risk Score (~50%)</strong>: Behavioral profile deviation.<br>
    2. <strong>Failed Login Attempts (~21%)</strong>: Credential stuffing / password guessing.<br>
    3. <strong>Transaction Hour (~14%)</strong>: Uncharacteristic midnight-to-4 AM activity.
  </div>

  <div style="margin-top: 30px; padding: 16px; background: #0f172a; color: #e2e8f0; border-radius: 8px; text-align: center; font-size: 9pt;">
    <strong>SENTINEL AI — INTELLIGENT BANKING FRAUD DETECTION &amp; PREVENTION PLATFORM</strong><br>
    Full-Stack Machine Learning Architecture • Production Verified • Ready for Presentation
  </div>
</div>

</body>
</html>
"""

html_path = os.path.abspath("Sentinel_AI_Documentation.html")
pdf_path = os.path.abspath("Sentinel_AI_Complete_Documentation.pdf")

print("Writing styled HTML documentation...")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("Compiling PDF with headless Chrome...")
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
cmd = [
    chrome_path,
    "--headless=new",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_path}",
    html_path
]

res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
print("Chrome exit code:", res.returncode)
if os.path.exists(pdf_path):
    print(f"SUCCESS: PDF created at '{pdf_path}' (Size: {os.path.getsize(pdf_path):,} bytes)")
else:
    print("ERROR: PDF was not generated.")
