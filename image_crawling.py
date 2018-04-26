# -*- coding: UTF-8 -*-
import urllib.request, urllib.parse
import requests
from bs4 import BeautifulSoup
import os

def get_url_content(url):
    html = urllib.request.urlopen(url).read()
    return html

def save_pics(soup, path):
    # information of films are in tags: 'tr'
    content_list = soup.tbody.find_all('tr')
    # loop in all 'tr's
    num = 1
    for film_item in content_list:
        pic_url = film_item.img.get('src')

        film_info_anchor = film_item.find_all('a')
        film_name_with_blanks = film_info_anchor[1].get_text()
        film_name = film_name_with_blanks.strip()

        pic_name =  '%s/%s/%s.jpg' % (os.path.abspath('.'), path, num)
        print('Downloading poster of '+film_name)
        num = num + 1
        with open(pic_name, "wb") as jpg_file:
            jpg_file.write(requests.get(pic_url).content)

def create_project_dir(path):
    if not os.path.exists(path):
        print('Create project ' + path)
        os.makedirs(path)

if __name__ == "__main__":


    # set base url
    base_url = 'https://www.imdb.com/chart/top'

    # get base url
    content = get_url_content(base_url)
    create_project_dir('IMDBTop250_pics')

    # use BeaurtifulSoup for further parsing
    soup = BeautifulSoup(content, 'html.parser')

    # get information from base_url
    save_pics(soup, 'IMDBTop250_pics')
