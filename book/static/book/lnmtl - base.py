import re
import os
from urllib.request import urlopen,Request, build_opener, HTTPCookieProcessor,HTTPPasswordMgrWithDefaultRealm,HTTPBasicAuthHandler,install_opener
from urllib.parse import urlencode
from http.cookiejar import CookieJar
import threading as th
from time import sleep
import requests


class Descargar():
    """docstring for ClassName"""
    titu = None
    lista_book = list()
    base = None

    def __init__(self, base, titulo=None):
        # self.base = self.leyendoPagina(base, timeout=25).decode('utf-8')
        # print("Conexion exitosa")
        # if titulo is not None:
        #     self.titu = titulo
        # else:
        #     titu = re.search(r'<h4>(.*?)</h4>', self.base)
        #     self.titu = self.replace(titu.group(1))
        # print("Pagina encontrada")
        # print(self.titu)
        # POST_LOGIN_URL = 'https://lnmtl.com/auth/login'
        requests.urllib3.disable_warnings()
        self.headers = {'accept': 'text/html,application/xhtml+xml,application/xml',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
        # response = requests.get(POST_LOGIN_URL, headers=self.headers, verify=False)
        # self.headers['cookie'] = '; '.join([x.name + '=' + x.value for x in response.cookies])
        # payload = {
        #    '_token':re.search(r'name="_token" value="(.*?)">', response.text),
        #    'email': 'ngcesarng@yahoo.es',
        #     'password': 'lncesarmtl/5'
        # }
        # header = self.headers.copy()
        # response = requests.post(POST_LOGIN_URL, data=payload, headers=header)  
        # print(response.text)
        # self.headers['cookie'] = '; '.join([x.name + '=' + x.value for x in response.cookies])

        response = requests.get('https://lnmtl.com/auth/login', headers=self.headers, verify=False)
        self.headers['cookie'] = '; '.join([x.name + '=' + x.value for x in response.cookies])
        headers = self.headers.copy()
        headers['content-type'] = 'application/x-www-form-urlencoded'
        token = re.search(r'name="_token" value="(.*?)">',response.text).group(1)
        body = {
            '_token': token,
            # 'email': 'ngcesarng@yahoo.es',
            # 'password': 'lncesarmtl/5'
            'email': 'dipu@algomatrix.co',
            'password': 'twill1123'
        }
        print('Attempt login...')
        response = requests.post('https://lnmtl.com/auth/login', data=body, headers=headers, verify=False)
        self.headers['cookie'] = '; '.join([x.name + '=' + x.value for x in response.cookies])

    def obtener_link(self, start=0):
        pag_padres = re.findall(
            r'<h4 class="panel-title">(.*?)</div>\n</div>\n</div>\n</div>\n</div>', self.base, re.DOTALL)
        print("Links padres encontrados")
        lista = list()
        for pag_padre in pag_padres:
            book = re.search(r'aria-controls="collapse-(\d+)">\n(.*?)\n ?</a>', pag_padre)
            enlaces = re.findall(r'<li class="chapter-item">\n ?<a href="(.*?)">\n ?<span>(.*?)</span>', pag_padre)
            for h, titulo in enlaces:
                chapter = re.search(r'-chapter-(\d+)', h).group(1)
                if not chapter:
                    continue
                lista.append([h, titulo])
            self.lista_book.append([book.group(1), book.group(2), lista])
            lista = list()
        print("lista de enlaces guardada")

    def hilo_busqueda_all_book(self, Padre, hilos, tupla, i):
        book = re.search(r'-book-(\d+)-', Padre).group(1)
        if not book:
            book = 0
        chapter = re.search(r'-chapter-(\d+)', Padre).group(1)
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
            r'<h4 class="">(.*?)</h4>', Data, re.DOTALL)
        content = re.search(r'<div class="fr-view">\n(.*?)\n<a href="')
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
        # postData = {
        # 'username': 'ngcesarng@yahoo.es',
        # 'password': 'lncesarmtl/5'
        # 'laravel_session': 'eyJpdiI6ImJCYlU2b0lmUTJlREl4d1pCY1FCUFE9PSIsInZhbHVlIjoiS0d0S1RPRmY3eG02NEREMjd3TlJiK1BWTUpKY2Zwd1ZDZkFKdnRRZ0JCMXV0SUtaVkhhTnBzVFdwV29na0xKOExCWm1tZ2JIZ010dzE0RnVGZ2dvc1E9PSIsIm1hYyI6IjkyMjUyYzU1Zjc4NjdjNjIxZmZmMTUxZGU5ZDYwMGJiM2U3ZmFhNTQyODMyMGYzYTBiZGQyY2Q0Mjg0ZTA2YmMifQ%3D%3D',
        # # '__cfduid':'d3e1408d23752f8a41ac2ef938bc95b7e1526963380',
        # # '_ga':'GA1.2.2022452800.1526963383',
        # # 'backgroundColor':'eyJpdiI6Ik9zQ3BsSjRZTlQ3ZDhiSkFvNUdWOGc9PSIsInZhbHVlIjoibDZUSzN2aWpYaU51dzN1TU45c2kzZz09IiwibWFjIjoiZTZkNWFhOWI2MGE2MWZmYWJlMzFhN2VkZWVlNjE5NzhlOGJiNmM5MWM0NjU1MjE1OWE5NDI4MTY5ZGNjYThmZSJ9',
        # # 'cookieconsent_status':'dismiss',
        # # 'fontColor':'eyJpdiI6IlZ2VmZIOVE1cjVGcHpPNUhIVTU5UEE9PSIsInZhbHVlIjoiWkJVTlM4RUZjUWh4U2ZmXC9URUdja2c9PSIsIm1hYyI6IjFiM2M0NjQ3MWZlM2I3ZTdlZjQxNzE2MzQ5NTgyMDEwNzQxNjkyYjBiNTNhMmQ3Y2ZiZmI4YzQ3MGVlM2IwYzAifQ%3D%3D',
        # # '_gid':'GA1.2.802783651.1541520088',
        # 'XSRF-TOKEN':'eyJpdiI6IllrMGhldXBCd1hDblpWVTdlVmk5MFE9PSIsInZhbHVlIjoiazdNTlFIb2F2RnJZK3gyeXo0VWd1QkE1WmdERmN4V1FHb1wvY1NrdlhiUDNZZkdyRVQzYmRad050dUFraXJ1ZEcyYVlkbmtsWHU2KzZWQ3lkS3g4bmZ3PT0iLCJtYWMiOiI3YzFmMTIzZDZmOWQ4YmJkMDNmMjM3NjFjZDI0MjI2Njg2ZmY5OGIzYWVmOTNiNzEyZDQzY2NlMDRkZGUzZGE5In0%3D',
        
        # 'XSRF-TOKEN' : 'eyJpdiI6InNtb3B5ckp4dHhcLzI4NzhhUWJURnFRPT0iLCJ2YWx1ZSI6InBTdGROTERSUll1aXUxWW50K3YwSGhEeTdVWHdWVFc1ZDZQdmJlOWpQek5kUVJua0RibWRpbHVVSmZWV3VZRk1oSjBTaFlFRzdzSTN0bklicU1tUUx3PT0iLCJtYWMiOiI0ZDFlZDdjOTE3ZDUyNTEwNzE0ODk3ODBlZDgyZjU4YzRmYTI0NjZmN2E5YzJlYTU5OWFiYjg1MWZjN2I5NmZmIn0%3D',           
        # '__cfduid ':'d618a46a0abbd11745e579eedeb00a04c1541542138',        
        # '_ga':'GA1.2.1331177222.1541542134',
        # '_gat' :'1',           
        # '_gid':'GA1.2.347414136.1541542134',     
        # 'backgroundColor':'eyJpdiI6Ik9zQ3BsSjRZTlQ3ZDhiSkFvNUdWOGc9PSIsInZhbHVlIjoibDZUSzN2aWpYaU51dzN1TU45c2kzZz09IiwibWFjIjoiZTZkNWFhOWI2MGE2MWZmYWJlMzFhN2VkZWVlNjE5NzhlOGJiNmM5MWM0NjU1MjE1OWE5NDI4MTY5ZGNjYThmZSJ9',
        # 'cookieconsent_status':'dismiss',            
        # 'fontColor' :  'eyJpdiI6IlZ2VmZIOVE1cjVGcHpPNUhIVTU5UEE9PSIsInZhbHVlIjoiWkJVTlM4RUZjUWh4U2ZmXC9URUdja2c9PSIsIm1hYyI6IjFiM2M0NjQ3MWZlM2I3ZTdlZjQxNzE2MzQ5NTgyMDEwNzQxNjkyYjBiNTNhMmQ3Y2ZiZmI4YzQ3MGVlM2IwYzAifQ%3D%3D',         
        # 'laravel_session':'eyJpdiI6IjlMVzU5SXhyNmgycE11RkFTazlTaXc9PSIsInZhbHVlIjoiSklsbHlWNnk3N2E4a2c5ejgzTUdOb1wvUmVpTE9nKzBGMmI3NjdLYXdPc3RVWlJkSE5pamlERlduM0lRWWg2cHloWnVZUkZWTjNySlVmTjhBTEVhZ29BPT0iLCJtYWMiOiI3YzI1MmM2MGFhYTM3MjBlZDA1NTdjYmQ0MWMwMzg2OGUxY2MyNGQ5YzJjZjQ0MWRkYTU5YmI0NzU1ZmUzYjRmIn0%3D'
        # }
        postData = None
        try:
