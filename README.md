# Titanic MLOps - WebApp + DBApp + Jenkins
## Overview
This project contains:
- `train_model.py` : trains a RandomForest on `titanic.csv` and saves `model/titanic_model.pkl`.
- `webapp/` : Flask web UI that loads model from `/model/titanic_model.pkl` and posts predictions to DB app.
- `dbapp/` : Flask DB API that stores predictions in SQLite at `./db_data/data/predictions.db` (persisted).
- `docker-compose.yml` : runs webapp + dbapp. db data persists to `./db_data`.
- `Jenkinsfile` : pipeline that clones repo, builds images, runs containers and performs basic smoke tests.

## Usage
1. Place your `titanic.csv` file in the project root (next to this README).
2. Option A: Train model locally
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r webapp/requirements.txt
    pip install -r dbapp/requirements.txt
    python train_model.py
    ```
   This creates `model/titanic_model.pkl`.
3. Option B: Use Docker Compose (if model already exists in ./model):
    ```bash
    docker-compose up --build
    ```
4. Open UI: http://localhost:5000  
   View stored predictions: http://localhost:5001/records

## Notes
- Jenkinsfile uses a placeholder repo URL; replace `yourusername` with your repo URL in Jenkins.
- SQLite data persists across container restarts in `./db_data`.
- For production, use proper model versioning (MLflow) and WSGI (gunicorn/uWSGI).
