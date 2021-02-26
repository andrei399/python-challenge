import requests
from bs4 import BeautifulSoup
URL = 'http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing=87696'
number_list = []
for i in range(401):
    page = requests.get(URL)
    next_number = [int(s) for s in page.content.split() if s.isdigit()]
    if next_number[0] not in number_list:
        URL = 'http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing=' + str(next_number[0])
        print(URL)
    else:
        print('LIST IS REPEATING!!!')
    number_list.append(next_number[0])
print(URL)