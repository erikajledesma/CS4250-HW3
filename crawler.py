import re
from urllib.request import urlopen
from pymongo import MongoClient
from bs4 import BeautifulSoup
from collections import deque

# creating database connection object using pymongo

DB_NAME = "hw3"
DB_HOST = "localhost"
DB_PORT = 27017

try:
    client = MongoClient(host=DB_HOST, port=DB_PORT)
    db = client[DB_NAME]
    pages = db['pages']
except:
    print("Database not connected successfully")

# define re for easier access to expression

html_shtml = r'^.*\.s?html\/?$'
cpp_full_address = r'^https?:\/\/www.cpp.edu'
relative_url = r'^(?!https?:\/\/www.)'
cpp_base =  "https://www.cpp.edu/"

# initialize frontier
frontier = deque()
frontier.append('https://www.cpp.edu/sci/computer-science/')
visited = set()

while frontier:
    # get the next URL from the queue
    url = frontier.popleft()
    html = urlopen(url)
    data = html.read()
    
    bs = BeautifulSoup(html, 'html.parser')

    # check if url was already visited
    if url in visited:
        continue

    # mark current url as visited
    # visited.add(url)
    # frontier.append(url)

    # store page url and html on mongo db
    pages.insert_one({ 'url': url, 'html': data.decode('utf-8') })

    # check if target is found
    target = bs.find('h1', {'class': 'cpp-h1'}, string='Permanent Faculty')
    if target:
        pages.insert_one({ 'url': url, 'html': data.decode('utf-8'), 'isTarget': True })
        # clear frontier
        frontier = deque()
        break
    else:
        pages.insert_one({ 'url': url, 'html': data.decode('utf-8') })
        linked_urls = []

        a_tag = bs.find_all('a', href=True)

        #for each url not visited through parsed html
        for tag in a_tag:
            url = tag['href'].strip()

            if re.match(r'^.*\/$', url):
                    url = url[:-1]

            # add base address to relative address
            if re.match(relative_url, url):
                # clean / in beginning of relative url
                if re.match(r'^\/', url):
                        url = url[1:]

                # clean urls that start with ~
                if re.match(r'^~', url):
                    url = url[1:]

                url = cpp_base + url
                
            # ensure that links are html, shtml or cpp only
            if re.match(html_shtml, url) and re.match(cpp_full_address, url):
                # append url to visited array
                if url not in linked_urls:
                     linked_urls.append(url)

        for url in linked_urls:
            if url not in visited:
                visited.add(url)
                frontier.append(url)

