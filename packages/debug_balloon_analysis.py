import json
import glob
import os
import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib
import seaborn as sns

def debug_image_sizes_and_balloons(annotations_dir: str, output_dir: str = "./"):
    """
    画像サイズと吹き出し情報をデバッグ・分析する
    
    Args:
        annotations_dir: JSONアノテーションファイルがあるディレクトリパス
        output_dir: 結果の保存先ディレクトリ
    """
    
    # 画像サイズとバルーン情報を格納する辞書
    image_info = {}
    image_sizes = []
    images_with_balloons = []
    images_without_balloons = []
    
    # JSONファイルを取得
    json_files = glob.glob(os.path.join(annotations_dir, "*.json"))
    
    print(f"Found {len(json_files)} JSON files")
    
    for json_path in json_files:
        print(f"Processing: {os.path.basename(json_path)}")
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # カテゴリID → クラス名のマッピング
        category_map = {cat['id']: cat['name'] for cat in data.get("categories", [])}
        
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
                'balloon_count': 0,
                'balloons': []
            }
            
            image_sizes.append((width, height))
        
        # 吹き出しアノテーションを処理
        for ann in data['annotations']:
            category_id = ann['category_id']
            class_name = category_map.get(category_id, f"category_{category_id}")
            
            # 吹き出し（balloon）クラスのみを対象とする
            if 'balloon' in class_name.lower() or 'speech' in class_name.lower():
                image_id = ann['image_id']
                if image_id in image_info:
                    bbox = ann['bbox']
                    x, y, width, height = bbox
                    
                    image_info[image_id]['balloon_count'] += 1
                    image_info[image_id]['balloons'].append({
                        'bbox': bbox,
                        'area': width * height,
                        'width': width,
                        'height': height
                    })
    
    # 吹き出しがある画像とない画像を分類
    for image_id, info in image_info.items():
        if info['balloon_count'] > 0:
            images_with_balloons.append(info)
        else:
            images_without_balloons.append(info)
    
    print(f"\n=== 画像情報サマリー ===")
    print(f"総画像数: {len(image_info)}")
    print(f"吹き出しがある画像: {len(images_with_balloons)}")
    print(f"吹き出しがない画像: {len(images_without_balloons)}")
    
    # 画像サイズの分析
    unique_sizes = list(set(image_sizes))
    print(f"\n=== 画像サイズ分析 ===")
    print(f"ユニークな画像サイズ数: {len(unique_sizes)}")
    
    size_counts = {}
    for size in image_sizes:
        if size in size_counts:
            size_counts[size] += 1
        else:
            size_counts[size] = 1
    
    print("上位10の画像サイズ:")
    sorted_sizes = sorted(size_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    for size, count in sorted_sizes:
        print(f"  {size[0]}x{size[1]}: {count}枚")
    
    # 吹き出しがある画像のサイズ分析
    balloon_image_sizes = [(info['width'], info['height']) for info in images_with_balloons]
    balloon_size_counts = {}
    for size in balloon_image_sizes:
        if size in balloon_size_counts:
            balloon_size_counts[size] += 1
        else:
            balloon_size_counts[size] = 1
    
    print(f"\n=== 吹き出しがある画像のサイズ分析 ===")
    print("上位10の画像サイズ:")
    sorted_balloon_sizes = sorted(balloon_size_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    for size, count in sorted_balloon_sizes:
        print(f"  {size[0]}x{size[1]}: {count}枚")
    
    # 詳細レポートをファイルに保存
    report_path = os.path.join(output_dir, 'image_balloon_debug_report.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("画像サイズと吹き出し情報デバッグレポート\n")
        f.write("=" * 50 + "\n\n")
        
        f.write(f"総画像数: {len(image_info)}\n")
        f.write(f"吹き出しがある画像: {len(images_with_balloons)}\n")
        f.write(f"吹き出しがない画像: {len(images_without_balloons)}\n\n")
        
        f.write("全画像のサイズ分布:\n")
        for size, count in sorted_sizes:
            f.write(f"  {size[0]}x{size[1]}: {count}枚\n")
        
        f.write("\n吹き出しがある画像のサイズ分布:\n")
        for size, count in sorted_balloon_sizes:
            f.write(f"  {size[0]}x{size[1]}: {count}枚\n")
        
        f.write("\n吹き出し統計:\n")
        if images_with_balloons:
            balloon_counts = [info['balloon_count'] for info in images_with_balloons]
            f.write(f"1画像あたりの吹き出し数 - 平均: {np.mean(balloon_counts):.2f}\n")
            f.write(f"1画像あたりの吹き出し数 - 中央値: {np.median(balloon_counts):.2f}\n")
            f.write(f"1画像あたりの吹き出し数 - 最大: {np.max(balloon_counts)}\n")
            
            # 吹き出しサイズの比率分析（画像サイズ別）
            f.write(f"\n吹き出しサイズ比率分析（代表的な画像サイズ別）:\n")
            
            for size, count in sorted_balloon_sizes[:5]:  # 上位5サイズ
                if count >= 10:  # 十分なサンプル数がある場合のみ
                    size_images = [info for info in images_with_balloons 
                                 if info['width'] == size[0] and info['height'] == size[1]]
                    
                    all_balloons = []
                    for img_info in size_images:
                        for balloon in img_info['balloons']:
                            area_ratio = balloon['area'] / (size[0] * size[1])
                            width_ratio = balloon['width'] / size[0]
                            height_ratio = balloon['height'] / size[1]
                            all_balloons.append({
                                'area_ratio': area_ratio,
                                'width_ratio': width_ratio,
                                'height_ratio': height_ratio
                            })
                    
                    if all_balloons:
                        area_ratios = [b['area_ratio'] for b in all_balloons]
                        width_ratios = [b['width_ratio'] for b in all_balloons]
                        height_ratios = [b['height_ratio'] for b in all_balloons]
                        
                        f.write(f"\n  画像サイズ {size[0]}x{size[1]} ({count}枚, {len(all_balloons)}個の吹き出し):\n")
                        f.write(f"    面積比率 - 平均: {np.mean(area_ratios):.4f}, 中央値: {np.median(area_ratios):.4f}\n")
                        f.write(f"    幅比率 - 平均: {np.mean(width_ratios):.4f}, 中央値: {np.median(width_ratios):.4f}\n")
                        f.write(f"    高さ比率 - 平均: {np.mean(height_ratios):.4f}, 中央値: {np.median(height_ratios):.4f}\n")
    
    print(f"\nデバッグレポートを保存しました: {report_path}")
    
    return images_with_balloons, images_without_balloons, unique_sizes

if __name__ == "__main__":
    # 使用例
    annotations_dir = "./../Manga109_released_2023_12_07/manga_seg_jsons/"
    output_dir = "./"
    
    debug_image_sizes_and_balloons(annotations_dir, output_dir)
