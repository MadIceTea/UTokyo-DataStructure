from __future__ import division
from bs4 import BeautifulSoup
import requests
import shutil
import os.path
import pathlib
import re
regex = {'allow': re.compile('[A-Z, \b, 0-9, -]')}
regex2 = {'punctuation': re.compile('[]!"#$%&()*+,./:;<=>?@\^_`{|}~]')}

pathlib.Path('./memes').mkdir(exist_ok=True)
save_path = 'memes'
n_templates = 9 #this number is the total number of webpages with templates on them (~*40 for total number of memes), must be 2 or more
n_captions = 9 #this number is number of webpages for each template's captions (limited at two for the benefit of memes with less popularity)
n_iterator = 1 #this number represents the ~12 instances of different captions on each captions webpage

Uerrors = 0

for i in range(1,n_templates):
    if i == 1:
        url = 'http://imgflip.com/memetemplates'
    else:
        url = 'http://imgflip.com/memetemplates?page=' + str(i)

    r = requests.get(url)
    soup = BeautifulSoup(r.text,'html.parser')
    chars = soup.find_all(class_='mt-img-wrap')
    links = [char.find('a') for char in chars]
    imgs = [char.find('img') for char in chars]	
    assert len(links) == len(imgs)
	
    for j,img in enumerate(imgs):
        img_url = 'http:' + img['src']
        response = requests.get(img_url, stream=True)
        name_of_file = img_url.split('/')[-1]
        completeName = os.path.join(save_path, name_of_file)
        with open(completeName,'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

    for k in range(1,n_captions):
        if k == 1:
            URL = 'http://imgflip.com' + links[j]['href']
        else:
            URL = 'http://imgflip.com' + links[j]['href'] + '?page=' + str(k)

        R = requests.get(URL)
        SOUP = BeautifulSoup(R.text,'html.parser')
        CHARS = SOUP.find_all(class_='base-img-link')
        IMGS = [char.find('img') for char in CHARS]
        string0 = (str(IMGS[0]['alt']))

        message0 = string0
        message_caps0 = ""

        for c in message0:
            if regex['allow'].match(c):
                    message_caps0 += c

        cleaned0 = (message_caps0)[5:][:-11]

        with open('Captions.txt', 'a+') as f:
            for IMG in IMGS:
                try:
                    f.write(str(cleaned0) + '\n')
                except UnicodeEncodeError:
                    Uerrors += 1	
                    pass

        for n in range(0,n_iterator):
            string = (str(IMGS[n]['alt']))

            message = string
            message_caps = ""

            for c in message:
                if regex['allow'].match(c):
                    message_caps += c

            cleaned2 = (message_caps)[5:][:-11]
            with open('Captions.txt', 'a+') as f:
                lines = [line.rstrip('\n') for line in f]
                for IMG in IMGS:
                    try:
                        f.write(str(cleaned2) + '\n')
                    except UnicodeEncodeError:
                        Uerrors += 1	
                        pass

    if i % 10 == 0:
        print('<'+'='*10+'>')
        print(i)
        print(Uerrors)

URL = 'http://imgflip.com' + links[0]['href']
R = requests.get(URL)
SOUP = BeautifulSoup(R.text,'html.parser')
CHARS = SOUP.find_all(class_='base-img-link')
IMGS = [char.find('img') for char in CHARS]
string = (str(IMGS[0]['alt']))

message = string
message_caps = ""

for c in message:
    if regex['allow'].match(c):
        message_caps += c

cleaned = (message_caps)[5:][:-11]
# with open('Captions.txt', 'r+b') as f:
    # for IMG in IMGS:
        # try:
            # f.write(str(cleaned) + '\n')
        # except UnicodeEncodeError:
            # Uerrors += 1	
            # pass
					
img_url = 'http:' + imgs[0]['src']
response = requests.get(img_url, stream=True)
name_of_file = img_url.split('/')[-1]
completeName = os.path.join(save_path, name_of_file)
with open(completeName,'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
del response
#wait(3000)