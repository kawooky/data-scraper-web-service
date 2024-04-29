from flask import Flask, jsonify, request
from flask_cors import CORS , cross_origin

import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def scrape_data(job_title, city):
    url = f'https://www.itjobswatch.co.uk/default.aspx?q=&ql={job_title.replace(" ", "+")}&ll={city.replace(" ", "+")}&id=0&p=6&e=5&sortby=&orderby='
    all_rows = []

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

    return all_rows
    

@app.route('/job_data')
@cross_origin()
def get_job_data():
    job_title = request.args.get('job_title', 'Software Developer')
    city = request.args.get('city', 'Leeds')
    job_title_data = [row for row in scrape_data(job_title.replace("+", " "), city.replace("+", " ")) if row[0] == job_title]
    return jsonify(job_title_data)

if __name__ == '__main__':
    app.run(debug=True)
