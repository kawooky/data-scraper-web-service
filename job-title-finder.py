from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

job_title = 'Software Developer'
city = 'Leeds'

url = f'https://www.itjobswatch.co.uk'


all_rows = []
all_job_titles= []

# url = f'https://www.itjobswatch.co.uk/default.aspx?q=&ql={job_title.replace(" ", "+")}&ll={city.replace(" ", "+")}&id=0&p=6&e=5&sortby=&orderby='



def extract_rows(table):
    rows = table.find_all('tr')
    data = [[cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])] for row in rows]
    return data[2:-1]  # Exclude the last sublist which contains pagination info

def get_next_page_link(soup):
    return soup.find('a', string='Next')
    

def fetch_page(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

soup = fetch_page(url)

while True:
    table = soup.find('table')
    all_rows.extend(extract_rows(table))
    next_page_link = get_next_page_link(soup)
    if next_page_link:
        soup = fetch_page('https://www.itjobswatch.co.uk/' + next_page_link['href'])
    else:
        break


all_job_titles = [entry[0] for entry in all_rows]


print(all_job_titles)

print("Length of the list:", len(all_job_titles))

# Convert the array to a JSON string
json_data = json.dumps(all_job_titles)

# Write the JSON string to a file
with open('job_titles.json', 'w') as file:
    file.write(json_data)