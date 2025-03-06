from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import pandas as pd
import joblib
from challenge.model import DelayModel
from pydantic import BaseModel, Field
from typing import List, Dict

# Definir la aplicación antes de usarla
app = FastAPI()

# Manejador para convertir errores de validación en 400
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={"detail": exc.errors()})

# Cargar el modelo entrenado
model = DelayModel()
try:
    model._model = joblib.load("model.pkl")
except FileNotFoundError:
    raise RuntimeError("El modelo no fue encontrado. Asegúrate de entrenarlo primero.")

# Definir el esquema de entrada con Pydantic
class FlightData(BaseModel):
    MES: int = Field(..., ge=1, le=12, description="Mes del vuelo (1-12)")
    TIPOVUELO: str = Field(..., regex="^(I|N)$", description="Tipo de vuelo: I para Internacional, N para Nacional")
    OPERA: str = Field(..., description="Nombre de la aerolínea")

# Endpoint para verificar el estado de la API
@app.get("/")
def read_root():
    return {"message": "API de predicción de retrasos en vuelos activa!!"}

# Endpoint para realizar predicciones
@app.post("/predict")
def predict(flights: Dict[str, List[FlightData]]):
    try:
        # Validar que la clave "flights" esté presente
        if "flights" not in flights:
            raise HTTPException(status_code=400, detail="Falta la clave 'flights' en la entrada")
        
        flight_list = flights["flights"]
        
        # Convertir datos de entrada a DataFrame
        input_data = pd.DataFrame([flight.dict() for flight in flight_list])
        print("📊 DataFrame recibido:\n", input_data)
        
        # Si 'Fecha-I' no está presente, asignar un valor por defecto
        if "Fecha-I" not in input_data.columns:
            input_data["Fecha-I"] = "2024-03-01T12:00:00"
            print("⚠️ 'Fecha-I' asignado por defecto")
        
        # Preprocesar los datos para adaptarlos al modelo
        features_df = model.preprocess(input_data)
        print("🔄 Features extraídas:", features_df.columns.tolist())
        
        # Realizar la predicción
        preds = model.predict(features_df)
        print("✅ Predicciones:", preds)
        
        return {"predict": preds}
    
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        print("❌ Error en /predict:", str(e))
        raise HTTPException(status_code=400, detail=str(e))
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import pandas as pd
import joblib
from challenge.model import DelayModel
from pydantic import BaseModel, Field
from typing import List, Dict

# Definir la aplicación
app = FastAPI()

# Manejador para convertir errores de validación en 400
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={"detail": exc.errors()})

# Cargar el modelo entrenado
model = DelayModel()
try:
    model._model = joblib.load("model.pkl")
except FileNotFoundError:
    raise RuntimeError("El modelo no fue encontrado. Asegúrate de entrenarlo primero.")

# Definir el esquema de entrada con validaciones de Pydantic
class FlightData(BaseModel):
    MES: int = Field(..., ge=1, le=12, description="Mes del vuelo (1-12)")
    TIPOVUELO: str = Field(..., regex="^(I|N)$", description="Tipo de vuelo: I para Internacional, N para Nacional")
    OPERA: str = Field(..., description="Nombre de la aerolínea")

# Endpoint para verificar el estado de la API
@app.get("/")
def read_root():
    return {"message": "API de predicción de retrasos en vuelos activa!!"}

# Endpoint para realizar predicciones
@app.post("/predict")
def predict(request_data: Dict[str, List[FlightData]]):
    try:
        # Validar que la clave "flights" esté presente
        if "flights" not in request_data:
            raise HTTPException(status_code=400, detail="Falta la clave 'flights' en la entrada")
        
        flights = request_data["flights"]
        
        # Convertir la lista de vuelos a DataFrame
        input_data = pd.DataFrame([flight.dict() for flight in flights])
        print("📊 DataFrame recibido:\n", input_data)
        
        # Si 'Fecha-I' no está presente, asignar un valor por defecto
        if "Fecha-I" not in input_data.columns:
            input_data["Fecha-I"] = "2024-03-01T12:00:00"
            print("⚠️ 'Fecha-I' asignado por defecto")
        
        # Si 'Fecha-O' no está presente, asignar un valor por defecto
        if "Fecha-O" not in input_data.columns:
            input_data["Fecha-O"] = "2024-03-01T13:00:00"
            print("⚠️ 'Fecha-O' asignado por defecto")
        
        # Preprocesar los datos para adaptarlos al modelo
        features_df = model.preprocess(input_data)
        print("🔄 Features extraídas:", features_df.columns.tolist())
        
        # Realizar la predicción
        preds = model.predict(features_df)
        print("✅ Predicciones:", preds)
        
        return {"predict": preds}
    
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        print("❌ Error en /predict:", str(e))
        raise HTTPException(status_code=400, detail=str(e))
