from flask import Flask, render_template, request
import joblib
import pandas as pd
import requests
import os

app = Flask(__name__)

# Determine model path: allow env override, then check container path, then local project path
MODEL_PATH = os.environ.get('MODEL_PATH') or "/model/titanic_model.pkl"
# try a couple of fallbacks when running outside container
if not os.path.exists(MODEL_PATH):
    # project-relative path (when running locally)
    alt = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model', 'titanic_model.pkl')
    if os.path.exists(alt):
        MODEL_PATH = alt
    else:
        alt2 = os.path.join(os.getcwd(), 'model', 'titanic_model.pkl')
        if os.path.exists(alt2):
            MODEL_PATH = alt2

if not os.path.exists(MODEL_PATH):
    print("Warning: model not found at", MODEL_PATH, "- run train_model.py first to create it.")
    model = None
else:
    try:
        model = joblib.load(MODEL_PATH)
        print("Loaded model from", MODEL_PATH)
    except Exception as e:
        print("Failed to load model from", MODEL_PATH, ":", e)
        model = None

# DB app service name (docker-compose uses 'dbapp'). Allow overriding with DB_URL or DBAPP_HOST env vars
DB_URL = os.environ.get('DB_URL')
if not DB_URL:
    db_host = os.environ.get('DBAPP_HOST', 'dbapp')
    DB_URL = f"http://{db_host}:5001/store"
print("DB URL set to", DB_URL)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form
    # Basic preprocessing consistent with training
    df = pd.DataFrame({
        'Pclass': [int(data['Pclass'])],
        'Sex': [1 if data['Sex']=='male' else 0],
        'Age': [float(data['Age'])],
        'SibSp': [int(data['SibSp'])],
        'Parch': [int(data['Parch'])],
        'Fare': [float(data['Fare'])],
        'Embarked': [ord(data['Embarked'][0]) % 3]
    })
    if model is None:
        result = "Model not available - run training"
    else:
        pred = model.predict(df)[0]
        result = "Survived" if pred == 1 else "Did Not Survive"

    # send to DB app (best-effort; ignore errors)
    try:
        # convert ImmutableMultiDict to normal dict for JSON
        payload = {"data": {k: data[k] for k in data.keys()}, "prediction": result}
        requests.post(DB_URL, json=payload, timeout=3)
    except Exception as e:
        print("DB API failed:", e)

    return render_template('index.html', prediction=result)

if __name__ == '__main__':
    # production note: use a WSGI server for production. This is for demo.
    app.run(host='0.0.0.0', port=5000)
