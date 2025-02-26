import pyxel
from myconfig import GameOperator
from myscene import GameScene
from myui import GameUI, GUICheckbox, GUIImage, GUIText, GUIRect
from mycls import pos, check_touch_area, Vector2, Bounds, draw_select_cursor, AnimationOnWave
from appconst import SINGLE_FONTSIZE, GameMode, TimeAttackRule, IMG_CONFIG_CHECK_X, IMG_CONFIG_CHECK_Y, IMG_CONFIG_UNCHECK_X, IMGPLT_1

time_line01 = pos(11)
time_line02 = pos(12)
time_line03 = pos(14)
time_line04 = pos(15)
time_line05 = pos(16)+2
time_line06 = pos(18)
time_line07 = pos(18)

class GameModeScene(GameScene):
    def __init__(self, app: GameOperator):
        super().__init__(app)        
        self.select = "bg_timeattack"
        
        self.setup_ui()
        
        self.selmode = "mode"  #---mode: mode select, time - time attack, surv - survival
        self.cursor = Bounds(self.ui["bg_timeattack"].bounds.x, self.ui["bg_timeattack"].bounds.y, pos(13), pos(3))
        
        self.bganime_cur = pos(15)
        self.bganime_img = ((Bounds(0,16,8,8),0),(Bounds(8,16,8,8),0),(Bounds(16,8,8,8),-90),(Bounds(16,64,8,8),0),(Bounds(16,72,16,8),0))
        
        self.bganime = AnimationOnWave(self, pos(0), pos(18))

    def change_locale(self):
        self.ui["mode_timeattack"].set_text(self.parent.t("txt_timeattack"))
        self.ui["mode_survival"].set_text(self.parent.t("txt_survival"))

    def setup_ui(self):
        retimg = self.parent.imgbnk.get("larrow")
        self.ui = {
            "return": GUIImage(pos(0)+4,pos(0)+4,retimg.page, Bounds(retimg.x, retimg.y, retimg.w, retimg.h),pyxel.COLOR_BLACK),
            "bg_timeattack" : GUIRect(pos(1),pos(3), pos(13), pos(3), pyxel.COLOR_NAVY, True, 0.9),
            "bg_survival" : GUIRect(pos(1),pos(7), pos(13), pos(3), pyxel.COLOR_NAVY, True, 0.9),
            "mode_timeattack" : GUIText(self.parent.t("txt_timeattack"), pos(1)+4,pos(3)+4, self.parent.jp_font12, pyxel.COLOR_GREEN),
            "mode_survival" : GUIText(self.parent.t("txt_survival"), pos(1)+4,pos(7)+4, self.parent.jp_font12, pyxel.COLOR_RED)
        }
        super().setup_ui()
            
        self.ui["return"].set_round(
            bottomui=self.ui["bg_timeattack"]
        )
        self.ui["bg_timeattack"].set_round(
            upui=self.ui["return"],
            bottomui=self.ui["bg_survival"]
        )
        self.ui["bg_survival"].set_round(
            upui=self.ui["bg_timeattack"]
        )
        self.ui["return"].selectable = True
        self.ui["return"].set_size(pos(1), pos(1))
        self.ui["mode_timeattack"].set_size(pos(13), pos(3))
        self.ui["bg_timeattack"].selectable = True
        self.ui["mode_survival"].set_size(pos(13), pos(3))
        self.ui["bg_survival"].selectable = True
    
        
    def decide_select(self, mode: int):
        self.parent.sound.play_select()        
        self.parent.states.current_gamemode = mode
        if mode == GameMode.TYPE_TIMEATTACK:
            self.parent.current_scene = "timeattack"
            self.parent.setup_timeattack_rule()
        elif mode == GameMode.TYPE_SURVIVAL:
            self.parent.current_scene = "survival"
            self.parent.setup_survival_rule()
        
    def check_and_config(self, is_decide = False):
        if self.select == "return" and is_decide:
            self.parent.current_scene = "start"
            self.parent.setup_start()
        elif self.select == "bg_timeattack" and is_decide:
            self.decide_select(GameMode.TYPE_TIMEATTACK)
        elif self.select == "bg_survival" and is_decide:
            self.decide_select(GameMode.TYPE_SURVIVAL)
        
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            self.parent.current_scene = "start"
            self.parent.setup_start()
            return

        if self.selmode == "mode":
            
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                #---return button
                """if self.ui["return"].check_touch_area(pyxel.mouse_x, pyxel.mouse_y):
                    self.parent.current_scene = "start"
                    self.parent.setup_start()
                    return"""
                
                
                #---time attack
                #if check_touch_area(pos(1), pos(3), pos(1) + pos(13), pos(3) + pos(3)):
                """if self.ui["mode_timeattack"].check_touch_area(pyxel.mouse_x, pyxel.mouse_y):
                    if self.select == 0:
                        self.decide_select(self.select)
                    else:
                        self.select = GameMode.TYPE_TIMEATTACK
                        self.cursor.y = pos(3)"""
                
                #---survival
                #if check_touch_area(pos(1), pos(7), pos(1) + pos(13), pos(3) + pos(7)):
                """if self.ui["mode_survival"].check_touch_area(pyxel.mouse_x, pyxel.mouse_y):
                    if self.select == 1:
                        self.decide_select(self.select)
                    else:
                        self.select = GameMode.TYPE_SURVIVAL
                        self.cursor.y = pos(7)"""

            
            keystr = ""
            #if (pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP)) :
            if self.keyman.is_up():
                #self.cursor.y -= pos(4)
                #self.select -= 1
                keystr = "up"
                
            elif self.keyman.is_down():  #(pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_S) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN)):
                #self.cursor.y += pos(4)
                #self.select += 1
                keystr = "bottom"
            
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
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    #print(f"mouse {pyxel.mouse_x}:{pyxel.mouse_y} => ui {self.select}vs{self.uikeys[i]} {ui.bounds.x}:{ui.bounds.y}")
                    
                    if ui.check_touch_area(pyxel.mouse_x, pyxel.mouse_y):
                        print(f"sel={self.uikeys[i]}")                        
                        if self.select == self.uikeys[i]:
                            #---already select same
                            self.check_and_config(True)
                        else:
                            self.cursor.x = ui.bounds.x
                            self.cursor.y = ui.bounds.y
                        self.select = self.uikeys[i]
                        print("owari")
                        break"""
            uoc = self.ui_operation_check(keystr)
            if uoc["mouse"]:
                self.check_and_config(True)
            elif uoc["mouse_already"]:
                self.check_and_config(True)
                    
            #---decide selection
            if self.keyman.is_enter(): # pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                #self.decide_select(self.select)
                #---final check select ui
                self.check_and_config(True)
                
            if self.keyman.is_cancel(): #pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
                self.parent.sound.play_disable()
                self.parent.current_scene = "start"
                self.parent.setup_start()
                return
                
        """if self.bganime_cur < 0:
            self.bganime_cur = pos(20)
        brnd = pyxel.rndi(1, 15)
        if pyxel.frame_count % brnd == 0:
            self.bganime_cur -= 1"""
        self.bganime.update()
    
    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)
        
        # return button
        for u in self.ui:            
            self.ui[u].draw()
        
        #---time attack
        """pyxel.dither(0.9)
        pyxel.rect(pos(1),pos(3), pos(13), pos(3), pyxel.COLOR_NAVY)
        pyxel.dither(1)
        #pyxel.text(pos(1)+5,pos(3)+4, "Time attack", pyxel.COLOR_WHITE, self.parent.jp_font12)
        pyxel.text(pos(1)+4,pos(3)+4, "Time attack", pyxel.COLOR_GREEN, self.parent.jp_font12)
        
        #---survival
        pyxel.dither(0.9)
        pyxel.rect(pos(1),pos(7), pos(13), pos(3), pyxel.COLOR_NAVY)
        pyxel.dither(1)
        #pyxel.text(pos(1)+5,pos(7)+4, "Survival", pyxel.COLOR_WHITE, self.parent.jp_font12)
        pyxel.text(pos(1)+4,pos(7)+4, "Survival", pyxel.COLOR_RED, self.parent.jp_font12)"""
        
        #---cursor
        if pyxel.frame_count % 15 == 0:
            pyxel.dither(0.25)
        elif pyxel.frame_count % 30 == 0:
            pyxel.dither(0.5)
        if self.select == "return":
            draw_select_cursor(self.cursor, 6, 6, offset_x=-1, offset_y=-1)
        else:
            draw_select_cursor(self.cursor, pos(13), pos(3), offset_x=-2, offset_y=-2)
        #pyxel.rect(self.cursor.x, self.cursor.y, self.cursor.w, self.cursor.h, pyxel.COLOR_PINK)
        pyxel.dither(1.0)
        
        #pyxel.bltm(pos(0),pos(18),0,32*8,0, 16*8, 2*8,pyxel.COLOR_BLACK)
        #pyxel.blt(self.bganime_cur,pos(18), 0, 0, 16, 8, 8, pyxel.COLOR_BLACK)
        self.bganime.draw()
        
        