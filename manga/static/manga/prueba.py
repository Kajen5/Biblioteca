
import re
from os import listdir
from os import scandir, getcwd, listdir
from os.path import abspath

class chapter:
    chap = 0
    pags = []

    def __init__(self, chap, pags):
        self.chap = chap
        self.pags = pags


def hola(h):
    beta = ls(r"G:\Proyectos\prueba01\manga\static\manga")
    lista = listdir(beta[h])
    r = re.compile(r"_(\d+\.*\d*)_")
    lista.sort(key=lambda x: float(r.search(x).group(1)))
    h = 0
    aux = []
    capitulos = []
    for i in lista:
        g = re.search(r"_(\d+\.*\d*)_", i).group(1)
        if h == g:
            aux.append(i)
            if i == lista[-1]:
                r = re.compile(r"_(\d+).jpg")
                aux.sort(key=lambda x: float(r.search(x).group(1)))
                k = chapter(h, aux)
                capitulos.append(k)
        else:
            if len(aux) > 0:
                r = re.compile(r"_(\d+).jpg")
                aux.sort(key=lambda x: float(r.search(x).group(1)))
                k = chapter(h, aux)
                capitulos.append(k)
                aux = []
            h = g
            aux.append(i)
    return capitulos


class somos:
    chap_range = dict()

    def __init__(self, lista):
        h = []
        h2 = []
        prev_chap2 = None
        chap_current = None
        prev_chap = None
        for i in range(len(lista)+1):
            if i < len(lista):
                chap_current, h = lista[i].chap, lista[i].pags
            else:
                chap_current, h = None, None
            if prev_chap:
                self.chap_range[prev_chap] = {'pages': h2, 'has_prev': prev_chap2, 'has_next': chap_current, 'current':prev_chap}
                prev_chap2 = prev_chap
            h2 = h
            prev_chap = chap_current

    def chapter(self, chap):
        return self.chap_range[chap]

    def keys(self):
        return self.chap_range.keys()


def ls(path):
    return [abspath(arch.path) for arch in scandir(path) if not arch.is_file()]


def mundo(lista):
    for a in lista:
        print(str(a.chap))
        print(str(a.pags))

def ao(k):
    h = somos(hola(k))
    e = h.chapter("22")
    for i in h.keys():
        print(i)
    print(h.keys())

if __name__ == '__main__':
    ao(5)
    ao(1)
