# 반복문 - while, for

# while문
# 1~10까지의 반복 출력
i = 1
while i < 11:
    print(i)
    i += 1

    
else:
    print("End")

nums = [1, 3, 5, 7, 9]
target = 2
i = 0

while i < len(nums):
    if target == nums[i]:
        print(f"{target} found.")

    i+=1
else: 
    print(f"{target} not found.")

i = 2
tot = 0

while i < 11:
    tot += i
    i += 2

print(tot)

