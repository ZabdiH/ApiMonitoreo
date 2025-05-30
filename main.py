from fastapi import FastAPI, Query, Response
from fastapi.responses import JSONResponse
from typing import Optional
from dotenv import load_dotenv
from readerS3 import ObtenerLogsBucketS3
from dynamoClient import GuardarLogs
from dynamoClient import ObtenerTodos
from dynamoClient import ObtenerPorFiltros
from fastapi.middleware.cors import CORSMiddleware
import os

# Cargar credenciales del archivo .env
load_dotenv()

BUCKET_NAME = os.getenv("BUCKET_NAME")

app = FastAPI()

# Habilitar CORS para acceder a la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Allow-Methods": "OPTIONS, GET, POST, DELETE"
}

# End Points
@app.post("/CargarLogs")
def cargar_logs_a_dynamodb():
    archivos = ObtenerLogsBucketS3(BUCKET_NAME)
    for nombre, contenido in archivos:
        GuardarLogs(nombre, contenido)
        
    return JSONResponse(
        content={"estado": "Archivos procesados y cargados en DynamoDB."},
        headers=CORS_HEADERS
    )

@app.get("/ObtenerTodos")
def listar_registros():
    return JSONResponse(
        content=ObtenerTodos(),
        headers=CORS_HEADERS
    )