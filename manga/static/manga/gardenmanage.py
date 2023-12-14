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
        self.base = self.leyendoPagina(base, timeout=25).decode(
            'utf-8', "backslashreplace")
        print("Conexion exitosa")
        if titulo:
            self.titu = titulo
        else:
            titu = re.search(r'<TITLE>(.*?) - Read', self.base)
            self.titu = titu.group(1)
        print("Pagina encontrada")
        print(self.titu)

    def obtener_link(self, start=0):
        pag_padres = re.findall(
            r'">.+?(?<![Vv]ol)(?<![Vv]olumen)\.* *(\d+\.*\d*)(?!\d*?;).*?</a></td>\n<td><a href="(.*?)"', self.base)
        print(len(pag_padres))
        for i in pag_padres:
            print(i)
        print("Links padres encontrados")
        pag_padres.reverse()
        linkBase = "https://taadd.com"
        for pag_padre in pag_padres:
            (numero, link_padre) = pag_padre
            # numero = ('%.15f' % (float(numero) + 1)).rstrip('0').rstrip('.')
            if not float(numero) >= start:
                continue
            # if not float(numero) <= 81:
            #     continue
            tuples = list()
            data2 = self.leyendoPagina(
                linkBase + link_padre, 10).decode('utf-8')
            print("Pagina padre cargada -->>" + numero)
            link_imagen = re.search(
                r'Page .*?">\n<meta property="og:image" ' +
                r'content="(.*?)">', data2)
            tuples.append((link_imagen.group(1), str(1)))
            print((link_imagen.group(1), str(1)))
            otro = re.search(
                r'id="page" onchange=".*?">\n<option value=".*?" ' +
                r'selected>1</option>\n(.*?)\n</select>\s *<a class="blue',
                data2, re.DOTALL)
            if otro:
                otros_link = re.findall(
                    r'<option value="(.+)">\d+</option>', otro.group(1))
                hilos = []
                philo = None
                for link in otros_link:
                    hilo = th.Thread(target=self.hilo_busqueda,
                                     args=(link, philo, tuples))
                    hilo.start()
                    philo = hilo
                    hilos.append(hilo)
                    # if len(hilos) > 6 and len(hilos) < len(otros_link) - 1:
                    if len(hilos) > 6:
                        hilos[-7].join()
                hilos[-1].join()
            print("Link de imagenes cargada -->>" + numero)
            print("\n")
            self.lista.append([numero, tuples])
            self.guardar()
        print("lista de enlaces guardada")

    def hilo_busqueda(self, link, philo, tupla):
        imagen = self.busqueda_secundaria(link)
        # if int(imagen[1]) > 2:
        #     hilos[int(imagen[1]) - 3].join()
        if philo:
            philo.join()
        print(imagen)
        tupla.append(imagen)

    def busqueda_secundaria(self, link):
        Data = self.leyendoPagina(link, 10).decode('utf-8')
        link_imagen = re.search(
            r'Page (\d+)\">\n<meta property="og:image" ' +
            'content="(.*?)">', Data)
        pag = link_imagen.group(1)
        imagen = (link_imagen.group(2), pag)
        return imagen

    def leyendoPagina(self, link, timeout):
        for k in range(10):
            try:
                Pagina = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
                Data = urlopen(Pagina, timeout=timeout).read()
                return Data
            except Exception as e:
                print("Reintentando... " + str(e))
                sleep(2)
        raise Exception("xD")

    def download_carpeta(self, cantidad=4):
        print("<<--- Comenzando descargas --->>\n")
        path = os.getcwd()
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
        for i in range(cantidad):
            hilos[i].join()
        os.chdir(path)

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
        lista = list()
        if not nombre:
            nombre = self.titu
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
        except:
            pass
        return lista

    def comprobar(self):
        i = len(os.listdir("."))
        h = sum(len(x[1]) for x in self.lista)
        print(i, h)

    def replace(s):
        str = ""
        for x in s:
            if x == "-5":
                str += ""
            else:
                str += x
        return str


if __name__ == '__main__':
    enlace = "https://www.taadd.com/book/My+Three+Thousand+Years+To+The+Sky.html"
    h = Descargar(enlace)
    # h.lista_guardada()
    h.obtener_link()
    h.download_carpeta()
    h.comprobar()
