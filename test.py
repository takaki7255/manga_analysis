import matplotlib.pyplot as plt
import japanize_matplotlib
import numpy as np
 
# 二次曲線の作成
x = np.linspace(-3,3)
y = x**2
  
# 二次曲線のプロット作成
plt.plot(x, y, label="二次曲線")
 
# タイトル・軸ラベル表示
plt.title("グラフタイトル")
plt.xlabel("x軸ラベル名")
plt.ylabel("y軸ラベル名")
 
# グラフ内テキスト表示
plt.text(0, 4,"テキスト例")
 
# 凡例表示
plt.legend()
 
plt.show()