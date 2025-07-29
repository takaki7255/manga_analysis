#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日本語フォント確認・設定スクリプト

このスクリプトは、システムで利用可能な日本語フォントを確認し、
matplotlibで日本語が正しく表示されるかテストします。
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

def check_japanese_fonts():
    """利用可能な日本語フォントを確認"""
    print("システムで利用可能なフォントを確認中...")
    
    # すべてのフォント取得
    font_list = [f.name for f in fm.fontManager.ttflist]
    
    # 日本語関連のキーワード
    japanese_keywords = ['gothic', 'hiragino', 'yu', 'meiryo', 'noto', 'ipa', 'takao', 'ms']
    
    # 日本語フォント候補を探す
    japanese_fonts = []
    for font in font_list:
        for keyword in japanese_keywords:
            if keyword.lower() in font.lower():
                japanese_fonts.append(font)
                break
    
    print("\n利用可能な日本語フォント候補:")
    for i, font in enumerate(sorted(set(japanese_fonts)), 1):
        print(f"{i:2d}. {font}")
    
    return sorted(set(japanese_fonts))

def test_japanese_display(font_name=None):
    """日本語表示のテスト"""
    if font_name:
        plt.rcParams['font.family'] = font_name
        print(f"\nテスト中のフォント: {font_name}")
    else:
        print("\nデフォルトフォントでテスト中...")
    
    plt.rcParams['axes.unicode_minus'] = False
    
    # テストプロット作成
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # データ作成
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    
    # プロット
    ax.plot(x, y1, label='サイン波', linewidth=2)
    ax.plot(x, y2, label='コサイン波', linewidth=2)
    
    # 日本語ラベル設定
    ax.set_title('日本語フォントテスト - 三角関数のグラフ', fontsize=16, fontweight='bold')
    ax.set_xlabel('X軸 (ラジアン)', fontsize=12)
    ax.set_ylabel('Y軸 (振幅)', fontsize=12)
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # 統計情報をテキストで追加
    ax.text(0.02, 0.98, '統計情報:\n平均値: 0.0\n標準偏差: 0.707', 
            transform=ax.transAxes, fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    
    # ファイル保存
    save_path = f'japanese_font_test_{font_name.replace(" ", "_") if font_name else "default"}.png'
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"テスト画像を保存しました: {save_path}")
    
    plt.show()

def install_font_recommendations():
    """フォントインストールの推奨事項"""
    print("\n" + "="*60)
    print("日本語フォントが見つからない場合の対処法:")
    print("="*60)
    print("\nmacOSの場合:")
    print("- システムに標準でインストールされているHiragino Sansを使用")
    print("- 追加で Noto Sans CJK JP をインストール可能")
    print("  brew install font-noto-sans-cjk-jp")
    print("\nLinuxの場合:")
    print("- sudo apt-get install fonts-noto-cjk")
    print("- sudo apt-get install fonts-ipafont-gothic")
    print("\nWindowsの場合:")
    print("- システムに標準でインストールされているMS Gothicやメイリオを使用")
    print("- 追加で Noto Sans CJK JP をダウンロード・インストール")
    
    print("\n推奨フォント (優先順):")
    recommended = [
        "Hiragino Sans (macOS標準)",
        "Yu Gothic (Windows/macOS)", 
        "Meiryo (Windows標準)",
        "Noto Sans CJK JP (マルチプラットフォーム)",
        "IPAexGothic (Linux)"
    ]
    for i, font in enumerate(recommended, 1):
        print(f"{i}. {font}")

def main():
    """メイン実行関数"""
    print("日本語フォント確認・テストツール")
    print("="*50)
    
    # 利用可能なフォント確認
    japanese_fonts = check_japanese_fonts()
    
    if not japanese_fonts:
        print("\n警告: 日本語フォントが見つかりません！")
        install_font_recommendations()
        return
    
    # デフォルトでテスト
    print("\n1. デフォルト設定でテスト...")
    test_japanese_display()
    
    # 推奨フォントでテスト
    recommended_fonts = ['Hiragino Sans', 'Yu Gothic', 'Meiryo', 'Noto Sans CJK JP']
    
    for font in recommended_fonts:
        if font in japanese_fonts:
            print(f"\n2. {font} でテスト...")
            test_japanese_display(font)
            break
    
    print("\n" + "="*50)
    print("テスト完了!")
    print("生成された画像ファイルで日本語が正しく表示されているか確認してください。")
    print("もし文字化けしている場合は、フォントのインストールが必要です。")

if __name__ == "__main__":
    main()
