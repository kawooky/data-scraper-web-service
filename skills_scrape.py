from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

job_title = 'Software Developer'
city = 'Leeds'

base_url = f'https://www.itjobswatch.co.uk'


url = f'https://www.itjobswatch.co.uk/default.aspx?q=&ql={job_title.replace(" ", "+")}&ll={city.replace(" ", "+")}&id=0&p=6&e=5&sortby=&orderby='

def get_skills_page_href(soup):
    return soup.find('a', string=job_title)['href']
    
def fetch_page(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

soup = fetch_page(url)


skill_soup = fetch_page(f'{base_url}{get_skills_page_href(soup)}')

itab_table = skill_soup.find('table', class_='itab')
rows = itab_table.find_all('tr')
data = [[cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])] for row in rows]

# Print out the elements for verification
print(data)

# rows=skill_soup.find_all()



# print('++++++', skill_soup.find())








