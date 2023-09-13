
################# 조건문 

age = int ( input('나이가 얼마인가요?') )

### 나이를 보고 투표권이 있는지 없는지를 판정하여 알려주는 코드를 작성하라.

if age > 100:
    print('2장의 투표권이 있습니다.')
elif age >= 18 :
    print('1장의 투표권이 있습니다.')
else :
    print("투표권이 없습니다")


################## 반복문

for i in range(0,10,1) :    # C style = for (int i=0; i<10; i+=1) {}
    print(i)


for i in range(10):
    print(i)


### 20보다 작은 홀수를 출력하라

for i in range(1, 20, 2):
    print(i)


    
