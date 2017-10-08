#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-07 21:33:18
# @Author  : ${Your Name} (${you@example.org})
# @Link    : 
# @Version : ${1.0.0}

import random

import requests
from pyquery import PyQuery as pq

GET_URL = "http://127.0.0.1:5010/get/"
DELETE_URL = "http://127.0.0.1:5010/delete/?proxy={}"

def get_proxy():
    '''获取一个可用的代理'''
    return requests.get(GET_URL).content.decode()

def delete_proxy(proxy):
    '''删除一个代理'''
    requests.get(DELETE_URL.format(proxy))

def get_user_agent():
    '''获取一个用户代理'''
    user_agent_list = [\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"\
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    return random.choice(user_agent_list)

def get_header():
    '''获取一个http请求的headers'''
    headers = {
        'Accept-Encoding':'gzip, deflate, sdch, br',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'Referer':'http://www.baidu.com',
        'User-Agent' : get_user_agent()
    }
    return headers

def get_html(url, is_use_proxy=False):
    '''根据url获取html页面'''
    proxy = 'http://{}'.format(get_proxy())
    try:
        if is_use_proxy:
            r = requests.get(url, timeout=30, headers=get_header(), proxies={'http':proxy})
        else:
            r = requests.get(url, timeout=30, headers=get_header())
        r.raise_for_status()
        # r.encoding = r.apparent_encoding
        return r.text
    except requests.RequestException as e:
        print(e)
        return 'ERROR'

def exactComment(comment_url):
    '''根据url爬取一页评论'''
    comment_page = get_html(comment_url)
    comment_doc = pq(comment_page)
    comment_content = comment_doc('#content')
    comment_title = comment_content('h1').text()
    comment_number = comment_content('li.is-active > span').text()
    comment_items = comment_content('#comments').items('div.comment-item')
    for item in comment_items:
        comment_id = item.attr('data-cid')
        user_url = item('div.avatar > a').attr('href')
        user_img = item('div.avatar > a > img').attr('src')
        user_name = item('div.avatar > a').attr('title')
        user_comment_votes = item('span.comment-vote > span.votes').text()
        user_watch_status = item('span.comment-info > span:nth-child(2)').text()
        try:
            user_score = item('span.comment-info > span.rating').attr('class').split(' ')[0]
        except:
            user_score = '暂未评分'
        user_ctime = item('span.comment-info > span.comment-time').attr('title')
        user_comment = item('div.comment > p').text()
        print('comment_id:{} \n user_url:{} \n user_img:{} \n user_name:{} \n \
            user_comment_votes:{}\n user_watch_status:{} \n user_score:{} \n \
            user_ctime:{} \n user_comment:{} \n\n'.format(comment_id, user_url, \
            user_img, user_name, user_comment_votes, user_watch_status, \
            user_score, user_ctime, user_comment))

def exact_movie_info(doc):
    '''
    提取电影相关信息
    '''
    movie_doc = doc
    movie_title = movie_doc('#content > h1').text()
    movie_img = movie_doc('#mainpic > a > img').attr('src')
    movie_director = movie_doc('#info > span:nth-child(1) > span.attrs > a').text()     # 导演
    movie_scriptwriter = movie_doc('#info > span:nth-child(3) > span.attrs > a').text() #编剧
    movie_actors = [item.text() for item in movie_doc('#info > span.actor > span.attrs > span > a').items()]       #主演
    movie_type = [item.text() for item in movie_doc('#info > span:nth-child(7) + span[property=v:genre]').items()]         #电影类型
    movie_area = ''         #制片国家/地区
    movie_lang = ''         #语言
    movie_showtime = [item.text() for item in movie_doc('#info > span[property=v:initialReleaseDate]').items()]     #上映日期
    movie_time = movie_doc('#info > span:nth-child(22)').text()        #片长
    movie_anothername=''    #又名
    movie_IMDBurl = movie_doc('#info > a').attr('href')      #IMDB链接
    movie_score = movie_doc('#interest_sectl > div.rating_wrap.clearbox > div.rating_self.clearfix > strong').text()        #豆瓣评分
    movie_votenum = movie_doc('#interest_sectl > div.rating_wrap.clearbox > div.rating_self.clearfix > span[property=v:votes]').text()      #评论人数
    movie_briefinfo = movie_doc('#link-report > span:nth-child(1)').text()    #简介
    print('电影名：{}\n电影图片：{}\n电影导演：{}电影编剧：{}'.format(movie_title, movie_img, movie_director, movie_scriptwriter)) 
    print('主演：{}'.format('/'.join(movie_actors)))
    print('类型：{}'.format('/'.join(movie_type)))
    print('上映日期：{}'.format('/'.join(movie_showtime)))
    print('片长：{}'.format(movie_time))
    print('IMDB链接：{}'.format(movie_IMDBurl))
    print('豆瓣评分：{}'.format(movie_score))
    print('评论人数：{}'.format(movie_votenum))
    print('简介：{}'.format(movie_briefinfo))

def spider(pages=10):
    '''爬虫'''
    #...
    base_url = 'https://movie.douban.com/subject/26580232/'
    page = get_html(base_url)
    doc = pq(page)
    print('title: ' + doc('title').text())
    print(doc('#link-report > span').html().strip().replace('<br/>', ''))
    comment_url = base_url + doc('#hot-comments > a').attr('href')
    exact_movie_info(doc)
    # for index in range(0, pages):
    #     print('**************第{}页*************'.format(index+1))
    #     url = comment_url + '&start=' + str(index * 20)
    #     exactComment(url)

def main():
    '''主方法'''
    spider()

if __name__ == '__main__':
    main()
