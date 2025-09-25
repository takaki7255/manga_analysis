#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Manga109 画像サイズと吹き出し情報デバッグスクリプト

このスクリプトは、画像サイズの分布と吹き出し配置の関係を調査し、
統計の妥当性を確認します。
"""

import sys
import os

# packagesディレクトリをパスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), 'packages'))

from packages.debug_balloon_analysis import debug_image_sizes_and_balloons


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
    print("Starting image size and balloon placement debug analysis...")
    
    try:
        # デバッグ分析実行
        images_with_balloons, images_without_balloons, unique_sizes = debug_image_sizes_and_balloons(annotations_dir, output_dir)
        
        print("\n" + "="*60)
        print("Debug analysis completed successfully!")
        print("="*60)
        print(f"Results saved in: {output_dir}")
        print("\nGenerated files:")
        print("  - image_balloon_debug_report.txt")
        
        # 簡易サマリーをコンソールに表示
        print(f"\n=== クイックサマリー ===")
        print(f"総画像数: {len(images_with_balloons) + len(images_without_balloons)}")
        print(f"吹き出しがある画像: {len(images_with_balloons)}")
        print(f"吹き出しがない画像: {len(images_without_balloons)}")
        print(f"ユニークな画像サイズ数: {len(unique_sizes)}")
        
        if images_with_balloons:
            balloon_counts = [info['balloon_count'] for info in images_with_balloons]
            print(f"1画像あたりの平均吹き出し数: {sum(balloon_counts)/len(balloon_counts):.2f}")
        
        print(f"\n詳細は image_balloon_debug_report.txt を確認してください。")
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
