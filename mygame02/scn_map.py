import pyxel
from myscene import GameScene
from mycls import Bounds, pos, draw_select_cursor
from mapman import MapEvent, GameMap
from appconst import CSV_BMAP1
from myui import GameUI, GUIText, GUIImage, GUIDialog

class MapScene(GameScene):
    def __init__(self, app):
        super().__init__(app)
        self.cursor = Bounds(0, 0, 8, 8)
        self.select = "e1"
        
        self.states = {
          
        }
        self.setup_ui()
        self.reset_select()

    def setup_ui(self):
        self.mapdata: GameMap = GameMap(self, 0, 0)
        self.mapdata.change_map(1, 0, 0, pos(15), pos(15))
        self.mapdata.load_map_event(CSV_BMAP1)
        
        retimg = self.parent.imgbnk.get("larrow")
        self.ui = {
            "return": GUIImage(pos(0)+4,pos(0)+4,retimg.page, Bounds(retimg.x, retimg.y, retimg.w, retimg.h),pyxel.COLOR_BLACK),
            "e1" : GUIText("E1", pos(3), pos(13)),
            "e2" : GUIText("E2", pos(9), pos(13)),
            "e3" : GUIText("E3", pos(13), pos(11)),
            "e4" : GUIText("E4", pos(9), pos(7)),
            "e5" : GUIText("E5", pos(8), pos(2)),
            "e6" : GUIText("E6", pos(2), pos(5)),
        }
        super().setup_ui()
            
        self.ui["return"].selectable = True
        self.ui["return"].set_round(
            leftui=self.ui["e6"],
            rightui=self.ui["e1"]
        )
        self.ui["e1"].selectable = True
        self.ui["e1"].set_round(
            leftui=self.ui["return"],
            rightui=self.ui["e2"]
        )
        self.ui["e2"].selectable = True
        self.ui["e2"].set_round(
            leftui=self.ui["e1"],
            rightui=self.ui["e3"]
        )
        self.ui["e4"].selectable = True
        self.ui["e3"].set_round(
            leftui=self.ui["e2"],
            rightui=self.ui["e4"]
        )
        self.ui["e4"].selectable = True
        self.ui["e4"].set_round(
            leftui=self.ui["e3"],
            rightui=self.ui["e5"]
        )
        self.ui["e5"].selectable = True
        self.ui["e5"].set_round(
            leftui=self.ui["e4"],
            rightui=self.ui["e6"]
        )
        self.ui["e6"].selectable = True
        self.ui["e6"].set_round(
            leftui=self.ui["e5"],
            rightui=self.ui["return"]
        )
        
        self.dialog = GUIDialog(0, pos(7), pos(15), pos(4),GUIDialog.BTN_YESNO)
        self.dialog.add_contents(GUIText("このマップに出撃しますか？", 0, pos(0), font=self.parent.jp_fontmisaki, color1=pyxel.COLOR_GREEN))
        

    def reset_select(self):
        self.cursor.x = self.ui["return"].bounds.x
        self.cursor.y = self.ui["return"].bounds.y

    def check_and_config(self):
        if self.select == "return":
            self.parent.current_scene = "start"
        elif self.select == "e1":
            self.dialog.open()
    
    def update(self):
        
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
                #print(f"!{self.select}!")
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
        if not self.dialog.is_open():
            uoc = self.ui_operation_check(keystr)
            if uoc["mouse"]:
                self.check_and_config()
        
        
        #---decide selection
        if self.keyman.is_enter():
            #self.decide_select(self.select)
            #---final check select ui
            self.check_and_config()
            
        if self.keyman.is_cancel():
            self.parent.sound.play_disable()
            self.parent.current_scene = "start"
            return
            
        
        self.mapdata.update()
        
        for u in self.ui:
            self.ui[u].update()
            
        self.dialog.update()
        if self.dialog.buttons[0].pressed:
            self.dialog.close()
        
        return super().update()
    
    
    
    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)
        self.mapdata.draw()
        for u in self.ui:
            self.ui[u].draw()
            
        #---cursor
        if pyxel.frame_count % 15 == 0:
            pyxel.dither(0.25)
        elif pyxel.frame_count % 30 == 0:
            pyxel.dither(0.5)
        draw_select_cursor(self.cursor, self.cursor.w, self.cursor.h, -2, -2)
        pyxel.dither(1.0)
        
        self.dialog.draw()
        
        return super().draw()