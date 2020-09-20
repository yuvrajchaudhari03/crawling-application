from django.shortcuts import render
from django.http import HttpResponse
from collections import defaultdict
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from getpass import getpass
import json
from django.http import JsonResponse
import http.cookiejar
import urllib.request
import re
def blogcontent(request):
    blog_url = request.GET.get('blog_url', None)
    print(blog_url)
    keyword = str(blog_url)
    pattern = r"{}".format(keyword)
    ht_r = requests.get(pattern)    
    soup = BeautifulSoup(ht_r.text, 'lxml')
    divs = soup.div
    single_blog_dict = {}
    n = 0
    blog_content1=[]
    for div in divs.find_all('div', {'class': 'ab ac ae af ag eo ai aj'}):
        single_blog_dict[n] = {}
        for blog_title in div.find_all('h1', {'class': 'ep eq er es b et eu ev ew ex ey ez fa fb fc fd fe ff fg fh fi dh'}):
            single_blog_dict[n].update({"blog_title": blog_title.text})
        for author_div in div.find_all('span',{'class': 'av aw ax ay dh'}):
            for author_name in author_div.find_all('a') :
                single_blog_dict[n].update({"author_name": author_name.text})
        for details_div in div.find_all('span',{'class': 'av aw ax ay az'}):
            # for blog_date in details_div.find_all('a',{'class': 'bq br bc bd be bf bg bh bi bj fz bm bu bv'}):
            single_blog_dict[n].update({"details_div": details_div.text})
        # for blog_content in div.find_all(['figure','p','h2','ol']):
        #     blog_content1.append(blog_content)
         
        
    single_blog_dict = dict(single_blog_dict)
    print(single_blog_dict)
    dataJSON = json.dumps(single_blog_dict)
    
    return render (request,'getblogs/blog.html',{'data': dataJSON})


def index(request):
    return render(request, 'getblogs/index.html')
    # return render(request,'index.html')


def search(request):
    tag_name = request.GET.get('tag_name', None)
    print(tag_name)
    keyword = str(tag_name)
    pattern = r"https://medium.com/tag/{}/latest".format(keyword)
    ht_r = requests.get(pattern)
    soup = BeautifulSoup(ht_r.text, 'lxml')
    divs = soup.div
    blog_dict = {}
    
    n = 0
    for div in divs.find_all('div', {'class': 'streamItem streamItem--postPreview js-streamItem'}):
        blog_dict[n] = {}
        for author_name in div.find_all('a', {'class': 'ds-link ds-link--styleSubtle link link--darken link--accent u-accentColor--textNormal u-accentColor--textDarken'}):
            # blog_dict[n]={'author_name':author_name.text}
            blog_dict[n].update({"author_name": author_name.text})
            for sub_div in div.find_all('div', {'class': 'ui-caption u-fontSize12 u-baseColor--textNormal u-textColorNormal js-postMetaInlineSupplemental'}):
                for date in sub_div.find_all('a', {'class': 'link link--darken'}):
                    blog_dict[n].update({"date": date.text})
                    
                for reading_time in sub_div.find_all('span', {'class': 'readingTime'}):
                    # print(reading_time["title"])
                    blog_dict[n].update({"reading_time": reading_time["title"]})
        for title in div.find_all('h3', {'class': ['graf graf--h3 graf-after--figure graf--title', 'graf graf--h3 graf--leading graf--title',
                                                   'graf graf--h3 graf-after--figure graf--trailing graf--title',  'graf graf--h3 graf-after--figure graf--titlelap',
                                                   'graf graf--h3 graf-after--h4 graf--trailing graf--title',
                                                   'graf graf--h3 graf-after--p']}):
            blog_dict[n].update({"title": title.text}) 
        for link_div in div.find_all('div',{'class': 'postArticle-readMore'}):
            for link in link_div.find_all('a',{'class': 'button button--smaller button--chromeless u-baseColor--buttonNormal'}):
                if link.has_attr('href'):
                    
                    blog_dict[n].update({"blog_link":link.get('href')})

        n += 1
    blog_dict = dict(blog_dict)
    print(blog_dict)
    data = {
        'blog_dict': blog_dict
    }
    print(data)
    # return render(request, 'getblogs/index.html', {'blog_dict':blog_dict})
    return JsonResponse(data)


