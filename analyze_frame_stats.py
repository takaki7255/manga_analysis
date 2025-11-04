#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Manga109 フレーム（コマ）統計分析スクリプト

このスクリプトは、Manga109データセットのアノテーションJSONファイルから
フレーム（id=1）の統計情報を分析します。
- 1画像あたりのフレーム個数
- フレームのサイズ比率（セグメンテーションベース）
- フレームのサイズ比率（バウンディングボックスベース）
"""

import sys
import os
import glob

# packagesディレクトリをパスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), 'packages'))

from packages.plot_frame_stats import plot_frame_stats


def main():
    """メイン実行関数"""
    
    # アノテーションディレクトリのパス
    annotations_dir = "./../Manga109_released_2023_12_07/manga_seg_jsons/"
    output_dir = "./statistics/"  # 結果の保存先
    
    # ディレクトリが存在するかチェック
    if not os.path.exists(annotations_dir):
        print(f"Error: Annotations directory not found: {annotations_dir}")
        print("Please check the path to your JSON annotation files.")
        return
    
    # JSONファイルが存在するかチェック
    json_files = glob.glob(os.path.join(annotations_dir, "*.json"))
    if not json_files:
        print(f"Error: No JSON files found in: {annotations_dir}")
        print("Please check that JSON annotation files exist in the specified directory.")
        return
    
    print(f"Found {len(json_files)} JSON files in {annotations_dir}")
    print("Starting frame (panel) statistics analysis...")
    
    try:
        # フレーム分析実行
        plot_frame_stats(annotations_dir, output_dir)
        
        print("\n" + "="*60)
        print("Frame statistics analysis completed successfully!")
        print("="*60)
        print(f"Results saved in: {output_dir}")
        print("\nGenerated files:")
        print("Frame Statistics:")
        print("  - frame_statistics.txt (English)")
        print("  - frame_statistics_jp.txt (Japanese)")
        print("\nDetailed Data:")
        print("  - frame_count_per_image.csv (Per-image frame count data)")
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()