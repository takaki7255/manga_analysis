#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
キャラクター（body）統計分析

Manga109データセットのアノテーションからキャラクター（id=4, body）の
個数とサイズ比の統計を分析します。
"""

import json
import glob
import os
import numpy as np
import pandas as pd
from pycocotools import mask as maskUtils
from collections import defaultdict, Counter


def plot_body_stats(annotations_dir: str, output_dir: str = "./"):
    """
    キャラクター（body）の統計情報を分析する
    
    Args:
        annotations_dir: JSONアノテーションファイルがあるディレクトリパス
        output_dir: 結果の保存先ディレクトリ
    """
    
    # 統計情報を格納する辞書
    stats = {
        'count_per_image': [],
        'size_ratios': [],
        'areas': [],
        'bbox_areas': [],
        'bbox_ratios': [],
        'manga_titles': [],
        'total_annotations': 0,
        'images_with_annotations': 0
    }
    
    # 画像情報を格納する辞書
    image_info = {}
    
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
                'body_count': 0
            }
    
    # アノテーションを処理
    for json_path in json_files:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # カテゴリID → クラス名のマッピング
        category_map = {cat['id']: cat['name'] for cat in data.get("categories", [])}
        
        # 各アノテーションを処理
        for ann in data['annotations']:
            image_id = ann['image_id']
            category_id = ann['category_id']
            class_name = category_map.get(category_id, f"category_{category_id}")
            
            if image_id not in image_info:
                continue
            
            img_info = image_info[image_id]
            
            # キャラクター（body） (id=4, body) の処理
            if category_id == 4:
                stats['total_annotations'] += 1
                img_info['body_count'] += 1
                
                # セグメンテーションマスクからサイズ比を計算
                if 'segmentation' in ann:
                    segmentation = ann['segmentation']
                    try:
                        mask = maskUtils.decode(segmentation)
                        if len(mask.shape) == 3:
                            mask = np.any(mask, axis=2).astype(np.uint8)
                        
                        # セグメンテーション領域のピクセル数を計算
                        seg_area = np.sum(mask)
                        size_ratio = seg_area / img_info['area']
                        
                        stats['size_ratios'].append(size_ratio)
                        stats['areas'].append(seg_area)
                    except Exception as e:
                        print(f"Warning: Failed to decode segmentation for body: {e}")
                
                # バウンディングボックスからサイズを計算
                if 'bbox' in ann:
                    bbox = ann['bbox']  # [x, y, width, height]
                    bbox_area = bbox[2] * bbox[3]
                    bbox_ratio = bbox_area / img_info['area']
                    
                    stats['bbox_areas'].append(bbox_area)
                    stats['bbox_ratios'].append(bbox_ratio)
                
                # マンガタイトルを取得
                file_name = img_info['file_name']
                manga_title = file_name.split("/")[0] if "/" in file_name else "unknown"
                stats['manga_titles'].append(manga_title)
    
    # 画像ごとの個数統計を集計（該当アノテーションがある画像のみ）
    for img_info in image_info.values():
        if img_info['body_count'] > 0:
            stats['count_per_image'].append(img_info['body_count'])
            stats['images_with_annotations'] += 1
    
    # 統計情報を出力
    print(f"\nBody Statistics:")
    print(f"Total annotations: {stats['total_annotations']}")
    print(f"Images with body: {stats['images_with_annotations']}")
    print(f"Size ratios count: {len(stats['size_ratios'])}")
    
    # 統計レポートを生成
    _save_body_reports(stats, output_dir, len(image_info))
    
    # CSVファイルも生成
    _save_body_csv_report(image_info, output_dir)
    
    print(f"\nBody statistics saved to {output_dir}")


def _save_body_reports(stats, output_dir, total_images):
    """キャラクター統計レポートを保存"""
    
    # Body統計レポート（英語版）
    body_stats_path = os.path.join(output_dir, 'body_statistics.txt')
    with open(body_stats_path, 'w', encoding='utf-8') as f:
        f.write("Body (Character) Statistics\n")
        f.write("=" * 40 + "\n")
        
        f.write(f"Total body annotations: {stats['total_annotations']}\n")
        f.write(f"Total images analyzed: {total_images}\n")
        f.write(f"Images with body: {stats['images_with_annotations']}\n")
        f.write(f"Images without body: {total_images - stats['images_with_annotations']}\n\n")
        
        if stats['count_per_image']:
            counts = stats['count_per_image']
            f.write("Count per Image Statistics (Images with Body Only):\n")
            f.write(f"Mean: {np.mean(counts):.6f}\n")
            f.write(f"Median: {np.median(counts):.6f}\n")
            f.write(f"Standard deviation: {np.std(counts):.6f}\n")
            f.write(f"Min: {np.min(counts)}\n")
            f.write(f"Max: {np.max(counts)}\n")
            f.write(f"25th percentile: {np.percentile(counts, 25):.2f}\n")
            f.write(f"75th percentile: {np.percentile(counts, 75):.2f}\n\n")
        
        if stats['size_ratios']:
            ratios = stats['size_ratios']
            f.write("Size Ratio Statistics (Segmentation-based):\n")
            f.write(f"Mean: {np.mean(ratios):.6f}\n")
            f.write(f"Median: {np.median(ratios):.6f}\n")
            f.write(f"Standard deviation: {np.std(ratios):.6f}\n")
            f.write(f"Min: {np.min(ratios):.6f}\n")
            f.write(f"Max: {np.max(ratios):.6f}\n")
            f.write(f"25th percentile: {np.percentile(ratios, 25):.6f}\n")
            f.write(f"75th percentile: {np.percentile(ratios, 75):.6f}\n\n")
        
        if stats['bbox_ratios']:
            bbox_ratios = stats['bbox_ratios']
            f.write("Bounding Box Size Ratio Statistics:\n")
            f.write(f"Mean: {np.mean(bbox_ratios):.6f}\n")
            f.write(f"Median: {np.median(bbox_ratios):.6f}\n")
            f.write(f"Standard deviation: {np.std(bbox_ratios):.6f}\n")
            f.write(f"Min: {np.min(bbox_ratios):.6f}\n")
            f.write(f"Max: {np.max(bbox_ratios):.6f}\n")
            f.write(f"25th percentile: {np.percentile(bbox_ratios, 25):.6f}\n")
            f.write(f"75th percentile: {np.percentile(bbox_ratios, 75):.6f}\n\n")
        
        if stats['areas']:
            areas = stats['areas']
            f.write("Area Statistics (pixels):\n")
            f.write(f"Mean: {np.mean(areas):.2f}\n")
            f.write(f"Median: {np.median(areas):.2f}\n")
            f.write(f"Standard deviation: {np.std(areas):.2f}\n")
            f.write(f"Min: {np.min(areas):.2f}\n")
            f.write(f"Max: {np.max(areas):.2f}\n")
    
    print(f"Body statistics saved to: {body_stats_path}")
    
    # Body統計レポート（日本語版）
    body_stats_path_jp = os.path.join(output_dir, 'body_statistics_jp.txt')
    with open(body_stats_path_jp, 'w', encoding='utf-8') as f:
        f.write("キャラクター（body）統計\n")
        f.write("=" * 40 + "\n")
        
        f.write(f"キャラクターアノテーション総数: {stats['total_annotations']}\n")
        f.write(f"分析対象画像総数: {total_images}\n")
        f.write(f"キャラクターがある画像数: {stats['images_with_annotations']}\n")
        f.write(f"キャラクターがない画像数: {total_images - stats['images_with_annotations']}\n\n")
        
        if stats['count_per_image']:
            counts = stats['count_per_image']
            f.write("個数統計（キャラクターがある画像のみ）:\n")
            f.write(f"平均: {np.mean(counts):.6f}\n")
            f.write(f"中央値: {np.median(counts):.6f}\n")
            f.write(f"標準偏差: {np.std(counts):.6f}\n")
            f.write(f"最小値: {np.min(counts)}\n")
            f.write(f"最大値: {np.max(counts)}\n")
            f.write(f"25パーセンタイル: {np.percentile(counts, 25):.2f}\n")
            f.write(f"75パーセンタイル: {np.percentile(counts, 75):.2f}\n\n")
        
        if stats['size_ratios']:
            ratios = stats['size_ratios']
            f.write("サイズ比率統計（セグメンテーションベース）:\n")
            f.write(f"平均: {np.mean(ratios):.6f}\n")
            f.write(f"中央値: {np.median(ratios):.6f}\n")
            f.write(f"標準偏差: {np.std(ratios):.6f}\n")
            f.write(f"最小値: {np.min(ratios):.6f}\n")
            f.write(f"最大値: {np.max(ratios):.6f}\n")
            f.write(f"25パーセンタイル: {np.percentile(ratios, 25):.6f}\n")
            f.write(f"75パーセンタイル: {np.percentile(ratios, 75):.6f}\n\n")
        
        if stats['bbox_ratios']:
            bbox_ratios = stats['bbox_ratios']
            f.write("バウンディングボックスサイズ比率統計:\n")
            f.write(f"平均: {np.mean(bbox_ratios):.6f}\n")
            f.write(f"中央値: {np.median(bbox_ratios):.6f}\n")
            f.write(f"標準偏差: {np.std(bbox_ratios):.6f}\n")
            f.write(f"最小値: {np.min(bbox_ratios):.6f}\n")
            f.write(f"最大値: {np.max(bbox_ratios):.6f}\n")
            f.write(f"25パーセンタイル: {np.percentile(bbox_ratios, 25):.6f}\n")
            f.write(f"75パーセンタイル: {np.percentile(bbox_ratios, 75):.6f}\n\n")
        
        if stats['areas']:
            areas = stats['areas']
            f.write("面積統計（ピクセル）:\n")
            f.write(f"平均: {np.mean(areas):.2f}\n")
            f.write(f"中央値: {np.median(areas):.2f}\n")
            f.write(f"標準偏差: {np.std(areas):.2f}\n")
            f.write(f"最小値: {np.min(areas):.2f}\n")
            f.write(f"最大値: {np.max(areas):.2f}\n")
    
    print(f"Japanese body statistics saved to: {body_stats_path_jp}")


def _save_body_csv_report(image_info, output_dir):
    """キャラクター統計CSVレポートを保存"""
    
    # データフレーム用のデータを準備
    csv_data = []
    for image_id, info in image_info.items():
        manga_title = info['file_name'].split("/")[0] if "/" in info['file_name'] else "unknown"
        csv_data.append({
            'image_id': image_id,
            'file_name': info['file_name'],
            'manga_title': manga_title,
            'width': info['width'],
            'height': info['height'],
            'area': info['area'],
            'body_count': info['body_count']
        })
    
    # CSVファイルとして保存
    df = pd.DataFrame(csv_data)
    csv_path = os.path.join(output_dir, "body_per_image.csv")
    df = df.sort_values(['manga_title', 'file_name'])
    df.to_csv(csv_path, index=False, encoding='utf-8')
    
    print(f"Body per image CSV saved to: {csv_path}")


if __name__ == "__main__":
    # テスト実行
    annotations_dir = "./../Manga109_released_2023_12_07/manga_seg_jsons/"
    output_dir = "./"
    plot_body_stats(annotations_dir, output_dir)