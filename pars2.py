import requests
from bs4 import BeautifulSoup
import math

print('Введите ссылку каталога(Например https://shop.samberi.com/catalog/myaso_ptitsa_yaytso/):')
mainurl = input(str().strip())
print('Введите количество товара которое необходимо сохранить(напишите "Все" чтобы сохранить '
      'все товары в данной категории)')
quantity = input()
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.408', 'accept': '*/*'}


def get_html(url, params=None):
    r = requests.get(url, headers=headers, params=params)
    return r


"""Определяем колличество страниц, исходя из того что на одной странце магазина по 18 товаров, и выписываем необходимое 
 колличество ссылок этих товаров"""
mainsoup = BeautifulSoup(get_html(mainurl).text, 'html.parser')
links = []


def get_links(request):
    for link in request:
        if int(len(links)) == int(quantity):
            break
        links.append(
            mainurl[:mainurl.index('.com') + 4] + link.find('a', class_='product-item-image-wrapper').get('href'))
    return links

try:
    pages = float(int(quantity) / 18)
except TypeError:
    subsoup = mainsoup.find('div', class_="bx-pagination-container row").find_all('li')
    num = []
    for i in pages:
        try:
            num.append(int(i.text))
        except ValueError:
            continue
    pages = max(num)
if pages <= 1:
    items = mainsoup.find_all('div', class_='col-xs-12 col-sm-3 col-md-3 col-lg-2 col-xl-4 product-item-small-card '
                                            'bcolor')
    get_links(items)
else:
    pages = math.ceil(pages)
    for page in range(1, pages + 1):
        mainsoup = BeautifulSoup(get_html(mainurl + '?PAGEN_1=' + str(page)).text, 'html.parser')
        items = mainsoup.find_all('div', class_='col-xs-12 col-sm-3 col-md-3 col-lg-2 col-xl-4 product-item-small-card '
                                                'bcolor')
        get_links(items)


class DataBaseContent:
    """Данный клас хранит в себе функиционал для сбора и систематизации данных с сайта."""

    def __init__(self, obj, stuff, img, path):
        self.path = path
        self.obj = obj
        self.stuff = stuff
        self.img = img

    def get_describe(self):
        x = True
        while x == True:
            try:
                self.remove('\t')
            except ValueError:
                x = False
        while self.count('\n') > 0:
            self.remove('\n')
        num = 0
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        char = ['.', ',', ':', '!', '-']
        for sim in self[1:]:
            num += 1
            if sim == sim.upper() and sim != ' ' and sim not in char:
                try:
                    if int(sim) in numbers:
                        continue
                except ValueError:
                    self.insert(num, ' ')
                    num += 1
            else:
                continue
        itemstr = str(''.join(self))
        return itemstr

    def get_category(self):
        categories = {'Зелень, овощи, фрукты': 1, 'Мясо, птица, яйцо': 2, 'Кондитерские изделия': 3,
                      'Рыба, морепродукты, икра': 4, 'Хлебобулочные изделия': 5, 'Чай, кофе, кокао': 6,
                      'Бакалейные товары': 7, 'Алкоголь': 8, 'Напитки, соки, вода': 9}
        return categories.get(self, 'Неизвестная категория')
