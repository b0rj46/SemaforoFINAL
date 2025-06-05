from django.db import models

class ConsumoDiario(models.Model):
    fecha_exacta = models.DateTimeField()
    precio = models.FloatField()
    peaje = models.FloatField()
    cargo = models.FloatField()

    @property
    def color_alerta(self):
        total = self.precio + self.peaje + self.cargo
        if total <= 0.10:
            return "verde"
        elif total <= 0.20:
            return "amarillo"
        else:
            return "rojo"