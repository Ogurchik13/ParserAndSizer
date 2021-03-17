from PIL import Image, UnidentifiedImageError
import os
print('Введите директорию с изображениями(полностью):')
path = str(input())
print('Введите высоту изображения(в пикселях):')
height = int(input())
print('Введите ширину изображения(в пикселях):')
width = int(input())
with os.scandir(path) as listOfEntries:
    for entry in listOfEntries:
        if entry.is_file():
            try:
                img = Image.open(path + '\\' + entry.name)
                resized_img = img.resize((width, height), Image.ANTIALIAS)
                resized_img.save(path + '\\' + entry.name)
            except UnidentifiedImageError:
                continue
