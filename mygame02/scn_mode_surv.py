import pyxel
from myscene import GameScene
from myconfig import GameOperator
from mycls import Bounds, pos, draw_select_cursor
from myui import GameUI, GUIText, GUIImage, GUICheckbox
from appconst import SurvivalRule

ENEMY_FORCE_STR = ["chk_enemy_vanguard","chk_enemy_smallship","chk_enemy_airforce","chk_enemy_highfire","chk_enemy_all"]

class SceneModeSurvival(GameScene):
    def __init__(self, app):
        super().__init__(app)
        self.cursor = Bounds(pos(1), pos(4), 8, 8)
        self.rule_select = {
            "forces" : SurvivalRule.TYPE_FORCES_VANGUARD
        }
        self.setup_ui()
    
    def reset_select(self):
        self.cursor.x = self.ui["chk_enemy_vanguard"].bounds.x
        self.cursor.y = self.ui["chk_enemy_vanguard"].bounds.y

    def change_locale(self):
        targets = [
            "txt_survival","txt_enemy",
        ]
        for t in targets:
            if self.ui[t].type == GameUI.TYPE_TEXT:
                self.ui[t].set_text(self.parent.t(t))
            elif self.ui[t].type == GameUI.TYPE_CHECKBOX:
                self.ui[t].text.set_text(self.parent.t(t))

    def setup_ui(self):
        retimg = self.parent.imgbnk.get("larrow")
        self.ui = {
            "return": GUIImage(pos(0)+4,pos(0)+4,retimg.page, Bounds(retimg.x, retimg.y, retimg.w, retimg.h),pyxel.COLOR_BLACK),
            "next": GUIImage(pos(13),pos(18),0, Bounds(8, 72, 8, 8),pyxel.COLOR_BLACK),
            "txt_survival" : GUIText(self.parent.t("txt_survival"), pos(3),pos(1), self.parent.jp_font12, pyxel.COLOR_GREEN),
            "txt_enemy": GUIText(self.parent.t("txt_enemy"), pos(1), pos(3),self.parent.jp_fontmisaki,color1=pyxel.COLOR_WHITE),
            "chk_enemy_vanguard" : GUICheckbox("DD,CL,CA", pos(2), pos(4)+4,font=self.parent.jp_fontmisaki,color1=pyxel.COLOR_WHITE),
            "chk_enemy_smallship" : GUICheckbox("SS,DD", pos(2), pos(6),font=self.parent.jp_fontmisaki,color1=pyxel.COLOR_WHITE),
            "chk_enemy_airforce" : GUICheckbox("CVL,CV", pos(2), pos(7)+4,font=self.parent.jp_fontmisaki,color1=pyxel.COLOR_WHITE),
            "chk_enemy_highfire" : GUICheckbox("CV,BC,BB", pos(2), pos(9),font=self.parent.jp_fontmisaki,color1=pyxel.COLOR_WHITE),
            "chk_enemy_all" : GUICheckbox("ALL", pos(2), pos(10)+4,font=self.parent.jp_fontmisaki,color1=pyxel.COLOR_WHITE),
            
        }
        
        super().setup_ui()
        
        self.ui["return"].selectable = True
        self.ui["return"].set_round(
            bottomui="chk_enemy_vanguard"
        )
        self.ui["next"].selectable = True
        self.ui["next"].set_round(
            upui="chk_enemy_all"
        )
        self.ui["chk_enemy_vanguard"].set_round(
            upui="return",
            bottomui="chk_enemy_smallship"
        )
        self.ui["chk_enemy_smallship"].set_round(
            upui="chk_enemy_vanguard",
            bottomui="chk_enemy_airforce"
        )
        self.ui["chk_enemy_airforce"].set_round(
            upui="chk_enemy_smallship",
            bottomui="chk_enemy_highfire"
        )
        self.ui["chk_enemy_highfire"].set_round(
            upui="chk_enemy_airforce",
            bottomui="chk_enemy_all"
        )
        self.ui["chk_enemy_all"].set_round(
            upui="chk_enemy_highfire",
            bottomui="next"
        )
        
        
        self.rule_select["forces"] = self.parent.states.survival_enemies
        for s in ENEMY_FORCE_STR:
            self.ui[s].checked = False
        self.ui[ENEMY_FORCE_STR[self.rule_select["forces"]]].checked = True
        
    def check_and_config(self):
        if self.select == "return":
            self.parent.current_scene = "gamemode"
            #self.parent.setup_start()
        elif self.select == "next":
            self.decide_select()
        elif self.select in ENEMY_FORCE_STR:
            self.rule_select["forces"] = ENEMY_FORCE_STR.index(self.select)
            for s in ENEMY_FORCE_STR:
                self.ui[s].checked = False
            self.ui[self.select].checked = True
    
    def decide_select(self):
        self.parent.sound.play_select()
        self.parent.states.survival_enemies = self.rule_select["forces"]
        self.parent.current_scene = "playerselect"
        self.parent.setup_selectplayer()
        
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            self.parent.current_scene = "gamemode"
            #self.parent.setup_start()
            return
        keystr = ""
        if self.keyman.is_up():
            keystr = "up"
        elif self.keyman.is_down():
            keystr = "bottom"
        elif self.keyman.is_left():
            keystr = "left"
        elif self.keyman.is_right():
            keystr = "right"
        uoc = self.ui_operation_check(keystr)
        if uoc["mouse"]:
            self.check_and_config()
        elif uoc["mouse_already"]:
            self.check_and_config()
            
        #---decide selection
        if self.keyman.is_enter():
            #self.decide_select(self.select)
            #---final check select ui
            self.check_and_config()
            
        if self.keyman.is_cancel():
            self.parent.sound.play_disable()
            self.parent.current_scene = "gamemode"
            return
        
        return super().update()
    
    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)
        for u in self.ui:
            self.ui[u].draw()
        
        #---cursor
        if pyxel.frame_count % 15 == 0:
            pyxel.dither(0.25)
        elif pyxel.frame_count % 30 == 0:
            pyxel.dither(0.5)
        draw_select_cursor(self.cursor, 6, 6, offset_x=-1, offset_y=-1)
        pyxel.dither(1.0)

        return super().draw()