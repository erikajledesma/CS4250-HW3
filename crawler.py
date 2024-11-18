import re
from urllib.request import urlopen;
from pymongo import MongoClient;
from bs4 import BeautifulSoup;
from collections import deque;

# html = urlopen('https://www.cpp.edu/sci/computer-science/')

# creating database connection object using pymongo

DB_NAME = "hw3"
DB_HOST = "localhost"
DB_PORT = 27017

try:
    client = MongoClient(host=DB_HOST, port=DB_PORT)
    db = client[DB_NAME]
    # return db
except:
    print("Database not connected successfully")

# initialize frontier
frontier = deque();
visited = set();
frontier.append('https://www.cpp.edu/sci/computer-science/');
target = 'https://www.cpp.edu/sci/computer-science/';

while frontier:
    # get the next URL from the queue
    url = frontier.popleft()
    html = urlopen(url)
    data = html.read()
    
    bs = BeautifulSoup(html, 'html.parser')

    # if current url visited, continue
    visited.add(url)

    # store page url and html on mongo db
    db.pages.insert_one({"url": url, "html": str(html)})

    if target :
        # targetFound = true
        # clear frontier
        frontier = deque()
        break
    else:
        #for each url not visited through parsed html
        # url = 
        frontier.append(url)

