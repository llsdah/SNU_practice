#4.6 numpy
"""
numpy : numerical python
array :배열사용으로 벡터 행렬 연산속도가 빠름

"""
import numpy as np
from numpy.random import randn

a1 = np.array([1,2,3]) #1 dimensional 
a2 = np.array([[1,2],[3,4]]) #2 dimensional [] 괄호가 2개있어야댐!! 감싸는것!
a3 = np.array([1,2,3,4], ndmin=3, dtype=float) # ndmin= 최소차원정의, dtype 데이터타입정의

print(a1, " a2: ",a2," a3 : ",a3)

print("shape : ",a3.shape," size : ",a3.size) #shape 차원, size 원소 갯수 반환

a4 =np.arange(24)# 0부터 23까지 24개의 원소를 가지는 1차원 배열반환

a5 =a4.reshape(2,3,4)# 밖에서부터 생각 3차원이 2개, 2차원(행)이 3개, 1차원(열)이 4개 a5.ndim은 3이다!

temp_one = np.ones(5) # 1이 5개 
temp_zeros =np.zeros([2,2])

a6 =np.arange(10,21,2) #10에서부터 21까지 2칸씩 21은없으므로 출력x
print(a6)

a7 = np.linspace(2.0,4.0,5) #2포함부터 4포함까지 5개의 수로 나눈다 

a8 = np.array(randn(4,4)*10,dtype=np.int8) # randn 정규분포생플링 소수점이라 그래서 10곱합닌다

a8.tolist() # a8의 list 반환
a8.flatten() #1차원으로 변환
a8 = np.array(randn(4,4)*10,dtype=np.int8) # randn 
a8.sum() #모든원소함0
a8.sum(axis=0) #axis=0, 행기준 즉!더해지는 방향이 1행 2행 순! 그렇다면 1열의 다 더하는것과 같은 개념
print(np.cos(a8)) # cos값구하지 입력되는 값은 radian으로 들어감

a9 = np.arange(1,17)
a9 = a9.reshape(1,4,4) # reshape안의 -1은 해당 차원의 갯수는 알아서 계산해 주겠다는의미

print(a9[0,1]) # a9은 3차원 ! 3차원은 첫번째 2차원의 2번쨰
print(a9[:,:,1:3])# 3차원의 전체, 2차원의 전체 1차원의 2번쨰에서 3번쨰!

a10 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15], [16, 17, 18]])
np.array_split(a10,3) # 행기준 3묶음으로 나눠라
print("np.array_split(a10,3)",np.array_split(a10,3))
np.array_split(a10,3,axis=1) # 열기준 3묶음으로 나눠라
print("np.array_split(a10,3,axis=1)",np.array_split(a10,3,axis=1))

#np.where(조건식)

a11 = np.arange(4, 20, 3) 
print("np.arange(4, 20, 3)",a11)
b = a11.reshape(2,-1)
print("a11.reshape(2,-1)",a11.reshape(2,-1))
np.where(a11%2==0)
np.where(b%2==0)


#pandas 
import pandas as pd
print()
print("print about pandas")
print()
p1 = pd.Series([1,2,3,4]) # 표를만들어준다. 1열만 생성
idx = pd.Index(["New York", "Los Angeles", "Chicago","Houston", "Philadelphia", "Phoenix", "San Antonio", "San Diego", "Dallas"]) #인덱스 즉, 행에대한 값넣어주기
p2 = pd.Series([8550, 3972, 2721, 2296, 1567, np.nan, 1470, 1395, 1300],  index=idx, name="Population") # name은 표?에 대응하는 이름

p3 = pd.DataFrame({'yes':[50,21],'No':[131,2] }) #우리가 아는 그 2차원행렬공간 :열의 이름 :[행입력]
p4 = pd.DataFrame({'Bob': ['I liked it.', 'It was awful.'], 'Sue': ['Pretty good.', 'Bland.']}, index=['Product A', 'Product B'])

#데이터불러오기

# 데이터 URL
url = 'https://raw.githubusercontent.com/chrisalbon/simulated_datasets/master/titanic.csv'
dataframe = pd.read_csv(url)#url의 데이터 읽기어서 담기 
dataframe.head(2) # 앞의 2개의 열만 찾기 +tail
dataframe.shape #차원확인
dataframe.describe() # 통계정보 요약확인 열별로!

#탐색
"""
iloc : interger location 약어, index로 탐색 df.iloc[0,2] 1행 3열
loc : 특정컬럼명을 적거나 조건식으로 사람이 읽기좋게 탐색    
"""
df1 = pd.read_csv('https://raw.githubusercontent.com/chrisalbon/simulated_datasets/master/titanic.csv')
df1.iloc[0:3] # 1~3행의.
df1.loc[1:4] # 2행에서 5행까지!!
df1 =df1.set_index(df1['Name']) # 기존 인덱스 0~숫자를 Name이라는 컬럼으로 변경한다
df1.loc[:'Allison, Miss Helen Loraine', 'Age':'Sex']
df1[['Age', 'Sex']].head(2) #해당컬럼만 선정할떄 리스트로

url = 'https://raw.githubusercontent.com/chrisalbon/simulated_datasets/master/titanic.csv'
df2 =pd.read_csv(url)
df2[(df2['Sex'] == 'female') & (df2['Age'] >= 65)].head(2) #조건식첨부가능
df2['Name'].str.find('Allison')#name열을 str 로 값변혼후. find allison 있으면 0 아니면 -1

