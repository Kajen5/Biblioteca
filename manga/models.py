from django.db import models


class manga_objeto:
    """docstring for manga_objeto"""
    nombre = str()
    numero = int()

    def __init__(self, nombre, numero):
        self.nombre = nombre
        self.numero = numero


class chapter:
    chap = 0
    pags = ()

    def __init__(self, chap, pags):
        self.chap = chap
        self.pags = pags



# Create your models here.
