from matplotlib import pyplot as plt
import japanize_matplotlib

def plot_layout(layout_list, title: str, file_name: str):
    frame_num = len(layout_list)
    layout_counts = {}
    for layout in layout_list:
        if layout in layout_counts:
            layout_counts[layout] += 1
        else:
            layout_counts[layout] = 1
            
    # 配置のリストと対応するカウントのリストを作成
    layouts = list(layout_counts.keys())
    counts = list(layout_counts.values())
    
    # 図とサブプロットを作成
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # 棒グラフを描画
    ax.bar(layouts, counts)
    
    # 棒の上に割合を表示
    
    # for i, count in enumerate(counts):
    #     ax.text(i, count, str(count), ha='center', va='bottom')
    
    # タイトルと軸ラベルを設定
    ax.set_title(title)
    ax.set_xlabel('コマ内キャラクタと吹き出しの位置関係(t=テキスト, c=キャラクタ)')
    ax.set_ylabel('コマ数(全コマ数: {})'.format(frame_num))
    
    # x軸のティックラベルを設定
    ax.set_xticklabels(layouts)
    
    # グリッドを表示
    ax.grid(True)
    
    # レイアウトの調整
    plt.tight_layout()
    
    # プロットを表示
    plt.savefig(f'{file_name}.png')
    plt.show()