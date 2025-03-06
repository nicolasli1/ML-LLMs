# Usa una imagen de Python liviana
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos necesarios
COPY requirements.txt .
COPY challenge challenge
COPY model.pkl .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto en el que corre FastAPI
EXPOSE 8080

# Comando para ejecutar la API
CMD ["uvicorn", "challenge.api:app", "--host", "0.0.0.0", "--port", "8080"]
