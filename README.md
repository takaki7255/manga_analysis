# manga_analysis

Manga109 のアノテーションを使って、漫画内オブジェクトの出現数・サイズ比を集計する分析プロジェクトです。

現在の主系統は **JSON アノテーション (`manga_seg_jsons`) を使う分析スクリプト** で、結果は `statistics/` にテキスト・CSV・画像として保存されます。

## 1. このプロジェクトでできること

- 吹き出し（balloon）の個数統計
- 吹き出しサイズ比（セグメンテーション面積ベース）
- 吹き出しサイズ比（BBox ベース）
- コマ（frame, id=1）の個数・面積統計
- キャラクター（body, id=4）の個数・面積統計
- オノマトペ（id=6）の個数・面積統計
- オノマトペと body の同時集計

## 2. ディレクトリ構成（要点）

- `analyze_*.py`: 実行用エントリースクリプト
- `packages/*.py`: 集計処理の本体
- `statistics/`: 出力先（`.txt`, `.csv`, `.png`）
- `debug_*.py`: 検算・デバッグ用
- `main.py`, `only_text.py`, `2_text_and_a_character.py`: 旧来の XML ベース実験コード

## 3. 前提データ配置

このリポジトリ (`manga_analysis`) の 1 つ上の階層に、Manga109 データを置く前提です。

期待される配置例:

```text
../Manga109_released_2023_12_07/
	manga_seg_jsons/
	annotations/
```

主要スクリプトは基本的に次を参照します:

- `./../Manga109_released_2023_12_07/manga_seg_jsons/`

## 4. セットアップ

Python 3.10+ を推奨。

必要ライブラリ（コード上の import から抽出）:

- `numpy`
- `pandas`
- `matplotlib`
- `seaborn`
- `scipy`
- `pycocotools`
- `japanize-matplotlib`
- `opencv-python`（`draw_bbox_and_show.py` を使う場合）

例:

```bash
pip install numpy pandas matplotlib seaborn scipy pycocotools japanize-matplotlib opencv-python
```

## 5. 主要な実行コマンド

すべて `manga_analysis/` 直下で実行。

### 5.1 吹き出し系

```bash
python analyze_balloon_count_stats.py
python analyze_balloon_size.py
python analyze_balloon_bbox_size.py
python analyze_balloon_comprehensive.py
```

`analyze_balloon_comprehensive.py` は以下を順にまとめて実行します。

- 吹き出しサイズ比（セグメンテーション）
- 吹き出しサイズ比（BBox）
- 1画像あたり吹き出し数

### 5.2 フレーム・body・オノマトペ系

```bash
python analyze_frame_stats.py
python analyze_body_stats.py
python analyze_onomatopeia_stats.py
python analyze_onomatopoeia_body_stats.py
```

## 6. 出力ファイル（`statistics/`）

代表例:

- 吹き出し
	- `balloon_count_statistics.txt`
	- `balloon_count_statistics_jp.txt`
	- `balloon_count_per_image.csv`
	- `balloon_size_statistics.txt`
	- `balloon_size_statistics_jp.txt`
	- `balloon_bbox_statistics.txt`
	- `balloon_bbox_statistics_jp.txt`
- フレーム
	- `frame_statistics.txt`
	- `frame_statistics_jp.txt`
	- `frame_count_per_image.csv`
- body
	- `body_statistics.txt`
	- `body_statistics_jp.txt`
	- `body_per_image.csv`
- オノマトペ
	- `onomatopeia_statistics.txt`
	- `onomatopeia_statistics_jp.txt`
	- `onomatopeia_per_image.csv`
	- `onomatopoeia_statistics.txt`
	- `onomatopoeia_statistics_jp.txt`
	- `onomatopoeia_per_image.csv`

補足:

- `onomatopeia` / `onomatopoeia` の表記揺れがコードと成果物に混在しています。
- 既存運用では、両方のファイル名が生成されうる前提で扱ってください。

## 7. デバッグ・補助スクリプト

- `debug_image_analysis.py`
	- 画像サイズと吹き出しの関係を検査
	- `image_balloon_debug_report.txt` を出力
- `debug_onomatopeia_calculation.py`
	- オノマトペの面積計算（RLE デコード）の検算
- `check_japanese_font.py`
	- matplotlib の日本語表示テスト

## 8. 旧来コード（XML 系）について

以下は `../Manga109_released_2023_12_07/annotations/*.xml` を読む系統です。

- `main.py`
- `only_text.py`
- `2_text_and_a_character.py`

この系統は、コマ内オブジェクト数やレイアウト調査用の実験コードです。主分析（`statistics/` を更新する JSON 系）とは別ラインです。

## 9. まず何を実行すべきか（引き継ぎ向け）

最初は次の順で動かすと全体を追いやすいです。

1. `python analyze_balloon_comprehensive.py`
2. `python analyze_frame_stats.py`
3. `python analyze_body_stats.py`
4. `python analyze_onomatopoeia_body_stats.py`

その後 `statistics/` の `.txt` と `.csv` を確認し、必要に応じて個別スクリプトを再実行してください。

## 10. 既知の注意点

- `analyze_balloon_bbox_size.py` は `annotations_dir = "./../annotations/"` になっており、他スクリプトと参照先が異なります。
	- データ配置によってはここだけ失敗します。
	- 実運用では `analyze_balloon_comprehensive.py` を使うか、同ファイルの `annotations_dir` を他スクリプトに合わせてください。
- 統計生成スクリプトの多くは既存ファイルを上書きします。履歴が必要なら事前バックアップを推奨。
