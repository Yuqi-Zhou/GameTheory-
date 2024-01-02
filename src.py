import random
from tqdm import tqdm
import numpy as np
RUN_TIME=1
WAIT_TIME=1
MAX_EVAL=15

def generate_random_list(user_num):
    random_list = [random.randint(0, 10) for _ in range(9)]
    
    # 调整列表中的元素，使其总和为20
    while sum(random_list) != user_num:
        index = random.randint(0, 8)
        difference = user_num - sum(random_list)
        random_list[index] = max(0, random_list[index] + difference)
    
    return random_list

def last_positive_index(lst):
    for i in range(len(lst) - 1, -1, -1):
        if lst[i] > 0:
            return i

def second_positive_index(lst):
    flag = 1
    for i in range(len(lst) - 1, -1, -1):
        if lst[i] > 0:
            if flag == 0:
                return i
            else:
                flag -= 1
    return None

def modify_single_time(user_list):
    index = last_positive_index(user_list)
    run_time = 2*(index+1)*RUN_TIME
    wait_floor = sum([1 for u in user_list if u > 0])
    wait_time = 2*(wait_floor-1)*WAIT_TIME + WAIT_TIME
    user_num = sum([i for i in user_list])
    return (run_time + wait_time) * user_num

def modify_multi_time(user_list):
    eval0, eval1 = 0, 0
    lst_index = last_positive_index(user_list)
    wait_floor = sum([1 for u in user_list if u > 0])
    second_index = second_positive_index(user_list)
    user_num = sum([i for i in user_list])

    if second_index is None:
        return ((lst_index+1)*RUN_TIME + WAIT_TIME)*user_num
    
    index = 0
    for i in range(lst_index+1):
        user_num = user_list[i]
        if user_num > 0:
            if index % 2 == 0:
                eval0 += user_num
            else:
                eval1 += user_num
            index += 1
    time0 = ((wait_floor+1)/2*WAIT_TIME + 2*(lst_index+1)*RUN_TIME ) * eval0
    time1 = ((wait_floor)/2*WAIT_TIME + 2*(second_index+1)*RUN_TIME ) * eval1
    return time0 + time1

def modify_single_fairness(user_list):
    # wait_floor = sum([1 for u in user_list if u > 0])
    index, num = 0, 0
    fairness = 0
    for i, u in enumerate(user_list):
        if u > 0:
            index += 1
            pre_num = num
            num += u
            fairness = fairness + (i+1) * max(0, num - max(2*MAX_EVAL, pre_num))
    return fairness

def modify_multi_fairness(user_list):
    index, eval0, eval1, fairness = 0, 0, 0, 0
    for i, u in enumerate(user_list):
        if u > 0:
            if index % 2 == 0:
                pre_num = eval0
                eval0 += u
                fairness = fairness + (i+1) * max(0, eval0 - max(MAX_EVAL, pre_num))
            else:
                pre_num = eval1
                eval1 += u
                fairness = fairness + (i+1) * max(0, eval1 - max(MAX_EVAL, pre_num))                
            index += 1
    return fairness
            
def modify_time(seed=2023):
    ## 生成用户列表
    random.seed(seed)
    user_list = generate_random_list(15)
    single_time = modify_single_time(user_list)
    multi_time = modify_multi_time(user_list)
    return single_time, multi_time

def modify_fairness(seed=2023):
    ## 生成用户列表
    random.seed(seed)
    user_list = generate_random_list(50)
    single_fairness = modify_single_fairness(user_list)
    multi_fairness = modify_multi_fairness(user_list)
    return single_fairness, multi_fairness

if __name__ == "__main__":
    single_times, multi_times = [], []
    single_fairnesses, multi_fairnesses = [], []
    for seed in range(2024):
        single_time, multi_time = modify_time(seed)
        single_fairness, multi_fairness = modify_fairness(seed)
        single_times.append(single_time)
        multi_times.append(multi_time)
        single_fairnesses.append(single_fairness)
        multi_fairnesses.append(multi_fairness)
    print(f"single time: {np.mean(single_times)} multi time: {np.mean(multi_times)}")
    print(f"single fairness: {np.mean(single_fairnesses)} multi fairness: {np.mean(multi_fairnesses)}")
