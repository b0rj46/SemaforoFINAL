from django.utils import timezone
from consumo.models import ConsumoDiario
import requests

PEAJE_P1 = 0.072
PEAJE_P2 = 0.038
PEAJE_P3 = 0.008
CARGO_P1 = 0.044
CARGO_P2 = 0.030
CARGO_P3 = 0.005

def obtener_precio_kwh(fecha):
    hoy = fecha.strftime("%Y%m%d")
    periodo = fecha.hour + 1
    filename = f"marginalpdbc_{hoy}.1"
    url = f"https://www.omie.es/es/file-download?filename={filename}&parents=marginalpdbc"
    headers = {"User-Agent": "Mozilla/5.0"}

    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()

    for linea in resp.text.splitlines():
        partes = linea.split(";")
        if len(partes) >= 6 and partes[0].isdigit():
            try:
                p = int(partes[3])
            except ValueError:
                continue
            if p == periodo:
                precio_mwh = float(partes[4].replace(",", "."))
                return round(precio_mwh / 1000, 5)
    raise ValueError("No se encontró el periodo en el archivo de precios.")

def obtener_peaje(fecha):
    hora = fecha.hour
    if fecha.weekday() >= 5:
        return PEAJE_P3
    elif 10 <= hora < 14 or 18 <= hora < 22:
        return PEAJE_P1
    elif 8 <= hora < 10 or 14 <= hora < 18 or 22 <= hora < 24:
        return PEAJE_P2
    return PEAJE_P3

def obtener_cargo(fecha):
    hora = fecha.hour
    if fecha.weekday() >= 5:
        return CARGO_P3
    elif 10 <= hora < 14 or 18 <= hora < 22:
        return CARGO_P1
    elif 8 <= hora < 10 or 14 <= hora < 18 or 22 <= hora < 24:
        return CARGO_P2
    return CARGO_P3

def guardar_consumo():
    fecha = timezone.now()
    try:
        precio = obtener_precio_kwh(fecha)
        peaje = obtener_peaje(fecha)
        cargo = obtener_cargo(fecha)

        ConsumoDiario.objects.create(
            fecha_exacta=fecha,
            precio=precio,
            peaje=peaje,
            cargo=cargo
        )
        print(f"Guardado: Precio={precio}, Peaje={peaje}, Cargo={cargo}")
    except Exception as e:
        print(f"Error al guardar en la base de datos: {e}")

def obtener_total_consumo():
    try:
        consumo = ConsumoDiario.objects.latest('fecha_exacta')
        total = consumo.precio + consumo.peaje + consumo.cargo
        return total
    except ConsumoDiario.DoesNotExist:
        print("No hay registros en la base de datos.")
        return None
    except Exception as e:
        print(f"Error al obtener total desde la base de datos: {e}")
        return None
