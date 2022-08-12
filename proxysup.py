import requests
import threading
from lxml.html import fromstring
import lxml.html
from time import time
from queue import Queue
import logging
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

max_threads = 10 # don't go too crazy
proxy_scheme = 'http' # https, ftp

keywords_list = open('keywords.txt', 'r')
output = open('paa.txt', 'w')

# List of proxies goes in proxies.txt, format one proxy per line:
# http://username:password@ip:port
# socks5://username:password@ip:port
proxies_list = open('proxies.txt', 'r')

keywords = keywords_list.readlines()
proxies = proxies_list.readlines()

if not proxies:
    proxies = None

header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'Accept-Language': 'tr-tr,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        }

class GoogleYoinker(threading.Thread):
   def __init__(self, queue):
      threading.Thread.__init__(self)
      self.queue = queue

   def run(self):
        print ("Starting " + self.name)
        while True:
            # Get the work from the queue and expand the tuple
            keyword = self.queue.get()
            try:
                query = keyword.strip()
                if proxies is not None:
                    proxy = {proxy_scheme: proxies[random.randint(0, len(proxies) - 1)].strip()}
                    logger.info("Using Proxy {}".format(proxy))
                    response = requests.get(f'https://www.google.com/search?q={query}&start=0', headers=header, proxies=proxy).text
                else:
                    response = requests.get(f'https://www.google.com/search?q={query}&start=0', headers=header).text
                tree = lxml.html.fromstring(response)
                nodes = tree.xpath('//@data-q')

                logger.info("Keyword Processed: {}".format(query))
                output.write(query)
                output.write(": ")
                for node in nodes:
                    output.write(node)
                    output.write(" , ")
                output.write("\n")

                logger.info('Exiting: {}'.format(self.name))
            finally:
                self.queue.task_done()


def main():
    ts = time()
    queue = Queue()

    # Create up to max_threads worker threads
    for x in range(max_threads):
        worker = GoogleYoinker(queue)

        # Setting daemon to True will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()

    # Put the keywords into the queue
    for keyword in keywords:
        logger.info('Queueing keyword: {}'.format(keyword))
        queue.put((keyword.strip()))

    # Causes the main thread to wait for the queue to finish processing all the tasks
    queue.join()
    logging.info('Took %s', time() - ts)

    keywords_list.close()
    proxies_list.close()
    output.close()


if __name__ == '__main__':
    main()