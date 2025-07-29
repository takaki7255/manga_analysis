#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Manga109 吹き出し総合分析スクリプト

このスクリプトは、セグメンテーションマスク、バウンディングボックスのサイズ分析、
および1画像中の吹き出し個数統計を一度に実行します。
"""

import sys
import os

# packagesディレクトリをパスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), 'packages'))

from packages.plot_balloon_size_ratio import plot_balloon_size_ratio
from packages.plot_balloon_bbox_ratio import plot_balloon_bbox_ratio
from packages.plot_balloon_count_stats import plot_balloon_count_stats


def main():
    """メイン実行関数"""
    
    # アノテーションディレクトリのパス
    annotations_dir = "./../Manga109_released_2023_12_07/manga_seg_jsons/"  # JSONファイルがあるディレクトリ
    output_dir = "./"  # 結果の保存先
    
    # ディレクトリが存在するかチェック
    if not os.path.exists(annotations_dir):
        print(f"Error: Annotations directory not found: {annotations_dir}")
        print("Please check the path to your JSON annotation files.")
        return
    
    # JSONファイルが存在するかチェック
    import glob
    json_files = glob.glob(os.path.join(annotations_dir, "*.json"))
    if not json_files:
        print(f"Error: No JSON files found in: {annotations_dir}")
        print("Please check that JSON annotation files exist in the specified directory.")
        return
    
    print(f"Found {len(json_files)} JSON files in {annotations_dir}")
    print("Starting comprehensive balloon analysis...")
    
    try:
        # 1. セグメンテーションマスクベースの分析
        print("\n" + "="*60)
        print("1. Segmentation Mask-based Analysis")
        print("="*60)
        plot_balloon_size_ratio(annotations_dir, output_dir)
        
        # 2. バウンディングボックスベースの分析
        print("\n" + "="*60)
        print("2. Bounding Box-based Analysis")
        print("="*60)
        plot_balloon_bbox_ratio(annotations_dir, output_dir)
        
        # 3. 1画像中の吹き出し個数統計
        print("\n" + "="*60)
        print("3. Balloon Count Statistics per Image")
        print("="*60)
        plot_balloon_count_stats(annotations_dir, output_dir)
        
        print("\n" + "="*60)
        print("All analyses completed successfully!")
        print("="*60)
        print(f"Results saved in: {output_dir}")
        print("\nGenerated files:")
        print("Segmentation-based:")
        print("  - balloon_size_ratio_analysis_en.png")
        print("  - balloon_size_ratio_analysis_jp.png")
        print("  - balloon_size_statistics.txt")
        print("  - balloon_size_statistics_jp.txt")
        print("\nBounding Box-based:")
        print("  - balloon_bbox_ratio_analysis_en.png")
        print("  - balloon_bbox_ratio_analysis_jp.png")
        print("  - balloon_bbox_statistics.txt")
        print("  - balloon_bbox_statistics_jp.txt")
        print("\nBalloon Count Statistics:")
        print("  - balloon_count_stats_en.png")
        print("  - balloon_count_stats_jp.png")
        print("  - balloon_count_statistics.txt")
        print("  - balloon_count_statistics_jp.txt")
        print("  - balloon_count_per_image.csv")
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
