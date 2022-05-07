# 4/7 데이터부석실습

from pickle import NONE
from xmlrpc.client import FastParser
import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt #그래프용

#테드 연습문제 
url = 'https://raw.githubusercontent.com/SLCFLAB/Data-Science-Python/main/Day%203/data/ted_main.csv'
a1 = pd.read_csv(url)
a1.shape
#a1.info()

#시간 변경 기존 시간값을 컴퓨터 언어로 되어있다.
a1['film_date'] = pd.to_datetime(a1['film_date'],unit='s')
a1['published_date'] = pd.to_datetime(a1['published_date'], unit='s')

a1.drop('film_date',axis=1,inplace=True) #해당열 자체 삭젠


# Abstract Syntax Trees modules AST
"""
예시

str_dict = "{'key_1': 'value_1', 'key_2': 'value_2'}"
# str_dict는 딕셔너리 형태를 가진 문자열임

real_dict = ast.literal_eval(str_dict)
# real_dict는 딕셔너리 형태로 변환되었기 때문에 key-value를 사용할 수 있음   
    
"""
import ast 
#기존의 ratings도 딕녀너리 구조형태 이기에 해당 문법으로 읽어 올수있다.
a1.ratings = a1.ratings.apply(ast.literal_eval)
#print(a1.ratings[0])

def co(i):
    counts =0
    for item in i: #딕녀너리 자료구조 자체를 이안에 넣고 돌린다.
        counts+=item["count"]
    return counts

#print(co(a1.ratings[0]))
a1['rating_count'] = a1.ratings.apply(lambda x : co(x))# 새 컬럼 생성및 해당 내용에 값들을 대응한다. 


#다양한 평가 받은것들은의 형용사 대응 컬럼 추가 
#가장 높은 평가를 받은것은 무엇인가 
for i, value in enumerate(a1.ratings):
    count =["",0] #최댓값 저장변수
    for item in value:
        #print( i,"  ",item['name'.lower()])
        a1.loc[i, item['name'].lower()] = item['count']
        #print(a1.loc[i,item['name'].lower()])
        if item['count']>count[1]:
            count = [item['name'].lower(),item['count']]
    a1.loc[i,'maxmum_rated']=count[0]
#print(a1.loc[0,temp['name'].lower()])
        
print()
"""    
comments  -  description  -  duration  -  event  -  languages  -  main_speaker  -  name  -  num_speaker  -  published_date  -  ratings  -  related_talks  -  speaker_occupation  -  tags  - title  -  url  -  views  -  rating_count  -  funny  -  beautiful  -  ingenious  -  courageous  -  longwinded  -  confusing  -  informative  -  fascinating  -  unconvincing  -  persuasive  -  jaw-dropping  -  ok  -  obnoxious  -  inspiring  -  maxmum_rated  -
"""

"""
1) 100만뷰 이하의 테드 강연 비율은?
2) 테드 강연 영상이 가장 많은 연도는?
event: TED 강연이 개최되었던 행사 이름에 해당하는 칼럼
상위 5개 출력
3) speaker들의 직업 목록과 가장 높은 비율의 직업은?
4) funny rating의 비율이 가장 높은 speaker의 직업군은?
speaker_occupation: 연사의 직업을 나타내는 칼럼
funny rating의 비율 평균 순으로 상위 10개 직업 출력
데이터셋 내 직업별 불균형이 있긴 함    
"""
 
print() 
print("문제")
print()
print( "1. : ")
#a1[ a1['views'] < 1000000 ].shape[0]/a1.shape[0] 

#print("2 ")
#기존에 날짜로 변경된 상태이기에 추충이 가능하다
for i,date in enumerate(a1.published_date):
    a1.loc[i,'year'] = date.year

#print( a1.groupby('year').count().sort_values(by='comments',ascending=False).head(5))#해당 year별로 갯수를 세서 열에 대입시킨것입# count는 없는 값을 안센다 그렇기에 숫자가 드러있것을 기준으로 변경해줘야한다.


#print(" 3 ")
#ted.groupby('speaker_occupation').count().sort_values(by='comments', ascending=False).head(1)
#채
a1.groupby('speaker_occupation').size().sort_values(ascending=False).head(1) # size 결측치까지 센다 그렇기에 해당 인덱스에만 값이 있고, 나머지느 값이 없기에 기준설정하면안됨

#print(" 4 ")
a1[['funny','speaker_occupation']].groupby('speaker_occupation').mean().sort_values(by='funny').tail()


#3-2
"""
Iris dataset
sklearn에 내장된 데이터셋. 붓꽃의 종류(3가지)에 따른 꽃받침과 꽃잎의 길이, 폭에 대한 데이터 Target

0: iris-setosa
1: iris-versicolor
2: iris-virginica    
"""



#3-3 dataframe exercise

# Q1아래 DataFrame을 활용해 남성과 여성 각각 Age가 30이상인 사람들의 평균 Height을 구해보자.

ex_df1 = pd.DataFrame({
    'Age': [37, 20, 30, 45, 25, 31, 41],
    'Height' : [156, 180, 170, 160, 150, 140, 181],
    'Sex' : ['f','m','m','f','f','f','m']
})
#print(ex_df1[ex_df1['Age']>=30].groupby("Sex").mean())


"""
column 별로 결측치가 어느만큼 있을까?

출생연도, 교육레벨, 연봉에 대한 정보만 들어있는 데이터프레임 만들어보기

연 수입의 범위에 따라 low(75000미만), medium(75000이상~120000미만), high(120000 이상) 값을 매기는 컬럼 만들기

교육 레벨에 따른 'annual_income', 'recency', 'store_purchases', 'online_purchases'의 평균 구해보기 (데이터프레임으로)

석사 졸업생 중 연봉이 75000이상인 데이터의 수는?
기타) 보고 싶은 데이터 있으면 실습해보기 (결혼상태, 생년월일 등)
"""
url = 'https://raw.githubusercontent.com/SLCFLAB/Data-Science-Python/main/Day%203/data/project_data.csv'
ex_df2 = pd.read_csv(url)
#print(ex_df2.isnull().sum())
#print(ex_df2['educational_level'])


#print(ex_df2.annual_income)



for i , value in enumerate(ex_df2.annual_income):
    temp =""
    if value <75000:
        temp="low"
    elif value<120000:
        temp="medium"
    else:
        temp="high"
    
    ex_df2.loc[i,"level"] =temp

#print(ex_df2.groupby('educational_level').mean())[[]]


ex_df2.iloc[list((ex_df2.annual_income > 75000) & (ex_df2.educational_level == 'Master')),  :]
print()
print(ex_df2.iloc[list((ex_df2.annual_income > 75000) & (ex_df2.educational_level == 'Master')),  :]
)
ex_df2.shape[0]


import matplotlib.pyplot as plt
import matplotlib_inline


url = 'https://raw.githubusercontent.com/SLCFLAB/Data-Science-Python/main/Day%203/data/bankchurn.csv'

df = pd.read_csv(url)




