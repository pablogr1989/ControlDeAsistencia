from datetime import datetime, timedelta

def convert_to_seconds(value, unit):
    try:
        val = float(value)
    except ValueError:
        return 0
        
    unit = str(unit).lower().strip()
    if "minuto" in unit:
        return val * 60
    elif "hora" in unit:
        return val * 3600
    else:
        return val
    
def convert_time_to_seconds(obj_time_str):
    now = datetime.now()    
    try:
        obj_time = datetime.strptime(obj_time_str, "%H:%M").time()            
        obj = datetime.combine(now.date(), obj_time)            
        if obj <= now:
            obj += timedelta(days=1)
        delta = obj - now
        return delta.total_seconds()
        
    except ValueError:
        print(f"Error: Formato de hora '{obj_time_str}' inválido. Usa HH:MM.")
        return 0
    
def parsear_tiempo(tiempo_str):
    """Convierte texto como '3 minutos' a int(180)"""
    try:
        # Extraemos solo los números del string "3 minutos"
        numeros = ''.join(filter(str.isdigit, tiempo_str))
        valor = int(numeros)
        
        texto = tiempo_str.lower()
        if "hora" in texto:
            return valor * 3600
        elif "minuto" in texto:
            return valor * 60
        else:
            return valor # Asumimos segundos
    except ValueError:
        return 0