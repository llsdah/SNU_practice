# -*- encoding: utf-8 -*-

# News crawling from Naver
from bs4 import BeautifulSoup
import requests
# from requests.adapters import HTTPAdapter
# from urllib3.util.retry import Retry
import re
import time
import random
from time import sleep
import calendar
import os


# 연도, 달이 주어지면 그 달의 마지막 날 반환
def getLastDayOfMonth(year, month):
    year = int(year)
    month = int(month)
    res = calendar.monthrange(year, month)
    return str(res[1])


search_start_year = '2007'  # 수집 시작 연도
search_start_month = '01'  # 수집 시작 달
search_start_day = '01'  # 수집 시작 일자

search_end_year = '2007'  # 수집 끝 연도
search_end_month = '01'  # 수집 끝 달
search_end_day = getLastDayOfMonth(search_end_year, search_end_month)
start_date = search_start_year + '.' + search_start_month + '.' + search_start_day  # 2005.01.01
end_date = search_end_year + '.' + search_end_month + '.' + search_end_day  # 2017.12.31

start_date_str = start_date.replace('.', '')
end_date_str = end_date.replace('.', '')


# param 형식: '2005.01.01'
# return: ['2005.01.01','2005.01.02' ... ]
def getDatesPeriod(start, end):
    from datetime import date, timedelta

    start_str = start.split('.')
    start_year = int(start_str[0])
    start_month = int(start_str[1])
    start_day = int(start_str[2])

    end_str = end.split('.')
    end_year = int(end_str[0])
    end_month = int(end_str[1])
    end_day = int(end_str[2])
    d1 = date(start_year, start_month, start_day)  # start date
    d2 = date(end_year, end_month, end_day)  # end date

    delta = d2 - d1  # timedelta

    for i in range(delta.days + 1):
        date = str(d1 + timedelta(i))
        date = date.replace('-', '.')

    res = [str(d1 + timedelta(i)).replace('-', '.') for i in range(delta.days + 1)]
    return res


def getLastPageNum(soup):
    # #main_pack > div.news.mynews.section._prs_nws > div.section_head > div.title_desc.all_my > span
    # '금리' 검색결과 총 기사갯수 정보 가져오기
    try:
        tmp = soup.select_one(
            '#main_pack > div.news.mynews.section._prs_nws > div.section_head > div.title_desc.all_my').text  # 1-10 / 76,863건

    except AttributeError:
        print('해당 일자 "금리" 검색결과 없음')
        return 0

    tmp = tmp.split('/ ')  # 1-10, 76,863건
    tmp = tmp[1].split('건')  # 76,863
    tmp = tmp[0].replace(',', '')
    total_article_num = int(tmp)
    print('검색결과 총 기사갯수[신문사 3개 이외의 다른 신문사 검색 결과도 같이 포함되어 있음 주의]:', total_article_num, ' 개')

    last_page = int(total_article_num / 10)
    if total_article_num % 10 > 0:
        last_page += 1
    print('검색결과 끝페이지:', last_page, ' 페이지')
    return last_page


#          일자   일자  1->11->21.. 다음페이지 조회
def getURL(start, end, first_article_id):
    start_string = start.replace('.', '')
    end_string = end.replace('.', '')
    # url (네이버 뉴스 조건검색 - 2페이지)
    # https://search.naver.com/search.naver?&where=news&query=%EA%B8%88%EB%A6%AC&sm=tab_pge&sort=2&photo=0&field=0&reporter_article=&pd=3&ds=2005.01.01&de=2017.12.31&docid=&nso=so:da,p:from20050101to20171231,a:all&mynews=1&start=11&refresh_start=0
    url = 'https://search.naver.com/search.naver?' \
          '&where=news&query=%EA%B8%88%EB%A6%AC' \
          '&sm=tab_pge&sort=2&photo=0&field=0' \
          '&reporter_article=&pd=3&ds=' + start + '&de=' + end + \
          '&docid=&nso=so:da,p:from' + start_string + 'to' + end_string + ',a:all' \
                                                                          '&mynews=1&start=' + first_article_id + '&refresh_start=0'
    return url


