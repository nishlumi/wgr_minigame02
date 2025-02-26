import pyxel
from myscene import GameScene
from myconfig import GameOperator
from mycls import pos, Bounds, AnimationOnWave
from myui import GameUI, GUIText, GUIImage

class HelpScene(GameScene):
    def __init__(self, app: GameOperator):
        super().__init__(app)
        self.setup_ui()
        
        self.bganime = AnimationOnWave(self, 0, pos(18))
        
    def change_locale(self):
        pass

    def setup_ui(self):
        retimg = self.parent.imgbnk.get("larrow")
        self.ui = {
            "return": GUIImage(pos(0)+4,pos(0)+4,retimg.page, Bounds(retimg.x, retimg.y, retimg.w, retimg.h),pyxel.COLOR_BLACK),
            "txt_title" : GUIText("Help",pos(3),pos(1),self.parent.jp_font10,pyxel.COLOR_WHITE),
            "txt_left" : GUIText("<-: A, Left",pos(1),pos(3),self.parent.jp_fontmisaki,pyxel.COLOR_WHITE),
            "txt_left2": GUIText("    Gamepad-Left button",pos(1),pos(4),self.parent.jp_fontmisaki,pyxel.COLOR_WHITE),
            "txt_right" : GUIText("->: D, Right",pos(1),pos(6),self.parent.jp_fontmisaki,pyxel.COLOR_WHITE),
            "txt_right2": GUIText("    Gamepad-Right button",pos(1),pos(7),self.parent.jp_fontmisaki,pyxel.COLOR_WHITE),
            "txt_mainshoot" : GUIText(self.parent.t("txt_mainshoot"),pos(1),pos(9),self.parent.jp_fontmisaki,pyxel.COLOR_WHITE),
            "txt_mainshoot2" : GUIText("    F, KP-1, Mouse Left",pos(1),pos(10),self.parent.jp_fontmisaki,pyxel.COLOR_WHITE),
            "txt_mainshoot3" : GUIText("    Gamepad A button",pos(1),pos(11),self.parent.jp_fontmisaki,pyxel.COLOR_WHITE),
            "txt_subshoot" : GUIText(self.parent.t("txt_subshoot"),pos(1),pos(13),self.parent.jp_fontmisaki,pyxel.COLOR_WHITE),
            "txt_subshoot2" : GUIText("    G, KP-2, Mouse Right",pos(1),pos(14),self.parent.jp_fontmisaki,pyxel.COLOR_WHITE),
            "txt_subshoot3" : GUIText("    Gamepad B button",pos(1),pos(15),self.parent.jp_fontmisaki,pyxel.COLOR_WHITE),
        }

        super().setup_ui()
        
        self.ui["return"].selectable = True
            
    def change_locale(self):
        self.ui["txt_mainshoot"].set_text(self.parent.t("txt_mainshoot"))
        
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            self.parent.current_scene = "start"
            self.parent.setup_start()
            return
        
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            #---return button
            if self.ui["return"].check_touch_area(pyxel.mouse_x, pyxel.mouse_y):
                self.parent.current_scene = "start"
                self.parent.setup_start()
        
        if self.keyman.is_cancel():
            self.parent.current_scene = "start"
            self.parent.setup_start()
            
        for u in self.ui:
            self.ui[u].update()
            
        self.bganime.update()
        return super().update()
    
    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)
        
        self.bganime.draw()
        
        for u in self.ui:
            self.ui[u].draw()
        return super().draw()
