import boto3
from dotenv import load_dotenv
import os

# Cargar credenciales del archivo .env
load_dotenv()

def ObtenerLogsBucketS3(bucket_name):
    # Crear cliente de S3
    s3 = boto3.client("s3",
                       aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
                       aws_secret_access_key=os.getenv("AWS_SECRETY_KEY"),
                       region_name=os.getenv("REGION_NAME"))
    
    # Obtener archivos en el bucket
    objetos = s3.list_objects_v2(Bucket=bucket_name)
    archivos = []

    # Almacenar archivos y contenido dentro de la lista de archivos a retornar
    for obj in objetos.get("Contents", []):
        key = obj["Key"]
        if key.endswith(".txt"):
            contenido = s3.get_object(Bucket=bucket_name, Key=key)["Body"].read().decode("utf-8")
            archivos.append((key, contenido))
    
    return archivos