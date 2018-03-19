# -*- coding: UTF-8 -*-
import urllib.request, urllib.parse
from bs4 import BeautifulSoup
import xlwt

def get_url_content(url):
    html = urllib.request.urlopen(url).read()
    return html

book=xlwt.Workbook(encoding='utf-8',style_compression=0)

sheet=book.add_sheet('Top250 Movies on IMDB.COM',cell_overwrite_ok=True)

sheet.write(0,0,'More Information')
sheet.write(0,1,'Image URL')
sheet.write(0,2,'Film Name')
sheet.write(0,3,'Rate')
sheet.write(0,4,'Year')
sheet.write(0,5,'Film Director')
sheet.write(0,6,'Main staff')

n=1

def parser_to_excel(soup):
    # information of films are in tags: 'tr'
    content_list = soup.tbody.find_all('tr')
    print(content)
    # loop in all 'tr's
    for film_item in content_list:
        # two urls: one for image and one for more information of the film
        # get urls
        film_detail_url = film_item.find_all('a')[0].get('href')
        film_pic_url = film_item.img.get('src')

        # find the film name text and clean the blanks with the text
        film_info_anchor = film_item.find_all('a')
        film_name_with_blanks = film_info_anchor[1].get_text()
        film_name = film_name_with_blanks.strip()

        # get the rate of the film
        film_rate = film_item.strong.get('title')

        #get the year of the film
        year_str = film_item.find(class_="secondaryInfo").get_text().strip()
        film_year = year_str[1:-1]

        #get the staff of the film
        film_staff_info = film_item.find_all('a')[1].get('title')
        director_list = film_staff_info.split(',')[0].split()
        director = director_list[0]+' '+director_list[1]

        #print information of crawling
        print ("Crawling：More Information："+film_detail_url+"，Image URL："+film_pic_url+"，Film Name："+film_name+"，Film Rate："+film_rate+", Film Year: "+film_year+", Film Director: "+director+", Main Staff: "+film_staff_info)

        global n
        sheet.write(n,0,base_url+film_detail_url)
        sheet.write(n,1,film_pic_url)
        sheet.write(n,2,film_name)
        sheet.write(n,3,film_rate)
        sheet.write(n,4,film_year)
        sheet.write(n,5,director)
        sheet.write(n,6,film_staff_info)
        print("Writing to "+str(n)+" row...")
        # move to the next row
        n=n+1

if __name__ == "__main__":

    # set base url
    base_url = 'https://www.imdb.com/chart/top'

    # get base url
    content = get_url_content(base_url)

    # use BeaurtifulSoup for further parsing
    soup = BeautifulSoup(content, 'html.parser')

    # get information from base_url
    parser_to_excel(soup)

    book.save(u'IMDBTop250.xls')
