import boto3
import os
from dotenv import load_dotenv
from utils import FormatearTimestamp
from boto3.dynamodb.conditions import Attr, Key
from datetime import datetime

# Cargar credenciales del archivo .env
load_dotenv()

# Crear cliente de dynamoDB
dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.getenv("REGION_NAME"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRETY_KEY"),
)

tabla = dynamodb.Table("RegistrosMonitoreoApp")

def GuardarLogs(nombre_archivo, contenido):
    archivosGuardados = True
    lineas = contenido.strip().splitlines()

    try:
        for i, linea in enumerate(lineas):
            if linea.strip():
                try:
                    pid, nombre, titulo, usuario, timestamp, url = [campo.strip() for campo in linea.split(",", 5)]
                except ValueError:
                    print(f"Línea mal formada en {nombre_archivo}: {linea}")
                    continue

                # Almacenar cada linea del archivo como un item en la tabla
                item = {
                    "id_archivo": f"{nombre_archivo}#{i}",  # Clave primaria
                    "Archivo": nombre_archivo,
                    "PID": pid,
                    "NombrePrograma": nombre,
                    "TituloVentana": titulo,
                    "Usuario": usuario,
                    "Timestamp": FormatearTimestamp(timestamp),
                    "URL": url
                }

                # Subir el item
                tabla.put_item(Item=item)
                
    except Exception as e:
        print(f"Error: {e}")
        archivosGuardados = False
        
    return archivosGuardados

def ObtenerTodos():
    response = tabla.scan()
    registros = response.get("Items", [])

    # Paginación por 1MB de datos
    while "LastEvaluatedKey" in response:
        response = tabla.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        registros.extend(response.get("Items", []))

    return registros
    
def ObtenerPorFiltros(nombre_programa=None, usuario=None, fecha_inicio=None, fecha_fin=None):
    filtros = []
    
    if nombre_programa:
        filtros.append(Attr('NombrePrograma').contains(nombre_programa))
    
    if usuario:
        filtros.append(Attr('Usuario').contains(usuario))

    if fecha_inicio and fecha_fin:
        filtros.append(Attr('Timestamp').between(fecha_inicio, fecha_fin))

    try:
        if filtros:
            # Combinar las condiciones con AND
            filtro_total = filtros[0]
            for f in filtros[1:]:
                filtro_total &= f

            response = tabla.scan(FilterExpression=filtro_total)
        else:
            response = tabla.scan()

        registros = response.get("Items", [])
        
        while "LastEvaluatedKey" in response:
            response = tabla.scan(
                FilterExpression=filtro_total,
                ExclusiveStartKey=response["LastEvaluatedKey"]
            )
            registros.extend(response.get("Items", []))

        return registros
    except Exception as e:
        print(f"Error: {e}")
        return []
    
