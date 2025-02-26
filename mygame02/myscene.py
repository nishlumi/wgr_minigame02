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
    
    def ui_operation_check(self, keystr: str):
        """
            return {cursor: bool, mouse: bool}
        """
        ishit = {"cursor": False, "mouse": False, "mouse_already": False}
        for i in range(0, self.lenui):
            ui = self.ui[self.uikeys[i]]
            #---ui cursor operation
            if ui.check_touch_area(self.cursor.x, self.cursor.y):
                if keystr != "" and ui.roundui[keystr]:
                    self.cursor.x = ui.roundui[keystr].bounds.x
                    self.cursor.y = ui.roundui[keystr].bounds.y
                    self.select = ui.roundui[keystr].name
                    ishit["cursor"] = True
                    break
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
                break
        return ishit
    
    def update(self):
        pass

    def draw(self):
        pass