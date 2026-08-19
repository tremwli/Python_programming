# 입출력 처리

# 1개 입력
a = input()
print(a)
print(type(a))

# 정수 변환
a = input()
a = int(a)
print(type(a))

# 한 번에 쓰자
a = int(input())
print(type(a))

# 실수 입력
b = float(input(a))
print(b, type(b))

# 정수 2개 입력
# 100
# 200
a = int(input())
b = int(input())
print(a, b)

# 100 200 입력
a = (
    input().split()  # 스플릿: 괄호 안에 나누는 기준을 쓰기. 생략 시 스페이스바가 기준이 됨
)
print(a)  # 리스트를 리턴함

# map 사용하기
# map(함수명, 리스트)
a, b, c = map(
    int, input().split(),  # input받은 거 리스트로 만들고 int로 형변환 후 a, b, c에 하나씩 넣어줌
)
print(a, b, c)

# 리스트로 변환
a = list(map(int, input().split()))
print(a)



