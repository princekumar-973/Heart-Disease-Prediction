import pickle
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import accuracy_score, roc_auc_score


# =========================================================
# 1) Load dataset (heart.csv)
# =========================================================
heart_df = pd.read_csv("heart.csv")
heart_df.columns = [c.strip() for c in heart_df.columns]

print("Shape:", heart_df.shape)

# =========================================================
# 2) Checks (as you asked)
# =========================================================
print("\n#checking the null values")
print(heart_df.isnull().sum())

print("\n#checking the dublicate")
print("Duplicates:", heart_df.duplicated().sum())

print("\n#checking no. of unoque value in each feature")
print(heart_df.nunique())

# Drop duplicates if any (safe)
heart_df = heart_df.drop_duplicates().reset_index(drop=True)

# =========================================================
# 3) Converting Categorical Variables to Numeric
#    (store mapping for Flask)
# =========================================================
cat_col = ["Sex", "ChestPainType", "RestingECG", "ExerciseAngina", "ST_Slope"]
cat_maps = {}

print("\nConverting Categorical Variables to Numeric")
for col in cat_col:
    print(col)
    print((heart_df[col].unique()), list(range(heart_df[col].nunique())))

    uniq = list(heart_df[col].unique())
    mapping = {k: i for i, k in enumerate(uniq)}
    cat_maps[col] = mapping

    # Safer than replace (avoids future downcast surprises)
    heart_df[col] = heart_df[col].map(mapping).astype("int32")

    print("*" * 90)
    print()

# =========================================================
# 4) Replace 0 -> NaN for columns where 0 means missing
# =========================================================
print("Cholesterol value_counts (top):")
print(heart_df["Cholesterol"].value_counts().head(10))

heart_df["Cholesterol"].replace(0, np.nan, inplace=True)
heart_df["RestingBP"].replace(0, np.nan, inplace=True)

print("NaNs after 0->NaN (Cholesterol, RestingBP):")
print(heart_df[["Cholesterol", "RestingBP"]].isna().sum())

# =========================================================
# 5) Train/test split
# =========================================================
TARGET = "HeartDisease"
X = heart_df.drop(columns=[TARGET])
y = heart_df[TARGET].astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

# =========================================================
# 6) ONLY 4 models (with preprocessing in pipeline)
#    KNNImputer is inside pipeline => no data leakage
# =========================================================
imputer = KNNImputer(n_neighbors=3)

models = {
    "logistic_regression": Pipeline([
        ("imputer", imputer),
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter=5000))
    ]),
    "svm": Pipeline([
        ("imputer", imputer),
        ("scaler", StandardScaler()),
        ("model", SVC(kernel="rbf", probability=True, random_state=42))
    ]),
    "random_forest": Pipeline([
        ("imputer", imputer),
        ("model", RandomForestClassifier(n_estimators=400, random_state=42))
    ]),
    "decision_tree": Pipeline([
        ("imputer", imputer),
        ("model", DecisionTreeClassifier(random_state=42))
    ]),
}

# =========================================================
# 7) CV scoring + fit
# =========================================================
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

cv_scores = {}
trained_models = {}

for name, pipe in models.items():
    cv_auc = float(cross_val_score(pipe, X, y, cv=cv, scoring="roc_auc").mean())
    cv_scores[name] = cv_auc

    pipe.fit(X_train, y_train)
    trained_models[name] = pipe

selected_model = max(cv_scores, key=cv_scores.get)

print("\nCV ROC-AUC scores:", cv_scores)
print("Selected model:", selected_model)

# =========================================================
# 8) Test metrics
# =========================================================
test_metrics = {}
for name, pipe in trained_models.items():
    y_pred = pipe.predict(X_test)
    y_proba = pipe.predict_proba(X_test)[:, 1]

    acc = float(accuracy_score(y_test, y_pred))
    auc = float(roc_auc_score(y_test, y_proba))

    test_metrics[name] = {"accuracy": acc, "roc_auc": auc}

print("\nTest metrics:", test_metrics)

# =========================================================
# 9) ChangeColumns type to int (except Oldpeak) - FIXED
#    (Your earlier error came because NaN cannot be cast to int)
# =========================================================
temp_df = heart_df.copy()

imputer_for_types = KNNImputer(n_neighbors=3)
temp_df[:] = imputer_for_types.fit_transform(temp_df)  # fills NaNs first

withoutOldPeak = temp_df.columns.drop("Oldpeak")
temp_df[withoutOldPeak] = temp_df[withoutOldPeak].round(0).astype("int32")

# (Optional) save this cleaned version if you want to inspect it
# temp_df.to_csv("heart_after_impute_int.csv", index=False)

# =========================================================
# 10) Save artifact for Flask
# =========================================================
# Ranges for UI validation (based on original dataframe after encoding)
ranges = {c: (float(heart_df[c].min()), float(heart_df[c].max()))
          for c in heart_df.columns if c != TARGET}

artifact = {
    "feature_cols": X.columns.tolist(),
    "cat_cols": cat_col,
    "cat_maps": cat_maps,
    "ranges": ranges,
    "models": trained_models,
    "cv_scores": cv_scores,
    "test_metrics": test_metrics,
    "selected_model": selected_model
}

with open("heart_artifact.pkl", "wb") as f:
    pickle.dump(artifact, f)

print("\nSaved: heart_artifact.pkl")
