# consumo/views.py
from django.http import HttpResponse
from consumo.models import ConsumoDiario

def test_view(request):
    try:
        consumo = ConsumoDiario.objects.latest('fecha_exacta')
        total = consumo.precio + consumo.peaje + consumo.cargo
        color = consumo.color_alerta
        return HttpResponse(f"Total del último consumo: {total:.4f} — Color alerta: {color}")
    except ConsumoDiario.DoesNotExist:
        return HttpResponse("No hay datos disponibles.")
    except Exception as e:
        return HttpResponse(f"Error: {e}")
