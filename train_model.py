import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# Load dataset (place titanic.csv in project root)
csv_path = "titanic.csv"
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"Place 'titanic.csv' in the project root: {os.path.abspath(csv_path)}")

df = pd.read_csv(csv_path)
df = df[['Survived','Pclass','Sex','Age','SibSp','Parch','Fare','Embarked']].dropna()

le = LabelEncoder()
df['Sex'] = le.fit_transform(df['Sex'])
df['Embarked'] = le.fit_transform(df['Embarked'])

X = df.drop('Survived', axis=1)
y = df['Survived']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/titanic_model.pkl")
print("✅ Model saved at model/titanic_model.pkl")
