# for 문

# for x in 리터러블(반복하능한)객체:
# ....

for i in range(5):
    print(i, end = " ")

a = range(5)
print()
print(a.start, a.stop, a.step)

# 1~5
for i in range(1, 6):
    print(i, end = " ")
print()

# 1~10, 2칸씩
for i in range(1, 10, 2):
    print(i, end=" ")
print()
# 5, 4, 3, 2, 1
for i in range(5, 0, -1):
    print(i, end=" ")

# 1~10까지의 합
tot = 0
for i in range(1, 11):
    tot += i
else:
    print()
    print(tot)

print(sum(range(1, 11)))

s = "hi오늘은JK의생일이야🌟花樣年華, 2014~forever"

for c in s:
    print(c) # 유니코드 기반이라 알파벳이든 한글이든 한자든 다 똑같이 셈
print(len(s))

# 구구단 출력
for i in range(2, 10):
    for j in range(1, 10):
        print(f"{i} * {j} = {i*j:<5d} | ", end=" ")
    print()



