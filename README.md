# 🫀 Heart Disease Prediction System

> Machine learning-based web application for predicting the likelihood of heart disease using clinical health parameters and real-time user input analysis.

---

## 🚀 Live Demo

[![Live App](https://img.shields.io/badge/Live%20App-Vercel-black?style=for-the-badge&logo=vercel)](https://heart-disease-prediction-peach-five.vercel.app/)

👉 **[https://heart-disease-prediction-peach-five.vercel.app/](https://heart-disease-prediction-peach-five.vercel.app/)**

---

## 📌 Features

- ✅ Real-time heart disease risk prediction
- ✅ Interactive Flask-based web interface
- ✅ Probability-based prediction output (0–100%)
- ✅ Clinical data preprocessing and feature engineering
- ✅ Multiple machine learning model evaluation & comparison
- ✅ Automated model selection using CV ROC-AUC score
- ✅ Interactive charts (doughnut + bar) via Chart.js
- ✅ Sortable & searchable model comparison table
- ✅ Risk-level based health tips (Low / Moderate / High / Very High)
- ✅ Fully responsive design with glassmorphism UI

---

## 📊 Dataset Information

| Property | Value |
|---|---|
| Dataset | UCI Heart Disease (Cleveland) |
| Total Records | 918 clinical records |
| Input Features | 11 health parameters |
| Target Variable | `HeartDisease` (0 = No, 1 = Yes) |
| Source | `heart.csv` |

### Input Features

| Feature | Type | Description |
|---|---|---|
| Age | Numeric | Patient age in years |
| Sex | Categorical | M / F |
| ChestPainType | Categorical | ATA / NAP / ASY / TA |
| RestingBP | Numeric | Resting blood pressure (mm Hg) |
| Cholesterol | Numeric | Serum cholesterol (mg/dl) |
| FastingBS | Binary | Fasting blood sugar > 120 mg/dl (1 = True) |
| RestingECG | Categorical | Normal / ST / LVH |
| MaxHR | Numeric | Maximum heart rate achieved |
| ExerciseAngina | Categorical | Y / N |
| Oldpeak | Numeric | ST depression induced by exercise |
| ST_Slope | Categorical | Up / Flat / Down |

---

## 🧠 Machine Learning Models

| Model | Accuracy | CV ROC-AUC |
|---|---|---|
| Logistic Regression | 86.4% | 0.9040 |
| SVM (RBF Kernel) | 85.3% | 0.9130 |
| **Random Forest** ✅ | **88.6%** | **0.9270** |
| Decision Tree | 80.4% | 0.8070 |

> ✅ **Selected Model: Random Forest** (highest CV ROC-AUC)

---

## ⚙️ Preprocessing Pipeline

- **KNN Imputation** — fills missing values for `Cholesterol` and `RestingBP` (where 0 = missing)
- **Categorical Encoding** — label encoding for `Sex`, `ChestPainType`, `RestingECG`, `ExerciseAngina`, `ST_Slope`
- **Standard Scaling** — applied for Logistic Regression & SVM
- **Stratified K-Fold CV** — 5-fold, prevents data leakage (imputer inside pipeline)

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| ML | Scikit-learn, Pandas, NumPy |
| Frontend | HTML5, CSS3 (Vanilla), Chart.js |
| Deployment | Vercel |
| Version Control | Git, GitHub |

---

## 📁 Project Structure

```
heart-disease-prediction/
├── app.py                  # Flask web server & routes
├── model.py                # ML training & artifact generation
├── heart.csv               # Dataset (918 records)
├── heart_artifact.pkl      # Trained models + metadata
├── requirements.txt        # Python dependencies
├── Procfile                # Gunicorn config (Render/Heroku)
├── vercel.json             # Vercel deployment config
├── static/
│   ├── style.css           # Full CSS design system
│   └── heartvideomp4.mp4   # Background video (home page)
└── templates/
    ├── index.html          # Landing page
    ├── predict.html        # Patient input form
    └── result.html         # Prediction results + charts
```

---

## ▶️ Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/princekumar-973/Heart-Disease-Prediction.git
cd Heart-Disease-Prediction
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the Flask server

```bash
python app.py
```

### 4. Open in browser

```
http://127.0.0.1:5000
```

---

## 🌐 Deploy on Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel
```

Or connect your GitHub repo directly at [vercel.com](https://vercel.com).

---

## ⚠️ Medical Disclaimer

> This application is a **screening tool only** and is **not a substitute for professional medical advice, diagnosis, or treatment**. Always consult a qualified healthcare professional for any health concerns.

---

## 👨‍💻 Author

**Prince Kumar Ram**

[![GitHub](https://img.shields.io/badge/GitHub-princekumar--973-181717?style=flat&logo=github)](https://github.com/princekumar-973)
