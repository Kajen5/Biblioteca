import asyncio
import random
import time
import re
from urllib.request import urlopen, Request
from time import sleep

url = 'https://www.taadd.com/chapter/XieYanChuanShou9/808918/'
async def worker(name, queue):
    while True:
        # Get a "work item" out of the queue.
        link = await queue.get()

        # Sleep for the "sleep_for" seconds.
        # await asyncio.sleep(sleep_for)

        h = busqueda_secundaria(link)
        # Notify the queue that the "work item" has been processed.
        queue.task_done()

        print(f'{name} has slept for {h} ')
        tuples = list()



async def main():
    # Create a queue that we will use to store our "workload".
    queue = asyncio.Queue()

    # Generate random timings and put them into the queue.
    numero = "2"
    total_sleep_time = 0
    sleep_for = 2
    tuples = list()
    data2 = leyendoPagina(url, 10).decode('utf-8')
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
        for _ in otros_link:
            queue.put_nowait(_)
    print("ok")
    # Create three worker tasks to process the queue concurrently.
    tasks = []
    for i in range(3):
        task = asyncio.create_task(worker(f'worker-{i}', queue))
        tasks.append(task)

    # Wait until the queue is fully processed.
    started_at = time.monotonic()
    await queue.join()
    total_slept_for = time.monotonic() - started_at

    # Cancel our worker tasks.
    for task in tasks:
        task.cancel()
    # Wait until all worker tasks are cancelled.
    await asyncio.gather(*tasks, return_exceptions=True)

    print('====')
    print(f'3 workers slept in parallel for {total_slept_for:.2f} seconds')
    print(f'total expected sleep time: {total_sleep_time:.2f} seconds')


async def leyendoPagina(link, timeout):
    for k in range(10):
        try:
            Pagina = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
            Data = urlopen(Pagina, timeout=timeout).read()
            return Data
        except Exception as e:
            print("Reintentando... " + str(e))
            sleep(2)
    raise Exception("xD")


async def busqueda_secundaria(link):
    Data = await leyendoPagina(link, 10).decode('utf-8')
    link_imagen = re.search(
        r'Page (\d+)\">\n<meta property="og:image" ' +
        'content="(.*?)">', Data)
    pag = link_imagen.group(1)
    imagen = (link_imagen.group(2), pag)
    return imagen
asyncio.run(main())
