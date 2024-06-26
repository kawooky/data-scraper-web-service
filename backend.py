from flask import Flask, jsonify, request
from flask_cors import CORS , cross_origin

import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
base_url = f'https://www.itjobswatch.co.uk'


def scrape_data(job_title, city):
    url = f'https://www.itjobswatch.co.uk/default.aspx?q=&ql={job_title.replace(" ", "+")}&ll={city.replace(" ", "+")}&id=0&p=6&e=5&sortby=&orderby='

    def extract_rows(table):
        rows = table.find_all('tr')
        noThTags= True
        for row in rows:
            if row.find('th'):
                print ('found 1!!!!!!!!!!!!!!')
                noThTags = False
            
        if noThTags :
            print('no th tags!')
            # Extract <p> tags from the page as the error message
            p_tags = soup.find_all('p')
            error_message = [p.get_text(strip=True) for p in p_tags][0]
            print(error_message, 'errrrrrrrr')
            return error_message
        else: 
            print('there are tags')


        data = [[cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])] for row in rows]

        print ('daaattttaaaa', data[2:-1][0])


        return data[2:-1][0]  # Exclude the last sublist which contains pagination info


    def fetch_page(url):
        response = requests.get(url)
        return BeautifulSoup(response.text, 'html.parser')

    soup = fetch_page(url)


    table = soup.find('table')

    return extract_rows(table)

def skills_scrape (job_title, city):
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

    return data
    

@app.route('/job_data')
@cross_origin()
def get_job_data():
    job_title = request.args.get('job_title', 'Software Developer')
    city = request.args.get('city', '')
    # Check if job_title is empty string, if so, assign default value
    if not job_title:
        job_title = 'Software Developer'

    # Check if city is empty string, if so, assign default value
    if not city:
        city = ''

    # Retrieve job data and replace spaces with '+' for consistency
    job_title_data = scrape_data(job_title.replace("+", " "), city.replace("+", " "))

    if type(job_title_data) == str: return jsonify({"error": job_title_data})
    
    # Call the skills_scrape function to get additional data
    additional_data = skills_scrape(job_title, city)

    # Return a nested array containing both sets of data
    return jsonify([job_title_data, additional_data])






    # return jsonify(job_title_data[0])

if __name__ == '__main__':
    app.run(debug=True)
