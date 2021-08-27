from bs4 import BeautifulSoup

with open('home.html', 'r') as htm_file:
    content = htm_file.read()
    
    soup = BeautifulSoup(content, 'lxml')

    # print(soup.prettify())  