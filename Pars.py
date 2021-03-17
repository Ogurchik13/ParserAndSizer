import requests
from bs4 import BeautifulSoup
from pars2 import links, get_html, DataBaseContent, mainurl, headers
import csv
import os

imgname = 1
url = ''
namefolder = str(mainurl[mainurl.index('catalog/') + 8:len(mainurl) - 1])
namefile = namefolder + '.csv'
directory = str(os.getcwd())


def getcontent(html):
    soup = BeautifulSoup(html, 'html.parser')
    item = soup.find('div', class_='col-xs-12').get_text(strip=True)
    price = soup.find('div', class_='col-xs-12 col-sm-6').find('p', class_='item_section_name_gray').get_text(strip=True)
    category = soup.find('div', class_="bx-breadcrumb-item").get_text(strip=True)
    products = []
    products.append({
        'Наименование продукта': item[:item.index('оценили') - 2],
        'Цена': price[5:price.index('₽')],
        'Описание продукта': DataBaseContent.get_describe(list(item[item.rindex('товара:') + 7:])),
        'Chosen': 0,
        'Slider': 0,
        'Категория': DataBaseContent.get_category(category)
    })

    return products


def parse():
    html = get_html(link)
    if html.status_code == 200:
        content = getcontent(html.text)
        return content
    else:
        print('При выполнении запроса возникла ошибка. Код ошибки:', html.status_code)


os.mkdir(directory + '\\' + namefolder)
os.mkdir(directory + '\\' + namefolder + '\\' + 'Изображения')
with open(directory + '\\' + namefolder + '\\' + namefile, 'w', newline='\n') as name:
    writer = csv.writer(name, delimiter=';')
    writer.writerow(['Наименование продукта', 'Цена', 'Описание продукта', 'Chosen', 'Slider', 'Категория'])
    for link in links:
        url = link
        for thing in parse():
            writer.writerow([thing['Наименование продукта'], thing['Цена'], thing['Описание продукта'],
                             thing['Chosen'], thing['Slider'], thing['Категория']])

for link in links:
    url = link
    soup = BeautifulSoup(get_html(url).text, 'html.parser')
    img = soup.find('div', class_='bx_bigimages_imgcontainer').find('img').get('src')
    session = requests.session()
    response = session.get('https://shop.samberi.com' + img, headers=headers)
    with open(directory + '\\' + namefolder + '\\' + 'Изображения' + '\\' + str(imgname) + '.jpg', 'wb') as fd:
        fd.write(response.content)
    imgname += 1
