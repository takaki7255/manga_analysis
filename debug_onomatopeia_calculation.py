#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
オノマトペデバッグ分析

オノマトペのセグメンテーション計算をデバッグして、
サイズ比率が異常に小さくないかを確認します。
"""

import json
import glob
import os
import numpy as np
from pycocotools import mask as maskUtils

def debug_onomatopoeia_calculation(annotations_dir: str):
    """オノマトペの計算をデバッグ"""
    
    json_files = glob.glob(os.path.join(annotations_dir, "*.json"))
    
    debug_samples = []
    total_processed = 0
    
    for json_path in json_files[:3]:  # 最初の3ファイルのみ処理
        print(f"Processing: {os.path.basename(json_path)}")
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 画像情報を収集
        image_info = {}
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
        
        # カテゴリマッピング
        category_map = {cat['id']: cat['name'] for cat in data.get("categories", [])}
        
        # オノマトペアノテーションをデバッグ
        for ann in data['annotations']:
            category_id = ann['category_id']
            
            if category_id == 6:  # オノマトペ
                image_id = ann['image_id']
                
                if image_id in image_info:
                    img_info = image_info[image_id]
                    class_name = category_map.get(category_id, f"category_{category_id}")
                    
                    print(f"\n--- Debug Sample {len(debug_samples) + 1} ---")
                    print(f"Image: {img_info['file_name']}")
                    print(f"Image size: {img_info['width']}x{img_info['height']} = {img_info['area']} pixels")
                    print(f"Category: {class_name} (id={category_id})")
                    
                    # セグメンテーション処理
                    if 'segmentation' in ann:
                        segmentation = ann['segmentation']
                        try:
                            print(f"Segmentation type: {type(segmentation)}")
                            
                            # RLEデコード
                            mask = maskUtils.decode(segmentation)
                            print(f"Mask shape: {mask.shape}")
                            print(f"Mask dtype: {mask.dtype}")
                            
                            if len(mask.shape) == 3:
                                mask = np.any(mask, axis=2).astype(np.uint8)
                                print(f"Mask after 3D->2D conversion: {mask.shape}")
                            
                            # セグメンテーション領域のピクセル数を計算
                            seg_area = np.sum(mask)
                            size_ratio = seg_area / img_info['area']
                            
                            print(f"Segmentation area: {seg_area} pixels")
                            print(f"Size ratio: {size_ratio:.6f} ({size_ratio*100:.4f}%)")
                            
                            # バウンディングボックスも確認
                            if 'bbox' in ann:
                                bbox = ann['bbox']
                                bbox_area = bbox[2] * bbox[3]
                                bbox_ratio = bbox_area / img_info['area']
                                print(f"BBox: {bbox}")
                                print(f"BBox area: {bbox_area:.2f} pixels")
                                print(f"BBox ratio: {bbox_ratio:.6f} ({bbox_ratio*100:.4f}%)")
                            
                            debug_samples.append({
                                'file_name': img_info['file_name'],
                                'image_area': img_info['area'],
                                'seg_area': seg_area,
                                'size_ratio': size_ratio,
                                'bbox_area': bbox_area if 'bbox' in ann else None,
                                'bbox_ratio': bbox_ratio if 'bbox' in ann else None
                            })
                            
                        except Exception as e:
                            print(f"Error processing segmentation: {e}")
                    
                    total_processed += 1
                    if total_processed >= 10:  # 10サンプルまで
                        break
        
        if total_processed >= 10:
            break
    
    # 統計概要
    print(f"\n=== Debug Summary ===")
    print(f"Total samples analyzed: {len(debug_samples)}")
    
    if debug_samples:
        seg_areas = [s['seg_area'] for s in debug_samples]
        size_ratios = [s['size_ratio'] for s in debug_samples]
        
        print(f"Segmentation areas: min={min(seg_areas)}, max={max(seg_areas)}, mean={np.mean(seg_areas):.2f}")
        print(f"Size ratios: min={min(size_ratios):.6f}, max={max(size_ratios):.6f}, mean={np.mean(size_ratios):.6f}")
        print(f"Size ratios (%): min={min(size_ratios)*100:.4f}%, max={max(size_ratios)*100:.4f}%, mean={np.mean(size_ratios)*100:.4f}%")

if __name__ == "__main__":
    annotations_dir = "./../Manga109_released_2023_12_07/manga_seg_jsons/"
    debug_onomatopoeia_calculation(annotations_dir)