#해당컬럼의 산출평균 max min,mean, sum 결측치 제외
df2['Age'].max()
df2.count() #각열의 갯수출력 결축지 제외

df3 = pd.DataFrame(np.round(np.random.randn(7, 3) * 10),columns=["AAA", "BBB", "CCC"], index=list("defcabg"))
df3.sort_index() #기본 오름차순정렬 # index(행) abcd
df3.sort_index(axis=1,ascending=False)#열기준 내림차준
df3.sort_values(by=['AAA','BBB']) # 해당 열의 값을 기준으로


#groupby 그룹 및 그룹라벨자동 index
df4 = pd.DataFrame({
    'city': ['부산', '부산', '부산', '부산', '서울', '서울', '서울'], 'fruits': ['apple', 'orange', 'banana', 'banana', 'apple', 'apple', 'banana'], 'price': [100, 200, 250, 300, 150, 200, 400], 'quantity': [1, 2, 3, 4, 5, 6, 7] })

temp4 = df4.groupby(['city','fruits'], as_index=False).mean()

# 데이터 URL
# 데이터를 적재합니다.
df5 = pd.read_csv('https://raw.githubusercontent.com/chrisalbon/simulated_datasets/master/titanic.csv')
def uppercase(x):# 함수를 만듭니다.
    return x.upper()
df5['Name'].apply(uppercase)[0:2]# 함수를 적용하고 두 개의 행을 출력합니다.
df5['Survived'].map({1:'Live',0:"Dead"})[:5]
df5['Age'].apply(lambda x, age: x < age, age=30)[:5] ##람다식안에 어떻게 들어가있는건강


#연결

data_a = {'id': ['1', '2', '3'], 'first': ['Alex', 'Amy', 'Allen'], 'last': ['Anderson', 'Ackerman', 'Ali']}
dataframe_a = pd.DataFrame(data_a, columns = ['id', 'first', 'last'])

# 데이터프레임을 만듭니다.
data_b = {'id': ['4', '5', '6'], 'first': ['Billy', 'Brian', 'Bran'],'last': ['Bonder', 'Black', 'Balwner']}
dataframe_b = pd.DataFrame(data_b, columns = ['id', 'first', 'last'])

# 행 방향으로 데이터프레임을 연결합니다. 즉, 아래로 붙인다 
pd.concat([dataframe_a, dataframe_b], axis=0)
pd.concat([dataframe_a, dataframe_b], axis=1) # 열방향 옆으로! 붙인다


#결측치 다루기 

df6 = pd.DataFrame([[np.nan, 2, np.nan, 0], [3, 4, np.nan, 1], [np.nan, np.nan, np.nan, 5], [3, 4, np.nan, 1], [3, 4, 0, 1]], columns=list('ABCD'))

df6.dropna() #결측치 있는 행을 없엔다
df6.dropna(axis=1) #결측치 있는 열을 없엔다
df6.dropna(subset=['A','B']) #a외b 열에 na가 있는 행삭제
df6.fillna(0) #결측치 0으롤
df6.isnull() #없으면 진실
df6.fillna(method='ffill') #결측치를열 바로 위에 값으로 대체 
df6.fillna(method='bfill') #결측치를열 바로 아래에 값으로 대체 

# 연습문제풀이

#Replace NaNs with ‘missing’ in columns 'Manufacturer', 'Model' and 'Type'
print()
print("exercise")
print()
ex_df1 = pd.read_csv('https://raw.githubusercontent.com/selva86/datasets/master/Cars93_miss.csv', usecols=[0,1,2,3,5]) #dataset에서 필요한 열

#print(ex_df1[ ['Manufacturer','Type','Model']].fillna("missing"))
#ans


#row sum < 100인 행들 중 마지막 두 행을 출력하기

ex_df2 = pd.DataFrame(np.random.randint(10, 40, 60).reshape(-1, 4))
#print(ex_df2.sum()) # 행기준 이니 열의합
#print(ex_df2[ex_df2.sum(axis=1)<100].head(2))


#데이터 프레임의 대각 원소를 모두 0으로 바꿔보기

ex_df3 = pd.DataFrame(np.random.randint(1,100, 100).reshape(10, -1))
#for i in range(10):
#    ex_df3.iloc[i,i]=0

#1) 과일별 가격의 평균?

ex_df4 = pd.DataFrame({'fruit': ['apple', 'banana', 'orange'] * 3,'rating': np.random.rand(9), 'price': np.random.randint(0, 15, 9)})
#print(ex_df4.groupby('fruit').mean()['price'])

#2) rating이 두번째로 높은 바나나의 rating 값은 얼마인가?
#print(ex_df4[ex_df4.sort_values('rating')['fruit']=='banana'].loc[1,'rating'])


#PetalLength > 1.5이고, SepalLength < 5.0인 행 갯수는?
"""
from sklearn.datasets import load_iris
iris = load_iris()
df = pd.DataFrame(data= np.c_[iris['data'], iris['target']], columns= iris['feature_names'] + ['target'])
df.head()
"""


#아래 데이터프레임의 빈 값을 각 열의 평균으로 채워넣기

ex_df7 = pd.DataFrame([[np.nan, 2, np.nan, 0], [3, 4, np.nan, 1], [np.nan, np.nan, np.nan, 5],[3, 4, np.nan, 1], [3, 4, 0, 1]], columns=list('ABCD'))
print(ex_df7.fillna(ex_df7.mean(axis=0)))


