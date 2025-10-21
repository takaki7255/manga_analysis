#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Manga109 キャラクター（body）統計分析スクリプト

このスクリプトは、Manga109データセットのアノテーションJSONファイルから
キャラクター（id=4, body）の統計情報を分析します。
"""

import sys
import os
import glob

# packagesディレクトリをパスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), 'packages'))

from packages.plot_body_stats import plot_body_stats


def main():
    """メイン実行関数"""
    
    # アノテーションディレクトリのパス
    annotations_dir = "./../Manga109_released_2023_12_07/manga_seg_jsons/"
    output_dir = "./"  # 結果の保存先
    
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
    print("Starting body (character) statistics analysis...")
    
    try:
        # キャラクター分析実行
        plot_body_stats(annotations_dir, output_dir)
        
        print("\n" + "="*60)
        print("Body (character) statistics analysis completed successfully!")
        print("="*60)
        print(f"Results saved in: {output_dir}")
        print("\nGenerated files:")
        print("Body (Character) Statistics:")
        print("  - body_statistics.txt (English)")
        print("  - body_statistics_jp.txt (Japanese)")
        print("\nDetailed Data:")
        print("  - body_per_image.csv (Per-image data)")
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()