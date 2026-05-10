from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__, template_folder="templates", static_folder="static")

with open("heart_artifact.pkl", "rb") as f:
    artifact = pickle.load(f)

models = artifact["models"]
feature_cols = artifact["feature_cols"]
ranges = artifact["ranges"]
cv_scores = artifact["cv_scores"]
selected_model = artifact["selected_model"]

cat_cols = artifact["cat_cols"]
cat_maps = artifact["cat_maps"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["GET", "POST"])
def predict():
    allowed = {c: list(cat_maps[c].keys()) for c in cat_cols}

    if request.method == "GET":
        return render_template("predict.html", ranges=ranges, allowed=allowed)

    row = {}
    for col in feature_cols:
        raw = request.form.get(col, "").strip()
        if raw == "":
            return render_template("predict.html", ranges=ranges, allowed=allowed,
                                   error=f"Missing value: {col}")

        # Categorical: map string -> code
        if col in cat_cols:
            if raw not in cat_maps[col]:
                return render_template("predict.html", ranges=ranges, allowed=allowed,
                                       error=f"Invalid value for {col}: {raw}")
            row[col] = int(cat_maps[col][raw])
            continue

        # Numeric
        try:
            val = float(raw)
        except ValueError:
            return render_template("predict.html", ranges=ranges, allowed=allowed,
                                   error=f"Invalid number for {col}")

        # Make 0 behave like missing for these (so pipeline KNNImputer fills)
        if col in ["Cholesterol", "RestingBP"] and val == 0:
            val = np.nan

        row[col] = val

    X_input = pd.DataFrame([row], columns=feature_cols)

    all_results = {}
    for name, pipe in models.items():
        pred = int(pipe.predict(X_input)[0])
        proba = float(pipe.predict_proba(X_input)[0][1])
        all_results[name] = {
            "pred": pred,
            "proba": proba,
            "cv_score": float(cv_scores.get(name)) if cv_scores.get(name) is not None else None
        }

    final_proba = all_results[selected_model]["proba"]
    final_pred = 1 if final_proba >= 0.5 else 0

    return render_template(
        "result.html",
        selected_model=selected_model,
        all_results=all_results,
        final_pred=final_pred,
        final_proba=final_proba
    )


if __name__ == "__main__":
    app.run(debug=True)
