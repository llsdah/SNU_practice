#4월 1주차

#4.5 basic
"""

- math : exp,log,sqrt
- String : split, join replae, upper, lower, capitalize

"""

# list
a_list = [1,2,2,3,2,3,4]
print( len(a_list),max(a_list),min(a_list) )
a_list.append(4)
a_list.remove(2) # 한개 선입선출

print("a_list",a_list)
a_list.pop()
b_list = "하이 는 이 것이다. 하하"
b_list = b_list.split(" ")
b_list.sort(key=len) #기준이되는것을 길이로 삼는다

# tuple 수정불가!
t = 1,3,4,2,5 #
print(type(t))
t = (1,3,4,2,5) #동일지정
print(type(t))


# dictionary
grade ={'pay':10,'juliet':99}
print(grade['pay']) # dic[key]=value
print(grade.get('pay')) # dic.get(key)=value, #없으면 none
grade.update({'bob':99,'tony':33}) #한꺼번에 수정가능
del grade['juliet'] #삭제
grade.keys() #리스트반환
grade.values() #  #([('pay', 10), ('bob', 99), ('tony', 33)]) 이런형식 반환.
print(grade.items(), " type : ",type(grade.items()))

#enumerate 순차자료형 index와 value 동시 처리 


#def 함수
def add_many(*args): #해당 값을다시 다른 함수로 넘길때 *args다시쓰면됨
    result =0
    for i in args:
        result+=result
    return result


#lambda 익명함수
 
#(lambda x: age=30; x+age) 


# map : map(function,iterable)
#=> map 처리후 list 또는tuple 사용

temp  = list(map(lambda x: x+1,[10,11,12]))
print(temp)
# class
class Person:
    def __init__(self,name,age, gender):
        self.Name =name
        self.Age =age
        self.Gender = gender
    
    def aboutMe(self):
        print("이름",self.Name)

class Employee(Person):
    def __init__(self, name, age, gender,salary,hiredate):
        super().__init__(name, age, gender)# 부모생성자
        self.Salary =salary
        self.Hiredate = hiredate
    def doWork(self):
        print("일한다")
    def aboutMe(self): # 재정의
        print("연본ㅇ",self.Salary)
person = Employee("정우진", "25", "female", "10억", "3월 1일")    
person.aboutMe()







