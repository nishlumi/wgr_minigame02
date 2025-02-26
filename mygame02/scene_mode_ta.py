import pyxel
from myscene import GameScene
from myconfig import GameOperator
from mycls import Bounds, pos, draw_select_cursor
from appconst import TimeAttackRule
from myui import GameUI, GUIText, GUIImage, GUICheckbox

TIME_REAL = [60, 120, 180]
LIMIT_TIME_STR = ["chk_time_short","chk_time_mid","chk_time_long"]
ENEMY_FORCE_STR = ["chk_enemy_all","chk_enemy_vanguard","chk_enemy_smallship","chk_enemy_airforce","chk_enemy_highfire"]
ENEMY_FREQ_STR = ["chk_lv1only","chk_lv2only","chk_lv3only","chk_lv1_2",
            "chk_lv1lots","chk_lv2lots","chk_lv3lots"]
class SceneModeTimeAttack(GameScene):
    def __init__(self, app: GameOperator):
        super().__init__(app)
        self.cursor = Bounds(pos(1), pos(4), 8, 8)
        self.select = ""
        self.rule_select = {
            "time" : TimeAttackRule.TYPE_TIME_SHORT,
            "forces" : TimeAttackRule.TYPE_FORCES_ALL,
            "firstlv" : TimeAttackRule.TYPE_LV1_ONLY
        }
        
        self.setup_ui()
        
        self.uikeys = list(self.ui.keys())
        self.lenui = len(self.uikeys)
        
    def reset_select(self):
        self.cursor.x = self.ui["chk_time_short"].bounds.x
        self.cursor.y = self.ui["chk_time_short"].bounds.y

    def change_locale(self):
        #self.ui["txt_timeattack"].set_text(self.parent.t("timeattack"))
        #self.ui["txt_time"].set_text(self.parent.t("txt_time"))
        #self.ui["txt_enemy"].set_text(self.parent.t("txt_enemy"))
        #self.ui["txt_firstlv"].set_text(self.parent.t("txt_firstlv"))
        targets = [
            "txt_timeattack","txt_time","txt_enemy","txt_firstlv",
            "chk_lv1only","chk_lv2only","chk_lv3only","chk_lv1_2",
            "chk_lv1lots","chk_lv2lots","chk_lv3lots",
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
            "txt_timeattack" : GUIText(self.parent.t("txt_timeattack"), pos(3),pos(1), self.parent.jp_font12, pyxel.COLOR_GREEN),
            "txt_time": GUIText(self.parent.t("txt_time"), pos(1), pos(3),self.parent.jp_fontmisaki,color1=pyxel.COLOR_WHITE),
            "chk_time_short" : GUICheckbox(f"{TIME_REAL[TimeAttackRule.TYPE_TIME_SHORT]}", pos(2), pos(4)+4,font=self.parent.jp_fontmisaki,color1=pyxel.COLOR_WHITE),
            "chk_time_mid" : GUICheckbox(f"{TIME_REAL[TimeAttackRule.TYPE_TIME_MIDDLE]}", pos(5), pos(4)+4,font=self.parent.jp_fontmisaki,color1=pyxel.COLOR_WHITE),
            "chk_time_long" : GUICheckbox(f"{TIME_REAL[TimeAttackRule.TYPE_TIME_LONG]}", pos(9), pos(4)+4,font=self.parent.jp_fontmisaki,color1=pyxel.COLOR_WHITE),
            "txt_enemy": GUIText(self.parent.t("txt_enemy"), pos(1), pos(6),self.parent.jp_fontmisaki,color1=pyxel.COLOR_WHITE),
            "chk_enemy_all" : GUICheckbox("ALL", pos(2), pos(7)+4,font=self.parent.jp_fontmisaki,color1=pyxel.COLOR_WHITE),
            "chk_enemy_vanguard" : GUICheckbox("DD,CL,CA", pos(9), pos(7)+4,font=self.parent.jp_fontmisaki,color1=pyxel.COLOR_WHITE),
            "chk_enemy_smallship" : GUICheckbox("SS,DD", pos(2), pos(9),font=self.parent.jp_fontmisaki,color1=pyxel.COLOR_WHITE),
            "chk_enemy_airforce" : GUICheckbox("CVL,CV", pos(9), pos(9),font=self.parent.jp_fontmisaki,color1=pyxel.COLOR_WHITE),
            "chk_enemy_highfire" : GUICheckbox("CV,BC,BB", pos(2), pos(10)+4,font=self.parent.jp_fontmisaki,color1=pyxel.COLOR_WHITE),
            "txt_firstlv": GUIText(self.parent.t("txt_firstlv"), pos(1), pos(12),self.parent.jp_fontmisaki,color1=pyxel.COLOR_WHITE),
            "chk_lv1only" : GUICheckbox(self.parent.t("chk_lv1only"), pos(2), pos(13),font=self.parent.jp_fontmisaki,color1=pyxel.COLOR_WHITE),
            "chk_lv2only" : GUICheckbox(self.parent.t("chk_lv2only"), pos(8), pos(13),font=self.parent.jp_fontmisaki,color1=pyxel.COLOR_WHITE),
            "chk_lv3only" : GUICheckbox(self.parent.t("chk_lv3only"), pos(2), pos(14)+4,font=self.parent.jp_fontmisaki,color1=pyxel.COLOR_WHITE),
            "chk_lv1_2"   : GUICheckbox(self.parent.t("chk_lv1_2"), pos(8), pos(14)+4,font=self.parent.jp_fontmisaki,color1=pyxel.COLOR_WHITE),
            "chk_lv1lots" : GUICheckbox(self.parent.t("chk_lv1lots"), pos(2), pos(16),font=self.parent.jp_fontmisaki,color1=pyxel.COLOR_WHITE),
            "chk_lv2lots" : GUICheckbox(self.parent.t("chk_lv2lots"), pos(8), pos(16),font=self.parent.jp_fontmisaki,color1=pyxel.COLOR_WHITE),
            "chk_lv3lots" : GUICheckbox(self.parent.t("chk_lv3lots"), pos(2), pos(17)+4,font=self.parent.jp_fontmisaki,color1=pyxel.COLOR_WHITE),
            
        }
        super().setup_ui()
            
        self.ui["return"].selectable = True
        self.ui["return"].set_round(
            bottomui=self.ui["chk_time_short"]
        )
        self.ui["next"].selectable = True
        self.ui["next"].set_round(
            upui=self.ui["chk_lv3lots"]
        )
        self.ui["chk_time_short"].text.set_size(pos(1),pos(1)); 
        self.ui["chk_time_short"].set_round(
            upui=self.ui["return"],
            rightui=self.ui["chk_time_mid"],
            bottomui=self.ui["chk_enemy_all"]
        )
        self.ui["chk_time_mid"].text.set_size(pos(2),pos(1))
        self.ui["chk_time_mid"].set_round(
            upui=self.ui["return"],
            leftui=self.ui["chk_time_short"],
            rightui=self.ui["chk_time_long"],
            bottomui=self.ui["chk_enemy_all"]
        )
        self.ui["chk_time_long"].text.set_size(pos(2),pos(1))
        self.ui["chk_time_long"].set_round(
            upui=self.ui["return"],
            leftui=self.ui["chk_time_mid"],
            bottomui=self.ui["chk_enemy_all"]
        )
        self.ui["chk_enemy_all"].text.set_size(pos(1),pos(1))
        self.ui["chk_enemy_all"].set_round(
            upui=self.ui["chk_time_short"],
            rightui=self.ui["chk_enemy_vanguard"],
            bottomui=self.ui["chk_enemy_smallship"]
        )
        self.ui["chk_enemy_vanguard"].text.set_size(pos(4),pos(1))
        self.ui["chk_enemy_vanguard"].set_round(
            upui=self.ui["chk_time_short"],
            leftui=self.ui["chk_enemy_all"],
            bottomui=self.ui["chk_enemy_airforce"]
        )
        self.ui["chk_enemy_smallship"].text.set_size(pos(1),pos(1))
        self.ui["chk_enemy_smallship"].set_round(
            upui=self.ui["chk_enemy_all"],
            rightui=self.ui["chk_enemy_airforce"],
            bottomui=self.ui["chk_enemy_highfire"]
        )
        self.ui["chk_enemy_airforce"].text.set_size(pos(3),pos(1))
        self.ui["chk_enemy_airforce"].set_round(
            upui=self.ui["chk_enemy_vanguard"],
            leftui=self.ui["chk_enemy_smallship"],
            bottomui=self.ui["chk_enemy_highfire"]
        )
        self.ui["chk_enemy_highfire"].text.set_size(pos(2),pos(1))
        self.ui["chk_enemy_highfire"].set_round(
            upui=self.ui["chk_enemy_smallship"],
            bottomui=self.ui["chk_lv1only"]
        )
        self.ui["chk_lv1only"].text.set_size(pos(1),pos(1))
        self.ui["chk_lv1only"].set_round(
            upui=self.ui["chk_enemy_highfire"],
            rightui=self.ui["chk_lv2only"],
            bottomui=self.ui["chk_lv3only"]
        )
        self.ui["chk_lv2only"].text.set_size(pos(1),pos(1))
        self.ui["chk_lv2only"].set_round(
            upui=self.ui["chk_enemy_highfire"],
            leftui=self.ui["chk_lv1only"],
            bottomui="chk_lv1_2"
        )
        self.ui["chk_lv3only"].text.set_size(pos(1),pos(1))
        self.ui["chk_lv3only"].set_round(
            upui=self.ui["chk_lv1only"],
            rightui="chk_lv1_2",
            bottomui=self.ui["chk_lv1lots"]
        )
        self.ui["chk_lv1_2"].text.set_size(pos(1),pos(1))
        self.ui["chk_lv1_2"].set_round(
            upui="chk_lv2only",
            leftui="chk_lv3only",
            bottomui="chk_lv2lots"
        )
        
        self.ui["chk_lv1lots"].text.set_size(pos(1),pos(1))
        self.ui["chk_lv1lots"].set_round(
            upui="chk_lv3only",
            rightui="chk_lv2lots",
            bottomui="chk_lv3lots"
        )
        self.ui["chk_lv2lots"].text.set_size(pos(1),pos(1))
        self.ui["chk_lv2lots"].set_round(
            upui="chk_lv1_2",
            leftui="chk_lv1lots",
            bottomui="chk_lv3lots"
        )
        self.ui["chk_lv3lots"].text.set_size(pos(1),pos(1))
        self.ui["chk_lv3lots"].set_round(
            upui="chk_lv1lots",
            rightui="next",
            bottomui="next"
        )
        
        
        #---restore value
        self.rule_select["time"] = self.parent.states.timeattack_time
        print(self.rule_select["time"])
        for s in LIMIT_TIME_STR:
            self.ui[s].checked = False
        self.ui[LIMIT_TIME_STR[self.rule_select["time"]]].checked = True
        
        self.rule_select["forces"] = self.parent.states.timeattack_enemies
        for s in ENEMY_FORCE_STR:
            self.ui[s].checked = False
        self.ui[ENEMY_FORCE_STR[self.rule_select["forces"]]].checked = True
        
        self.rule_select["firstlv"] = self.parent.states.timeattack_firstlv
        for s in ENEMY_FREQ_STR:
            self.ui[s].checked = False
        self.ui[ENEMY_FREQ_STR[self.rule_select["firstlv"]]].checked = True
        
        self.reset_select()

    
    def check_and_config(self):
        if self.select == "return":
            self.parent.current_scene = "gamemode"
            #self.parent.setup_start()
        elif self.select == "next":
            self.decide_select()
        
        elif self.select in LIMIT_TIME_STR:
            self.rule_select["time"] = LIMIT_TIME_STR.index(self.select)
            for s in LIMIT_TIME_STR:
                self.ui[s].checked = False
            self.ui[self.select].checked = True
        
        elif self.select in ENEMY_FORCE_STR:
            self.rule_select["forces"] = ENEMY_FORCE_STR.index(self.select)
            for s in ENEMY_FORCE_STR:
                self.ui[s].checked = False
            self.ui[self.select].checked = True
        
        elif self.select in ENEMY_FREQ_STR:
            self.rule_select["firstlv"] = ENEMY_FREQ_STR.index(self.select)
            for s in ENEMY_FREQ_STR:
                self.ui[s].checked = False
            self.ui[self.select].checked = True        
    
    def decide_select(self):
        self.parent.sound.play_select()
        self.parent.states.timeattack_time = self.rule_select["time"]
        self.parent.states.timeattack_enemies = self.rule_select["forces"]
        self.parent.states.timeattack_firstlv = self.rule_select["firstlv"]
        self.parent.current_scene = "playerselect"
        self.parent.setup_selectplayer()
        
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            self.parent.current_scene = "gamemode"
            #self.parent.setup_start()
            return
        """if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            #---return button
            if self.ui["return"].check_touch_area(pyxel.mouse_x, pyxel.mouse_y):
                self.parent.current_scene = "start"
                self.parent.setup_start()
                return"""
        
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
                #self.select = self.uikeys[i]
                if keystr != "" and ui.roundui[keystr]:
                    print("cur select=",ui.name)
                    if ui.roundui[keystr].type == GameUI.TYPE_CHECKBOX:
                        self.cursor.x = ui.roundui[keystr].check_bounds.x
                        self.cursor.y = ui.roundui[keystr].check_bounds.y
                    else:
                        self.cursor.x = ui.roundui[keystr].bounds.x
                        self.cursor.y = ui.roundui[keystr].bounds.y
                    self.select = ui.roundui[keystr].name
                    print("    2nd select=",self.select)
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
        """
        self.ui["return"].draw()
        self.ui["txt_timeattack"].draw()
        
        #---time
        self.ui["txt_time"].draw()
        self.ui["chk_time_short"].draw()
        self.ui["chk_time_mid"].draw()
        self.ui["chk_time_long"].draw()"""
        
        #---cursor
        if pyxel.frame_count % 15 == 0:
            pyxel.dither(0.25)
        elif pyxel.frame_count % 30 == 0:
            pyxel.dither(0.5)
        draw_select_cursor(self.cursor, 6, 6, offset_x=-1, offset_y=-1)
        #pyxel.rect(self.cursor.x, self.cursor.y, self.cursor.w, self.cursor.h, pyxel.COLOR_PINK)
        pyxel.dither(1.0)
        
        
        return super().draw()