from django.db import models

# Create your models here.
class index_objeto:
    """docstring for manga_objeto"""
    nombre = str()
    numero = int()

    def __init__(self, nombre, numero):
        self.nombre = nombre
        self.numero = numero