from bs4 import BeautifulSoup

with open('home.html', 'r') as htm_file:
    content = htm_file.read()
    
    soup = BeautifulSoup(content, 'lxml')
  
    course_cards = soup.find_all('div', class_="card")
    for c in course_cards:
        print(f'{c.h5.text} costs {c.a.text.split()[-1]}')

