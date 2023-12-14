import re
import os
from urllib.request import urlopen, Request, build_opener, HTTPCookieProcessor, HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, install_opener
from urllib.parse import urlencode
from http.cookiejar import CookieJar
import threading as th
from time import sleep
import requests
import json


class Descargar():
    """docstring for ClassName"""
    titu = None
    lista_book = list()
    base = None
    strTitulo= re.compile(r'<title>(.*?)</title>')

    def __init__(self, base, titulo=None):
        self.login('https://lnmtl.com/auth/login',{
            # 'email': 'ngcesarng@yahoo.es',
            # 'password': 'lncesarmtl/5'
            'email': 'dipu@algomatrix.co',
            'password': 'twill1123'})
        self.base = self.leyendoPagina(base, timeout=25)
        if titulo is not None:
            self.titu = titulo
        else:
            titu = re.search(self.strTitulo, self.base)
            self.titu = self.replace(titu.group(1))
        print("Pagina encontrada")
        print(self.titu)


    def login(self, link_auth, body):
        requests.urllib3.disable_warnings()
        self.headers = {'accept': 'text/html,application/xhtml+xml,application/xml',
                        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
        response = requests.get(
            link_auth, headers=self.headers, verify=False)
        self.headers['cookie'] = '; '.join(
            [x.name + '=' + x.value for x in response.cookies])
        headers = self.headers.copy()
        headers['content-type'] = 'application/x-www-form-urlencoded'
        body['_token'] = re.search(r'name="_token" value="(.*?)">',
                          response.text).group(1)
        print('Attempt login...')
        response = requests.post(
            link_auth, data=body, headers=headers, verify=False)
        self.headers['cookie'] = '; '.join(
            [x.name + '=' + x.value for x in response.cookies])

    def obtener_link(self, start=0):
        # obtener volumenes
        contendor = re.search(
            r';lnmtl.volumes = (.*?);lnmtl.route = ', self.base).group(1)
        print("Links padres encontrados")
        vols = json.loads(contendor)
        for idvol, vol in enumerate(vols):
            print(idvol)
            if int(idvol) <= 27:
                continue
            print('Book --> ' + str(idvol))
            i = 1
            lista = list()
            hilos = []
            link = 'https://lnmtl.com/chapter?page={}&volumeId={}'.format(
                i, vol['id'])
            pag_padre = json.loads(
                self.leyendoPagina(link, 10))
            # obtener chapters
            for h in pag_padre['data']:
                if not h['number']: continue
                print((h['number'] + " --- " + h['title']))
                lista.append([h['slug'], h['title']])
            # obtener continuacion de chapters
            while i < pag_padre['last_page']:
                link = 'https://lnmtl.com/chapter?page={}&volumeId={}'.format(
                    i + 1, vol['id'])
                hilo = th.Thread(target=self.hilo_busqueda,
                                 args=(link, hilos, lista))
                hilo.start()
                hilos.append(hilo)
                if i > 6 and i < pag_padre['last_page'] - 1:
                    hilos[i - 7].join()
                i += 1
                sleep(1)
            # esperar a que termine de adquirir
            if len(hilos) > 0:
                hilos[len(hilos) - 1].join()
            # añade la lista completa
            self.lista_book.append([idvol, vol['title'], lista])
            print('Book --> ' + str(idvol) + '\n\n')
        print("lista de enlaces guardada")


    def hilo_busqueda(self, link, hilos, tupla):
        imagen = json.loads(self.leyendoPagina(link, 10))
        if imagen['current_page'] > 2:
            hilos[imagen['current_page'] - 3].join()
        # obtener chapters
        for h in imagen['data']:
            if not h['number']: continue
            print((h['number'] + " --- " + h['title']))
            tupla.append([h['slug'], h['title']])


    # def hilo_busqueda_all_book(self, Padre, hilos, tupla, i):
    #     book = re.search(r'-book-(\d+)-', Padre).group(1)
    #     if not book:
    #         book = 0
    #     chapter = re.search(r'-chapter-(\d+)', Padre).group(1)
    #     if i > 0:
    #         hilos[i - 1].join()
    #     print("Pagina padre cargada -->>" + book)
    #     for pagina in imagen_list:
    #         print(pagina)
    #     print("Link de imagenes cargada -->>" + book)
    #     print("\n")
    #     tupla.append([book, imagen_list])

    # def hilo_busqueda_all(self, Padre, hilos, tupla, i):
    #     link, numero = Padre
    #     imagen_list = self.busqueda_secundaria_all(link)
    #     if i > 0:
    #         hilos[i - 1].join()
    #     print("Pagina padre cargada -->>" + numero)
    #     for pagina in imagen_list:
    #         print(pagina)
    #     print("Link de imagenes cargada -->>" + numero)
    #     print("\n")
    #     tupla.append([numero, imagen_list])
    #     self.guardar()

    def busqueda_secundaria_all_book(self, link):
        Data = self.leyendoPagina(link, 10).decode('utf-8')
        titulo = re.search(
            r'<h4 class="">(.*?)</h4>', Data, re.DOTALL)
        content = re.search(r'<div class="fr-view">\n(.*?)\n<a href="')
        chapter = {'titulo': titulo, 'content': content}
        return chapter

    # def busqueda_secundaria_all(self, link):
    #     imagen_list = list()
    #     Data = self.leyendoPagina(link, 10).decode('utf-8')
    #     link_imagen = re.search(
    #         r'<center>(.*?)</center', Data, re.DOTALL)
    #     pag_padres = re.findall(r'src=["\'](.*?)["\']', link_imagen.group(1))
    #     pag = 1
    #     for link in pag_padres:
    #         imagen = (link, str(pag))
    #         imagen_list.append(imagen)
    #         pag += 1
    #     return imagen_list

    def leyendoPagina(self, link, timeout):
        try:
            Data = requests.get(link, headers=self.headers).text
        except Exception as e:
            print("Reintentando... " + str(e))
            sleep(3)
            Data = self.leyendoPagina(link, timeout)
        return Data

    def download_carpeta_book(self, cantidad=7):
        print("<<--- Comenzando descargas --->>\n")
        directorio = os.path.join(self.titu)
        if not os.path.isdir(directorio):
            os.mkdir(directorio)
        os.chdir(directorio)
        self.guardar()
        hilos = []
        cola = []
        for i in range(cantidad):
            h = th.Thread(target=self.otro, args=(cola, ))
            hilos.append(h)
            hilos[i].start()
            sleep(4)
        for i in range(cantidad):
            hilos[i].join()

    def otro(self, cola):
        for numero, titulo, links in self.lista_book:
            for link, titulo in links:
                chapter = re.search(r'chapter-(\d+)', link).group(1)
                if link in cola:
                    continue
                cola.append(link)
                nombre = "{}_{}.txt".format(numero, chapter)
                if not os.path.isfile(nombre):
                    self.download_archivo(
                        "https://lnmtl.com/chapter/" + link, str(nombre))
                cola.remove(link)

    def download_archivo(self, url, NOMBRE):
        print("Descarga iniciada -->>\t" + NOMBRE)
        data1 = self.leyendoPagina(url, 60)
        f = open(NOMBRE, 'w', encoding="utf-8")
        titulo = re.search(
            r'<span class="chapter-title" data-content=".*?">(.*?)</span> </h4>', data1).group(1)
        try:
            content = re.search(
                r'</div>   (.*?)  <nav> <ul class="pager">', data1, re.DOTALL).group(1)
        except Exception as e:
            print(data1)
            raise e
        f.write("Titulo: " + titulo + "\n")
        f.write("Conenido:\n" + remove_html_tags(content) + "\n<--final-->")
        f.close()
        print("\t Descarga completada -->>\t" + NOMBRE)

    def guardar(self):
        f = open("enlaces.txt", 'w', encoding="utf-8")
        f.write(self.titu + "\n\n")
        for numero, titulo, chapter in self.lista_book:
            f.write("book cargada -->>{} Titulo: {}\n".format(numero, titulo))
            for link, titulo in chapter:
                chapt = re.search(r'-chapter-(\d+)', link).group(1)
                f.write("{}_{}.txt -- {} {}\n".format(numero, chapt, numero, titulo))
            f.write("Link de book -->>{}\n\n".format(numero))
        f.close()
        print("lista de enlaces guardada")

    # def lista_guardada(self, nombre=None):
    #     if not nombre:
    #         nombre = self.titu
    #     lista = list()
    #     try:
    #         f = open("enlaces.txt", "r")
    #         text = f.read()
    #         pag_padres = re.findall(
    #             r"padre cargada -->>(\d+\.*\d*)\n(.*?)\nLink", text, re.DOTALL)
    #         for pag_padre in pag_padres:
    #             (numero, link_padres) = pag_padre
    #             print("Pagina padre cargada -->>" + numero)
    #             tuples = re.findall(r"\('(.*?)', '(\d+)'\)", link_padres)
    #             self.lista.append((numero, tuples))
    #             for row in tuples:
    #                 print(row)
    #             print("Link de imagenes cargada -->>" + numero)
    #             print("\n")
    #         f.close()
    #     except Exception as e:
    #         pass

    def comprobar(self):
        i = len(os.listdir("."))
        h = sum(len(x[2]) for x in self.lista_book)
        print(i, h)

    def replace(self, s):
        cadena = ""
        for x in s:
            if x == ":" or x == '?':
                pass
            else:
                cadena += x
        return cadena


# def hola():
#     numero = 18
#     i = 1883
#     lista = []
#     lista_final = []
#     while i < 3444:
#         url = "https://lnmtl.com/chapter/emperor-s-domination-chapter-" + \
#             str(i)
#         nombre = str(numero) + "_" + str(i) + ".txt"
#         lista.append((url, i))
#         i += 1
#         if (i % 100) == 0:
#             lista_final.append((numero, lista))
#             print((numero, lista))
#             numero += 1
#             lista = []
#     lista_final.append((numero, lista))

def remove_html_tags(text):
    """Remove html tags from a string"""
    h = {
        ('</span.*?>', ''),
        ('<span.*?>', ''),
        ('style=.*?>', '>'),
        ('data-title=', 'data-content='),
        ('<sentence', '<p'),
        ('</sentence', '</p'),
        ('dir="ltr"', ''),
        ('</p>.*?<p', '</p><p')
    }
    for i, k in h:
        clean = re.compile(i)
        text = re.sub(clean, k, text)
    return text

