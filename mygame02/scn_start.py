import pyxel
from mycls import pos, Bounds, draw_select_cursor
from myscene import GameScene
from myui import GameUI,GUIText, GUIRect
from appconst import SINGLE_FONTSIZE
from apptranslate import LOCALE_EN, LOCALE_JA
from extimg import ImageObject
isloadjs = False
try:
    import js
    isloadjs =  True
except Exception as e:
    print(e)
    isloadjs = False
    
    

class StartScene(GameScene):
    def __init__(self, app):
        super().__init__(app)
        #self.parent = app
        self.sam1 = ImageObject("assets/img/gametitle_wgrfangame01.png",pos(2),pos(2))
        self.teststr = ""
        
        self.setup_ui()
        self.select = "mnstart" #Vector2(0, 0)
        self.cursor = Bounds(self.ui["mnstart"].bounds.x, self.ui["mnstart"].bounds.y, pos(5), pos(1))
        
        self.uikeys = list(self.ui.keys())
        self.lenui = len(self.uikeys)

    def setup_ui(self):
        self.ui = {
            #"pretitle_rect" : GUIRect(pos(2),pos(8)+4,pos(12),pos(1), pyxel.COLOR_LIGHT_BLUE, True, 0.75, 30),
            "pretitle": GUIText(self.parent.t("pretitle"),pos(2)+4,pos(8)+4,self.parent.jp_fontmisaki,pyxel.COLOR_WHITE,pyxel.COLOR_BLACK, 1, 0),
            "title1": GUIText("Warship Shooting R",pos(1),pos(5),self.parent.jp_font12,pyxel.COLOR_RED,pyxel.COLOR_BLACK, 1, 0),
            "mnstart": GUIText(self.parent.t("start"),pos(2),pos(15),self.parent.jp_fontmisaki,pyxel.COLOR_WHITE,pyxel.COLOR_BLACK, 0, 0),
            "mnoption": GUIText(self.parent.t("option"),pos(9),pos(15),self.parent.jp_fontmisaki,pyxel.COLOR_WHITE,pyxel.COLOR_BLACK, 0, 0),
            "mnhelp": GUIText(self.parent.t("help"),pos(9),pos(17),self.parent.jp_fontmisaki,pyxel.COLOR_WHITE,pyxel.COLOR_BLACK, 0, 0),
            "author": GUIText(f"@{self.parent.meta.author}",pos(10), pos(19),self.parent.jp_fontmisaki,color1=pyxel.COLOR_RED)
        }
        super().setup_ui()
            
        self.ui["mnstart"].set_size(pos(7), pos(1))
        self.ui["mnoption"].set_size(pos(6), pos(1))
        self.ui["mnhelp"].set_size(pos(6), pos(1))
        self.ui["mnstart"].selectable = True
        self.ui["mnoption"].selectable = True
        self.ui["mnhelp"].selectable = True
        
        self.ui["mnstart"].set_round(
            rightui=self.ui["mnoption"],
            bottomui=None
        )
        self.ui["mnoption"].set_round(
            leftui=self.ui["mnstart"],
            bottomui=self.ui["mnhelp"]
        )
        self.ui["mnhelp"].set_round(
            upui=self.ui["mnoption"],
            leftui=self.ui["mnstart"],
        )
        

        
    def change_locale(self):
        self.ui["pretitle"].set_text(self.parent.t("pretitle"))
        if self.parent.config["locale"] == LOCALE_JA:
            self.ui["pretitle"].set_pos(pos(4)+4,pos(8)+4)
        else:
            self.ui["pretitle"].set_pos(pos(3),pos(8)+4)
        self.ui["mnstart"].set_text(self.parent.t("start"))
        self.ui["mnoption"].set_text(self.parent.t("option"))
        self.ui["mnhelp"].set_text(self.parent.t("help"))

    def check_and_config(self):
        if self.select == "mnstart":
            self.parent.current_scene = "gamemode"
            self.parent.setup_gamemode()
        elif self.select == "mnoption":
            self.parent.current_scene = "option"
            self.parent.setup_option()
        elif self.select == "mnhelp":
            self.parent.current_scene = "help"
            self.parent.setup_help()
        
        
    def update(self):
        #---to play
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            """if self.ui["mnstart"].check_touch_area(pyxel.mouse_x, pyxel.mouse_y):
                self.parent.current_scene = "gamemode"
                self.parent.setup_gamemode()
                
        
            #---to option
            if self.ui["mnoption"].check_touch_area(pyxel.mouse_x, pyxel.mouse_y):
                self.parent.current_scene = "option"
                self.parent.setup_option()
            
            #---to help
            if self.ui["mnhelp"].check_touch_area(pyxel.mouse_x, pyxel.mouse_y):
                self.parent.current_scene = "help"
                self.parent.setup_help()"""
                
            #---to test
        
            if (
                (pos(6) <= pyxel.mouse_x <= pos(8))
                and
                (pos(18) <= pyxel.mouse_y <= pos(19))
            ):
                print("test!")
                if isloadjs:
                    js.window.localStorage.setItem("houge",f"time is {pyxel.frame_count}.")
            if (
                (pos(6) <= pyxel.mouse_x <= pos(8))
                and
                (pos(14) <= pyxel.mouse_y <= pos(15))
            ):
                print("load !")
                if isloadjs:
                    self.teststr = js.window.localStorage.getItem("houge")
        
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
        elif uoc["mouse_already"]:
                self.check_and_config()
                
        #---decide selection
        if self.keyman.is_enter():
            self.check_and_config()
        
        for u in self.ui:
            self.ui[u].update()
        
        return super().update()

    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)
        #pyxel.blt(pos(2),pos(5), 0, 32, 208, 16 * 4, 16 * 2)
        self.sam1.set_pos(pos(0), pos(0))
        self.sam1.draw()
        
        #pyxel.dither(0.75)
        #pyxel.rect(pos(0),pos(0)+4,pos(12),pos(1),pyxel.COLOR_LIGHT_BLUE)
        #pyxel.dither(1.0)
        
        #pyxel.text(pos(1)+1, pos(5),"Warship-Girls R", pyxel.COLOR_BLACK, self.parent.jp_font12)
        #pyxel.text(pos(1), pos(5),"Warship-Girls R", pyxel.COLOR_RED, self.parent.jp_font12)
        #pyxel.text(pos(3)+1, pos(7),"FAN Game 02", pyxel.COLOR_BLACK, self.parent.jp_font10)
        #pyxel.text(pos(3), pos(7),"FAN Game 02", pyxel.COLOR_RED, self.parent.jp_font10)
        for u in self.ui:
            self.ui[u].draw()
        #self.ui["title2"].draw()
        
        draw_select_cursor(self.cursor, self.cursor.w, self.cursor.h, -2, -2)
        
        if pyxel.frame_count % 30 == 0:
            pyxel.dither(0.5)
        #elif pyxel.frame_count % 30 == 0:
            #pyxel.dither(0.75)
        if self.parent.is_test:
            pyxel.text(pos(3),pos(10), "TEST", pyxel.COLOR_RED,self.parent.jp_font12)
            #pyxel.text(pos(2), pos(9) + 4,"No BGM (show an Option)", pyxel.COLOR_RED)
            pyxel.text(pos(2), pos(11) + 4,"ゲームオーバーなし", pyxel.COLOR_RED, self.parent.jp_fontmisaki)
            #pyxel.text(pos(2), pos(13) + 4,"芸夢オーバーover", pyxel.COLOR_RED, self.parent.jp_font8)
            
        pyxel.dither(1)
        #pyxel.text(pos(10), pos(13) + 4,f"@{self.parent.meta.author}", pyxel.COLOR_RED)
        #self.ui["author"].draw()
        
        #---new menu
        #pyxel.text(pos(2), pos(15), "Start", pyxel.COLOR_WHITE, self.parent.jp_font10)
        #pyxel.text(pos(9), pos(15), "Option", pyxel.COLOR_WHITE, self.parent.jp_font10)
        #pyxel.text(pos(9), pos(17), "Help", pyxel.COLOR_WHITE, self.parent.jp_font10)
        #self.ui["mnstart"].draw()
        #self.ui["mnoption"].draw()
        #self.ui["mnhelp"].draw()
    
        #pyxel.text(pos(6), pos(14), "load", pyxel.COLOR_RED)
        #pyxel.text(pos(6), pos(10), self.teststr, pyxel.COLOR_RED)
        #pyxel.text(pos(6), pos(18), "test", pyxel.COLOR_CYAN)
        
        return super().draw()