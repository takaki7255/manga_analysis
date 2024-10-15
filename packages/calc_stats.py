import numpy as np
from scipy import stats

def calc_stats(data):
    mode_result = stats.mode(data)
    mode = mode_result.mode if mode_result.mode.size > 0 else None
    median = np.median(data)
    mean = np.mean(data)
    variance = np.var(data, ddof=1)
    std_dev = np.std(data, ddof=1)
    # write to file
    with open('result.txt', 'w') as f:
        f.write(f'最頻値: {mode}\n')
        f.write(f'中央値: {median}\n')
        f.write(f'平均: {mean}\n')
        f.write(f'分散: {variance}\n')
        f.write(f'標準偏差: {std_dev}\n')
    return mode, median, mean, variance, std_dev