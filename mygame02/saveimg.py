# ドット絵のキャプチャ用プログラム
# プログラムを実行してPyxel画面で Alt+1 キー を押すと
# PNG画像ファイルがデスクトップに作成される

RESOURCE = "sample"     # リソースファイルの名前
IMAGE_NO = 0
WIDTH    = 256
HEIGHT   = 256
SCALE    = 1            # 1ドットの大きさ

import pyxel
import sys

print(sys.argv)
respath = sys.argv[1]

pyxel.init(WIDTH,HEIGHT,display_scale=SCALE,capture_scale=SCALE)
#pyxel.load(RESOURCE + ".pyxres")
pyxel.load(respath)

#pyxel.blt( 0, 0, IMAGE_NO, 0, 0, WIDTH, HEIGHT )
pyxel.blt( 0, 0, int(sys.argv[2]), 0, 0, WIDTH, HEIGHT )
pyxel.show()