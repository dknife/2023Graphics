
'''
# C style function

int factorial(int n) {
    int result = 1;
    for(int i=n; i>1; i--) {
        result *= i
    }
    return result
}
'''

# 파이썬 함수는 반환값의 형을 지정할 필요가 없다.

def factorial(n) :
    ### 함수의 몸체 블럭이 놓인다
    result = 1
    for i in range(n, 1, -1):
        result = result * i
    
    return n, result

n, nFact = factorial(7)
print(n, '의 팩토리얼은 ', nFact)

