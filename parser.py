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

# Use div tag clearfix to find each professor on the page

clearfix = bs.find('div', { 'id': 'main'}).find_all('div', { 'class': 'clearfix'})
# print(clearfix)

# Regular expression to extract content inside the <p> tags
# p_tag_pattern = r'<p>(.*?)</p>'

# Iterate through each professor's HTML
for prof in clearfix:
    h2_tag = prof.find('h2')
    prof_name = h2_tag.get_text(strip=True) if h2_tag else "No Name Found"

    p_tag = prof.find('p')
    p_content = p_tag.get_text(separator=' ', strip=True) if p_tag else "No Details Found"

    print(f"Professor: {prof_name}, P Content: {p_content}")



