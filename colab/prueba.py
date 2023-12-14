import re
from os import scandir, getcwd, listdir, walk
from os.path import abspath
import json
from time import sleep
from urllib.request import urlopen, Request


def carpeta_lista(book_id):
    lista = ls(r"G:\Proyectos\prueba01\book\static\book")
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
    chap_range[item] = {
        'has_prev': lista[c - 1] if c > 0 else None,
        'has_next': lista[c + 1] if c < len(lista) else None}
    return chap_range


def prueba1():
    contendor = "[{'id': 5937, 'novel_id': '331', 'title': None, 'slug': 'lord-of-the-mysteries-volume-1', 'number': '1', 'is_fake': '0', 'created_at': '2018-12-24 07:20:18', 'updated_at': '2018-12-24 07:20:18'} {'id': 5946, 'novel_id': '331', 'title': None, 'slug': 'lord-of-the-mysteries-volume-2', 'number': '2', 'is_fake': '0', 'created_at': '2018-12-24 07:20:44', 'updated_at': '2018-12-24 07:20:44'}{'id': 5959, 'novel_id': '331', 'title': None, 'slug': 'lord-of-the-mysteries-volume-3', 'number': '3', 'is_fake': '0', 'created_at': '2018-12-24 07:21:16', 'updated_at': '2018-12-24 07:21:16'}{'id': 6127, 'novel_id': '331', 'title': None, 'slug': 'lord-of-the-mysteries-volume-4', 'number': '4', 'is_fake': '0', 'created_at': '2019-02-20 15:11:14', 'updated_at': '2019-02-20 15:11:14'}{'id': 6295, 'novel_id': '331', 'title': None, 'slug': 'lord-of-the-mysteries-volume-5', 'number': '5', 'is_fake': '0', 'created_at': '2019-04-06 05:07:19', 'updated_at': '2019-04-06 05:07:19'}{'id': 5937, 'novel_id': '331', 'title': None, 'slug': 'lord-of-the-mysteries-volume-1', 'number': '1', 'is_fake': '0', 'created_at': '2018-12-24 07:20:18', 'updated_at': '2018-12-24 07:20:18'}]"
    print("Links padres encontrados")
    vols = json.loads(contendor)
    for i in vols:
        print(i)
    for idvol, vol in enumerate(vols):
        print(vol)
        pag = 0        
        lista = list()
        while True:
            link = 'https://lnmtl.com/chapter?page={}&volumenId={}'.format(
                pag, vol['id'])
            pag_padre = json.loads(
                self.leyendoPagina(link, 10))
            for i in pag_padre:
                lista.append([i['slug'], i['title']])
            if pag_padre['current_page'] >= pag_padre['last_page']:
                break
            pag += 1
        self.lista_book.append([idvol, vol['title'], lista])
    print("lista de enlaces guardada")

def prueba2(hola):
    hola['hola'] = 156
    print(hola)

def prueba3(hola):
    print(leyendoPagina(hola, 10).decode('utf-8'))

def leyendoPagina( link, timeout = 30):
    try:
        Pagina = Request(link, headers={'User-Agent': 'Mozilla/5.0','laravel_session':'MTE1YmNmZjI0YWE0ZjdlMDNhYmVhNGQzMyJ9'})
        Data = urlopen(Pagina, timeout=timeout).read()
    except Exception as e:
        print("Reintentando... " + str(e))
        sleep(3)
        Data = leyendoPagina(link, timeout)
    return Data

def prueba4():
    h = {(1,5),(6,5)}
    i = {(6,9)}
    h.add(i)

if __name__ == '__main__':
    b = '''<a href="https://s3.us-south.cloud-object-storage.appdomain.cloud/btc-certificates/0bf1a50d-9f25-4aa5-b828-901982dd7824.pdf" target="_blank" rel="noopener noreferrer" class="css-1xl6vsh"><div class="css-1qtkp2j"><p class="css-65bj4q">Desafío 1</p></div></a><a href="https://s3.us-south.cloud-object-storage.appdomain.cloud/btc-certificates/22422958-e62e-4673-b568-3096c62043d6.pdf" target="_blank" rel="noopener noreferrer" class="css-1xl6vsh"><div class="css-1qtkp2j"><p class="css-65bj4q">Desafío 2</p></div></a><a href="https://s3.us-south.cloud-object-storage.appdomain.cloud/btc-certificates/7c4a4a38-162f-466f-9e9b-31893cdd4e9d.pdf" target="_blank" rel="noopener noreferrer" class="css-1xl6vsh"><div class="css-1qtkp2j"><p class="css-65bj4q">Desafío 3</p></div></a><a href="https://s3.us-south.cloud-object-storage.appdomain.cloud/btc-certificates/699b3520-3d48-4c24-ad4d-3a23166a7992.pdf" target="_blank" rel="noopener noreferrer" class="css-1xl6vsh"><div class="css-1qtkp2j"><p class="css-65bj4q">Desafío 4</p></div></a><a href="https://s3.us-south.cloud-object-storage.appdomain.cloud/btc-certificates/5ce4c215-c94b-4b4a-8821-633de2cc5319.pdf" target="_blank" rel="noopener noreferrer" class="css-1xl6vsh"><div class="css-1qtkp2j"><p class="css-65bj4q">Desafío 5</p></div></a><a href="https://s3.us-south.cloud-object-storage.appdomain.cloud/btc-certificates/bcaed313-b82f-4b7d-8887-09e89b6ccf57.pdf" target="_blank" rel="noopener noreferrer" class="css-1xl6vsh"><div class="css-1qtkp2j"><p class="css-65bj4q">Desafío 6</p></div></a><a href="https://s3.us-south.cloud-object-storage.appdomain.cloud/btc-certificates/da977191-baae-43c6-993a-3f72dfbdd861.pdf" target="_blank" rel="noopener noreferrer" class="css-1xl6vsh"><div class="css-1qtkp2j"><p class="css-65bj4q">Desafío 7</p></div></a>'''
    k = re.findall(r'href="(.*?)".*?<p class="css-65bj4q">(.*?)</p>',b)
    print(k)
    for i, NOMBRE in k:
        print(NOMBRE)
        data1 = leyendoPagina(i, 30)
        f = open(NOMBRE + '.pdf', 'wb')
        f.write(data1)

