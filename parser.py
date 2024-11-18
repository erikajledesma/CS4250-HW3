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

    # extract and parse <p> tag content
    p_tag = prof.find('p')
    
    # extract fields

    if p_tag:
        details = {}
        for strong_tag in p_tag.find_all('strong'):
            key = strong_tag.get_text(strip=True).strip(':')
            value = strong_tag.next_sibling.strip() if strong_tag.next_sibling else ""

        # Handle special cases like <a> tags for email and web
            if strong_tag.find_next('a'):
                value = strong_tag.find_next('a').get('href', value)
            details[key] = value
    else:
        details = {}
        
    # insert document into mongodb

    professors.insert_one({'name': prof_name, 'details': details})



