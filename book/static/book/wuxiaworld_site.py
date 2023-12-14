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
            titu = re.search(r'<title.*?>.*?(\S.*?\S) &#8211;', self.base, re.DOTALL)
            self.titu = self.replace(titu.group(1))
        del lista_book 
        print("Pagina encontrada")
        print(self.titu)

    def obtener_link(self, start=0):
        # obtener volumenes
        print("Links padres encontrados")
        lista = list()
        book = re.search(r'<ul class="main version-chap">(.*?)</ul>', self.base, re.DOTALL)
        print(book.group(1))

        # obtener capitulos
        enlaces = re.findall(r'<a href="(.*?)">.*?(\S.*?\S)  .*?</a>', book.group(1), re.DOTALL)
        print(enlaces)
        # comprueba que sean chapters
        for h, titulo in enlaces:
            chapter = re.search(r'chapter-(\d+)', h)
            if not chapter or int(chapter.group(1)) < start:
                continue
            lista.append([h, titulo])
        # añade la lista completa
        lista = lista[::-1]
        nChap = 150
        if len(lista) > nChap:
            chapters = [lista[i:i+nChap] for i in range(0, len(lista), nChap) ]
        else:
            chapters = [lista]
        for n, k in enumerate(chapters):
            # if n < 6:
            #     continue
            self.lista_book.append([str(n), 'None', k])
            print('Book ---> ' + str(n))
            print()
            print(*[i[0] for i in k], sep='\n')
            print('Book ---> ' + str(n) + '\n\n')
        print("lista de enlaces guardada")

    def hilo_busqueda_all_book(self, Padre, hilos, tupla, i):
        book = re.search(r'-book-(\d+)-', Padre).group(1)
        if not book:
            book = 0
        chapter = re.search(r'chapter-(\d+)', Padre).group(1)
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
        titulo = re.search(
            r'<h3>(.*?)</h3>', Data, re.DOTALL)
        content = re.search(r'<div class="cha-words">\n(.*?)\n<div class="ad c-ads cust', data, re.DOTALL)
        k = {
        ('<div.*?</style>', '' )
        }
        content = remove_html_tags(content, k)
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
        try:
            for i in range(cantidad):
                h = th.Thread(target=self.otro, args=(cola, ))
                hilos.append(h)
                hilos[i].start()
                sleep(4)
            for i in range(cantidad):
                hilos[i].join()
        except Exception as e:
            raise e
        finally:
            os.getcwd() 


    def otro(self, cola):
        for numero, titulo, links in self.lista_book:
            for link, titulo in links:
                chapter = re.search(r'chapter-(\d+)', link).group(1)
                if link in cola:
                    continue
                cola.append(link)
                nombre = str(numero) + "_" + str(chapter) + ".txt"
                if not os.path.isfile(nombre):
                    self.download_archivo(link, str(nombre))
                cola.remove(link)

    def download_archivo(self, url, NOMBRE):
        print("Descarga iniciada -->>\t" + NOMBRE)
        data1 = self.leyendoPagina(url, 60).decode('utf-8')
        titulo = re.search(
            r"ted='selected'>(.*?)</option>", data1, re.DOTALL).group(1)
        content = re.search(r'(<div class="reading-content">.*?)<div class="c-select-bottom">', data1, re.DOTALL).group(1)
        k = { ('</p*?<p>', '' )}
        f = open(NOMBRE, 'w', encoding="UTF-8")
        f.write("Titulo: " + titulo + "\n")
        f.write("Conenido:\n" + remove_html_tags(content, k) + "\n<--final-->")
        f.close()
        print("\t Descarga completada -->>\t" + NOMBRE)

    def guardar(self):
        f = open("enlaces.txt", 'w', encoding="utf-8")
        f.write(self.titu + "\n\n")
        for capitulo in self.lista_book:
            (numero, titulo, chapter) = capitulo
            f.write("book cargada -->>" + numero + " Titulo: " + titulo + "\n")
            for link, titulo in chapter:
                chapt = re.search(r'chapter-(\d+)', link).group(1)
                f.write(str(str(numero) + "_" + str(chapt) + ".txt") + " -- " + titulo + "\n")
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


def remove_html_tags(text, add = None):
    """Remove html tags from a string"""
    h = {
        ('</span.*?>', ''),
        ('<span.*?>', ''),
        ('style=.*?>', '>'),
        ('data-title=', 'data-content='),
        ('<sentence', '<p'),
        ('</sentence', '</p'),
        ('dir="ltr"', ''),
        ('</p>.*?<p', '</p><p'),
        ('\n', '')
    }
    h.update(add)
    for i, k in h:
        clean = re.compile(i, re.DOTALL)
        text = re.sub(clean, k, text)
    return text


