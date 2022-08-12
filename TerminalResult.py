import requests
from lxml.html import fromstring
import lxml.html
header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        }
query = 'weight loss tips'
response = requests.get(f'https://www.google.com/search?q={query}&start=0', headers=header).text
tree = lxml.html.fromstring(response)
node = tree.xpath('//@data-q')
print(node)