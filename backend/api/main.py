from fastapi import FastAPI, Body
from backend.models.model_stub import EnergyPredictor
import numpy as np

app = FastAPI()

model = EnergyPredictor()
# Simulação de treinamento inicial
X_train = np.array([[1],[2],[3],[4],[5]])
y_train = np.array([10, 20, 30, 40, 50])
model.train(X_train, y_train)

@app.get("/")
def read_root():
    return {"message": "EcoOptima AI Backend rodando!"}

@app.post("/predict")
def predict_energy(data: dict = Body(...)):
    # Espera: { "values": [6, 7, 8] }
    values = np.array(data["values"]).reshape(-1, 1)
    prediction = model.predict(values)
    return {"prediction": prediction.tolist()}
