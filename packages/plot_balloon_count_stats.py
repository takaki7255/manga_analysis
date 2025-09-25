import json
import glob
import os
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
import seaborn as sns
from collections import defaultdict, Counter

def plot_balloon_count_stats(annotations_dir: str, output_dir: str = "./"):
    """
    1画像中の吹き出し個数の統計情報を分析してプロットする
    （吹き出しがある画像のみを対象とする）
    
    Args:
        annotations_dir: JSONアノテーションファイルがあるディレクトリパス
        output_dir: グラフの保存先ディレクトリ
    """
    
    # 画像ごとの吹き出し個数を格納する辞書
    image_balloon_counts = defaultdict(int)
    manga_balloon_counts = defaultdict(list)
    all_counts = []
    
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
        
        # 各画像の吹き出し個数をカウント
        for ann in data['annotations']:
            category_id = ann['category_id']
            class_name = category_map.get(category_id, f"category_{category_id}")
            
            # 吹き出し（balloon）クラスのみを対象とする
            if 'balloon' in class_name.lower() or 'speech' in class_name.lower():
                image_id = ann['image_id']
                file_name = id_to_filename[image_id]
                
                # 画像ごとのカウントを増加
                image_balloon_counts[file_name] += 1
                
                # マンガタイトルを取得
                manga_title = file_name.split("/")[0] if "/" in file_name else "unknown"
    
    # 画像ごとの吹き出し個数リストを作成（吹き出しがある画像のみ）
    for file_name, count in image_balloon_counts.items():
        if count > 0:  # 吹き出しがある画像のみ
            manga_title = file_name.split("/")[0] if "/" in file_name else "unknown"
            manga_balloon_counts[manga_title].append(count)
            all_counts.append(count)
    
    # 統計情報の表示
    total_images_with_balloons = len(all_counts)
    total_images = len(image_balloon_counts)
    
    print(f"Analyzed {total_images} images")
    print(f"Images with balloons: {total_images_with_balloons}")
    print(f"Images without balloons: {total_images - total_images_with_balloons}")
    print(f"Total balloon annotations: {sum(all_counts)}")
    
    if len(all_counts) == 0:
        print("No images found!")
        return
    
    def create_graphs(language='english'):
        """グラフを作成する関数（言語切り替え対応）"""
        # グラフのスタイル設定
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 言語別のタイトルとラベル
        if language == 'japanese':
            fig.suptitle('1画像中の吹き出し個数統計（吹き出しがある画像のみ）', fontsize=16, fontweight='bold')
            xlabel_count = '1画像中の吹き出し個数'
            ylabel_frequency = '画像数'
            title_count_dist = '1画像中の吹き出し個数の分布'
            title_cumulative = '吹き出し個数の累積分布'
            title_boxplot = 'マンガタイトル別吹き出し個数 (上位10作品)'
            title_pie = '吹き出し個数別画像割合'
            xlabel_manga = 'マンガタイトル'
            ylabel_count = '吹き出し個数'
            ylabel_cumulative = '累積確率'
            mean_label = f'平均: {np.mean(all_counts):.2f}'
            median_label = f'中央値: {np.median(all_counts):.2f}'
        else:
            fig.suptitle('Balloon Count Statistics per Image (Images with Balloons Only)', fontsize=16, fontweight='bold')
            xlabel_count = 'Number of Balloons per Image'
            ylabel_frequency = 'Number of Images'
            title_count_dist = 'Distribution of Balloon Count per Image'
            title_cumulative = 'Cumulative Distribution of Balloon Count'
            title_boxplot = 'Balloon Count by Manga Title (Top 10)'
            title_pie = 'Image Proportion by Balloon Count'
            xlabel_manga = 'Manga Title'
            ylabel_count = 'Balloon Count'
            ylabel_cumulative = 'Cumulative Probability'
            mean_label = f'Mean: {np.mean(all_counts):.2f}'
            median_label = f'Median: {np.median(all_counts):.2f}'
        
        # 1. 吹き出し個数のヒストグラム
        max_count = max(all_counts) if all_counts else 0
        min_count = min(all_counts) if all_counts else 1
        bins = range(min_count, max_count + 2)
        axes[0, 0].hist(all_counts, bins=bins, alpha=0.7, color='skyblue', edgecolor='black')
        axes[0, 0].set_xlabel(xlabel_count)
        axes[0, 0].set_ylabel(ylabel_frequency)
        axes[0, 0].set_title(title_count_dist)
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].axvline(np.mean(all_counts), color='red', linestyle='--', label=mean_label)
        axes[0, 0].axvline(np.median(all_counts), color='orange', linestyle='--', label=median_label)
        axes[0, 0].legend()
        
        # 2. 累積分布関数
        sorted_counts = np.sort(all_counts)
        cumulative = np.arange(1, len(sorted_counts) + 1) / len(sorted_counts)
        axes[0, 1].plot(sorted_counts, cumulative, linewidth=2, color='purple', marker='o', markersize=3)
        axes[0, 1].set_xlabel(xlabel_count)
        axes[0, 1].set_ylabel(ylabel_cumulative)
        axes[0, 1].set_title(title_cumulative)
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. マンガタイトル別のボックスプロット
        if len(manga_balloon_counts) > 1:
            # 上位10タイトルのみ表示（画像数が多い順）
            sorted_manga = sorted(manga_balloon_counts.items(), 
                                key=lambda x: len(x[1]), reverse=True)[:10]
            
            box_data = [counts for _, counts in sorted_manga]
            box_labels = [title for title, _ in sorted_manga]
            
            axes[1, 0].boxplot(box_data, labels=box_labels)
            axes[1, 0].set_xlabel(xlabel_manga)
            axes[1, 0].set_ylabel(ylabel_count)
            axes[1, 0].set_title(title_boxplot)
            axes[1, 0].tick_params(axis='x', rotation=45)
            axes[1, 0].grid(True, alpha=0.3)
        else:
            no_data_text = 'マンガタイトル数が\n不足しています' if language == 'japanese' else 'Not enough manga titles\nfor comparison'
            axes[1, 0].text(0.5, 0.5, no_data_text, 
                           ha='center', va='center', transform=axes[1, 0].transAxes)
            axes[1, 0].set_title(title_boxplot)
        
        # 4. 吹き出し個数別画像割合の円グラフ
        count_distribution = Counter(all_counts)
        labels = []
        sizes = []
        colors = plt.cm.Set3(np.linspace(0, 1, len(count_distribution)))
        
        for count, freq in sorted(count_distribution.items()):
            if language == 'japanese':
                label = f'{count}個' if count > 0 else '0個'
            else:
                label = f'{count} balloons' if count != 1 else '1 balloon'
            labels.append(f'{label}\n({freq}枚)' if language == 'japanese' else f'{label}\n({freq} images)')
            sizes.append(freq)
        
        # 小さい割合をまとめる（5%未満）
        total_images = len(all_counts)
        threshold = 0.05 * total_images
        
        new_labels = []
        new_sizes = []
        other_count = 0
        
        for i, (label, size) in enumerate(zip(labels, sizes)):
            if size >= threshold:
                new_labels.append(label)
                new_sizes.append(size)
            else:
                other_count += size
        
        if other_count > 0:
            other_label = f'その他\n({other_count}枚)' if language == 'japanese' else f'Others\n({other_count} images)'
            new_labels.append(other_label)
            new_sizes.append(other_count)
        
        if new_sizes:
            wedges, texts, autotexts = axes[1, 1].pie(new_sizes, labels=new_labels, autopct='%1.1f%%', 
                                                     startangle=90, colors=colors[:len(new_sizes)])
            axes[1, 1].set_title(title_pie)
        
        # レイアウトの調整
        plt.tight_layout()
        
        return fig

    # 英語版グラフを作成・保存
    fig_en = create_graphs('english')
    output_path_en = os.path.join(output_dir, 'balloon_count_stats_en.png')
    fig_en.savefig(output_path_en, dpi=300, bbox_inches='tight')
    print(f"English graph saved to: {output_path_en}")
    
    # 日本語版グラフを作成・保存
    fig_jp = create_graphs('japanese')
    output_path_jp = os.path.join(output_dir, 'balloon_count_stats_jp.png')
    fig_jp.savefig(output_path_jp, dpi=300, bbox_inches='tight')
    print(f"Japanese graph saved to: {output_path_jp}")
    
    # 後方互換性のため、英語版を従来のファイル名でも保存
    output_path = os.path.join(output_dir, 'balloon_count_stats.png')
    fig_en.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Graph saved to: {output_path}")
    
    # 統計情報をテキストファイルに保存（英語版）
    stats_path = os.path.join(output_dir, 'balloon_count_statistics.txt')
    with open(stats_path, 'w', encoding='utf-8') as f:
        f.write("Balloon Count Statistics per Image (Images with Balloons Only)\n")
        f.write("=" * 65 + "\n")
        f.write(f"Images with balloons analyzed: {len(all_counts)}\n")
        f.write(f"Total balloon annotations: {sum(all_counts)}\n\n")
        
        f.write("Balloon Count Statistics:\n")
        f.write(f"Mean: {np.mean(all_counts):.6f}\n")
        f.write(f"Median: {np.median(all_counts):.6f}\n")
        f.write(f"Standard deviation: {np.std(all_counts):.6f}\n")
        f.write(f"Min: {np.min(all_counts)}\n")
        f.write(f"Max: {np.max(all_counts)}\n")
        f.write(f"25th percentile: {np.percentile(all_counts, 25):.2f}\n")
        f.write(f"75th percentile: {np.percentile(all_counts, 75):.2f}\n\n")
        
        # 吹き出し個数別の画像数分布
        count_distribution = Counter(all_counts)
        f.write("Distribution by Balloon Count:\n")
        for count in sorted(count_distribution.keys()):
            freq = count_distribution[count]
            percentage = (freq / len(all_counts)) * 100
            f.write(f"{count} balloons: {freq} images ({percentage:.1f}%)\n")
        
        f.write("\nTop 10 Manga Titles by Image Count:\n")
        sorted_manga = sorted(manga_balloon_counts.items(), 
                            key=lambda x: len(x[1]), reverse=True)[:10]
        for i, (title, counts) in enumerate(sorted_manga, 1):
            avg_count = np.mean(counts)
            f.write(f"{i:2d}. {title}: {len(counts)} images, avg {avg_count:.2f} balloons\n")
    
    print(f"Statistics saved to: {stats_path}")
    
    # 統計情報をテキストファイルに保存（日本語版）
    stats_path_jp = os.path.join(output_dir, 'balloon_count_statistics_jp.txt')
    with open(stats_path_jp, 'w', encoding='utf-8') as f:
        f.write("1画像中の吹き出し個数統計（吹き出しがある画像のみ）\n")
        f.write("=" * 65 + "\n")
        f.write(f"吹き出しがある画像数: {len(all_counts)}\n")
        f.write(f"吹き出しアノテーション総数: {sum(all_counts)}\n\n")
        
        f.write("吹き出し個数統計:\n")
        f.write(f"平均: {np.mean(all_counts):.6f}\n")
        f.write(f"中央値: {np.median(all_counts):.6f}\n")
        f.write(f"標準偏差: {np.std(all_counts):.6f}\n")
        f.write(f"最小値: {np.min(all_counts)}\n")
        f.write(f"最大値: {np.max(all_counts)}\n")
        f.write(f"25パーセンタイル: {np.percentile(all_counts, 25):.2f}\n")
        f.write(f"75パーセンタイル: {np.percentile(all_counts, 75):.2f}\n\n")
        
        # 吹き出し個数別の画像数分布
        count_distribution = Counter(all_counts)
        f.write("吹き出し個数別分布:\n")
        for count in sorted(count_distribution.keys()):
            freq = count_distribution[count]
            percentage = (freq / len(all_counts)) * 100
            f.write(f"{count}個: {freq}枚 ({percentage:.1f}%)\n")
        
        f.write("\n画像数上位10マンガタイトル:\n")
        sorted_manga = sorted(manga_balloon_counts.items(), 
                            key=lambda x: len(x[1]), reverse=True)[:10]
        for i, (title, counts) in enumerate(sorted_manga, 1):
            avg_count = np.mean(counts)
            f.write(f"{i:2d}. {title}: {len(counts)}枚, 平均{avg_count:.2f}個\n")
    
    print(f"Japanese statistics saved to: {stats_path_jp}")
    
    # 詳細なCSVファイルも出力（吹き出しがある画像のみ）
    csv_path = os.path.join(output_dir, 'balloon_count_per_image.csv')
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write("manga_title,image_filename,balloon_count\n")
        for filename, count in sorted(image_balloon_counts.items()):
            if count > 0:  # 吹き出しがある画像のみ
                manga_title = filename.split("/")[0] if "/" in filename else "unknown"
                f.write(f"{manga_title},{filename},{count}\n")
    
    print(f"Detailed CSV saved to: {csv_path}")
    
    # 日本語版グラフを表示
    plt.show()


if __name__ == "__main__":
    # 使用例
    annotations_dir = "./../annotations/"  # JSONファイルがあるディレクトリを指定
    output_dir = "./"
    
    plot_balloon_count_stats(annotations_dir, output_dir)
