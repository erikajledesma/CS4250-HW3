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
    professors = db['professors']
except:
    print("Database not connected successfully")

# find the target document in the pages collection
target = pages.find_one({'isTarget': True})
target_content = target['html']

# use BeautifulSoup to parse through html of target page
bs = BeautifulSoup(target_content, 'html.parser')



