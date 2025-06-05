from django.apps import AppConfig
from threading import Thread
import os
import time

class ConsumoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'consumo'

    def ready(self):
        if os.environ.get('RUN_MAIN') != 'true':
            return

        def guardarConsumoBucle():
            from scrapper.core import guardar_consumo
            while True:
                guardar_consumo()
                time.sleep(15 * 60)

        Thread(target=guardarConsumoBucle, daemon=True).start()
