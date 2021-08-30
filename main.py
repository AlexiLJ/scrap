from bs4 import BeautifulSoup
import requests


html_text = requests.get('https://www.jobs.cz/prace/praha/?q%5B%5D=python').text

# print(html_text)
# with open('home.html', 'r') as htm_file:
#     content = htm_file.read()


soup = BeautifulSoup(html_text, 'lxml')

# jobs = soup.find_all('div', class_="grid__item")

company_name=soup.find_all('h3', class_='search-list__main-info__title')

for x in company_name:
    l = x.find('a').text
    print(l)
  
#     course_cards = soup.find_all('div', class_="card")
#     for c in course_cards:
#         print(f'{c.h5.text} costs {c.a.text.split()[-1]}')