# 기사 url 열어서 기사 내용 반환
def getContent(url, headers):
    # session = requests.Session()
    # retry = Retry(connect=3, backoff_factor=0.5)
    # adapter = HTTPAdapter(max_retries=retry)
    # session.mount('http://', adapter)
    # session.mount('https://', adapter)
    #
    # session.headers.update(headers)
    # session.get(url)

    sleep(random.uniform(1.0, 1.5))

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    try:
        text = soup.select_one('#articleBodyContents').text
        article_content = text.split('back() {}')[1]
    except AttributeError:
        # print('AttributeError')
        article_content = None

    return article_content


# 네이버가 아닌 각 신문사 홈페이지에서 raw content 가지고 오기
def getContentFromOtherSite(url, headers, source):
    sleep(random.uniform(1.0, 1.5))

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    if source == '연합인포맥스':
        try:
            text = soup.select_one('#article-view-content-div').text
            article_content = text
        except AttributeError:
            # print('기사삭제됨')
            article_content = None
    elif source == '연합뉴스':
        try:
            # #articleWrap > div.article
            text = soup.select_one('#articleWrap > div.article').text

            article_content = text
        except AttributeError:
            # print('기사삭제됨')
            article_content = None

    else:
        try:
            # #contents > section.center1080.position_r > section.aside_left > div.article_news > div.newscontainer > div.news_body
            text = soup.select_one('div.newscontainer > div.news_body').text
            article_content = text
        except AttributeError:
            # print('기사삭제됨')
            article_content = None
    return article_content


# 기사 내용중 header/footer부분(기자명,기사출처명,(끝),저작권명명)을 제거하고
# 기사 내용 반환
def removeHeaderFooter(type, text):
    # 기사 출처에 따라 적용하는 정규식이 다름
    if type in ['연합뉴스', '연합인포맥스']:
        # header 제거
        p_yhnews = re.compile('\(.+?연합뉴스')  # 출처표시검색 ex.(서울=연합뉴스)
        res = p_yhnews.findall(text)
        # (서울=연합뉴스) 있으면 제거
        if res:
            text = text.replace(res[0], '')

        p_yhinfo = re.compile('\(.+?연합인포맥스')
        res = p_yhinfo.findall(text)
        # (서울=연합인포맥스) 있으면 제거
        if res:
            text = text.replace(res[0], '')

        p_reporter = re.compile('\).+?기자\s{0,1}=')  # 글쓴이 정보 검색 #기자
        res = p_reporter.findall(text)
        if res:
            text = text.replace(res[0], '')

        p_cor = re.compile('\).+?특파원\s{0,1}=')  # 특파원
        res = p_cor.findall(text)
        if res:
            text = text.replace(res[0], '')

        # footer 제거
        text = re.split(r'[(][끝][)]', text)[0]  # footer 제거

    else:
        # type:이데일리
        # header 제거
        p_edlyhd = re.compile('\[.+?\]')  # [이데일리 안혜신 기자]
        res = p_edlyhd.findall(text)
        if res:
            text = text.replace(res[0], '')

        # footer 제거
        # 유형 1
        p_edlyft = re.compile('<.+?>')
        res = p_edlyft.findall(text)
        if res:
            text = text.replace(res[-1], '')
        # 유형 2 ＜
        p_edlyft = re.compile('＜.+?＞')
        res = p_edlyft.findall(text)
        if res:
            text = text.replace(res[-1], '')
    return text


def writeFirstlineOfContentOnFile(type, text, f):
    # 기사 내용중 첫번째 줄만 분리 --> header 형태 보기위한 함수
    res = re.split(r'[.]', text)[0]
    data = '%s, %s\n' % (type, res)
    f.write(data)


# import the os module
import os

# detect the current working directory and print it
path = os.getcwd()
path = path + "/naverNews_output"

try:
    if os.path.exists(path):
        print('/naverNews_output 폴더 이미 존재')
    else:
        print('/naverNews_output 폴더 생성')
        os.mkdir(path)
except OSError:
    print("폴더 생성 실패 %s" % path)
else:
    pass

# output to file
current_time = time.strftime("%m_%d_%H_%M", time.localtime())

dates_list = getDatesPeriod(start_date, end_date)
article_cnt = 0  # 긁어온 총 기사갯수

