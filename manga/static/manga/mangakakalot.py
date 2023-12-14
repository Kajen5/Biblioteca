import re
import os
from urllib.request import urlopen, Request
import threading as th
from time import sleep
import cloudscraper


class Descargar():
    """docstring for ClassName"""
    titu = None
    lista = list()
    base = None
    scraper = None

    def __init__(self, base, titulo=None):
        self.scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'android',
                'desktop': False
            }
        )
        # self.base = self.leyendoPagina(base, timeout=25).decode('utf-8')
        self.base = self.leyendoPagina(base, timeout=25).text
        print("Conexion exitosa")
        if titulo:
            self.titu = titulo
        else:
            titu = re.search(r'<h1>(.*?)</h1>', self.base)
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
        aux = re.search(r'Chapter name<(.*?)<script type=',
                        self.base, re.DOTALL)
        pag_padres = re.findall(
            r"\n.*? href=\"(.*?)\" title.*?[Cc]hap.*? (\d+\.*\d*)", aux.group(1))
        print("Links padres encontrados")
        pag_padres.reverse()
        hilos = []
        philo = None
        print(len(pag_padres))
        for pag_padre in pag_padres:
            (link_padre, numero) = pag_padre
            if not float(numero) >= start:
                continue
            hilo = th.Thread(target=self.hilo_busqueda_all,
                             args=(pag_padre, philo, self.lista))
            hilo.start()
            philo = hilo
            hilos.append(hilo)
            if len(hilos) > 6:
                hilos[-7].join()
            sleep(0.5)
        hilos[-1].join()
        print("lista de enlaces guardada")

    def hilo_busqueda_all(self, Padre, philo, tupla):
        link, numero = Padre
        imagen_list = self.busqueda_secundaria_all(link)
        if philo:
            philo.join()
        print("Pagina padre cargada -->>" + numero)
        for pagina in imagen_list:
            print(pagina)
        print("Link de imagenes cargada -->>" + numero)
        print("\n")
        tupla.append([numero, imagen_list])
        # for link_imagen, pag in imagen_list:
        #     nombre = self.titu + "/" +self.titu + "_" + \
        #         str(numero) + "_" + str(pag) + ".jpg"
        #     if not os.path.isfile(nombre):
        #         self.download_archivo(link_imagen, str(nombre))
        self.guardar()

    def busqueda_secundaria_all(self, link):
        imagen_list = list()
        # Data = self.leyendoPagina(link, 10).decode('utf-8')
        Data = self.leyendoPagina(link, 10).text
        link_imagen = re.search(
            r'</iframe>(.*?)<a href=', Data, re.DOTALL)
        pag_padres = re.findall(
            r'<img src=["\'](.*?)["\']', link_imagen.group(1))
        pag = 1
        for link in pag_padres:
            temp = re.search(r'.*?url=(.*)', link)
            if temp:
                link = temp.group(1)
            imagen = (link, str(pag))
            imagen_list.append(imagen)
            pag += 1
        return imagen_list

    def leyendoPagina(self, link, timeout):
        for k in range(10):
            try:
                Data = self.scraper.get(link, timeout=timeout)
                return Data
            except Exception as e:
                print("Reintentando... " + str(e))
                sleep(2)
        raise Exception("xD")

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
        try:
            data1 = self.leyendoPagina(url, 30)
            f = open(NOMBRE, 'wb')
            f.write(data1)
            print("\t Descarga completada -->>\t" + NOMBRE)
        except:
            print("--- NO DISPONIBLE --- " + NOMBRE)

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
    enlace = "https://manganelo.com/manga/ab925267"

    h = Descargar(enlace)
    # h.lista_guardada()
    h.obtener_link()
    h.download_carpeta()
    h.comprobar()
