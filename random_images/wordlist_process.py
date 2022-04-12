import random
import requests
from bs4 import BeautifulSoup
import concurrent.futures

MAX_PHOTOS = 5
MIN_PHOTOS = 2
SEARCH_URL = 'https://unsplash.com/s/photos/'
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'}

def img_dowloader(img, word_num, it):
    src = img.get('src')
    if src:
        try:
            image = requests.get(src, headers=HEADERS, stream=True)
            img_name = str(word_num) + '-' + str(it)
            with open('images/' + img_name + '.jpg', 'wb') as new_img:
                for chunk in image:
                    new_img.write(chunk)
            print(img_name + ',' + img.get('title'))
        except:
            pass 

def img_finder(word, word_num):
    try:
        photos_page = requests.get(SEARCH_URL + word, headers=HEADERS).content
        soup = BeautifulSoup(photos_page,features="html.parser")

        images = []
        images.append(soup.find('img',{ 'class': 'YVj9w'}))

        num_imgs = 5 #random.randrange(MIN_PHOTOS, MAX_PHOTOS)
        while len(images) <= num_imgs:
            images.append(images[-1].find_next('img',{ 'class': 'YVj9w'}))

        it = 0
        no_threads_imgs = 5
        with concurrent.futures.ThreadPoolExecutor(max_workers=no_threads_imgs) as executor_images:
            for img in images:
                it += 1
                print("Thread starting download")
                executor_images.submit(img_dowloader, img, word_num, it)
    except:
        pass

with open("wordlist","r",encoding="utf8") as f:
    words = f.readlines()
    f.close()

no_threads = 100
with concurrent.futures.ThreadPoolExecutor(max_workers=no_threads) as executor:
    for word_num in range(0, 100):
        word = words[word_num]
        word = word[:len(word)-1]
        #img_finder(word)
        print("Thread starting Search for " + word + " - " + str(word_num))
        executor.submit(img_finder, word, word_num)
            