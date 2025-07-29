import json
import glob
import os
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
import seaborn as sns
from pycocotools import mask as maskUtils

def plot_balloon_size_ratio(annotations_dir: str, output_dir: str = "./"):
    """
    吹き出し領域のサイズと画像全体のサイズの比をプロットする
    
    Args:
        annotations_dir: JSONアノテーションファイルがあるディレクトリパス
        output_dir: グラフの保存先ディレクトリ
    """
    # 画像サイズ（固定）
    IMAGE_WIDTH = 1654
    IMAGE_HEIGHT = 1170
    IMAGE_AREA = IMAGE_WIDTH * IMAGE_HEIGHT
    
    # 吹き出しサイズの比率を格納するリスト
    balloon_ratios = []
    balloon_areas = []
    manga_titles = []
    
    # JSONファイルを取得
    json_files = glob.glob(os.path.join(annotations_dir, "*.json"))
    
    print(f"Found {len(json_files)} JSON files")
    
    for json_path in json_files:
        print(f"Processing: {os.path.basename(json_path)}")
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # カテゴリID → クラス名のマッピング
        category_map = {cat['id']: cat['name'] for cat in data.get("categories", [])}
        
        # 画像ID → ファイル名のマッピング
        id_to_filename = {img['id']: img['file_name'] for img in data['images']}
        
        # 各アノテーションを処理
        for ann in data['annotations']:
            category_id = ann['category_id']
            class_name = category_map.get(category_id, f"category_{category_id}")
            
            # 吹き出し（balloon）クラスのみを対象とする
            if 'balloon' in class_name.lower() or 'speech' in class_name.lower():
                segmentation = ann['segmentation']
                
                # RLEデコードしてマスクを取得
                mask = maskUtils.decode(segmentation)
                if len(mask.shape) == 3:
                    mask = np.any(mask, axis=2).astype(np.uint8)
                
                # 吹き出し領域のピクセル数を計算
                balloon_area = np.sum(mask)
                
                # 画像全体に対する比率を計算
                ratio = balloon_area / IMAGE_AREA
                
                # データを保存
                balloon_ratios.append(ratio)
                balloon_areas.append(balloon_area)
                
                # マンガタイトルを取得
                image_id = ann['image_id']
                file_name = id_to_filename[image_id]
                manga_title = file_name.split("/")[0] if "/" in file_name else "unknown"
                manga_titles.append(manga_title)
    
    print(f"Found {len(balloon_ratios)} balloon annotations")
    
    if len(balloon_ratios) == 0:
        print("No balloon annotations found!")
        return
    
    def create_graphs(language='english'):
        """グラフを作成する関数（言語切り替え対応）"""
        # 日本語フォント設定
        # if language == 'japanese':
        #     plt.rcParams['font.family'] = ['DejaVu Sans', 'Hiragino Sans', 'Yu Gothic', 'Meiryo', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']
        
        # グラフのスタイル設定
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 言語別のタイトルとラベル
        if language == 'japanese':
            fig.suptitle('吹き出しサイズ分析', fontsize=16, fontweight='bold')
            xlabel_ratio = '吹き出しサイズ比率 (吹き出し面積 / 画像面積)'
            ylabel_frequency = '頻度'
            title_ratio_dist = '吹き出しサイズ比率の分布'
            xlabel_area = '吹き出し面積 (ピクセル)'
            title_area_dist = '吹き出し面積の分布'
            xlabel_manga = 'マンガタイトル'
            ylabel_ratio = '吹き出しサイズ比率'
            title_boxplot = 'マンガタイトル別吹き出しサイズ比率 (上位10作品)'
            ylabel_cumulative = '累積確率'
            title_cumulative = '吹き出しサイズ比率の累積分布'
            mean_label = f'平均: {mean_ratio:.4f}'
            median_label = f'中央値: {median_ratio:.4f}'
            no_titles_text = 'マンガタイトル数が\n不足しています'
        else:
            fig.suptitle('Balloon Size Analysis', fontsize=16, fontweight='bold')
            xlabel_ratio = 'Balloon Size Ratio (Balloon Area / Image Area)'
            ylabel_frequency = 'Frequency'
            title_ratio_dist = 'Distribution of Balloon Size Ratios'
            xlabel_area = 'Balloon Area (pixels)'
            title_area_dist = 'Distribution of Balloon Areas'
            xlabel_manga = 'Manga Title'
            ylabel_ratio = 'Balloon Size Ratio'
            title_boxplot = 'Balloon Size Ratios by Manga Title (Top 10)'
            ylabel_cumulative = 'Cumulative Probability'
            title_cumulative = 'Cumulative Distribution of Balloon Size Ratios'
            mean_label = f'Mean: {mean_ratio:.4f}'
            median_label = f'Median: {median_ratio:.4f}'
            no_titles_text = 'Not enough manga titles\nfor comparison'
        
        # 1. 吹き出しサイズ比率のヒストグラム
        axes[0, 0].hist(balloon_ratios, bins=50, alpha=0.7, color='skyblue', edgecolor='black')
        axes[0, 0].set_xlabel(xlabel_ratio)
        axes[0, 0].set_ylabel(ylabel_frequency)
        axes[0, 0].set_title(title_ratio_dist)
        axes[0, 0].grid(True, alpha=0.3)
        
        # 統計情報を追加
        axes[0, 0].axvline(mean_ratio, color='red', linestyle='--', label=mean_label)
        axes[0, 0].axvline(median_ratio, color='orange', linestyle='--', label=median_label)
        axes[0, 0].legend()
        
        # 2. 吹き出し面積のヒストグラム
        axes[0, 1].hist(balloon_areas, bins=50, alpha=0.7, color='lightgreen', edgecolor='black')
        axes[0, 1].set_xlabel(xlabel_area)
        axes[0, 1].set_ylabel(ylabel_frequency)
        axes[0, 1].set_title(title_area_dist)
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. 吹き出しサイズ比率のボックスプロット（マンガタイトル別）
        if len(set(manga_titles)) > 1:
            # マンガタイトル別のデータを準備
            title_ratios = {}
            for title, ratio in zip(manga_titles, balloon_ratios):
                if title not in title_ratios:
                    title_ratios[title] = []
                title_ratios[title].append(ratio)
            
            # 上位10タイトルのみ表示（データが多い場合）
            sorted_titles = sorted(title_ratios.items(), key=lambda x: len(x[1]), reverse=True)[:10]
            
            box_data = [ratios for _, ratios in sorted_titles]
            box_labels = [title for title, _ in sorted_titles]
            
            axes[1, 0].boxplot(box_data, labels=box_labels)
            axes[1, 0].set_xlabel(xlabel_manga)
            axes[1, 0].set_ylabel(ylabel_ratio)
            axes[1, 0].set_title(title_boxplot)
            axes[1, 0].tick_params(axis='x', rotation=45)
            axes[1, 0].grid(True, alpha=0.3)
        else:
            axes[1, 0].text(0.5, 0.5, no_titles_text, 
                           ha='center', va='center', transform=axes[1, 0].transAxes)
            axes[1, 0].set_title(title_boxplot)
        
        # 4. 累積分布関数
        sorted_ratios = np.sort(balloon_ratios)
        cumulative = np.arange(1, len(sorted_ratios) + 1) / len(sorted_ratios)
        axes[1, 1].plot(sorted_ratios, cumulative, linewidth=2, color='purple')
        axes[1, 1].set_xlabel(xlabel_ratio)
        axes[1, 1].set_ylabel(ylabel_cumulative)
        axes[1, 1].set_title(title_cumulative)
        axes[1, 1].grid(True, alpha=0.3)
        
        # レイアウトの調整
        plt.tight_layout()
        
        return fig

    # 統計情報を事前に計算
    mean_ratio = np.mean(balloon_ratios)
    median_ratio = np.median(balloon_ratios)
    
    # 英語版グラフを作成・保存
    fig_en = create_graphs('english')
    output_path_en = os.path.join(output_dir, 'balloon_size_ratio_analysis_en.png')
    fig_en.savefig(output_path_en, dpi=300, bbox_inches='tight')
    print(f"English graph saved to: {output_path_en}")
    
    # 日本語版グラフを作成・保存
    fig_jp = create_graphs('japanese')
    output_path_jp = os.path.join(output_dir, 'balloon_size_ratio_analysis_jp.png')
    fig_jp.savefig(output_path_jp, dpi=300, bbox_inches='tight')
    print(f"Japanese graph saved to: {output_path_jp}")
    
    # 後方互換性のため、英語版を従来のファイル名でも保存
    output_path = os.path.join(output_dir, 'balloon_size_ratio_analysis.png')
    fig_en.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Graph saved to: {output_path}")
    
    # 統計情報をテキストファイルに保存（英語版）
    stats_path = os.path.join(output_dir, 'balloon_size_statistics.txt')
    with open(stats_path, 'w', encoding='utf-8') as f:
        f.write("Balloon Size Ratio Statistics\n")
        f.write("=" * 40 + "\n")
        f.write(f"Total balloon annotations: {len(balloon_ratios)}\n")
        f.write(f"Image size: {IMAGE_WIDTH} x {IMAGE_HEIGHT} pixels\n")
        f.write(f"Total image area: {IMAGE_AREA:,} pixels\n\n")
        
        f.write("Ratio Statistics:\n")
        f.write(f"Mean: {np.mean(balloon_ratios):.6f}\n")
        f.write(f"Median: {np.median(balloon_ratios):.6f}\n")
        f.write(f"Standard deviation: {np.std(balloon_ratios):.6f}\n")
        f.write(f"Min: {np.min(balloon_ratios):.6f}\n")
        f.write(f"Max: {np.max(balloon_ratios):.6f}\n")
        f.write(f"25th percentile: {np.percentile(balloon_ratios, 25):.6f}\n")
        f.write(f"75th percentile: {np.percentile(balloon_ratios, 75):.6f}\n\n")
        
        f.write("Area Statistics (pixels):\n")
        f.write(f"Mean: {np.mean(balloon_areas):.2f}\n")
        f.write(f"Median: {np.median(balloon_areas):.2f}\n")
        f.write(f"Standard deviation: {np.std(balloon_areas):.2f}\n")
        f.write(f"Min: {np.min(balloon_areas):.2f}\n")
        f.write(f"Max: {np.max(balloon_areas):.2f}\n")
    
    print(f"Statistics saved to: {stats_path}")
    
    # 統計情報をテキストファイルに保存（日本語版）
    stats_path_jp = os.path.join(output_dir, 'balloon_size_statistics_jp.txt')
    with open(stats_path_jp, 'w', encoding='utf-8') as f:
        f.write("吹き出しサイズ比率統計\n")
        f.write("=" * 40 + "\n")
        f.write(f"吹き出しアノテーション総数: {len(balloon_ratios)}\n")
        f.write(f"画像サイズ: {IMAGE_WIDTH} x {IMAGE_HEIGHT} ピクセル\n")
        f.write(f"画像総面積: {IMAGE_AREA:,} ピクセル\n\n")
        
        f.write("比率統計:\n")
        f.write(f"平均: {np.mean(balloon_ratios):.6f}\n")
        f.write(f"中央値: {np.median(balloon_ratios):.6f}\n")
        f.write(f"標準偏差: {np.std(balloon_ratios):.6f}\n")
        f.write(f"最小値: {np.min(balloon_ratios):.6f}\n")
        f.write(f"最大値: {np.max(balloon_ratios):.6f}\n")
        f.write(f"25パーセンタイル: {np.percentile(balloon_ratios, 25):.6f}\n")
        f.write(f"75パーセンタイル: {np.percentile(balloon_ratios, 75):.6f}\n\n")
        
        f.write("面積統計 (ピクセル):\n")
        f.write(f"平均: {np.mean(balloon_areas):.2f}\n")
        f.write(f"中央値: {np.median(balloon_areas):.2f}\n")
        f.write(f"標準偏差: {np.std(balloon_areas):.2f}\n")
        f.write(f"最小値: {np.min(balloon_areas):.2f}\n")
        f.write(f"最大値: {np.max(balloon_areas):.2f}\n")
    
    print(f"Japanese statistics saved to: {stats_path_jp}")
    
    # 日本語版グラフを表示
    plt.show()


if __name__ == "__main__":
    # 使用例
    annotations_dir = "./../annotations/"  # JSONファイルがあるディレクトリを指定
    output_dir = "./"
    
    plot_balloon_size_ratio(annotations_dir, output_dir)
