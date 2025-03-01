import pyxel
from myconfig import GameOperator
from mycls import KeyManager
from myui import GameUI

class GameScene:
    def __init__(self, app: GameOperator):
        self.parent = app
        self.keyman = KeyManager()
        self.select = ""
        self.ui: dict[GameUI] = {}
        self.uikeys = list(self.ui.keys())
        self.lenui = len(self.uikeys)

    def setup_ui(self):
        for u in self.ui:
            self.ui[u].name = u
            self.ui[u].referlist = self.ui

        self.uikeys = list(self.ui.keys())
        self.lenui = len(self.uikeys)
    
    def get_ui(self, name: str):
        if name in self.ui:
            return self.ui[name]
        else:
            for u in self.ui:
                if self.ui[u].type == GameUI.TYPE_SCROLLAREA:
                    if name in self.ui[u].contents:
                        return self.ui[u].contents[name]
                elif self.ui[u].type == GameUI.TYPE_RESULTCARD:
                    if name in self.ui[u].contents:
                        return self.ui[u].contents[name]
        return None
            
    def ui_operation_check(self, keystr: str):
        """
            return {cursor: bool, mouse: bool}
        """
        ishit = {"cursor": False, "mouse": False, "mouse_already": False}
        for i in range(0, self.lenui):
            ui: GameUI = self.ui[self.uikeys[i]]
            hitbreak = False
            #---ui cursor operation
            if ui.check_touch_area(self.cursor.x, self.cursor.y):
                if keystr != "" and ui.roundui[keystr]:
                    self.cursor.x = ui.roundui[keystr].bounds.x
                    self.cursor.y = ui.roundui[keystr].bounds.y
                    self.select = ui.roundui[keystr].name
                    ishit["cursor"] = True
                    hitbreak = True
            #---mouse, touch operation
            if ui.check_touch_area(pyxel.mouse_x, pyxel.mouse_y) and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                if self.select == self.uikeys[i]:
                    #---already select same
                    ishit["mouse_already"] = True
                else:
                    self.cursor.x = ui.bounds.x
                    self.cursor.y = ui.bounds.y
                    ishit["mouse"] = True
                self.select = self.uikeys[i]
                hitbreak = True
            
            if ui.type == GameUI.TYPE_SCROLLAREA:
                conlst: list[GameUI] = ui.contents
                for c in conlst:
                    con: GameUI = conlst[c]
                    if con.enabled:
                        if con.check_touch_area(self.cursor.x, self.cursor.y):
                            if keystr != "" and con.roundui[keystr]:
                                self.cursor.x = con.roundui[keystr].bounds.x
                                self.cursor.y = con.roundui[keystr].bounds.y
                                self.select = con.roundui[keystr].name
                                ishit["cursor"] = True
                                hitbreak = True
                                print(f"    cursor hit this={con.name} {keystr}={con.roundui[keystr].name}")
                                break
                        if con.check_touch_area(pyxel.mouse_x, pyxel.mouse_y) and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                            if self.select == c:
                                #---already select same
                                ishit["mouse_already"] = True
                            else:
                                self.cursor.x = con.bounds.x
                                self.cursor.y = con.bounds.y
                                ishit["mouse"] = True
                            self.select = c
                            hitbreak = True
                            break
            if hitbreak:
                break
        
        return ishit
    
    def ui_operation_check2(self, keystr: str):
        ishit = {"cursor": False, "mouse": False, "mouse_already": False, "virtual_roundui": None}
        ui = self.get_ui(self.select)
        #print(f"current ui={ui.name}")
        #---normal cursor next - prev check 
        if ui:
            #---current select check
            if keystr != "" and ui.roundui[keystr]:
                ishit["virtual_roundui"] = ui.roundui[keystr]
                print(f"    {keystr} ui={ishit['virtual_roundui'].name}")
                if ui.roundui[keystr].enabled:
                    print(f"    enabled hit!")
                    self.cursor.x = ui.roundui[keystr].bounds.x
                    self.cursor.y = ui.roundui[keystr].bounds.y
                    self.select = ui.roundui[keystr].name
                    ishit["cursor"] = True
        
        #---mouse(touch) directly check
        for i in range(0, self.lenui):
            ui: GameUI = self.ui[self.uikeys[i]]
            if ui.check_touch_area(pyxel.mouse_x, pyxel.mouse_y) and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                if self.select == self.uikeys[i]:
                    #---already select same
                    ishit["mouse_already"] = True
                else:
                    self.cursor.x = ui.bounds.x
                    self.cursor.y = ui.bounds.y
                    ishit["mouse"] = True
                self.select = self.uikeys[i]
            
            hitbreak = False
            #---inside scroll area
            if ui.type == GameUI.TYPE_SCROLLAREA:
                conlst: list[GameUI] = ui.contents
                for c in conlst:
                    con: GameUI = conlst[c]
                    if con.check_touch_area(pyxel.mouse_x, pyxel.mouse_y) and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                        if self.select == c:
                            #---already select same
                            ishit["mouse_already"] = True
                        else:
                            self.cursor.x = con.bounds.x
                            self.cursor.y = con.bounds.y
                            ishit["mouse"] = True
                        self.select = c
                        hitbreak = True
                        break
                if hitbreak:
                    break
        return ishit
    
    def update(self):
        pass

    def draw(self):
        pass