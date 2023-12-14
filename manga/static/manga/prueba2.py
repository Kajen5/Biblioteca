import re
import os
from urllib.request import urlopen, Request
import threading as th
from time import sleep

# class h():

#     def __init__(self):
#         pass

#     def download_archivo(self, url, NOMBRE):
#         print("Descarga iniciada -->>\t" + NOMBRE)
#         data1 = self.leyendoPagina(url, 30)
#         f = open(NOMBRE, 'wb')
#         f.write(data1)
#         print("\t Descarga completada -->>\t" + NOMBRE)

#     def leyendoPagina(self, link, timeout):
#         try:
#             Pagina = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
#             Data = urlopen(Pagina, timeout=timeout).read()
#         except Exception as e:
#             print("Reintentando... " + str(e))
#             sleep(2)
#             Data = self.leyendoPagina(link, timeout)
#         return Data


# if __name__ == '__main__':
#     hola = h()
#     hola.download_archivo(
#         "https://heavenmanga.ca/content/upload/file/2017/11/10/the-gamer-chap-23-page-2.jpg", "pruebss.jpg")
def hola():
    cadena = "Yuukyuu no Gusha Asley no, Kenja no Susume Vol. 3 Ch. 18"
    hola = re.search(r'.+?(?<![Vv]ol\.)(?<![Vv]olumen) (\d+\.*\d*)(?!\d*?;).*?',cadena)
    return hola

if __name__ == '__main__':
    print(hola().group(1))

