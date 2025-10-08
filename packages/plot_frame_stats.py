import json
import glob
import os
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
import seaborn as sns
from pycocotools import mask as maskUtils
from collections import defaultdict, Counter
import pandas as pd

def plot_frame_stats(annotations_dir: str, output_dir: str = "./"):
    """
    フレーム（コマ）領域の統計情報を分析する
    - 1画像あたりのフレーム個数
    - フレームのサイズ比率（セグメンテーションベース）
    - フレームのサイズ比率（バウンディングボックスベース）
    
    Args:
        annotations_dir: JSONアノテーションファイルがあるディレクトリパス
        output_dir: 結果の保存先ディレクトリ
    """
    
    # フレーム統計を格納するリスト・辞書
    frame_ratios = []
    frame_bbox_ratios = []
    frame_areas = []
    frame_bbox_areas = []
    image_frame_counts = defaultdict(int)
    
    # 画像情報を格納する辞書
    image_info = {}
    
    # JSONファイルを取得
    json_files = glob.glob(os.path.join(annotations_dir, "*.json"))
    
    print(f"Found {len(json_files)} JSON files")
    
    # 最初に全画像情報を収集
    total_processed_files = 0
    for json_path in json_files:
        print(f"Processing: {os.path.basename(json_path)}")
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error reading {json_path}: {e}")
            continue
        
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
                'area': width * height
            }
        
        total_processed_files += 1
    
    print(f"Successfully processed {total_processed_files} JSON files")
    print(f"Total images found: {len(image_info)}")
    
    # 次にフレームアノテーションを処理
    total_frame_annotations = 0
    processed_frame_annotations = 0
    
    for json_path in json_files:
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            continue
        
        # カテゴリID → クラス名のマッピング
        category_map = {cat['id']: cat['name'] for cat in data.get("categories", [])}
        
        # 各アノテーションを処理
        for ann in data['annotations']:
            category_id = ann['category_id']
            
            # フレーム（id=1）のみを対象とする
            if category_id == 1:
                total_frame_annotations += 1
                image_id = ann['image_id']
                
                if image_id in image_info:
                    img_info = image_info[image_id]
                    file_name = img_info['file_name']
                    
                    # フレームカウント
                    image_frame_counts[file_name] += 1
                    
                    try:
                        # セグメンテーションマスクの処理
                        segmentation = ann['segmentation']
                        mask = maskUtils.decode(segmentation)
                        if len(mask.shape) == 3:
                            mask = np.any(mask, axis=2).astype(np.uint8)
                        
                        # フレーム領域のピクセル数を計算
                        frame_area = np.sum(mask)
                        
                        # 実際の画像サイズに対する比率を計算
                        ratio = frame_area / img_info['area']
                        
                        # データを保存
                        frame_ratios.append(ratio)
                        frame_areas.append(frame_area)
                        
                        processed_frame_annotations += 1
                        
                    except Exception as e:
                        print(f"Error processing segmentation for image {image_id}: {e}")
                    
                    try:
                        # バウンディングボックスの処理
                        bbox = ann['bbox']
                        bbox_width, bbox_height = bbox[2], bbox[3]
                        bbox_area = bbox_width * bbox_height
                        
                        # バウンディングボックスの比率を計算
                        bbox_ratio = bbox_area / img_info['area']
                        
                        frame_bbox_ratios.append(bbox_ratio)
                        frame_bbox_areas.append(bbox_area)
                        
                    except Exception as e:
                        print(f"Error processing bbox for image {image_id}: {e}")
    
    print(f"Total frame annotations found: {total_frame_annotations}")
    print(f"Successfully processed frame annotations: {processed_frame_annotations}")
    
    # フレームがある画像のみの個数統計を計算
    frame_counts_only = [count for count in image_frame_counts.values() if count > 0]
    
    print(f"Total images: {len(image_info)}")
    print(f"Images with frames: {len(frame_counts_only)}")
    print(f"Images without frames: {len(image_info) - len(frame_counts_only)}")
    
    if len(frame_counts_only) == 0:
        print("Warning: No frames found in any images!")
        return
    
    # 統計レポートを生成
    _save_frame_statistics_report(
        frame_ratios, frame_bbox_ratios, frame_areas, frame_bbox_areas,
        frame_counts_only, len(image_info), output_dir
    )
    
    # CSVファイルを生成
    _save_frame_csv_report(image_frame_counts, output_dir)
    
    print(f"Frame statistics saved to {output_dir}")


