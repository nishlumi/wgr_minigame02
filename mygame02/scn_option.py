import pyxel
from myscene import GameScene
from myconfig import GameOperator
from myui import GameUI,GUIText, GUICheckbox, GUIImage
from mycls import pos, Bounds, draw_select_cursor
from appconst import SINGLE_FONTSIZE, IMGPLT_1, IMG_CONFIG_CHECK_X, IMG_CONFIG_CHECK_Y, IMG_CONFIG_UNCHECK_X
from apptranslate import LOCALE_JA, LOCALE_EN

MODESTRING = ["Easy","Normal","Hard","Hell"]

class OptionScene(GameScene):
    def __init__(self, app: GameOperator):
        super().__init__(app)
        
        self.setup_ui()
        
        self.select = "bgm"
        self.cursor = Bounds(pos(1),pos(3), 8, 8)
        
        self.setup_config()
    
    def setup_ui(self):
        retimg = self.parent.imgbnk.get("larrow")
        self.ui = {
            "return": GUIImage(pos(0)+4,pos(0)+4,retimg.page, Bounds(retimg.x, retimg.y, retimg.w, retimg.h),pyxel.COLOR_BLACK),
            "bgm": GUICheckbox("BGM", pos(1), pos(3),False,font=self.parent.jp_fontmisaki,color1=pyxel.COLOR_WHITE),
            "se": GUICheckbox("SE", pos(5), pos(3),False,font=self.parent.jp_fontmisaki,color1=pyxel.COLOR_WHITE),
            "txt_locale" : GUIText("Language:", pos(1), pos(5),font=self.parent.jp_fontmisaki,color1=pyxel.COLOR_WHITE),
            "locale_ja": GUICheckbox("Japanese", pos(2), pos(6)+4,font=self.parent.jp_fontmisaki,color1=pyxel.COLOR_WHITE),
            "locale_en": GUICheckbox("English", pos(8), pos(6)+4,font=self.parent.jp_fontmisaki,color1=pyxel.COLOR_WHITE),
            #"txt_mode": GUIText("Mode:",pos(1), pos(5),color1=pyxel.COLOR_WHITE),
            "testmode": GUICheckbox("Test mode", pos(1), pos(8),False,font=self.parent.jp_fontmisaki,color1=pyxel.COLOR_WHITE),
            
        }
        super().setup_ui()
        
        self.ui["bgm"].text.set_size(pos(2), pos(1))
        self.ui["se"].text.set_size(pos(1), pos(1))
        self.ui["locale_ja"].text.set_size(pos(6), pos(1))
        self.ui["locale_en"].text.set_size(pos(6), pos(1))
        
        self.ui["return"].selectable = True
        self.ui["return"].set_round(
            bottomui=self.ui["bgm"]
        )
        self.ui["bgm"].set_round(
            upui=self.ui["return"],
            rightui=self.ui["se"],
            bottomui=self.ui["locale_ja"],
        )
        self.ui["se"].set_round(
            upui=self.ui["return"],
            leftui=self.ui["bgm"],
            bottomui=self.ui["locale_en"],
        )
        self.ui["locale_ja"].set_round(
            upui=self.ui["bgm"],
            rightui=self.ui["locale_en"],
        )
        self.ui["locale_en"].set_round(
            upui=self.ui["se"],
            leftui=self.ui["locale_ja"],
        )
        
        
    def setup_config(self):
        self.ui["bgm"].checked = self.parent.config["use_bgm"]
        self.ui["se"].checked = self.parent.config["use_se"]
        if self.parent.config["locale"] == LOCALE_JA:
            self.ui["locale_ja"].checked = True
            self.ui["locale_en"].checked = False
        elif self.parent.config["locale"] == LOCALE_EN:
            self.ui["locale_ja"].checked = False
            self.ui["locale_en"].checked = True
        
        self.ui["testmode"].checked = self.parent.is_test
        
    def check_and_config(self):
        if self.select == "return":
            self.parent.save()
            self.parent.current_scene = "start"
            self.parent.setup_start()
        
        #---use bgm
        elif self.select == "bgm":
            self.parent.config["use_bgm"] = not self.parent.config["use_bgm"]
            self.parent.sound.use_bgm = self.parent.config["use_bgm"]
            self.ui["bgm"].checked = self.parent.config["use_bgm"]
        
        #---use se
        elif self.select == "se":
            self.parent.config["use_se"] = not self.parent.config["use_se"]
            self.parent.sound.use_se = self.parent.config["use_se"]
            self.ui["se"].checked = self.parent.config["use_se"]
            print("flag=", self.parent.sound.use_se)
        
        #---locale
        elif self.select == "locale_ja":
            self.parent.config["locale"] = LOCALE_JA
            self.ui["locale_ja"].checked = True
            self.ui["locale_en"].checked = False
            
        elif self.select  == "locale_en":
            self.parent.config["locale"] = LOCALE_EN
            self.ui["locale_ja"].checked = False
            self.ui["locale_en"].checked = True
        
        elif self.select == "testmode":
            self.parent.is_test = not self.parent.is_test
            self.ui["testmode"].checked = self.parent.is_test
        
    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            #---return button
            if self.ui["return"].check_touch_area(pyxel.mouse_x, pyxel.mouse_y):
                self.parent.save()
                self.parent.current_scene = "start"
                self.parent.setup_start()
        
            #---use bgm
            """if self.ui["bgm"].check_touch_area(pyxel.mouse_x, pyxel.mouse_y):
                self.parent.config["use_bgm"] = not self.parent.config["use_bgm"]
                self.parent.sound.use_bgm = self.parent.config["use_bgm"]
                self.ui["bgm"].checked = self.parent.config["use_bgm"]
            
            #---use se
            if self.ui["se"].check_touch_area(pyxel.mouse_x, pyxel.mouse_y):
                self.parent.config["use_se"] = not self.parent.config["use_se"]
                self.parent.sound.use_se = self.parent.config["use_se"]
                self.ui["se"].checked = self.parent.config["use_se"]
                print("flag=", self.parent.sound.use_se)
            
            #---locale
            if self.ui["locale_ja"].check_touch_area(pyxel.mouse_x, pyxel.mouse_y):
                self.parent.config["locale"] = LOCALE_JA
                self.ui["locale_ja"].checked = True
                self.ui["locale_en"].checked = False
                
            if self.ui["locale_en"].check_touch_area(pyxel.mouse_x, pyxel.mouse_y):
                self.parent.config["locale"] = LOCALE_EN
                self.ui["locale_ja"].checked = False
                self.ui["locale_en"].checked = True"""
        
        keystr = ""
        if self.keyman.is_up():
            keystr = "up"
        elif self.keyman.is_down():
            keystr = "bottom"
        elif self.keyman.is_left():
            keystr = "left"
        elif self.keyman.is_right():
            keystr = "right"
        
        """for i in range(0, self.lenui):
            ui = self.ui[self.uikeys[i]]
            #---ui cursor operation
            if ui.check_touch_area(self.cursor.x, self.cursor.y):
                self.select = self.uikeys[i]
                if keystr != "" and ui.roundui[keystr]:
                    if ui.roundui[keystr].type == GameUI.TYPE_CHECKBOX:
                        self.cursor.x = ui.roundui[keystr].check_bounds.x
                        self.cursor.y = ui.roundui[keystr].check_bounds.y
                    else:
                        self.cursor.x = ui.roundui[keystr].bounds.x
                        self.cursor.y = ui.roundui[keystr].bounds.y
                    self.select = ui.roundui[keystr].name
                    break
            #---mouse, touch operation
            if ui.check_touch_area(pyxel.mouse_x, pyxel.mouse_y) and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.select = self.uikeys[i]
                if ui.type == GameUI.TYPE_CHECKBOX:
                    self.cursor.x = ui.check_bounds.x
                    self.cursor.y = ui.check_bounds.y
                else:
                    self.cursor.x = ui.bounds.x
                    self.cursor.y = ui.bounds.y
                self.check_and_config()
                break"""
        uoc = self.ui_operation_check(keystr)
        if uoc["mouse"]:
            self.check_and_config()
        
        if self.keyman.is_enter():
            self.check_and_config()
        
        for u in self.ui:
            self.ui[u].update()

    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)
        
        # return button
        #pyxel.blt(pos(1), pos(1), IMGPLT_1, 0, 72, 8, 8, pyxel.COLOR_BLACK)
        for u in self.ui:
            self.ui[u].draw()        
        
        draw_select_cursor(self.cursor, 8, 8, -2, -2)
        
        #---help
        """pyxel.text(pos(1), pos(12), "---Help---",pyxel.COLOR_WHITE)
        pyxel.text(pos(1), pos(13), "<-: A-key, Left-key",pyxel.COLOR_WHITE)
        pyxel.text(pos(1), pos(14), "->: D-key, Right-key",pyxel.COLOR_WHITE)
        pyxel.text(pos(1), pos(15), "Shot: SPACE, Mouse left,",pyxel.COLOR_WHITE)
        pyxel.text(pos(5), pos(16), "Gamepad A-button",pyxel.COLOR_WHITE)
        pyxel.text(pos(1), pos(17), "Boost:  Shift-key",pyxel.COLOR_WHITE)        
        pyxel.text(pos(5), pos(18), "Gamepad B-button",pyxel.COLOR_WHITE)
        pyxel.blt(pos(2),  pos(18), IMGPLT_1, 0, 32, 16, 16, pyxel.COLOR_BLACK)
        pyxel.text(pos(5), pos(19), "- button",pyxel.COLOR_WHITE)"""