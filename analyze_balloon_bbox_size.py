#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Manga109 吹き出しバウンディングボックスサイズ分析スクリプト

このスクリプトは、Manga109データセットの吹き出し領域アノテーションJSONファイルから
バウンディングボックスサイズと画像全体のサイズの比を分析し、グラフにプロットします。
"""

import sys
import os

# packagesディレクトリをパスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), 'packages'))

from packages.plot_balloon_bbox_ratio import plot_balloon_bbox_ratio


def main():
    """メイン実行関数"""
    
    # アノテーションディレクトリのパス
    annotations_dir = "./../annotations/"  # JSONファイルがあるディレクトリ
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
    print("Starting balloon bounding box size ratio analysis...")
    
    try:
        # 分析実行
        plot_balloon_bbox_ratio(annotations_dir, output_dir)
        print("\nBounding box analysis completed successfully!")
        print(f"Results saved in: {output_dir}")
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
