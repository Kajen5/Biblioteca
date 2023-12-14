import re
import os
from urllib.request import urlopen, Request
import threading as th
from time import sleep


class Descargar():
    """docstring for ClassName"""
    titu = None
    lista = list()
    base = None

    def __init__(self, base, titulo=None):
        self.base = self.leyendoPagina(base, timeout=25).decode('utf-8')
        print("Conexion exitosa")
        if titulo is not None:
            self.titu = titulo
        else:
            titu = re.search(r'<h1 class="name bigger">(.*?)</h1>', self.base)
            self.titu = self.replace(titu.group(1))
        print("Pagina encontrada")
        print(self.titu)


    def obtener_link(self, start=0):
        '''
        pag_padres = []
        pagination = re.findall(r'"page-numbers" href="(.*?)">', self.base).reverse()
        print(pagination)
        if pagination:
            for i in pagination:
                k = self.leyendoPagina(i, timeout=25).decode('utf-8')
                pag_padres.append(re.findall(
            r'2 class="chap"><a href="(.*?)">.*? Chap (\d+\.*\d*).*?<span', k).reverse())
                print(pag_padres)
                print("\n\n<---------------->\n")
        pag_padres.append(re.findall(
            r'2 class="chap"><a href="(.*?)">.*? Chap (\d+\.*\d*).*?<span', self.base).reverse())
        print(pag_padres)
        '''
        pag_padres = re.findall(
            r'2 class="chap"><a href="(.*?)">.*? Chap.*? (\d+\.*\d*).*?<span', self.base)
        print("Links padres encontrados")
        pag_padres.reverse()
        hilos = []
        i = 0
        for pag_padre in pag_padres:
            (link_padre, numero) = pag_padre
            if not float(numero) >= start:
                continue
            hilo = th.Thread(target=self.hilo_busqueda_all,
                             args=(pag_padre, hilos, self.lista, i))
            hilo.start()
            hilos.append(hilo)
            if i > 6 and i < len(pag_padres) - 1:
                hilos[i - 7].join()
            i += 1
            sleep(0.5)
        hilos[len(hilos) - 1].join()
        print("lista de enlaces guardada")

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

    def busqueda_secundaria_all(self, link):
        imagen_list = list()
        Data = self.leyendoPagina(link, 10).decode('utf-8')
        link_imagen = re.search(
            r'<center>(.*?)</center></br>', Data, re.DOTALL)
        pag_padres = re.findall(r'src=["\'](.*?)["\']', link_imagen.group(1))
        pag = 1
        for link in pag_padres:
            imagen = (link, str(pag))
            imagen_list.append(imagen)
            pag += 1
        return imagen_list

    def leyendoPagina(self, link, timeout):
        try:
            Pagina = Request(link, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0',
        'Cookie':'__cfduid=db4b9e5a81b45a08258afbf40dfcd6eca1571286124; cf_clearance=c9ae64239339bd8092dd7e3ba552982b29da4e22-1571317616-0-150; _ga=GA1.2.1197880204.1571286191; _gid=GA1.2.1548739479.1571286191; PHPSESSID=n308icgbnioa03mhon5e7498u3; _gat_gtag_UA_138663173_1=1'})
            Data = urlopen(Pagina, timeout=timeout).read()
        except Exception as e:
            print("Reintentando... " + str(e))
            sleep(3)
            Data = self.leyendoPagina(link, timeout)
        return Data

    def download_carpeta(self, cantidad=4):
        print("<<--- Comenzando descargas --->>\n")
        directorio = os.path.join(self.titu)
        if not os.path.isdir(directorio):
            os.mkdir(directorio)
        os.chdir(directorio)
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
        for capitulo in self.lista:
            (numero, imagenes) = capitulo
            for imagen in imagenes:
                (link_imagen, pag) = imagen
                if link_imagen in cola:
                    continue
                cola.append(link_imagen)
                nombre = self.titu + "_" + \
                    str(numero) + "_" + str(pag) + ".jpg"
                if not os.path.isfile(nombre):
                    self.download_archivo(link_imagen, str(nombre))
                cola.remove(link_imagen)

    def download_archivo(self, url, NOMBRE):
        print("Descarga iniciada -->>\t" + NOMBRE)
        temp = re.search(r'.*?url=(.*)', url)
        if temp:
            url = temp.group(1)
        data1 = self.leyendoPagina(url, 60)
        f = open(NOMBRE, 'wb')
        f.write(data1)
        f.close()
        print("\t Descarga completada -->>\t" + NOMBRE)

    def guardar(self):
        f = open(self.titu + "-enlaces.txt", 'w')
        for capitulo in self.lista:
            (numero, imagenes) = capitulo
            f.write("Pagina padre cargada -->>" + numero + "\n")
            for imagen in imagenes:
                f.write(str(imagen) + "\n")
            f.write("Link de imagenes cargada -->>" + numero + "\n\n")
        f.close()
        pass

    def lista_guardada(self, nombre=None):
        if not nombre:
            nombre = self.titu
        lista = list()
        try:
            f = open(nombre + "-enlaces.txt", "r")
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
        h = sum(len(x[1]) for x in self.lista)
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
    enlace = "http://ww7.heavenmanga.org/the-world-is-overflowing-with-monster-im-taking-a-liking-to-this-life/"
    h = Descargar(enlace)
    # h.lista_guardada()
    h.obtener_link(3)
    h.download_carpeta()
    h.comprobar()
