import re
import os
from urllib.request import urlopen, Request
import threading as th
from time import sleep
import json


class Descargar():
    """docstring for ClassName"""
    titu = None
    lista_book = list()
    base = None

    def __init__(self, base, titulo=None):
        numero = re.search(r'(\d+)', base).group(0)
        link = 'https://jpmtl.com/v2/book/' + numero
        self.base = json.loads(
            self.leyendoPagina(link, timeout=25).decode('utf-8'))
        print("Conexion exitosa")
        if titulo is not None:
            self.titu = titulo
        else:
            # titu = re.search(
            #     r'<h1 class="book-sidebar__title".*?>(.*?)</h1>', self.base)
            titu = self.base['title']
            self.titu = self.replace(titu) + "-JPMTL"
        print("Pagina encontrada")
        print(self.titu)

    def obtener_link(self, start=0):
        # obtener volumenes
        #pag_padres = re.findall(r'lume__item"(.*?)</ol></li>', self.base)
        link = 'https://jpmtl.com/v2/chapter/' + \
            self.base + \
            '/list?state=published&structured=true&direction=false'
        chapters = self.leyendoPagina(link, timeout=25).decode('utf-8')
        pag_padres = json.loads(chapters)
        print("Links padres encontrados")
        lista = list()
        for key, pag_padre in enumerate(pag_padres):
            # book = re.search(
            #     r'volume__title">Volume (\d+) (.*?)</div>', pag_padre)
            print(f"Volume {key}: {pag_padre['volume_title']}")
            # obtener capitulos
            enlaces = pag_padre['chapters']
            # comprueba que sean chapters
            for e in enlaces:
                print("\tChapter {}: {}".format(e['index'], e['title']))
                lista.append([str(e['id']), str(e['index']), e['title']])
            if len(pag_padres) > 1:
                # añade la lista completa
                self.lista_book.append(
                    [str(key), pag_padre['volume_title'], lista])
            else:
                nChap = 45
                if len(lista) > nChap:
                    chapters = [lista[i:i + nChap]
                                for i in range(0, len(lista), nChap)]
                else:
                    chapters = [lista]
                for n, k in enumerate(chapters):
                    # if n < 6:
                    #     continue
                    self.lista_book.append([str(n), 'None', k])
            lista = list()
        print("lista de enlaces guardada")

    # def hilo_busqueda_all_book(self, Padre, hilos, tupla, i):
    #     book = re.search(r'-book-(\d+)-', Padre).group(1)
    #     if not book:
    #         book = 0
    #     chapter = re.search(r'chapter-(.+)', Padre).group(1)
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

    # def busqueda_secundaria_all_book(self, link):
    #     Data = self.leyendoPagina(link, 10).decode('utf-8')
    #     titulo = re.search(
    #         r'<h4 class="">(.*?)</h4>', Data, re.DOTALL)
    #     content = re.search(r'<div class="fr-view">\n(.*?)\n<a href="')
    #     chapter = {'titulo': titulo, 'content': content}
    #     return chapter

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
            Pagina = Request(link, headers={
                             'User-Agent': 'Mozilla/5.0', 'laravel_session': 'MTE1YmNmZjI0YWE0ZjdlMDNhYmVhNGQzMyJ9'})
            Data = urlopen(Pagina, timeout=timeout).read()
        except Exception as e:
            print("Reintentando... " + str(e))
            sleep(3)
            Data = self.leyendoPagina(link, timeout)
        return Data

    def download_carpeta_book(self, cantidad=8):
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
            for link, chapter, titulo in links:
                if link in cola:
                    continue
                cola.append(link)
                nombre = str(numero) + "_" + str(chapter) + ".txt"
                if not os.path.isfile(nombre):
                    self.download_archivo(
                        'https://jpmtl.com/v2/chapter/' + link, str(nombre))
                cola.remove(link)

    def download_archivo(self, url, NOMBRE):
        print("Descarga iniciada -->>\t" + NOMBRE)
        data1 = self.leyendoPagina(url, 60).decode('utf-8')
        f = open(NOMBRE, 'w', encoding="UTF-8")
        data = json.loads(data1)['chapter']
        content = ""
        lg = self.base['language']
        for p in data['content']:
            content += f"<p class=\"{lg}\">{p['original']}</p><p>{p['content']}</p>"
        f.write("Titulo: " + data['title'] + "\n")
        f.write("Conenido:\n" + content + "\n<--final-->")
        f.close()
        print("\t Descarga completada -->>\t" + NOMBRE)

    def guardar(self):
        f = open("enlaces.txt", 'w', encoding="utf-8")
        f.write(self.titu + "\n\n")
        for capitulo in self.lista_book:
            (numero, titulo, chapter) = capitulo
            f.write("book cargada -->>" + numero + " Titulo: " + titulo + "\n")
            for link, chapt, titulo in chapter:
                f.write(str(str(numero) + "_" + str(chapt) +
                            ".txt") + " -- " + titulo + "\n")
            f.write("Link de book -->>" + numero + "\n\n")
        f.close()

    def lista_guardada(self, nombre=None):
        if not nombre:
            nombre = self.titu
        lista = list()
        try:
            f = open("enlaces.txt", "r")
            text = f.read()
            pag_padres = re.findall(
                r"padre cargada -->>(\d+\.*\d*)\n(.*?)\nLink", text, re.DOTALL)
            for pag_padre in pag_padres:
                (numero, link_padres) = pag_padre
                print("Pagina padre cargada -->>" + numero)
                tuples = re.findall(r"\('(.*?)', '(\d+)'\)", link_padres)
                self.lista.append((numero, tuples))
                for row in tuples:
                    print(row)
                print("Link de imagenes cargada -->>" + numero)
                print("\n")
            f.close()
        except Exception as e:
            pass

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


# def remove_html_tags(text):
#     """Remove html tags from a string"""
#     h = {
#         ('</span.*?>', ''),
#         ('<span.*?>', ''),
#         ('style=.*?>', '>'),
#         ('<sentence', '<p'),
#         ('</sentence', '</p'),
#         ('dir="ltr"', ''),
#         ('</p>.*?<p', '</p><p')
#     }
#     for i, k in h:
#         clean = re.compile(i)
#         text = re.sub(clean, k, text)
#     return text


if __name__ == '__main__':
    enlace = "https://jpmtl.com/books/27/"

    h = Descargar(enlace)
    h.obtener_link()
    h.download_carpeta_book()
    h.comprobar()
