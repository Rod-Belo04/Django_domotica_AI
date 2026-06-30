from django.db import models

class Thermo(models.Model):
    Data = models.DateTimeField()
    Temperatura = models.FloatField()

class Irrigazione(models.Model):
    Data = models.DateTimeField()
    valido = models.BooleanField()

class ConsumoElettrico(models.Model):
    Data = models.DateTimeField()
    Consumo = models.FloatField()