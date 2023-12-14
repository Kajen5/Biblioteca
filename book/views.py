from django.shortcuts import render
import re
from os import scandir, getcwd, listdir
from os.path import abspath
from book.models import index_objeto

path = "/run/media/canc/h/Proyectos/prueba01"

def carpeta_lista(book_id):
    lista = ls(path + r"/book/static/book")
    beta = listdir(lista[book_id])
    r = re.compile(r"(\d+)_\d+.txt")
    beta.remove("enlaces.txt")
    beta.sort(key=lambda x: float(r.search(x).group(1)))
    h = 0
    aux = []
    capitulos = []
    for i in beta:
        g = re.search(r"(\d+)_", i).group(1)
        if h == g:
            aux.append(i)
            if i == beta[-1]:
                r = re.compile(r"\d+_(\d+).txt")
                aux.sort(key=lambda x: float(r.search(x).group(1)))
                capitulos += aux
        else:
            if len(aux) > 0:
                r = re.compile(r"\d+_(\d+).txt")
                aux.sort(key=lambda x: float(r.search(x).group(1)))
                capitulos += aux
                aux = []
            h = g
            aux.append(i)
    return capitulos


def ls(path):
    return [abspath(arch.path) for arch in scandir(path) if not arch.is_file()]


def book_completo(item, book_id):
    lista = carpeta_lista(book_id)
    chap_range = dict()
    c = lista.index(item)
    numero = len(lista)
    chap_range = {
        'has_prev': lista[c - 1][:-4] if c > 0 else None,
        'has_next': lista[c + 1][:-4] if (c + 1) < len(lista) else None}
    return chap_range


def book_index(request, book_id):
    lista = ls(path + r"/book/static/book")
    lista_book = list()
    novel = lista[book_id].split('/')[-1]
    try:
        f = open(path + r"/book/static/book" + '/' +
                 novel + '/' +
                 "enlaces.txt", "r", encoding="utf-8")
        text = f.read()
        pag_padres = re.findall(
            r"book cargada -->>(\d+) Titulo: (.*?)\n(.*?)Link de book -->>",
            text, re.DOTALL)
        for numero, book, chapters in pag_padres:
            lista_chapters = re.findall(
                r'(\d+?_\d+?).txt -- (.*?)\n', chapters)
            lista_book.append((numero, book, lista_chapters))
        f.close()
    except Exception as e:
        print(e)
        pass
    return render(request, 'book/book_index.html', {'novel': novel, 'lista': lista_book})


def book_id(request, book_id, chapter):
    lista = ls(path + r"/book/static/book")
    novel = lista[book_id].split('/')[-1]
    try:
        f = open(path + r"/book/static/book" + '/' +
                 novel + '/' + chapter + ".txt", "r", encoding="utf-8")
        text = f.read()
    except Exception as e:
        f = open(path + r"/book/static/book" + '/' +
                 novel + '/' + chapter + ".txt", "r")
        text = f.read()
    pag_padres = re.search(
        "Titulo: (.*?)\nConenido:\n(.*?)\n<--final-->",
        text, re.DOTALL)
    titulo = pag_padres.group(1)
    contenido = pag_padres.group(2)
    f.close()
    return render(request, 'book/book_show.html',
                  {'novel': novel, 'titulo': titulo,
                   'contenido': contenido,
                   'barra': book_completo(chapter + ".txt", book_id),
                   'numero': book_id})


def index(request):
    lista = ls(path + r"/book/static/book")
    carpetas = []
    for i in lista:
        carpetas.append(index_objeto(i.split('/')[-1], lista.index(i)))
    context = {
        'carpetas': carpetas
    }
    return render(request, 'book/index.html', context)
