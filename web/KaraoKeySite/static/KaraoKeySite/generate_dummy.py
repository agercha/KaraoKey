import random


l =  random.randint(50, 150)
# l = 146

target_arr = []
user_arr= []
val = 1
for i in range(l):
    target_diff = 0
    user_diff = 0
    if random.randint(0, 10) > 7:
        target_diff = (random.randint(int(-val*50),100)/100)
    val += target_diff
    target_arr.append(val)
    if random.randint(0, 10) > 7:
        user_diff = (random.randint(int(-val*20),20)/100)
    user_arr.append(val + user_diff)

# print(f'\"length\": {l},\n\t"target\": {target_arr},\n\t\"user\": {user_arr},\n\t\t')

# with open("../../../../scratchwork/Kelly/C_Major_Scale_Slow_piano.txt") as f:
with open("hbdtarget.txt") as f:
    all_vals = f.read().split("\n")

new_arr = [min(600, round(float(line.split()[1]), 2)) for line in all_vals]
# print(new_arr)
# print(len(new_arr))

print(new_arr.index(303.2))

# 