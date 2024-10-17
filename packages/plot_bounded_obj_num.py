import matplotlib.pyplot as plt
import japanize_matplotlib
import numpy as np
from collections import Counter

def plot_bounded_obj_num(bouded_obj_num: list, title: str, file_name: str):
    frame_sum = len(bouded_obj_num)
    # 10以上のオブジェクト数を10にまとめる
    processed_data = [10 if x >= 10 else x for x in bouded_obj_num]

    # オブジェクト数の頻度を計算
    counter = Counter(processed_data)

    # キーを整数として取得し、ソート
    sorted_keys = sorted(int(k) if isinstance(k, str) else k for k in counter.keys())
    values = [counter[k] for k in sorted_keys]

    # プロットの準備
    plt.figure(figsize=(12, 6))
    bars = plt.bar(range(len(sorted_keys)), values)

    # グラフの設定
    plt.title(f'{title}')
    plt.xlabel('オブジェクト数')
    plt.ylabel(f'コマ数({frame_sum}コマ)')

    # x軸のラベルを調整（10を「10以上」に変更）
    labels = [str(k) if k < 10 else '<10' for k in sorted_keys]
    plt.xticks(range(len(sorted_keys)), labels)

    # 各バーの上に値を表示
    for i, v in enumerate(values):
        plt.text(i, v, str(v), ha='center', va='bottom')

    # グリッドの追加
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # プロットの表示
    plt.tight_layout()
    plt.savefig(f'{file_name}.png')
    plt.show()