import matplotlib.pyplot as plt
import japanize_matplotlib
import numpy as np
from collections import Counter

def plot_bounded_obj_num(bouded_obj_num: list, title: str):
    frame_sum = len(bouded_obj_num)
    counter = Counter(bouded_obj_num)
    print(counter)
    plt.figure(figsize=(10, 5))
    plt.bar(counter.keys(), counter.values())
    
    plt.title(title)
    plt.xlabel("オブジェクト数")
    plt.ylabel(f"コマ数({frame_sum}コマ)")
    plt.xticks(np.arange(0, len(counter)+1, 1))
    
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.savefig("bounded_obj_num.png")
    plt.show()