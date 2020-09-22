from django.shortcuts import render
from django.http import HttpResponse
from collections import defaultdict
import requests
from bs4 import BeautifulSoup
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
        # single_blog_dict[n] = {}
        for blog_title in div.find_all('h1', {'class': 'ep eq er es b et eu ev ew ex ey ez fa fb fc fd fe ff fg fh fi dh'}):
            single_blog_dict.update({"blog_title": blog_title.text})
        for author_div in div.find_all('span',{'class': 'av aw ax ay dh'}):
            for author_name in author_div.find_all('a') :
                single_blog_dict.update({"author_name": author_name.text})
        for details_div in div.find_all('span',{'class': 'av aw ax ay az'}):
            single_blog_dict.update({"details_div": details_div.text})
        # for blog_content in div.find_all(['figure','p','h2','ol']):
        #     blog_content1.append(blog_content)
    tags_names=[]
    for tag_div in divs.find('div',{'class':['lg jk n ke p','ma hi n kq p','mt hn n lr p','mg ii n kp p']}): 
        for lis in tag_div.find_all('li',{'class':['gp lj ha du','gp md ha du','gu mw hf du','ho ci ia eq']}):
            print(lis.text)
            tags_names.append(lis.text)
            
    print(tags_names)
    single_blog_dict.update({'tag_names':tags_names})       
                       
    single_blog_dict = dict(single_blog_dict)
    print(single_blog_dict)
    dataJSON = json.dumps(single_blog_dict)
    
    return render (request,'getblogs/blog.html',{'data': dataJSON})


def index(request):
    blog_tag_name = request.GET.get('tag_name', None)
    return render(request, 'getblogs/index.html',{'blog_tag_name':blog_tag_name})
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