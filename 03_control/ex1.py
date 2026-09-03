# 조건문 : if문, match문 (switch-case문같은거) ( 3.10 이상 )

age = 17
if age >= 18:
    print("성인")
else:
    print("미성년자")

score = 85

if score >= 90:
    print('A')
elif score >= 80:
    print('B')
elif score >= 70:
    print('C')
else:
    print('D')

grade = "A"

# match문
match grade:
    case "A" : 
        print("우수") # break 안 씀
    case "B" :
        print("양호")
    case "C" | "D":
        print("보통")
    case _: # 디폴트
        print("알 수 없음")

