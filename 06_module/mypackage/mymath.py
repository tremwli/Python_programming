# 사용자 정의 모듈
print("start:", __name__)       # __name__: 모듈의 이름을 가져오는 내장 함수
PI = 3.14

def add(a, b):
    return a, b

if __name__ == "__main__":      # 내가 실행했을 때만 프린트되고, import 했을때는 프린트 안됨
    print(PI)
    print(add(1, 2))

