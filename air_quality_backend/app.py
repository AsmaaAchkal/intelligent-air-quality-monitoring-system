from flask import Flask, request, jsonify
import joblib
import numpy as np
import os
import csv
from datetime import datetime

app = Flask(__name__)

# =============================
# Charger modèle et scaler
# =============================
model = joblib.load("random_forest_air_quality_model.joblib")
scaler = joblib.load("scaler.joblib")

# =============================
# Fichier historique
# =============================
DATA_FILE = "air_quality_history.csv"

# Créer le fichier s’il n’existe pas
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp",
            "temperature",
            "humidity",
            "mq2",
            "air_quality"
        ])


# =============================
# Dernière mesure
# =============================
latest_data = {}
latest_result = {}

# Mapping des classes
LABELS = ["Dangerous", "Good", "Moderate", "Poor"]

# Routes
@app.route("/")
def home():
    return "API Qualité de l'air - Random Forest opérationnelle"

@app.route("/predict", methods=["POST"])
def predict():
    global latest_data, latest_result

    data = request.get_json()
    print("📥 Données reçues :", data)

    try:
        temperature = float(data["temperature"])
        humidity = float(data["humidity"])
        mq2 = float(data["mq2"])
    except (KeyError, TypeError, ValueError) as e:
        return jsonify({
            "error": "Données invalides",
            "details": str(e),
            "received": data
        }), 400

    # Préparation données
    X = np.array([[temperature, humidity, mq2]])
    X_scaled = scaler.transform(X)

    # Prédiction IA
    pred_class = model.predict(X_scaled)[0]
    pred_label = LABELS[pred_class]

    # Sauvegarde dernière mesure
    latest_data = {
        "temperature": round(temperature, 2),
        "humidity": round(humidity, 2),
        "mq2": int(mq2)
    }

    latest_result = {
        "air_quality": pred_label,
    }

    # Sauvegarde HISTORIQUE CSV
    with open(DATA_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            round(temperature, 2),
            round(humidity, 2),
            int(mq2),
            pred_label
        ])


    # Réponse vers ESP32 / Frontend
    return jsonify({
        "air_quality": pred_label,
    }), 200

@app.route("/latest", methods=["GET"])
def latest():
    if not latest_data:
        return jsonify({"message": "Aucune donnée reçue"}), 404

    return jsonify({
        **latest_data,
        **latest_result
    })

@app.route("/history", methods=["GET"])
def history():
    if not os.path.exists(DATA_FILE):
        return jsonify([])

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        data = list(reader)

    return jsonify(data)


# Lancement serveur
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