print('검색 기간:', start_date, '~', end_date)
for date in dates_list:
    article_daily_cnt = 0  # 해당 일자 긁어온 기사 갯수
    start_article_id = '1'

    output_name = 'naverNews_output/news_%s_%s.txt' % (date, current_time)
    f = open(output_name, 'w', -1, "utf-8")
    print('==')
    print('검색 일자: ', date)
    print('결과 파일: ', output_name)

    last_page = 1
    current_page = 1
    headers = {'User-Agent': 'Mozilla/5.0'}

    # '금리'로 네이버 뉴스 기사 검색
    # 페이지별로 결과 받아오기
    while current_page <= last_page:
        # 해당페이지의 뉴스 10개 url을 모두 긁어온다
        sleep(random.uniform(1.0, 1.5))
        url = getURL(date, date, start_article_id)
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        if current_page == 1:
            print(url)
            last_page = getLastPageNum(soup)
            if last_page == 0:
                break

        # 검색결과 페이지 읽어오기
        # #main_pack > div.news.mynews.section._prs_nws > ul
        # 하위에 <li> 태그가 10개 있음
        article_boxes = soup.select('#main_pack > div.news.mynews.section._prs_nws > ul > li > dl')
        # sp_nws1 > dl > dt > a 제목 url
        # #sp_nws1 > dl > dd.txt_inline > span._sp_each_source 신문사
        # sp_nws1 > dl > dd.txt_inline > span:nth-child(2)
        # #sp_nws1 > dl > dd.txt_inline 의 text 요소 날짜

        # num_of_articles_on_page = len(article_boxes)
        for box in article_boxes:
            flag_naverPageExist = True
            try:
                article_source = box.select_one('dd.txt_inline > span._sp_each_source').text
            except AttributeError:
                # 신문사 출처 없는 경우
                print('신문사 출처 없음')
                continue

            # 기사 출처가 이데일리, 연합뉴스, 연합인포맥스인 경우만 기사 크롤링
            source_list = ['이데일리', '연합뉴스', '연합인포맥스']

            if article_source in source_list:
                try:
                    article_url = box.select_one('dd.txt_inline > a').get("href")
                except AttributeError:
                    # 기사 상세 정보(네이버 뉴스 링크) 없는 경우
                    flag_naverPageExist = False
                    article_url = box.select_one('dt > a').get('href')

                try:
                    article_title = box.select_one('dt > a').get("title")
                    article_date = box.select_one('dd.txt_inline').text
                except AttributeError:
                    # 기사 상세 정보 없는 경우
                    print('기사 상세 정보 없음')
                    continue

                article_date = article_date.split(' ')[2]

                if flag_naverPageExist:
                    article_raw_content = getContent(article_url, headers)
                else:
                    article_raw_content = getContentFromOtherSite(article_url, headers, article_source)

                if article_raw_content is None:
                    # 기사 삭제되서 링크 못 열경우 다른 기사로 넘어감
                    continue

                # header, footer 제거
                article_content = removeHeaderFooter(article_source, article_raw_content)
                article_content = article_content.strip()
                info = '%s@@@%s@@@%s@@@%s@@@%s' \
                       % (article_source,
                          date,
                          article_title,
                          article_url,
                          article_content)
                # 크롤링한 기사 출처, 날짜, 제목, 내용
                f.write(info)
                f.write(article_content)
                f.write('\n===\n')

                #                 if article_cnt % 100 == 0:
                #                     current_time = time.strftime("%m_%d_%H_%M", time.localtime())
                #                     print('수집 기사 갯수: ',article_cnt,' 기사 날짜: ', article_date, ' 수집 시각: ',current_time)
                article_cnt += 1
                article_daily_cnt += 1

        start_article_id = str(int(start_article_id) + 10)  # 다음페이지로 넘어간다
        current_page += 1
    f.flush()
    f.close()
    # 일자별
    current_time = time.strftime("%m_%d_%H_%M", time.localtime())
    print('해당 일자 수집 기사 갯수: ', article_daily_cnt
          , ' 일자: ', article_date
          , ' 시각(서버시간): ', current_time
          , ' 누적 수집 기사 갯수: ', article_cnt)

print('수집한 총 기사 갯수', article_cnt)
