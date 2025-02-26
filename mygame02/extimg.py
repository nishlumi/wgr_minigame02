import pyxel

class ImageObject:
    class Pos:
        def __init__(self, x: float, y: float) -> None:
            self.x = x
            self.y = y

    def __init__(self, path: str, x: float=0, y: float=0, colkey=-1) -> None:
        """
        ImageObjectのコンストラクタ

        Parameters:
        path (str): 画像ファイルのパス
        x (float): オブジェクトの初期X座標
        y (float): オブジェクトの初期Y座標
        colkey (int): 透過色のパレット番号（デフォルトは-1)
        """
        self.set_pos(x, y)
        self.set_image(path)
        self.set_colkey(colkey)

    def get_pos(self) -> Pos:
        return self.Pos(self.x, self.y)

    def set_pos(self, x: float=None, y: float=None) -> None:
        """
        オブジェクトの座標を設定する

        Parameters:
        x (float): X座標
        y (float): Y座標
        """
        self.x = self.x if x is None else x
        self.y = self.y if y is None else y

    def set_colkey(self, colkey: int):
        '''
        画像の透過色を指定する

        colkey (int): 透過色のパレット番号
        '''
        self.colkey = colkey if colkey > -1 else None

    def move(self, dx: float=0, dy: float=0) -> None:
        '''
        オブジェクトの座標を移動する

        Parameters:
        dx (float): X座標の変位
        dy (float): Y座標の変位
        '''
        self.x += dx
        self.y += dy

    def set_image(self, path: str) -> None:
        """
        画像を設定する

        Parameters:
        path (str): 画像ファイルのパス
        """
        self.img: pyxel.Image = pyxel.Image.from_image(filename=f"{path}")
        self.width = self.img.width
        self.height = self.img.height

    def update(self) -> None:
        """
        オブジェクトの更新処理（必要に応じてオーバーライド）
        """
        pass

    def draw(self) -> None:
        """
        オブジェクトを描画する

        Parameters:
        colkey (float): 透明色キー（デフォルトはなし）
        """
        pyxel.blt(self.x, self.y, self.img, 0, 0, self.width, self.height, colkey=self.colkey)



