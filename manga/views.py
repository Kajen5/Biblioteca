from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from os import scandir, listdir
from os.path import abspath, getmtime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import re
from manga.models import chapter

path = "/run/media/canc/h/Proyectos/prueba01"


def index(request):
    return HttpResponse('hola')


def manga(request):
    lista = ls(path + r"/manga/static/manga/")
    carpetas = []
    SortBy = request.POST.get('SortBy', None)
    ordenado = lista.copy()
    if SortBy == 'Release':
        ordenado.sort(key=lambda x: getmtime(x))
        ordenado = ordenado[::-1]
    for i in ordenado:
        carpetas.append({'nombre': i.split('/')[-1], 'numero': lista.index(i)})
    context = {
        # 'carpetas': [x.__dict__ for x in carpetas]
        'carpetas': carpetas
    }
    if request.method == "POST":
        # h = Template('{% for carpeta in carpetas %}<tr><th><a href="{{carpeta.numero}}">{{carpeta.nombre}}</a></th></tr>\n{% endfor %}')
        # return HttpResponse(h.render(Context(context)))
        return JsonResponse(context)
    return render(request, 'manga/index.html', context)

class manga2():
    template_name = 'manga/index.html'
    context_object_name = 'carpetas'

    def get_queryset(self):
        lista = ls(path + r"/manga/static/manga/")
        carpetas = []
        ordenado = lista.copy()
        if self.kwargs['SortBy'] == 'Release':
            ordenado.sort(key=lambda x: getmtime(x))
            ordenado = ordenado[::-1]
        for i in ordenado:
            carpetas.append({'nombre': i.split('/')[-1], 'numero': lista.index(i)})
        context = {
            # 'carpetas': [x.__dict__ for x in carpetas]
            'carpetas': carpetas
        }
        if request.method == "POST":
            # h = Template('{% for carpeta in carpetas %}<tr><th><a href="{{carpeta.numero}}">{{carpeta.nombre}}</a></th></tr>\n{% endfor %}')
            # return HttpResponse(h.render(Context(context)))
            return JsonResponse(context)
        return carpetas

def manga_id(request, manga_id):
    lista = ls(path + r"/manga/static/manga")
    beta = listdir(lista[manga_id])
    r = re.compile(r"_(\d+\.*\d*)_")
    beta.sort(key=lambda x: float(r.search(x).group(1)))
    h = 0
    aux = []
    capitulos = []
    for i in beta:
        g = re.search(r"_(\d+\.*\d*)_", i).group(1)
        if h == g:
            aux.append(
                'manga/' + lista[manga_id].split('/')[-1] + '/' + replace(i))
            if i == beta[-1]:
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
            aux.append(
                'manga/' + lista[manga_id].split('\\')[-1] + '/' + replace(i))
    page = request.GET.get('page', 1)
    paginator = Paginator(capitulos, 1)
    try:
        imagenes = paginator.page(page)
    except PageNotAnInteger:
        imagenes = paginator.page(1)
    except EmptyPage:
        imagenes = paginator.page(paginator.num_pages)
    return render(request, 'manga/manga_show.html', {'imagenes': imagenes})


def manga_id2(request, manga_id):
    lista = ls(path + r"/manga/static/manga")
    beta = listdir(lista[manga_id])
    name = lista[manga_id].split('/')[-1]
    rch = re.compile(r"_(\d+\.*\d*)_")
    rpg = re.compile(r"_(\d+).jpg")
    beta.sort(key=lambda x: float(rch.search(x).group(1)))
    h = 0
    aux = []
    capitulos = []
    chapter_objeto = None
    for i in beta:
        i = i[len(name):]
        g = rch.search(i).group(1)
        if h == g:
            aux.append(i)
            if i == beta[-1][len(name):]:
                aux.sort(key=lambda x: float(rpg.search(x).group(1)))
                k = chapter(h, aux)
                capitulos.append(k)
        else:
            if len(aux) > 0:
                aux.sort(key=lambda x: float(rpg.search(x).group(1)))
                k = chapter(h, aux)
                capitulos.append(k)
                aux = []
            h = g
            aux.append(i)
    if len(beta) == 1:
        k = chapter(h, aux)
        capitulos.append(k)
    chapter_n = request.GET.get('Chapter', 1)
    chapter_objeto = manga_completo(capitulos)
    try:
        imagenes = chapter_objeto[str(chapter_n)]
    except KeyError:
        imagenes = chapter_objeto[[*chapter_objeto][0]]
    print(imagenes)
    return render(request, 'manga/manga_show2.html',
                  {'chapter': imagenes, 'lista': chapter_objeto.keys(), 'name': name})


def replace(s):
    # eliminar las barras y los espacios
    cadena = ""
    for x in s:
        if x == "\\":
            cadena += "/"
        elif x == ' ':
            cadena += '%20'
        else:
            cadena += x
    return cadena


def ls(path):
    # obtener carpetas
    return [abspath(arch.path) for arch in scandir(path) if not arch.is_file()]


def ls2(path):
    # obtener archivos
    return [abspath(arch.path) for arch in scandir(path) if arch.is_file()]


def manga_completo(lista):
    # pagination adaptado
    chap_range = dict()
    h = []
    h2 = []
    p2 = None
    c = None
    p1 = None
    for i in range(len(lista) + 1):
        if i < len(lista):
            c, h = lista[i].chap, lista[i].pags
        else:
            c, h = None, None
        if p1:
            chap_range[p1] = {
                'pages': h2, 'has_prev': p2, 'has_next': c, 'current': p1}
            p2 = p1
        h2 = h
        p1 = c
    return chap_range


def Prueba(request):
    return render(request, 'manga/prueba.html', {})
