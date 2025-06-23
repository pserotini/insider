from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, ConfigDict
import joblib
import os
import pandas as pd
import logging
from contextlib import asynccontextmanager
from src.preprocessing import TitanicPreprocessor

# logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# variáveis globais
model = None
preprocessor = None
history = []

# schemas
class InputData(BaseModel):
    pclass: int
    name: str
    sex: str
    age: float
    sibsp: int
    parch: int                  
    ticket: str
    fare: float
    cabin: str
    embarked: str
    passengerid: int

    model_config = ConfigDict(extra="forbid") # reforçar schema

# funções de carregamento
def load_model(model_path: str = "./notebooks/pickle_files/selected_model.pkl"):
    global model
    model = joblib.load(model_path)
    logger.info(f"Modelo carregado: {model_path}")

def load_preprocessor(preprocessor_path: str = "./notebooks/pickle_files/preprocessor.pkl"):
    global preprocessor
    preprocessor = joblib.load(preprocessor_path)
    logger.info(f"Pré-processador carregado: {preprocessor_path}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_model()
    load_preprocessor()
    yield

# inicialização do fastapi com lifespan
app = FastAPI(lifespan=lifespan)

# endpoints
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(input_data: InputData, request: Request):
    if model is None or preprocessor is None:
        raise HTTPException(status_code=500, detail="Modelo ou pré-processador não carregado")

    df = pd.DataFrame([input_data.model_dump()])

    try:
        df_processed = preprocessor.transform(df)
        print(f"df_processed:{df_processed}")
    except ValueError as ve:
        logger.error(f"Value error durante pré-processamento: {ve}")
        raise HTTPException(status_code=422, detail=f"Value error durante pré-processamento: {ve}")        

    try:
        prediction = model.predict(df_processed)[0]
    except ValueError as ve:
        logger.error(f"Value error during prediction: {ve}")
        raise HTTPException(status_code=422, detail=f"Value error during prediction: : {ve}")

    entry = {
        "ip": request.client.host if request.client else None,
        "input": input_data.model_dump(),
        "prediction": int(prediction),
    }
    history.append(entry)

    logger.info(f"Predição feita: {entry}")

    return {"prediction": int(prediction)}

@app.post("/load")
def load_new_model(path: str):
    try:
        load_model(path)
        return {"status": f"Novo modelo carregado de {path}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar modelo: {e}")

@app.get("/history")
def get_history():
    return history
