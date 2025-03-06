import pandas as pd
import numpy as np
from typing import Tuple, Union, List
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

class DelayModel:
    def __init__(self):
        self._model = None  # Aquí se almacena el modelo entrenado.
    
    def preprocess(self, data: pd.DataFrame, target_column: str = None) -> Union[Tuple[pd.DataFrame, pd.Series], pd.DataFrame]:
        data = data.copy()
        
        # Convertir fechas
        data['Fecha-I'] = pd.to_datetime(data['Fecha-I'], errors='coerce')
        data['Fecha-O'] = pd.to_datetime(data['Fecha-O'], errors='coerce')
        
        # Variables derivadas
        data['min_diff'] = (data['Fecha-O'] - data['Fecha-I']).dt.total_seconds() / 60.0
        data['delay'] = (data['min_diff'] > 15).astype(int)
        data['MES'] = data['Fecha-I'].dt.month
        
        # One-Hot Encoding para MES
        mes_dummies = pd.get_dummies(data['MES'], prefix='MES')
        data = pd.concat([data, mes_dummies], axis=1)
        
        # Variables esperadas por los tests
        data['TIPOVUELO_I'] = (data['TIPOVUELO'] == 'I').astype(int)  
        
        # Codificar OPERA (Aerolínea) con One-Hot Encoding
        opera_dummies = pd.get_dummies(data['OPERA'], prefix='OPERA')
        data = pd.concat([data, opera_dummies], axis=1)
        
        # Lista de features esperadas por los tests
        feature_cols = [
            "OPERA_Latin American Wings", 
            "MES_7", "MES_10", "MES_12", "MES_4", "MES_11", 
            "OPERA_Grupo LATAM", "OPERA_Sky Airline", "OPERA_Copa Air", 
            "TIPOVUELO_I"
        ]
        
        # Asegurar que solo están las columnas esperadas
        for col in feature_cols:
            if col not in data.columns:
                data[col] = 0
        
        features = data[feature_cols]

        # Imprimir las features generadas
        print("Features generadas:", features.columns.tolist())
        print("Número de features:", len(features.columns))

        if target_column is not None:
            target = data[[target_column]]  # Convertir a DataFrame
            return features, target
        return features
    
    def fit(self, features: pd.DataFrame, target: pd.DataFrame) -> None:
        """ Entrena el modelo con balanceo de clases. """
        self._model = RandomForestClassifier(
            random_state=42, 
            class_weight="balanced", 
            max_depth=5  # Reducimos la profundidad del árbol
        )
        self._model.fit(features, target.values.ravel())
        joblib.dump(self._model, 'model.pkl')

    def predict(self, features: pd.DataFrame) -> List[int]:
        """ Realiza predicciones sobre nuevos datos. """
        if self._model is None:
            self._model = joblib.load('model.pkl')
        return self._model.predict(features).tolist()
    
    def evaluate(self, features: pd.DataFrame, target: pd.DataFrame) -> float:
        """ Evalúa el modelo en un conjunto de prueba. """
        predictions = self.predict(features)
        return accuracy_score(target, predictions)

# Ejemplo de uso:
if __name__ == "__main__":
    data = pd.read_csv("data/data.csv", low_memory=False, dtype={"Vlo-I": str, "Vlo-O": str})
    model = DelayModel()
    features, target = model.preprocess(data, target_column="delay")
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    print("Accuracy:", model.evaluate(X_test, y_test))