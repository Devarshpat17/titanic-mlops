from flask import Flask, request, jsonify
import sqlite3, os

app = Flask(__name__)
DB_DIR = "data"
os.makedirs(DB_DIR, exist_ok=True)
DB_FILE = os.path.join(DB_DIR, "predictions.db")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pclass INT,
                    sex TEXT,
                    age FLOAT,
                    sibsp INT,
                    parch INT,
                    fare FLOAT,
                    embarked TEXT,
                    prediction TEXT
                )''')
    conn.commit()
    conn.close()

@app.route('/store', methods=['POST'])
def store():
    data = request.get_json()
    user_input, pred = data.get('data', {}), data.get('prediction', '')

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''INSERT INTO predictions 
                 (pclass, sex, age, sibsp, parch, fare, embarked, prediction)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
              (user_input.get('Pclass'), user_input.get('Sex'), user_input.get('Age'),
               user_input.get('SibSp'), user_input.get('Parch'), user_input.get('Fare'),
               user_input.get('Embarked'), pred))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "prediction": pred})

@app.route('/records', methods=['GET'])
def records():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM predictions")
    rows = c.fetchall()
    conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5001)
