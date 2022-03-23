import os
import requests
from bs4 import BeautifulSoup

FISHES_URL = 'https://fishbase.us/photos/ThumbnailsSummary.php?id='
FISH_OFICIAL_URL = 'http://d1iraxgbwuhpbw.cloudfront.net/images/species/'
FISH_UPLOADS_URL = 'http://d1iraxgbwuhpbw.cloudfront.net/tools/uploadphoto/uploads/'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'}
cont_tot = 0
for fish_id in range(10,20000):
    photos_page = requests.get(FISHES_URL + str(fish_id), headers=headers).content
    soup = BeautifulSoup(photos_page,features="html.parser")
    images = soup.findAll('img')
    cont = 0
    for img in images:
        img_src = img.get('src')
        if 'workimagethumb' not in img_src:
            if '/species/' in img_src:
                fish_name = img_src[img_src.find('/species/')+9:].lower()
                filename = str(fish_id)+'-'+str(cont)+'_'+fish_name
                #print(FISH_OFICIAL_URL + fish_name)
                image = requests.get(FISH_OFICIAL_URL + fish_name, headers=headers, stream=True)
                with open('photos/'+filename, 'wb') as img:
                    for chunk in image:
                        img.write(chunk)
                cont += 1
            elif '/uploads/' in img_src:
                fish_name = img_src[img_src.find('/uploads/')+9:].lower()
                filename = str(fish_id)+'-'+str(cont)+'_community.jpg'
                #print(FISH_UPLOADS_URL + fish_name)
                image = requests.get(FISH_UPLOADS_URL + fish_name, headers=headers, stream=True)
                with open('photos/'+filename, 'wb') as img:
                    for chunk in image:
                        img.write(chunk)
                cont += 1
    cont_tot += cont
    print(str(fish_id)+','+str(cont)+','+str(cont_tot))

    
    