import re
import os
from urllib.request import urlopen, Request
import threading as th
from time import sleep


class Descargar():
    """docstring for ClassName"""
    titu = None
    lista_book = list()
    base = None

    def __init__(self, base, titulo=None):
        self.base = self.leyendoPagina(base, timeout=25).decode('utf-8')
        print("Conexion exitosa")
        if titulo is not None:
            self.titu = titulo
        else:
            titu = re.search(r'novel_title">(.*?)</p>', self.base)
            self.titu = self.replace(titu.group(1))
        print("Pagina encontrada")
        print(self.titu)

    def obtener_link(self, start=0):
        pag_padres = re.findall(
            r'chapter_title">(.*?)</div>(.*?)(?<!--index_box-->)<div', self.base, re.DOTALL)
        i = 0
        lista = []
        if pag_padres:
            print("Links padres encontrados")
            for titu, pag_padre in pag_padres:
                enlaces = re.findall(
                r'<dd class="subtitle">\n<a href="(.*?)">(.*?)</a>', pag_padre, re.DOTALL)
                if start != 0:
                    for link, titulo in enlaces:
                        k = re.search(r'/.*?/(\d+)/', link).group(1)
                        if int(k) < start:
                            print(k)
                            continue
                        lista.append((link, titulo))
                else:
                    lista = enlaces
                self.lista_book.append([i, titu, lista])
                i += 1
                lista = []
        else:
            enlaces = re.findall(
                r'<dd class="subtitle">\n<a href="(.*?)">(.*?)</a>', self.base, re.DOTALL)
            if start != 0:
                for link, titulo in enlaces:
                    k = re.search(r'/.*?/(\d+)/', link).group(1)
                    if int(k) < start:
                        continue
                    lista.append((link, titulo))
            else:
                lista = enlaces
            self.lista_book.append([0, "hola", lista])
        print("lista de enlaces guardada")

    def hilo_busqueda_all_book(self, Padre, hilos, tupla, i):
        book = re.search(r'-book-(\d+)-', Padre).group(1)
        if not book:
            book = 0
        chapter = re.search(r'/.*?/(\d+)/', Padre).group(1)
        if i > 0:
            hilos[i - 1].join()
        print("Pagina padre cargada -->>" + book)
        for pagina in imagen_list:
            print(pagina)
        print("Link de imagenes cargada -->>" + book)
        print("\n")
        tupla.append([book, imagen_list])

    def hilo_busqueda_all(self, Padre, hilos, tupla, i):
        link, numero = Padre
        imagen_list = self.busqueda_secundaria_all(link)
        if i > 0:
            hilos[i - 1].join()
        print("Pagina padre cargada -->>" + numero)
        for pagina in imagen_list:
            print(pagina)
        print("Link de imagenes cargada -->>" + numero)
        print("\n")
        tupla.append([numero, imagen_list])
        self.guardar()

    def busqueda_secundaria_all_book(self, link):
        Data = self.leyendoPagina(link, 10).decode('utf-8')
        titulo = re.search( r'vel_subtitle">(.*?)</p>', Data).group(1)
        content = re.search(r'(<div id="novel_honbun.*?)<div class="novel_bn">', Data, re.DOTALL).group(1)
        chapter = {'titulo': titulo, 'content': content}
        return chapter

    def busqueda_secundaria_all(self, link):
        imagen_list = list()
        Data = self.leyendoPagina(link, 10).decode('utf-8')
        link_imagen = re.search(
            r'<center>(.*?)</center', Data, re.DOTALL)
        pag_padres = re.findall(r'src=["\'](.*?)["\']', link_imagen.group(1))
        pag = 1
        for link in pag_padres:
            imagen = (link, str(pag))
            imagen_list.append(imagen)
            pag += 1
        return imagen_list

    def leyendoPagina(self, link, timeout):
        try:
            Pagina = Request(link, headers={'User-Agent': 'Mozilla/5.0','laravel_session':'MTE1YmNmZjI0YWE0ZjdlMDNhYmVhNGQzMyJ9'})
            Data = urlopen(Pagina, timeout=timeout).read()
        except Exception as e:
            print("Reintentando... " + str(e))
            sleep(3)
            Data = self.leyendoPagina(link, timeout)
        return Data

    def download_carpeta_book(self, cantidad=4):
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
        for capitulo in self.lista_book:
            (numero, titulo, links) = capitulo
            for link, titulo in links:
                chapter = re.search(r'/.*?/(\d+)', link).group(1)
                if link in cola:
                    continue
                cola.append(link)
                nombre = str(0) + "_" + str(chapter) + ".txt"
                if not os.path.isfile(nombre):
                    self.download_archivo('https://ncode.syosetu.com'+ link, str(nombre))
                cola.remove(link)

    def download_archivo(self, url, NOMBRE):
        print("Descarga iniciada -->>\t" + NOMBRE)
        h = self.busqueda_secundaria_all_book(url)
        f = open(NOMBRE, 'w', encoding="UTF-8")
        f.write("Titulo: " + h["titulo"] + "\n")
        f.write("Conenido:\n" + h["content"] + "\n<--final-->")
        f.close()
        print("\t Descarga completada -->>\t" + NOMBRE)

    def guardar(self):
        f = open("enlaces.txt", 'w', encoding="UTF-8")
        f.write(self.titu + "\n\n")
        for capitulo in self.lista_book:
            (numero, titulo, chapter) = capitulo
            f.write("book cargada -->>" + str(numero) + " Titulo: " + titulo + "\n")
            for link, titulo in chapter:
                chapt = re.search(r'/.*?/(\d+)/', link).group(1)
                f.write(str(str(0) + "_" + str(chapt) + ".txt") + " -- " + titulo + "\n")
            f.write("Link de book -->>" + str(numero) + "\n\n")
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


if __name__ == '__main__':
    enlace = "https://ncode.syosetu.com/n3191eh/"

    h = Descargar(enlace)
    h.obtener_link()
    h.download_carpeta_book()
    h.comprobar()
