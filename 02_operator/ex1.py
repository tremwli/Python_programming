# 연산자

# 산술 연산자
a = 10
b = 3
print(a + b)
print(a - b)
print(a * b)
print(a / b) # 무조건 플롯 타입
print(a % b)
print( a // b)
print(a ** b) # 거듭제곱

# 복합 대입 연산자
a = 0
a += 4

# 증감 연산자 없음
# b = a++ << 오류남
a += 1

# 비교 연산자
print(3 == 3.0)
print(3 != 4)
print("apple" < "apble") # c처럼 사전순
print(1 < 2 < 3) # 연쇄 비교 가능, 1 < 2 and 2 < 3 이렇게 해석함
print(1 < 3 < 2) # true and false 여서 false 로 나옴

# 논리 연산자 (and, or, not)
a = True
b = False

print(a and b)
print(a or b)
print(not b)

# print(a / b)

if a > 0 or a /b :
    print("yes")
else:
    print("no")

# 비트 연산자
a = 5 # 0000 0101
b = 3 # 0000 0011

print(a & b) # 둘 다 1이여야 1
print(a | b) # 둘 중에 하나라고 1이면 1
print(a ^ b) # 둘이 다르면 1
print(a << b) # 5 -> 10 -> 20 -> 40 (3칸 옮겼으니까 2의 3승 곱한거랑 같음)
print(40 >> b) # 5
print(~a) # 1111 1010 반전

# 멤버십 연산자
print("a" in "apple")
print(3 in [1, 2, 3])

# 삼항 연산자
# C로는 int max = a > b ? a : b;
a if a > b else b # a다. 만약 a가 b보다 크면. 아니면 b다.
print("짝수") if a % 2 == 0 else print("홀수") 

score = 85
grade = None
grade = 'A' if score >= 90 else 'B' if score >= 80 else 'C' if score >= 70 else 'D'  
print(grade)





