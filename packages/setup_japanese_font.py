import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

def setup_japanese_font():
    """
    日本語フォントを設定する関数
    利用可能な日本語フォントを探して設定
    """
    # システムで利用可能なフォント一覧を取得
    font_list = [f.name for f in fm.fontManager.ttflist]
    
    # 日本語フォントのリスト（優先順）
    japanese_fonts = [
        'Hiragino Sans',
        'Hiragino Kaku Gothic Pro', 
        'Yu Gothic',
        'Meiryo',
        'MS Gothic',
        'Takao PGothic',
        'IPAexGothic',
        'IPAPGothic',
        'VL PGothic',
        'Noto Sans CJK JP',
        'DejaVu Sans'
    ]
    
    # 利用可能な日本語フォントを探す
    available_font = None
    for font in japanese_fonts:
        if font in font_list:
            available_font = font
            break
    
    if available_font:
        plt.rcParams['font.family'] = available_font
        print(f"Using font: {available_font}")
    else:
        # フォールバック：デフォルトフォントを使用
        plt.rcParams['font.family'] = ['DejaVu Sans']
        print("Warning: No Japanese font found. Using default font.")
        print("Available fonts:", [f for f in font_list if any(j in f.lower() for j in ['gothic', 'hiragino', 'yu', 'meiryo', 'noto'])])
    
    # マイナス記号の文字化け対策
    plt.rcParams['axes.unicode_minus'] = False
    
    return available_font

if __name__ == "__main__":
    # テスト用
    setup_japanese_font()
    
    # 簡単なテストプロット
    import numpy as np
    
    plt.figure(figsize=(8, 6))
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    
    plt.plot(x, y, label='サイン波')
    plt.title('日本語フォントテスト')
    plt.xlabel('X軸ラベル')
    plt.ylabel('Y軸ラベル')
    plt.legend()
    plt.grid(True)
    plt.show()
