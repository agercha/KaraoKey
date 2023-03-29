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
    if random.randint(0, 10) > 7:
        user_diff = (random.randint(int(-val*20),100)/100)
    user_arr.append(val + user_diff)
    val += target_diff
    target_arr.append(val)

print(f'\"length\": {l},\n\"target\": {target_arr},\n\"user\": {user_arr},\n')