#             header = {
#             'authority': 'lnmtl.com',
# 'method': 'GET',
# # :path: /chapter/emperor-s-domination-chapter-1807
# 'scheme': 'https',

# 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
# # 'accept-encoding': 'gzip, deflate, br',
# 'accept-language': 'es,es-419;q=0.9,en;q=0.8',
# 'cache-control': 'max-age=0',
# 'cookie': 'cookieconsent_status=dismiss; backgroundColor=eyJpdiI6Ik9zQ3BsSjRZTlQ3ZDhiSkFvNUdWOGc9PSIsInZhbHVlIjoibDZUSzN2aWpYaU51dzN1TU45c2kzZz09IiwibWFjIjoiZTZkNWFhOWI2MGE2MWZmYWJlMzFhN2VkZWVlNjE5NzhlOGJiNmM5MWM0NjU1MjE1OWE5NDI4MTY5ZGNjYThmZSJ9; fontColor=eyJpdiI6IlZ2VmZIOVE1cjVGcHpPNUhIVTU5UEE9PSIsInZhbHVlIjoiWkJVTlM4RUZjUWh4U2ZmXC9URUdja2c9PSIsIm1hYyI6IjFiM2M0NjQ3MWZlM2I3ZTdlZjQxNzE2MzQ5NTgyMDEwNzQxNjkyYjBiNTNhMmQ3Y2ZiZmI4YzQ3MGVlM2IwYzAifQ%3D%3D; _gat=1; _ga=GA1.2.1331177222.1541542134; _gid=GA1.2.347414136.1541542134; __cfduid=d618a46a0abbd11745e579eedeb00a04c1541542138; XSRF-TOKEN=eyJpdiI6InNtb3B5ckp4dHhcLzI4NzhhUWJURnFRPT0iLCJ2YWx1ZSI6InBTdGROTERSUll1aXUxWW50K3YwSGhEeTdVWHdWVFc1ZDZQdmJlOWpQek5kUVJua0RibWRpbHVVSmZWV3VZRk1oSjBTaFlFRzdzSTN0bklicU1tUUx3PT0iLCJtYWMiOiI0ZDFlZDdjOTE3ZDUyNTEwNzE0ODk3ODBlZDgyZjU4YzRmYTI0NjZmN2E5YzJlYTU5OWFiYjg1MWZjN2I5NmZmIn0%3D; laravel_session=eyJpdiI6IjlMVzU5SXhyNmgycE11RkFTazlTaXc9PSIsInZhbHVlIjoiSklsbHlWNnk3N2E4a2c5ejgzTUdOb1wvUmVpTE9nKzBGMmI3NjdLYXdPc3RVWlJkSE5pamlERlduM0lRWWg2cHloWnVZUkZWTjNySlVmTjhBTEVhZ29BPT0iLCJtYWMiOiI3YzI1MmM2MGFhYTM3MjBlZDA1NTdjYmQ0MWMwMzg2OGUxY2MyNGQ5YzJjZjQ0MWRkYTU5YmI0NzU1ZmUzYjRmIn0%3D',
# 'referer': 'https://lnmtl.com/chapter/emperor-s-domination-chapter-1806',
# 'upgrade-insecure-requests': '1',
# 'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
#             Pagina = Request(link, headers=header)
#             Data = urlopen(Pagina, timeout=timeout).read()
#             print(Data)
            # opener = build_opener(HTTPCookieProcessor(CookieJar()))
            # if postData:
            #     pData = urlencode(postData).encode("utf-8")
            # else:
            #     pData = None
            
            # httpReq = Request(link, pData, headers=header, unverifiable=True)
            # Data = opener.open(httpReq, timeout=timeout).read()
            # print(Data)
            # # create a password manager
            # password_mgr = HTTPPasswordMgrWithDefaultRealm()

            # # Add the username and password.
            # # If we knew the realm, we could use it instead of None.
            # top_level_url = 'https://lnmtl.com/auth/login'
            # password_mgr.add_password(None, top_level_url, 'ngcesarng@yahoo.es','lncesarmtl/5')

            # handler = HTTPBasicAuthHandler(password_mgr)

            # # create "opener" (OpenerDirector instance)
            # opener = build_opener(handler)
            # opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            # # use the opener to fetch a URL
            # Data = opener.open(link).read()

            # # Install the opener.
            # # Now all calls to urllib.request.urlopen use our opener.
            # install_opener(opener)
            Data = requests.get(link,headers=self.headers).text
        except Exception as e:
            print("Reintentando... " + str(e))
            sleep(3)
            Data = self.leyendoPagina(link, timeout)
        return Data

    def download_carpeta_book(self, cantidad=1):
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
        for capitulo in self.lista_book:
            (numero, links) = capitulo
            for link, chapter in links:
                if link in cola:
                    continue
                cola.append(link)
                nombre = str(numero) + "_" + str(chapter) + ".txt"
                if not os.path.isfile(nombre):
                    self.download_archivo(link, str(nombre))
                cola.remove(link)

    def prueba(self):
        self.titu = "Emperor’s Domination"
        numero = 34
        i = 3422
        directorio = os.path.join(self.titu)
        lista= []
        lista_final = []
        while i < 3444:
            url = "https://lnmtl.com/chapter/emperor-s-domination-chapter-" + str(i)
            nombre = str(numero) + "_" + str(i) + ".txt"
            lista.append((url,i))
            i += 1
            if (i % 100) == 0:
                lista_final.append((numero,lista))
                numero += 1
                lista = []
        lista_final.append((numero,lista))
        self.lista_book = lista_final


    def download_archivo(self, url, NOMBRE):
        print("Descarga iniciada -->>\t" + NOMBRE)
        data1 = self.leyendoPagina(url, 60)
        f = open(NOMBRE, 'w', encoding="utf-8")
        titulo = re.search( r'<span class="chapter-title" data-content=".*?">(.*?)</span> </h4>', data1).group(1)
        try:
            content = re.search(r'</div>   (.*?)  <nav> <ul class="pager">', data1, re.DOTALL).group(1)
        except Exception as e:
            print(data1)
            raise e
        f.write("Titulo: " + titulo + "\n")
        f.write("Conenido:\n" + remove_html_tags(content) + "\n<--final-->")
        f.close()
        print("\t Descarga completada -->>\t" + NOMBRE)

    def guardar(self):
        f = open("enlaces.txt", 'w')
        f.write(self.titu + "\n\n")
        for capitulo in self.lista_book:
            (numero, titulo, chapter) = capitulo
            f.write("book cargada -->>" + numero + " Titulo: " + titulo + "\n")
            for link, titulo in chapter:
                chapt = re.search(r'-chapter-(\d+)', link).group(1)
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
        h = sum(len(x[1]) for x in self.lista_book)
        print(i, h)

    def replace(self, s):
        cadena = ""
        for x in s:
            if x == ":" or x == '?':
                pass
            else:
                cadena += x
        return cadena
def hola():

    numero = 18
    i = 1883

    lista= []
    lista_final = []
    while i < 3444:
        url = "https://lnmtl.com/chapter/emperor-s-domination-chapter-" + str(i)
        nombre = str(numero) + "_" + str(i) + ".txt"
        lista.append((url,i))
        i += 1
        if (i % 100) == 0:
            lista_final.append((numero,lista))
            print((numero,lista))
            numero += 1
            lista = []
    lista_final.append((numero,lista))


def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<\\span.*?>')
    clean2 = re.compile('<span.*?>')
    clean3 = re.compile('style=.*?>')
    clean4 = re.compile('data-title=')
    text = re.sub(clean, '', text)
    text = re.sub(clean2, '', text)
    text = re.sub(clean3, '>', text)
    text = re.sub(clean4, 'data-content=', text)
    return text



if __name__ == '__main__':
    enlace = "https://lnmtl.com/novel/lord-of-the-mysteries"

    h = Descargar(enlace)
    h.obtener_link()
    h.download_carpeta_book()
    h.comprobar()
