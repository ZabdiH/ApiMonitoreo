from datetime import datetime

def FormatearTimestamp(ts_str):
    try:
        # Formato esperado de entrada
        dt = datetime.strptime(ts_str, "%d/%m/%Y %H:%M:%S")
        # Convertir al formato ISO 8601
        return dt.strftime("%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return ts_str
