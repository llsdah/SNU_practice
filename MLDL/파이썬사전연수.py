""" 사직연산 사능 
// 나눗셈 후 몫
** 제곱승 2**3 2의 3승
% 나머지 반환 


문자열안에 작은따움표 큰따움표
+ 안에 \ 백슬레쉬 포함하면됨
\n  엔터 느낌입니다. 

인덱싱
a[-1]위에서 첫번째 입니다. 

4차시  문자열 format  
Formatting  원하느 자리에 넣는다 
%s 문자열 %c 문자 1개 %d 정수 %f 부동소수 
%o 8진수 %x 16진수

%0.5f 소수를 5째 자리까지만 표현합니다. 

a.count()  갯수  a.fing() 최소 나오는 인덱스 반환 없으면 -1 
a.index() 최초 나오는 문자 인덱스 없으묜 에러 
join 문자열 삽입 upper 대문자  lower 소무자 
rstrip() 오른쪽 공백 날리기 

5차 리스트 
리스트명 = [ , , ] 구별 합니다. 

a = [ 1,2,3]

a*3 하면 1,2,3,1,2,3,1,2,3 입니다 . 리스트 현산 다릅니다. 
a+a = a*2 
len(a) 길이 세기 

a.append() 붙이기 
a.sort() 정렬하기 
a.insert(0.1) 0번 위치에 1삽입하기. 
a.index()  찾기
a.pop() 맨뒤에 있는것을 꺼내면서 없에기 
a.remove()
a.clear()


6.차시  튜플
튜플은 () 둘러쌈 값변경 불가 
변경시 리스트 변경하고 삭제 하기 

딕셔너리 {} 대응 관계 key value  쌍 자료형 순차적 해당 요솟값
Key 로 value 값 얻는다.  
 
 
7차시 집합 자료형. 
순서 필요 없다. 중복 허용 안함. 

 s1 = set([1,2,34])
 교집합 s1&s1 또는 intersection()
합집합 | union  차집합 - difference()

add(), remove(), update()== 한꺼번에 추가 

리스트 복사 주의 !!
b= a 하면 너무 용량이 커긴다 . b = a[:]으로 하다 

8차시 boolean
비어 있으면 false !!! 숫자형은 0 은 거짓


9차시 사용자 입력과 출력

print() 안에 그냥 , 가 있으면 그거다 띄어쓰기
print( i, end ='') end는 띄어쓰기 가 default 값이다. 

input() 입력값 받기 

open(파일이름, 파일열기 모드) 
파일 열기 모드 R 읽기 읽는것만 가능, W 쓰기모드 내용 쓸때ㅐ, A 마지막내용 추가할때 

t = open('text.txt','w')
for i in range( 1 ,11):
    t.write('{} 너재 줄입니다. '.format(i))
    
t.close() # 저장하고 종료해주는 기능. 

t =open('text.txt'.'r)
data = t.read()
t.close()

print(data)


10차시 클래스 
class Bank : #클래스 : 함수 저장 주머니
    def deposit(self, a): # self 클래스 안에서 함수 사용시 꼭 필요
        self.money =a 


class Bank : #클래스 : 함수 저장 주머니

    def __init__(self, a) # 권한 줄때 자도응로 한번 실행되는 함수
        self.money =a   #즉 Bank(50000) 이면 최초에 실행하자마자 5만원 있다는 의미
    
    def deposit(self, a): # self 클래스 안에서 함수 사용시 꼭 필요
        self.money =a 

class Bank2(Bank) : #Bank2는 Bank 제공하느 서비스 모두 상속받는다는 의미


16차시 모듈
함수나변수 또는 클래스르 모아 놓은 파일 현재 py 파일입니다. 

import 묘듈 : 전체 가지고옴

from  모듈 import A : 모듈에서 한개 가지고옵니다.

예외처리 
try except   오류발생시 오류 발생시 except 실행
try except() 해당오류 발생시  없이 오류 발생시 except 실행

그냥함수에서 raise 시 강제 오류발새이


17차시 내장함수 

chr  아스키코드값
enumerate(x)  for문과 같이 사용가능. 

for i,name in enumerate(['body','foo','bar']):
    print(i,name) # i는 인덱스 , name 대응되는 값

eval(expression) # 해당된것이 실행될 수 있는가.

fiter(f,iterable)
iterable 자료형의 요소가 함수 f에 입력되었을때 반환값이 참인것만 묶어서 반환

def positive(x):
    return x>0
Print(list(filter(positive,[1,23,45,-1])))

hex(x) 16진수 변환  oct(x) 8진수 변환 
ord(c)  문자의 아스키값 pow(x,y) x의 y승
round(x,오려서 표현하고픈 소수자릿수 ) 반올림(0.5기준) sorted() 입력값 정렬후 리스트반환 

instance(object, class) #object가 해당 클래스인지 boolean

list(iterable)  list 변환 해준다. 
map(f,iterable)  
str() 문자열 변환 sum()모두 합하기 
tuple() 자료형을 튜플형태로 합니다. 
type() 무슨타입인지 알려 줍니다. 

list(zip([1,2,3],[4,5,6])) == [(1, 4), (2, 5), (3, 6)]



"""

print(list(zip([1,2,3],[4,5,6])))


a = [10,10.4, 20, 30, 'Java','Python']

char = len(a)

a[3] = 20

print(a.index('Java'))
a.append([20,'C#'])
print(a)

a.clear()
print(a)

#=======  딕셔너리  무조건 키값기준
a = {1:'a',2:'b'}
a[5] ='b'
print(a)
del a[1]
print(a)
print(a.keys())
print(a.values())
print( 2 in a)
print(a.items())

print(a)

print()

for i in range(1,6,1):
    for j in range(1,i+1,1):
        print( "*" , end= " ")
    
    print(i)


str = "you 1 2 3"
print("".join(['you','need','python']))
print('you'.join('ser'))
print(str.split())

stocks = {'005930':'삼성전자', '035420':'네이버'}
stocks['035420'] = 'NAVER'

print(stocks)

print()

import numpy as np 

arr = np.arange(1,17)
arr = arr.reshape(1,4,4) 
#arr = arr.reshape(1,-1,4)
#arr = arr.reshape(1,4,-1)

print(arr)

print()
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15], [16, 17, 18]])
print(np.array_split(arr, 3))
print()
print(np.array_split(arr, 3, axis=1))