# GEtting news from Times of India
"""
toi_r = requests.get("https://timesofindia.indiatimes.com/briefs")
toi_soup = BeautifulSoup(toi_r.content, 'html.parser')

toi_headings = toi_soup.find_all('h2')

toi_headings = toi_headings[0:-13] # removing footers
toi_news = []

for th in toi_headings:
    toi_news.append(th.text)

"""

"""
driver = webdriver.Firefox()
driver.get("https://medium.com/")

username="yuvrajchaudhari4@gmail.com"
password="yuvrajchaudhari"
signin_button = driver.find_element_by_id("lo-homepage-get-started-button").click()
signin_button = driver.find_element_by_id("susi-modal-fb-button").click()
email_textbox =driver.find_element_by_id("email")
email_textbox.send_keys(username)
pass_textbox =driver.find_element_by_id("pass")
pass_textbox.send_keys(password)
login_submit_button =driver.find_element_by_id("loginbutton")
login_submit_button.submit()
signin_button = driver.find_element_by_class_name("_42ft _4jy0 layerConfirm _1fm0 _51_n autofocus _4jy3 _4jy1 selected _51sy").click()

"""
"""
#keyword=input("enter keywords")
keyword="python"
#Getting news from Hindustan times
#pattern = r"https://medium.com/search?q={}".format(keyword)
pattern = r"https://medium.com/tag/{}/latest".format(keyword)
#links = soup.find_all('a', href=re.compile(pattern))
ht_r = requests.get(pattern)
#ht_soup = BeautifulSoup(ht_r.text, 'html.parser')
soup = BeautifulSoup(ht_r.text, 'lxml')

divs = soup.div
blog_dict=defaultdict(list)
n=0
for div in divs.find_all('div', {'class' : 'streamItem streamItem--postPreview js-streamItem'}):
    for author_name in div.find_all('a',{'class' : 'ds-link ds-link--styleSubtle link link--darken link--accent u-accentColor--textNormal u-accentColor--textDarken'}):
        blog_dict[n].append(author_name.text)
        for sub_div in div.find_all('div',{'class' : 'ui-caption u-fontSize12 u-baseColor--textNormal u-textColorNormal js-postMetaInlineSupplemental'}):
            for date in sub_div.find_all('a',{'class':'link link--darken'}):
                blog_dict[n].append(date.text)
            for reading_time in sub_div.find_all('span',{'class':'readingTime'}):
                #print(reading_time["title"])
                blog_dict[n].append(reading_time["title"])
    for title in div.find_all('h3',{'class':['graf graf--h3 graf-after--figure graf--title',
                                            'graf graf--h3 graf--leading graf--title',
                                            'graf graf--h3 graf-after--figure graf--trailing graf--title',
                                            'graf graf--h3 graf-after--figure graf--titlelap',
                                            'graf graf--h3 graf-after--h4 graf--trailing graf--title',
                                            'graf graf--h3 graf-after--p']}):
        blog_dict[n].append(title.text)
                

    n+=1

blog_dict= dict(blog_dict)

print(type(blog_dict) )      
print(blog_dict)
"""
# title = soup.find_all('h3', {'class' : ['graf graf--h3 graf--leading graf--title',
#                                       'graf graf--h3 graf-after--figure graf--trailing graf--title',
#                                      'graf graf--h3 graf-after--figure graf--title',
#                                     'graf graf--h3 graf-after--figure graf--titlelap',
#                                    'graf graf--h3 graf-after--h4 graf--trailing graf--title']})
#title = soup.find_all('h3')

#title = soup.find_all('div', {'class' : 'u-paddingTop20 u-paddingBottom25 u-borderBottomLight js-block'})
#print("all stuff:--",title)
# for url in title.find_all('a'):
# print(url.get('href'))
# for t in title:
#    print(t.text)


# def index(req):
#   return render(req, 'getblogs/index.html', {'blog_dict':blog_dict})