def _save_frame_statistics_report(frame_ratios, frame_bbox_ratios, frame_areas, frame_bbox_areas, 
                                frame_counts, total_images, output_dir):
    """フレーム統計レポートを保存"""
    
    # 英語版レポート
    stats_path = os.path.join(output_dir, 'frame_statistics.txt')
    with open(stats_path, 'w', encoding='utf-8') as f:
        f.write("Frame Statistics\n")
        f.write("=" * 40 + "\n")
        f.write(f"Total frame annotations: {len(frame_ratios)}\n")
        f.write(f"Total images analyzed: {total_images}\n")
        f.write(f"Images with frames: {len(frame_counts)}\n")
        f.write(f"Images without frames: {total_images - len(frame_counts)}\n\n")
        
        if frame_counts:
            f.write("Count per Image Statistics (Images with Frames Only):\n")
            f.write(f"Mean: {np.mean(frame_counts):.6f}\n")
            f.write(f"Median: {np.median(frame_counts):.6f}\n")
            f.write(f"Standard deviation: {np.std(frame_counts):.6f}\n")
            f.write(f"Min: {np.min(frame_counts)}\n")
            f.write(f"Max: {np.max(frame_counts)}\n")
            f.write(f"25th percentile: {np.percentile(frame_counts, 25):.2f}\n")
            f.write(f"75th percentile: {np.percentile(frame_counts, 75):.2f}\n\n")
        
        if frame_ratios:
            f.write("Size Ratio Statistics (Segmentation-based):\n")
            f.write(f"Mean: {np.mean(frame_ratios):.6f}\n")
            f.write(f"Median: {np.median(frame_ratios):.6f}\n")
            f.write(f"Standard deviation: {np.std(frame_ratios):.6f}\n")
            f.write(f"Min: {np.min(frame_ratios):.6f}\n")
            f.write(f"Max: {np.max(frame_ratios):.6f}\n")
            f.write(f"25th percentile: {np.percentile(frame_ratios, 25):.6f}\n")
            f.write(f"75th percentile: {np.percentile(frame_ratios, 75):.6f}\n\n")
        
        if frame_bbox_ratios:
            f.write("Bounding Box Size Ratio Statistics:\n")
            f.write(f"Mean: {np.mean(frame_bbox_ratios):.6f}\n")
            f.write(f"Median: {np.median(frame_bbox_ratios):.6f}\n")
            f.write(f"Standard deviation: {np.std(frame_bbox_ratios):.6f}\n")
            f.write(f"Min: {np.min(frame_bbox_ratios):.6f}\n")
            f.write(f"Max: {np.max(frame_bbox_ratios):.6f}\n")
            f.write(f"25th percentile: {np.percentile(frame_bbox_ratios, 25):.6f}\n")
            f.write(f"75th percentile: {np.percentile(frame_bbox_ratios, 75):.6f}\n\n")
        
        if frame_areas:
            f.write("Area Statistics (pixels):\n")
            f.write(f"Mean: {np.mean(frame_areas):.2f}\n")
            f.write(f"Median: {np.median(frame_areas):.2f}\n")
            f.write(f"Standard deviation: {np.std(frame_areas):.2f}\n")
            f.write(f"Min: {np.min(frame_areas):.2f}\n")
            f.write(f"Max: {np.max(frame_areas):.2f}\n")
    
    print(f"Frame statistics saved to: {stats_path}")
    
    # 日本語版レポート
    stats_path_jp = os.path.join(output_dir, 'frame_statistics_jp.txt')
    with open(stats_path_jp, 'w', encoding='utf-8') as f:
        f.write("フレーム（コマ）統計\n")
        f.write("=" * 40 + "\n")
        f.write(f"フレームアノテーション総数: {len(frame_ratios)}\n")
        f.write(f"分析対象画像総数: {total_images}\n")
        f.write(f"フレームがある画像数: {len(frame_counts)}\n")
        f.write(f"フレームがない画像数: {total_images - len(frame_counts)}\n\n")
        
        if frame_counts:
            f.write("個数統計（フレームがある画像のみ）:\n")
            f.write(f"平均: {np.mean(frame_counts):.6f}\n")
            f.write(f"中央値: {np.median(frame_counts):.6f}\n")
            f.write(f"標準偏差: {np.std(frame_counts):.6f}\n")
            f.write(f"最小値: {np.min(frame_counts)}\n")
            f.write(f"最大値: {np.max(frame_counts)}\n")
            f.write(f"25パーセンタイル: {np.percentile(frame_counts, 25):.2f}\n")
            f.write(f"75パーセンタイル: {np.percentile(frame_counts, 75):.2f}\n\n")
        
        if frame_ratios:
            f.write("サイズ比率統計（セグメンテーションベース）:\n")
            f.write(f"平均: {np.mean(frame_ratios):.6f}\n")
            f.write(f"中央値: {np.median(frame_ratios):.6f}\n")
            f.write(f"標準偏差: {np.std(frame_ratios):.6f}\n")
            f.write(f"最小値: {np.min(frame_ratios):.6f}\n")
            f.write(f"最大値: {np.max(frame_ratios):.6f}\n")
            f.write(f"25パーセンタイル: {np.percentile(frame_ratios, 25):.6f}\n")
            f.write(f"75パーセンタイル: {np.percentile(frame_ratios, 75):.6f}\n\n")
        
        if frame_bbox_ratios:
            f.write("バウンディングボックスサイズ比率統計:\n")
            f.write(f"平均: {np.mean(frame_bbox_ratios):.6f}\n")
            f.write(f"中央値: {np.median(frame_bbox_ratios):.6f}\n")
            f.write(f"標準偏差: {np.std(frame_bbox_ratios):.6f}\n")
            f.write(f"最小値: {np.min(frame_bbox_ratios):.6f}\n")
            f.write(f"最大値: {np.max(frame_bbox_ratios):.6f}\n")
            f.write(f"25パーセンタイル: {np.percentile(frame_bbox_ratios, 25):.6f}\n")
            f.write(f"75パーセンタイル: {np.percentile(frame_bbox_ratios, 75):.6f}\n\n")
        
        if frame_areas:
            f.write("面積統計（ピクセル）:\n")
            f.write(f"平均: {np.mean(frame_areas):.2f}\n")
            f.write(f"中央値: {np.median(frame_areas):.2f}\n")
            f.write(f"標準偏差: {np.std(frame_areas):.2f}\n")
            f.write(f"最小値: {np.min(frame_areas):.2f}\n")
            f.write(f"最大値: {np.max(frame_areas):.2f}\n")
    
    print(f"Japanese frame statistics saved to: {stats_path_jp}")


def _save_frame_csv_report(image_frame_counts, output_dir):
    """フレーム統計CSVレポートを保存"""
    
    csv_path = os.path.join(output_dir, 'frame_count_per_image.csv')
    
    # CSVデータを準備
    csv_data = []
    for file_name, count in image_frame_counts.items():
        manga_title = file_name.split("/")[0] if "/" in file_name else "unknown"
        csv_data.append({
            'manga_title': manga_title,
            'file_name': file_name,
            'frame_count': count
        })
    
    # DataFrameに変換して保存
    df = pd.DataFrame(csv_data)
    df = df.sort_values(['manga_title', 'file_name'])
    df.to_csv(csv_path, index=False, encoding='utf-8')
    
    print(f"Frame count per image CSV saved to: {csv_path}")


if __name__ == "__main__":
    # テスト実行
    annotations_dir = "./../Manga109_released_2023_12_07/manga_seg_jsons/"
    output_dir = "./"
    plot_frame_stats(annotations_dir, output_dir)