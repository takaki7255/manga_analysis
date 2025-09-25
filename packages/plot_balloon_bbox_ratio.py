import json
import glob
import os
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
import seaborn as sns

def plot_balloon_bbox_ratio(annotations_dir: str, output_dir: str = "./"):
    """
    吹き出し領域のバウンディングボックスサイズと画像全体のサイズの比をプロットする
    （吹き出しがある画像のみを対象とする）
    
    Args:
        annotations_dir: JSONアノテーションファイルがあるディレクトリパス
        output_dir: グラフの保存先ディレクトリ
    """
    
    # バウンディングボックスサイズの比率を格納するリスト
    bbox_ratios = []
    bbox_areas = []
    bbox_widths = []
    bbox_heights = []
    width_ratios = []
    height_ratios = []
    manga_titles = []
    
    # 画像情報を格納する辞書
    image_info = {}
    images_with_balloons = []
    
    # JSONファイルを取得
    json_files = glob.glob(os.path.join(annotations_dir, "*.json"))
    
    print(f"Found {len(json_files)} JSON files")
    
    # 最初に全画像情報を収集
    for json_path in json_files:
        print(f"Processing: {os.path.basename(json_path)}")
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 画像情報を収集
        for img in data['images']:
            image_id = img['id']
            file_name = img['file_name']
            width = img['width']
            height = img['height']
            
            image_info[image_id] = {
                'file_name': file_name,
                'width': width,
                'height': height,
                'area': width * height,
                'balloon_count': 0
            }
    
    # 次に吹き出しアノテーションを処理
    for json_path in json_files:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # カテゴリID → クラス名のマッピング
        category_map = {cat['id']: cat['name'] for cat in data.get("categories", [])}
        
        # 各アノテーションを処理
        for ann in data['annotations']:
            category_id = ann['category_id']
            class_name = category_map.get(category_id, f"category_{category_id}")
            
            # 吹き出し（balloon）クラスのみを対象とする
            if 'balloon' in class_name.lower() or 'speech' in class_name.lower():
                image_id = ann['image_id']
                
                if image_id in image_info:
                    img_info = image_info[image_id]
                    
                    # 吹き出しカウント
                    img_info['balloon_count'] += 1
                    
                    # バウンディングボックス情報を取得 [x, y, width, height]
                    bbox = ann['bbox']
                    x, y, width, height = bbox
                    
                    # バウンディングボックス面積を計算
                    bbox_area = width * height
                    
                    # 実際の画像サイズに対する比率を計算
                    area_ratio = bbox_area / img_info['area']
                    width_ratio = width / img_info['width']
                    height_ratio = height / img_info['height']
                    
                    # データを保存
                    bbox_ratios.append(area_ratio)
                    bbox_areas.append(bbox_area)
                    bbox_widths.append(width)
                    bbox_heights.append(height)
                    width_ratios.append(width_ratio)
                    height_ratios.append(height_ratio)
                    
                    # マンガタイトルを取得
                    file_name = img_info['file_name']
                    manga_title = file_name.split("/")[0] if "/" in file_name else "unknown"
                    manga_titles.append(manga_title)
    
    # 吹き出しがある画像を抽出
    images_with_balloons = [info for info in image_info.values() if info['balloon_count'] > 0]
    
    print(f"Found {len(bbox_ratios)} balloon bounding box annotations")
    print(f"Total images: {len(image_info)}")
    print(f"Images with balloons: {len(images_with_balloons)}")
    print(f"Images without balloons: {len(image_info) - len(images_with_balloons)}")
    
    # 画像サイズの統計
    image_sizes = [(info['width'], info['height']) for info in images_with_balloons]
    unique_sizes = list(set(image_sizes))
    print(f"Unique image sizes (with balloons): {len(unique_sizes)}")
    
    if len(bbox_ratios) == 0:
        print("No balloon annotations found!")
        return
    
    def create_graphs(language='english'):
        """グラフを作成する関数（言語切り替え対応）"""
        # グラフのスタイル設定
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(3, 2, figsize=(15, 18))
        
        # 言語別のタイトルとラベル
        if language == 'japanese':
            fig.suptitle('吹き出しバウンディングボックスサイズ分析', fontsize=16, fontweight='bold')
            xlabel_area_ratio = 'バウンディングボックス面積比率 (BBox面積 / 画像面積)'
            xlabel_width_ratio = 'バウンディングボックス幅比率 (BBox幅 / 画像幅)'
            xlabel_height_ratio = 'バウンディングボックス高さ比率 (BBox高さ / 画像高さ)'
            xlabel_width = 'バウンディングボックス幅 (ピクセル)'
            xlabel_height = 'バウンディングボックス高さ (ピクセル)'
            ylabel_frequency = '頻度'
            title_area_ratio_dist = 'バウンディングボックス面積比率の分布'
            title_width_ratio_dist = 'バウンディングボックス幅比率の分布'
            title_height_ratio_dist = 'バウンディングボックス高さ比率の分布'
            title_width_dist = 'バウンディングボックス幅の分布'
            title_height_dist = 'バウンディングボックス高さの分布'
            title_scatter = '幅 vs 高さ の散布図'
            mean_label_area = f'平均: {np.mean(bbox_ratios):.4f}'
            median_label_area = f'中央値: {np.median(bbox_ratios):.4f}'
            mean_label_width = f'平均: {np.mean(width_ratios):.4f}'
            median_label_width = f'中央値: {np.median(width_ratios):.4f}'
            mean_label_height = f'平均: {np.mean(height_ratios):.4f}'
            median_label_height = f'中央値: {np.median(height_ratios):.4f}'
        else:
            fig.suptitle('Balloon Bounding Box Size Analysis', fontsize=16, fontweight='bold')
            xlabel_area_ratio = 'Bounding Box Area Ratio (BBox Area / Image Area)'
            xlabel_width_ratio = 'Bounding Box Width Ratio (BBox Width / Image Width)'
            xlabel_height_ratio = 'Bounding Box Height Ratio (BBox Height / Image Height)'
            xlabel_width = 'Bounding Box Width (pixels)'
            xlabel_height = 'Bounding Box Height (pixels)'
            ylabel_frequency = 'Frequency'
            title_area_ratio_dist = 'Distribution of Bounding Box Area Ratios'
            title_width_ratio_dist = 'Distribution of Bounding Box Width Ratios'
            title_height_ratio_dist = 'Distribution of Bounding Box Height Ratios'
            title_width_dist = 'Distribution of Bounding Box Widths'
            title_height_dist = 'Distribution of Bounding Box Heights'
            title_scatter = 'Width vs Height Scatter Plot'
            mean_label_area = f'Mean: {np.mean(bbox_ratios):.4f}'
            median_label_area = f'Median: {np.median(bbox_ratios):.4f}'
            mean_label_width = f'Mean: {np.mean(width_ratios):.4f}'
            median_label_width = f'Median: {np.median(width_ratios):.4f}'
            mean_label_height = f'Mean: {np.mean(height_ratios):.4f}'
            median_label_height = f'Median: {np.median(height_ratios):.4f}'
        
        # 1. バウンディングボックス面積比率のヒストグラム
        axes[0, 0].hist(bbox_ratios, bins=50, alpha=0.7, color='skyblue', edgecolor='black')
        axes[0, 0].set_xlabel(xlabel_area_ratio)
        axes[0, 0].set_ylabel(ylabel_frequency)
        axes[0, 0].set_title(title_area_ratio_dist)
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].axvline(np.mean(bbox_ratios), color='red', linestyle='--', label=mean_label_area)
        axes[0, 0].axvline(np.median(bbox_ratios), color='orange', linestyle='--', label=median_label_area)
        axes[0, 0].legend()
        
        # 2. バウンディングボックス幅比率のヒストグラム
        axes[0, 1].hist(width_ratios, bins=50, alpha=0.7, color='lightgreen', edgecolor='black')
        axes[0, 1].set_xlabel(xlabel_width_ratio)
        axes[0, 1].set_ylabel(ylabel_frequency)
        axes[0, 1].set_title(title_width_ratio_dist)
        axes[0, 1].grid(True, alpha=0.3)
        axes[0, 1].axvline(np.mean(width_ratios), color='red', linestyle='--', label=mean_label_width)
        axes[0, 1].axvline(np.median(width_ratios), color='orange', linestyle='--', label=median_label_width)
        axes[0, 1].legend()
        
        # 3. バウンディングボックス高さ比率のヒストグラム
        axes[1, 0].hist(height_ratios, bins=50, alpha=0.7, color='lightcoral', edgecolor='black')
        axes[1, 0].set_xlabel(xlabel_height_ratio)
        axes[1, 0].set_ylabel(ylabel_frequency)
        axes[1, 0].set_title(title_height_ratio_dist)
        axes[1, 0].grid(True, alpha=0.3)
        axes[1, 0].axvline(np.mean(height_ratios), color='red', linestyle='--', label=mean_label_height)
        axes[1, 0].axvline(np.median(height_ratios), color='orange', linestyle='--', label=median_label_height)
        axes[1, 0].legend()
        
        # 4. バウンディングボックス幅のヒストグラム
        axes[1, 1].hist(bbox_widths, bins=50, alpha=0.7, color='gold', edgecolor='black')
        axes[1, 1].set_xlabel(xlabel_width)
        axes[1, 1].set_ylabel(ylabel_frequency)
        axes[1, 1].set_title(title_width_dist)
        axes[1, 1].grid(True, alpha=0.3)
        
        # 5. バウンディングボックス高さのヒストグラム
        axes[2, 0].hist(bbox_heights, bins=50, alpha=0.7, color='mediumpurple', edgecolor='black')
        axes[2, 0].set_xlabel(xlabel_height)
        axes[2, 0].set_ylabel(ylabel_frequency)
        axes[2, 0].set_title(title_height_dist)
        axes[2, 0].grid(True, alpha=0.3)
        
        # 6. 幅 vs 高さの散布図
        axes[2, 1].scatter(bbox_widths, bbox_heights, alpha=0.6, color='darkblue', s=10)
        axes[2, 1].set_xlabel(xlabel_width)
        axes[2, 1].set_ylabel(xlabel_height)
        axes[2, 1].set_title(title_scatter)
        axes[2, 1].grid(True, alpha=0.3)
        
        # レイアウトの調整
        plt.tight_layout()
        
        return fig

    # 統計情報を事前に計算
    mean_area_ratio = np.mean(bbox_ratios)
    median_area_ratio = np.median(bbox_ratios)
    mean_width_ratio = np.mean(width_ratios)
    median_width_ratio = np.median(width_ratios)
    mean_height_ratio = np.mean(height_ratios)
    median_height_ratio = np.median(height_ratios)
    
    # 英語版グラフを作成・保存
    fig_en = create_graphs('english')
    output_path_en = os.path.join(output_dir, 'balloon_bbox_ratio_analysis_en.png')
    fig_en.savefig(output_path_en, dpi=300, bbox_inches='tight')
    print(f"English graph saved to: {output_path_en}")
    
    # 日本語版グラフを作成・保存
    fig_jp = create_graphs('japanese')
    output_path_jp = os.path.join(output_dir, 'balloon_bbox_ratio_analysis_jp.png')
    fig_jp.savefig(output_path_jp, dpi=300, bbox_inches='tight')
    print(f"Japanese graph saved to: {output_path_jp}")
    
    # 後方互換性のため、英語版を従来のファイル名でも保存
    output_path = os.path.join(output_dir, 'balloon_bbox_ratio_analysis.png')
    fig_en.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Graph saved to: {output_path}")
    
    # 統計情報をテキストファイルに保存（英語版）
    stats_path = os.path.join(output_dir, 'balloon_bbox_statistics.txt')
    with open(stats_path, 'w', encoding='utf-8') as f:
        f.write("Balloon Bounding Box Size Ratio Statistics (Images with Balloons Only)\n")
        f.write("=" * 70 + "\n")
        f.write(f"Total balloon annotations: {len(bbox_ratios)}\n")
        f.write(f"Images with balloons: {len(images_with_balloons)}\n")
        f.write(f"Unique image sizes: {len(unique_sizes)}\n\n")
        
        f.write("Area Ratio Statistics:\n")
        f.write(f"Mean: {np.mean(bbox_ratios):.6f}\n")
        f.write(f"Median: {np.median(bbox_ratios):.6f}\n")
        f.write(f"Standard deviation: {np.std(bbox_ratios):.6f}\n")
        f.write(f"Min: {np.min(bbox_ratios):.6f}\n")
        f.write(f"Max: {np.max(bbox_ratios):.6f}\n")
        f.write(f"25th percentile: {np.percentile(bbox_ratios, 25):.6f}\n")
        f.write(f"75th percentile: {np.percentile(bbox_ratios, 75):.6f}\n\n")
        
        f.write("Width Ratio Statistics:\n")
        f.write(f"Mean: {np.mean(width_ratios):.6f}\n")
        f.write(f"Median: {np.median(width_ratios):.6f}\n")
        f.write(f"Standard deviation: {np.std(width_ratios):.6f}\n")
        f.write(f"Min: {np.min(width_ratios):.6f}\n")
        f.write(f"Max: {np.max(width_ratios):.6f}\n")
        f.write(f"25th percentile: {np.percentile(width_ratios, 25):.6f}\n")
        f.write(f"75th percentile: {np.percentile(width_ratios, 75):.6f}\n\n")
        
        f.write("Height Ratio Statistics:\n")
        f.write(f"Mean: {np.mean(height_ratios):.6f}\n")
        f.write(f"Median: {np.median(height_ratios):.6f}\n")
        f.write(f"Standard deviation: {np.std(height_ratios):.6f}\n")
        f.write(f"Min: {np.min(height_ratios):.6f}\n")
        f.write(f"Max: {np.max(height_ratios):.6f}\n")
        f.write(f"25th percentile: {np.percentile(height_ratios, 25):.6f}\n")
        f.write(f"75th percentile: {np.percentile(height_ratios, 75):.6f}\n\n")
        
        f.write("Bounding Box Area Statistics (pixels):\n")
        f.write(f"Mean: {np.mean(bbox_areas):.2f}\n")
        f.write(f"Median: {np.median(bbox_areas):.2f}\n")
        f.write(f"Standard deviation: {np.std(bbox_areas):.2f}\n")
        f.write(f"Min: {np.min(bbox_areas):.2f}\n")
        f.write(f"Max: {np.max(bbox_areas):.2f}\n\n")
        
        f.write("Bounding Box Width Statistics (pixels):\n")
        f.write(f"Mean: {np.mean(bbox_widths):.2f}\n")
        f.write(f"Median: {np.median(bbox_widths):.2f}\n")
        f.write(f"Standard deviation: {np.std(bbox_widths):.2f}\n")
        f.write(f"Min: {np.min(bbox_widths):.2f}\n")
        f.write(f"Max: {np.max(bbox_widths):.2f}\n\n")
        
        f.write("Bounding Box Height Statistics (pixels):\n")
        f.write(f"Mean: {np.mean(bbox_heights):.2f}\n")
        f.write(f"Median: {np.median(bbox_heights):.2f}\n")
        f.write(f"Standard deviation: {np.std(bbox_heights):.2f}\n")
        f.write(f"Min: {np.min(bbox_heights):.2f}\n")
        f.write(f"Max: {np.max(bbox_heights):.2f}\n\n")
        
        f.write("Image Size Distribution (Images with Balloons):\n")
        image_sizes = [(info['width'], info['height']) for info in images_with_balloons]
        size_counts = {}
        for size in image_sizes:
            if size in size_counts:
                size_counts[size] += 1
            else:
                size_counts[size] = 1
        
        sorted_sizes = sorted(size_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        for size, count in sorted_sizes:
            f.write(f"{size[0]}x{size[1]}: {count} images\n")
    
    print(f"Statistics saved to: {stats_path}")
    
    # 統計情報をテキストファイルに保存（日本語版）
    stats_path_jp = os.path.join(output_dir, 'balloon_bbox_statistics_jp.txt')
    with open(stats_path_jp, 'w', encoding='utf-8') as f:
        f.write("吹き出しバウンディングボックスサイズ比率統計（吹き出しがある画像のみ）\n")
        f.write("=" * 70 + "\n")
        f.write(f"吹き出しアノテーション総数: {len(bbox_ratios)}\n")
        f.write(f"吹き出しがある画像数: {len(images_with_balloons)}\n")
        f.write(f"ユニークな画像サイズ数: {len(unique_sizes)}\n\n")
        
        f.write("面積比率統計:\n")
        f.write(f"平均: {np.mean(bbox_ratios):.6f}\n")
        f.write(f"中央値: {np.median(bbox_ratios):.6f}\n")
        f.write(f"標準偏差: {np.std(bbox_ratios):.6f}\n")
        f.write(f"最小値: {np.min(bbox_ratios):.6f}\n")
        f.write(f"最大値: {np.max(bbox_ratios):.6f}\n")
        f.write(f"25パーセンタイル: {np.percentile(bbox_ratios, 25):.6f}\n")
        f.write(f"75パーセンタイル: {np.percentile(bbox_ratios, 75):.6f}\n\n")
        
        f.write("幅比率統計:\n")
        f.write(f"平均: {np.mean(width_ratios):.6f}\n")
        f.write(f"中央値: {np.median(width_ratios):.6f}\n")
        f.write(f"標準偏差: {np.std(width_ratios):.6f}\n")
        f.write(f"最小値: {np.min(width_ratios):.6f}\n")
        f.write(f"最大値: {np.max(width_ratios):.6f}\n")
        f.write(f"25パーセンタイル: {np.percentile(width_ratios, 25):.6f}\n")
        f.write(f"75パーセンタイル: {np.percentile(width_ratios, 75):.6f}\n\n")
        
        f.write("高さ比率統計:\n")
        f.write(f"平均: {np.mean(height_ratios):.6f}\n")
        f.write(f"中央値: {np.median(height_ratios):.6f}\n")
        f.write(f"標準偏差: {np.std(height_ratios):.6f}\n")
        f.write(f"最小値: {np.min(height_ratios):.6f}\n")
        f.write(f"最大値: {np.max(height_ratios):.6f}\n")
        f.write(f"25パーセンタイル: {np.percentile(height_ratios, 25):.6f}\n")
        f.write(f"75パーセンタイル: {np.percentile(height_ratios, 75):.6f}\n\n")
        
        f.write("バウンディングボックス面積統計 (ピクセル):\n")
        f.write(f"平均: {np.mean(bbox_areas):.2f}\n")
        f.write(f"中央値: {np.median(bbox_areas):.2f}\n")
        f.write(f"標準偏差: {np.std(bbox_areas):.2f}\n")
        f.write(f"最小値: {np.min(bbox_areas):.2f}\n")
        f.write(f"最大値: {np.max(bbox_areas):.2f}\n\n")
        
        f.write("バウンディングボックス幅統計 (ピクセル):\n")
        f.write(f"平均: {np.mean(bbox_widths):.2f}\n")
        f.write(f"中央値: {np.median(bbox_widths):.2f}\n")
        f.write(f"標準偏差: {np.std(bbox_widths):.2f}\n")
        f.write(f"最小値: {np.min(bbox_widths):.2f}\n")
        f.write(f"最大値: {np.max(bbox_widths):.2f}\n\n")
        
        f.write("バウンディングボックス高さ統計 (ピクセル):\n")
        f.write(f"平均: {np.mean(bbox_heights):.2f}\n")
        f.write(f"中央値: {np.median(bbox_heights):.2f}\n")
        f.write(f"標準偏差: {np.std(bbox_heights):.2f}\n")
        f.write(f"最小値: {np.min(bbox_heights):.2f}\n")
        f.write(f"最大値: {np.max(bbox_heights):.2f}\n\n")
        
        f.write("画像サイズ分布（吹き出しがある画像）:\n")
        for size, count in sorted_sizes:
            f.write(f"{size[0]}x{size[1]}: {count}枚\n")
    
    print(f"Japanese statistics saved to: {stats_path_jp}")
    
    # 日本語版グラフを表示
    plt.show()


if __name__ == "__main__":
    # 使用例
    annotations_dir = "./../annotations/"  # JSONファイルがあるディレクトリを指定
    output_dir = "./"
    
    plot_balloon_bbox_ratio(annotations_dir, output_dir)
