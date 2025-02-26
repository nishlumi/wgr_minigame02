import pyxel
from typing import NamedTuple, TypedDict
from myconfig import GameOperator
from myscene import GameScene
from mycls import Bounds, Vector2, pos, check_touch_area, draw_select_cursor, ShipJob, AttackCommand
from appconst import GameMode, SINGLE_FONTSIZE, IMG_CHARA_X, PLAYER_MOTION, WEAPON_IMAGES, CSV_PLAYABLE
from myui import GameUI, GUIImage, GUIText

SELDOTIMG_SIZE = 16
"""
SELIMG_SIZE = 56
class CursorImagePosition(NamedTuple):
    x: int
    y: int

CIP = TypedDict
CIP.top = CursorImagePosition(2, 80)
CIP.left = CursorImagePosition(0, 82)
CIP.right = CursorImagePosition(14, 82)
CIP.bottom = CursorImagePosition(2, 94)

SHOW_CURSOR_POS_Y = pos(10)

CHARALIST = [
    [("SS U47",0), ("DD Ayanami",1),("ADSG Changchun",2),("CL Atlanta",3)],
    [("CA Quincy",4), ("CVL Junyo", 5),("CV-16 Lexington",6), ("BC Renown",7)]
]
CHARA_TOPIMAGE_LIST = [
    [(32, 48), (48, 48),(64, 48),(80, 48)],
    [(96, 48), (112, 48),(128, 48),(144, 48)]
]
"""

class SelectScene(GameScene):
    def __init__(self, app: GameOperator):
        super().__init__(app)
        #self.sound = SoundManager()
        self.setup_ui()
        
        self.select = "img_dd" #Vector2(0, 0)
        self.cursor = Bounds(self.ui["img_dd"].bounds.x, self.ui["img_dd"].bounds.y, 16, 16)
        self.img_page = 1
        
        
        self.motionkeys = list(PLAYER_MOTION.keys())
        self.cur_motionskey = 6
        self.equiptype = 0
        
        self.setup_selectjob(CSV_PLAYABLE[self.select].jobtype)
    
    def setup_ui(self):
        retimg = self.parent.imgbnk.get("larrow")
        self.ui = {
            "return": GUIImage(pos(0)+4,pos(0)+4,retimg.page, Bounds(retimg.x, retimg.y, retimg.w, retimg.h),pyxel.COLOR_BLACK),
            "sel_charaname" : GUIText("", pos(2), pos(0.5), self.parent.jp_font10, color1=pyxel.COLOR_RED,color2=pyxel.COLOR_WHITE, shifted_x=1),
            "img_ss" : GUIImage(pos(2),pos(10),0,Bounds(32,48,SELDOTIMG_SIZE,SELDOTIMG_SIZE),pyxel.COLOR_BLACK),
            "img_dd" : GUIImage(pos(5),pos(10),0,Bounds(48,48,SELDOTIMG_SIZE,SELDOTIMG_SIZE),pyxel.COLOR_BLACK),
            "img_asdg" : GUIImage(pos(8),pos(10),0,Bounds(64,48,SELDOTIMG_SIZE,SELDOTIMG_SIZE),pyxel.COLOR_BLACK),
            "img_cl" : GUIImage(pos(11),pos(10),0,Bounds(80,48,SELDOTIMG_SIZE,SELDOTIMG_SIZE),pyxel.COLOR_BLACK),
            "img_ca" : GUIImage(pos(2),pos(13),0,Bounds(96,48,SELDOTIMG_SIZE,SELDOTIMG_SIZE),pyxel.COLOR_BLACK),
            "img_cvl" : GUIImage(pos(5),pos(13),0,Bounds(112,48,SELDOTIMG_SIZE,SELDOTIMG_SIZE),pyxel.COLOR_BLACK),
            "img_cv" : GUIImage(pos(8),pos(13),0,Bounds(128,48,SELDOTIMG_SIZE,SELDOTIMG_SIZE),pyxel.COLOR_BLACK),
            "img_bc" : GUIImage(pos(11),pos(13),0,Bounds(144,48,SELDOTIMG_SIZE,SELDOTIMG_SIZE),pyxel.COLOR_BLACK),
        }
        super().setup_ui()
            
        self.ui["return"].selectable = True
        self.ui["return"].set_round(
            bottomui=self.ui["img_ss"]
        )
        self.ui["img_ss"].selectable = True
        self.ui["img_ss"].set_round(
            upui=self.ui["return"],
            leftui=None,
            rightui=self.ui["img_dd"],
            bottomui=self.ui["img_ca"]
        )
        self.ui["img_dd"].selectable = True
        self.ui["img_dd"].set_round(
            upui=self.ui["return"],
            leftui=self.ui["img_ss"],
            rightui=self.ui["img_asdg"],
            bottomui=self.ui["img_cvl"]
        )
        self.ui["img_asdg"].selectable = True
        self.ui["img_asdg"].set_round(
            upui=self.ui["return"],
            leftui=self.ui["img_dd"],
            rightui=self.ui["img_cl"],
            bottomui=self.ui["img_cv"]
        )
        self.ui["img_cl"].selectable = True
        self.ui["img_cl"].set_round(
            upui=self.ui["return"],
            leftui=self.ui["img_asdg"],
            rightui=None,
            bottomui=self.ui["img_bc"]
        )
        #---2 line
        self.ui["img_ca"].selectable = True
        self.ui["img_ca"].set_round(
            upui=self.ui["img_ss"],
            leftui=None,
            rightui=self.ui["img_cvl"]
        )
        self.ui["img_cvl"].selectable = True
        self.ui["img_cvl"].set_round(
            upui=self.ui["img_dd"],
            leftui=self.ui["img_ca"],
            rightui=self.ui["img_cv"]
        )
        self.ui["img_cv"].selectable = True
        self.ui["img_cv"].set_round(
            upui=self.ui["img_asdg"],
            leftui=self.ui["img_cvl"],
            rightui=self.ui["img_bc"]
        )
        self.ui["img_bc"].selectable = True
        self.ui["img_bc"].set_round(
            upui=self.ui["img_cl"],
            leftui=self.ui["img_cv"],
            rightui=None
        )
        
    def reset_select(self):
        self.select = "img_dd"
        self.cursor = Bounds(self.ui["img_dd"].bounds.x, self.ui["img_dd"].bounds.y, 16, 16)
    
    def setup_selectjob(self, jobid):
        self.tempjob = ShipJob(jobid, self.equiptype)
        
    def decide_select(self):
        if self.select == "return":
            if self.parent.states.current_gamemode == GameMode.TYPE_TIMEATTACK:
                self.parent.current_scene = "timeattack"
                self.parent.setup_timeattack_rule()
            elif self.parent.states.current_gamemode == GameMode.TYPE_SURVIVAL:
                self.parent.current_scene = "survival"
                self.parent.setup_survival_rule()
        else:
            self.parent.sound.play_select()
            self.parent.setup_mainstage(CSV_PLAYABLE[self.select].jobtype, self.equiptype)
            self.parent.current_scene = "mainstage"
        
    def check_and_config(self):
        if self.select == "return":
            if self.parent.states.current_gamemode == GameMode.TYPE_TIMEATTACK:
                self.parent.current_scene = "timeattack"
                self.parent.setup_timeattack_rule()
            elif self.parent.states.current_gamemode == GameMode.TYPE_SURVIVAL:
                self.parent.current_scene = "survival"
                self.parent.setup_survival_rule()
        
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            self.parent.current_scene = "gamemode"
            self.parent.setup_gamemode()
            return
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            #---return button
            """if check_touch_area(pos(0)+4, pos(0)+4, pos(0)+4 + SINGLE_FONTSIZE, pos(0)+4 + SINGLE_FONTSIZE):
                self.parent.current_scene = "gamemode"
                self.parent.setup_start()
                return"""
                
            #---touch select: up
            """if check_touch_area(12, SHOW_CURSOR_POS_Y, 12+pos(2), SHOW_CURSOR_POS_Y+pos(2)):
                if self.select.x == 0 and self.select.y == 0:
                    self.decide_select()
                else:
                    self.select.x = 0
                    self.select.y = 0
                    self.equiptype = 0
                    self.cursor.x = 12
                    self.cursor.y = SHOW_CURSOR_POS_Y
            if check_touch_area(12+24, SHOW_CURSOR_POS_Y, 12+24+pos(2), SHOW_CURSOR_POS_Y+pos(2)):
                if self.select.x == 1 and self.select.y == 0:
                    self.decide_select()
                else:
                    self.select.x = 1
                    self.select.y = 0
                    self.equiptype = 0
                    self.cursor.x = 12+24
                    self.cursor.y = SHOW_CURSOR_POS_Y
            
            if check_touch_area(12+24+24, SHOW_CURSOR_POS_Y, 12+24+24+pos(2), SHOW_CURSOR_POS_Y+pos(2)):
                if self.select.x == 2 and self.select.y == 0:
                    self.decide_select()
                else:
                    self.select.x = 2
                    self.select.y = 0
                    self.equiptype = 0
                    self.cursor.x = 12+24+24
                    self.cursor.y = SHOW_CURSOR_POS_Y
            if check_touch_area(12+24+24+24, SHOW_CURSOR_POS_Y, 12+24+24+24+pos(2), SHOW_CURSOR_POS_Y+pos(2)):
                if self.select.x == 3 and self.select.y == 0:
                    self.decide_select()
                else:
                    self.select.x = 3
                    self.select.y = 0
                    self.equiptype = 0
                    self.cursor.x = 12+24+24+24
                    self.cursor.y = SHOW_CURSOR_POS_Y
            #---touch select: bottom
            if check_touch_area(12, SHOW_CURSOR_POS_Y+24, 12+pos(2), SHOW_CURSOR_POS_Y+24+pos(2)):
                if self.select.x == 0 and self.select.y == 1:
                    self.decide_select()
                else:
                    self.select.x = 0
                    self.select.y = 1
                    self.equiptype = 0
                    self.cursor.x = 12
                    self.cursor.y = SHOW_CURSOR_POS_Y+24
            if check_touch_area(12+24, SHOW_CURSOR_POS_Y+24, 12+24+pos(2), SHOW_CURSOR_POS_Y+24+pos(2)):
                if self.select.x == 1 and self.select.y == 1:
                    self.decide_select()
                else:
                    self.select.x = 1
                    self.select.y = 1
                    self.equiptype = 0
                    self.cursor.x = 12+24
                    self.cursor.y = SHOW_CURSOR_POS_Y+24
            
            if check_touch_area(12+24+24, SHOW_CURSOR_POS_Y+24, 12+24+24+pos(2), SHOW_CURSOR_POS_Y+24+pos(2)):
                if self.select.x == 2 and self.select.y == 1:
                    self.decide_select()
                else:
                    self.select.x = 2
                    self.select.y = 1
                    self.equiptype = 0
                    self.cursor.x = 12+24+24
                    self.cursor.y = SHOW_CURSOR_POS_Y+24
            if check_touch_area(12+24+24+24, SHOW_CURSOR_POS_Y+24, 12+24+24+24+pos(2), SHOW_CURSOR_POS_Y+24+pos(2)):
                if self.select.x == 3 and self.select.y == 1:
                    self.decide_select()
                else:
                    self.select.x = 3
                    self.select.y = 1
                    self.equiptype = 0
                    self.cursor.x = 12+24+24+24
                    self.cursor.y = SHOW_CURSOR_POS_Y+24"""
        
        keystr = ""
        if self.keyman.is_right():
            keystr = "right"
        elif self.keyman.is_left():
            keystr = "left"
        if self.keyman.is_up():
            keystr = "up"
        elif self.keyman.is_down():
            keystr = "bottom"
            
        #---new ui loop
        """for i in range(0, self.lenui):
            ui = self.ui[self.uikeys[i]]
            #---ui cursor operation
            if ui.check_touch_area(self.cursor.x, self.cursor.y):
                self.select = self.uikeys[i]
                if keystr != "" and ui.roundui[keystr]:
                    self.select = ui.roundui[keystr].name
                    self.equiptype = 0
                    if ui.roundui[keystr].type == GameUI.TYPE_CHECKBOX:
                        self.cursor.x = ui.roundui[keystr].check_bounds.x
                        self.cursor.y = ui.roundui[keystr].check_bounds.y
                    else:
                        self.cursor.x = ui.roundui[keystr].bounds.x
                        self.cursor.y = ui.roundui[keystr].bounds.y
                    break
            #---mouse, touch operation
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                #print(f"mouse {pyxel.mouse_x}:{pyxel.mouse_y} => ui {self.select}vs{self.uikeys[i]} {ui.bounds.x}:{ui.bounds.y}")
                
                if ui.check_touch_area(pyxel.mouse_x, pyxel.mouse_y):
                    if self.select == self.uikeys[i]:
                        #---already select same
                        self.check_and_config()
                    else:
                        self.cursor.x = ui.bounds.x
                        self.cursor.y = ui.bounds.y
                        self.equiptype = 0
                    self.select = self.uikeys[i]
                    self.select = ui.name
                    
                    break"""
        uoc = self.ui_operation_check(keystr)
        if uoc["mouse"]:
            self.check_and_config()
        elif uoc["mouse_already"]:
            self.check_and_config()
        
        #---Change equip type
        if self.keyman.is_thirdaction():  #pyxel.btnp(pyxel.KEY_E) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B):
            if (
                (self.select == "img_dd") or #---DD
                (self.select == "img_cl") or #---CL
                (self.select == "img_cvl") or   #---CVL
                (self.select == "img_cv")    #---CV
            ):
                self.parent.sound.play_change_action()
                self.equiptype += 1
                if self.equiptype > 2:
                    self.equiptype = 0
                    
                #self.setup_selectjob(CSV_PLAYABLE[self.select].jobtype)
            else:
                self.parent.sound.play_disable()
            
        
        #---decide selection
        if self.keyman.is_enter():
            self.decide_select()
        
        if self.keyman.is_cancel():
            self.select = "return"
            self.check_and_config()
        
        if pyxel.frame_count % 30 == 0:
            self.cur_motionskey = pyxel.rndi(0, 6)
    
        #---other update
        if self.select != "return":
            self.setup_selectjob(CSV_PLAYABLE[self.select].jobtype)
            self.ui["sel_charaname"].set_text(CSV_PLAYABLE[self.select].title)
        
        for u in self.ui:
            self.ui[u].update()
        
    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)
        
        #---big preview
        if self.select != "return":
            pyxel.blt(pos(3), pos(4), 
                    0, 
                    CSV_PLAYABLE[self.select].image_x, #CHARA_TOPIMAGE_LIST[self.select.y][self.select.x][0],
                    PLAYER_MOTION[self.motionkeys[self.cur_motionskey]], 
                    16, 16, scale=2.0
            )
            pyxel.blt(pos(10), pos(3), 
                    0, 
                    CSV_PLAYABLE[self.select].image_x, #CHARA_TOPIMAGE_LIST[self.select.y][self.select.x][0],
                    PLAYER_MOTION[self.motionkeys[7]], 
                    16, 32, scale=2.0
            )


        for u in self.ui:
            self.ui[u].draw()
        
        # return button
        #pyxel.blt(pos(0)+4, pos(0)+4, 0, 0, 72, 8, 8, pyxel.COLOR_BLACK)
        
        # select image
        #---new image
        """sca = 1
        
        ln1x = SELDOTIMG_SIZE
        ln1y = 4+SHOW_CURSOR_POS_Y
        pyxel.blt(ln1x, ln1y, 0, 32, 48, SELDOTIMG_SIZE, SELDOTIMG_SIZE,scale=sca)
        ln1x += SELDOTIMG_SIZE + SELDOTIMG_SIZE/2
        pyxel.blt(ln1x, ln1y, 0, 48, 48, SELDOTIMG_SIZE, SELDOTIMG_SIZE,scale=sca)
        ln1x += SELDOTIMG_SIZE + SELDOTIMG_SIZE/2
        pyxel.blt(ln1x, ln1y, 0, 64, 48, SELDOTIMG_SIZE, SELDOTIMG_SIZE,scale=sca)
        ln1x += SELDOTIMG_SIZE + SELDOTIMG_SIZE/2
        pyxel.blt(ln1x, ln1y, 0, 80, 48, SELDOTIMG_SIZE, SELDOTIMG_SIZE,scale=sca)
        ln1x = SELDOTIMG_SIZE
        ln1y = pos(3)+4+SHOW_CURSOR_POS_Y
        pyxel.blt(ln1x, ln1y, 0, 96, 48, SELDOTIMG_SIZE, SELDOTIMG_SIZE,scale=sca)
        ln1x += SELDOTIMG_SIZE + SELDOTIMG_SIZE/2
        pyxel.blt(ln1x, ln1y, 0, 112, 48, SELDOTIMG_SIZE, SELDOTIMG_SIZE,scale=sca)
        ln1x += SELDOTIMG_SIZE + SELDOTIMG_SIZE/2
        pyxel.blt(ln1x, ln1y, 0, 128, 48, SELDOTIMG_SIZE, SELDOTIMG_SIZE,scale=sca)
        ln1x += SELDOTIMG_SIZE + SELDOTIMG_SIZE/2
        pyxel.blt(ln1x, ln1y, 0, 144, 48, SELDOTIMG_SIZE, SELDOTIMG_SIZE,scale=sca)"""
        #if self.parent.is_test:
        #    pyxel.rect(2, pos(6), 56, 10, pyxel.COLOR_BROWN)
        #    pyxel.rect(62, pos(6), 56, 10, pyxel.COLOR_BROWN)
        #    pyxel.rect(2, pos(14), 56, 10, pyxel.COLOR_BROWN)
        #    pyxel.rect(62, pos(14), 56, 10, pyxel.COLOR_BROWN)
        
        
        #---Name
        #pyxel.text(pos(2)+1, pos(0.5), CHARALIST[self.select.y][self.select.x][0], pyxel.COLOR_WHITE, self.parent.jp_font10)
        #pyxel.text(pos(2), pos(0.5), CHARALIST[self.select.y][self.select.x][0], pyxel.COLOR_RED, self.parent.jp_font10)

        #---cursor
        if self.select == "return":
            draw_select_cursor(self.cursor, 8, 8, -2, -2)
        else:
            draw_select_cursor(self.cursor, 16, 16, -2, -2)
        """
        if pyxel.frame_count % 15 == 0:
            pyxel.dither(0.5)
        elif pyxel.frame_count % 30 == 0:
            pyxel.dither(0.7)
        #---top
        pyxel.blt(self.cursor.x, self.cursor.y, 0, 0, 80, 2, 2, pyxel.COLOR_BLACK)
        pyxel.blt(self.cursor.x+2, self.cursor.y, 0, CIP.top.x, CIP.top.y, 10, 2, pyxel.COLOR_BLACK)
        pyxel.blt(self.cursor.x+2+10, self.cursor.y, 0, CIP.top.x, CIP.top.y, 10, 2, pyxel.COLOR_BLACK)
        pyxel.blt(self.cursor.x+2+20, self.cursor.y, 0, 14, 80, 2, 2, pyxel.COLOR_BLACK)
        #---left
        pyxel.blt(self.cursor.x, self.cursor.y+2, 0, CIP.left.x, CIP.left.y, 2, 10, pyxel.COLOR_BLACK)
        pyxel.blt(self.cursor.x, self.cursor.y+2+10, 0, CIP.left.x, CIP.left.y, 2, 10, pyxel.COLOR_BLACK)
        pyxel.blt(self.cursor.x, self.cursor.y+2+20, 0, 0, 94, 2, 2, pyxel.COLOR_BLACK)
        #---bottom
        bottom_y = self.cursor.y+2+20
        pyxel.blt(self.cursor.x+2, bottom_y, 0, CIP.bottom.x, CIP.bottom.y, 10, 2, pyxel.COLOR_BLACK)
        pyxel.blt(self.cursor.x+2+10, bottom_y, 0, CIP.bottom.x, CIP.bottom.y, 10, 2, pyxel.COLOR_BLACK)
        pyxel.blt(self.cursor.x+2+20, bottom_y, 0, 14, 94, 2, 2, pyxel.COLOR_BLACK)
        #---right
        right_x = self.cursor.x+2+20
        pyxel.blt(right_x, self.cursor.y+2, 0, CIP.right.x, CIP.right.y, 2, 10, pyxel.COLOR_BLACK)
        pyxel.blt(right_x, self.cursor.y+2+10, 0, CIP.right.x, CIP.right.y, 2, 10, pyxel.COLOR_BLACK)
        pyxel.blt(right_x, self.cursor.y+2+20, 0, 14, 94, 2, 2, pyxel.COLOR_BLACK)
        
        pyxel.dither(1.0)"""
        
        #---explain a weapon
        mainpos = (pos(1), pos(4))
        subpos = (pos(8), pos(11))
        mainimgposy = pos(18)
        #---new code
        if self.tempjob.commands[0].type == AttackCommand.TYPE_BBGUN:
            mainimgposy = pos(17)
        pyxel.text(pos(1),pos(18),"Main:",pyxel.COLOR_WHITE)
        pyxel.blt(pos(4),mainimgposy,self.tempjob.commands[0].img_page, 
                  self.tempjob.commands[0].img_bnd.x, self.tempjob.commands[0].img_bnd.y, self.tempjob.commands[0].img_bnd.w, self.tempjob.commands[0].img_bnd.h,
                  pyxel.COLOR_BLACK
        )
        pyxel.text(pos(5),pos(18),f"x {self.tempjob.commands[0].max_count}",pyxel.COLOR_WHITE)
        pyxel.text(subpos[0],pos(18),"Sub:",pyxel.COLOR_WHITE)
        pyxel.blt(subpos[1],pos(18),self.tempjob.commands[1].img_page, 
                  self.tempjob.commands[1].img_bnd.x, self.tempjob.commands[1].img_bnd.y, self.tempjob.commands[1].img_bnd.w, self.tempjob.commands[1].img_bnd.h,
                  pyxel.COLOR_BLACK
        )
        pyxel.text(subpos[1]+pos(1),pos(18),f"x {self.tempjob.commands[1].max_count}",pyxel.COLOR_WHITE)
        
        """if self.select == "img_ss": #---SS
            pyxel.text(pos(1),pos(18),"Main:",pyxel.COLOR_WHITE)
            pyxel.blt(pos(4),pos(18),0, WEAPON_IMAGES["TORPEDO"][0],WEAPON_IMAGES["TORPEDO"][1], 8,8, pyxel.COLOR_BLACK)
            pyxel.blt(pos(5),pos(18),0, WEAPON_IMAGES["TORPEDO"][0],WEAPON_IMAGES["TORPEDO"][1], 8,8, pyxel.COLOR_BLACK)
            pyxel.text(subpos[0],pos(18),"Sub:",pyxel.COLOR_WHITE)
            pyxel.blt(subpos[1],pos(18),0, WEAPON_IMAGES["TORPEDO"][0],WEAPON_IMAGES["TORPEDO"][1], 8,8, pyxel.COLOR_BLACK)
            pyxel.blt(subpos[1]+pos(1),pos(18),0, WEAPON_IMAGES["TORPEDO"][0],WEAPON_IMAGES["TORPEDO"][1], 8,8, pyxel.COLOR_BLACK)
        elif self.select == "img_dd": #---DD
            pyxel.text(pos(1),pos(18),"Main:",pyxel.COLOR_WHITE)
            pyxel.blt(pos(4),pos(18),0, WEAPON_IMAGES["TORPEDO"][0],WEAPON_IMAGES["TORPEDO"][1], 8,8, pyxel.COLOR_BLACK)
            pyxel.blt(pos(5),pos(18),0, WEAPON_IMAGES["TORPEDO"][0],WEAPON_IMAGES["TORPEDO"][1], 8,8, pyxel.COLOR_BLACK)
            pyxel.text(subpos[0],pos(18),"Sub:",pyxel.COLOR_WHITE)
            if self.equiptype == 0:
                pyxel.blt(subpos[1],pos(17),0, WEAPON_IMAGES["AASHOOT"][0],WEAPON_IMAGES["AASHOOT"][1], 8,8, pyxel.COLOR_BLACK)
                pyxel.blt(subpos[1]+4,pos(17),0, WEAPON_IMAGES["AASHOOT"][0],WEAPON_IMAGES["AASHOOT"][1], 8,8, pyxel.COLOR_BLACK)
                pyxel.blt(subpos[1]+8,pos(17),0, WEAPON_IMAGES["AASHOOT"][0],WEAPON_IMAGES["AASHOOT"][1], 8,8, pyxel.COLOR_BLACK)
                pyxel.blt(subpos[1],pos(18),0, WEAPON_IMAGES["AASHOOT"][0],WEAPON_IMAGES["AASHOOT"][1], 8,8, pyxel.COLOR_BLACK)
                pyxel.blt(subpos[1]+4,pos(18),0, WEAPON_IMAGES["AASHOOT"][0],WEAPON_IMAGES["AASHOOT"][1], 8,8, pyxel.COLOR_BLACK)
            else:
                pyxel.blt(subpos[1],pos(18),0, WEAPON_IMAGES["DEPTHCHARGE"][0],WEAPON_IMAGES["DEPTHCHARGE"][1], 8,8, pyxel.COLOR_BLACK)
                pyxel.blt(subpos[1]+8,pos(18),0, WEAPON_IMAGES["DEPTHCHARGE"][0],WEAPON_IMAGES["DEPTHCHARGE"][1], 8,8, pyxel.COLOR_BLACK)
        if self.select == "img_asdg": #---ASDG
            pyxel.text(pos(1),pos(18),"Main:",pyxel.COLOR_WHITE)
            pyxel.blt(pos(4),pos(18),0, WEAPON_IMAGES["MISSILE"][0],WEAPON_IMAGES["MISSILE"][1], 8,8, pyxel.COLOR_BLACK)
            pyxel.text(subpos[0],pos(18),"Sub:",pyxel.COLOR_WHITE)
            pyxel.blt(subpos[1],pos(17),0, WEAPON_IMAGES["AASHOOT"][0],WEAPON_IMAGES["AASHOOT"][1], 8,8, pyxel.COLOR_BLACK)
            pyxel.blt(subpos[1]+4,pos(17),0, WEAPON_IMAGES["AASHOOT"][0],WEAPON_IMAGES["AASHOOT"][1], 8,8, pyxel.COLOR_BLACK)
            pyxel.blt(subpos[1]+8,pos(17),0, WEAPON_IMAGES["AASHOOT"][0],WEAPON_IMAGES["AASHOOT"][1], 8,8, pyxel.COLOR_BLACK)
            pyxel.blt(subpos[1],pos(18),0, WEAPON_IMAGES["AASHOOT"][0],WEAPON_IMAGES["AASHOOT"][1], 8,8, pyxel.COLOR_BLACK)
            pyxel.blt(subpos[1]+4,pos(18),0, WEAPON_IMAGES["AASHOOT"][0],WEAPON_IMAGES["AASHOOT"][1], 8,8, pyxel.COLOR_BLACK)
        elif self.select == "img_cl": #---CL
            pyxel.text(pos(1),pos(18),"Main:",pyxel.COLOR_WHITE)
            pyxel.blt(pos(4),pos(18),0, WEAPON_IMAGES["GUN"][0],WEAPON_IMAGES["GUN"][1], 8,8, pyxel.COLOR_BLACK)
            pyxel.blt(pos(5),pos(18),0, WEAPON_IMAGES["GUN"][0],WEAPON_IMAGES["GUN"][1], 8,8, pyxel.COLOR_BLACK)
            pyxel.blt(pos(6),pos(18),0, WEAPON_IMAGES["GUN"][0],WEAPON_IMAGES["GUN"][1], 8,8, pyxel.COLOR_BLACK)
            pyxel.text(subpos[0],pos(18),"Sub:",pyxel.COLOR_WHITE)
            if self.equiptype == 0:
                pyxel.blt(subpos[1],pos(17),0, WEAPON_IMAGES["AASHOOT"][0],WEAPON_IMAGES["AASHOOT"][1], 8,8, pyxel.COLOR_BLACK)
                pyxel.blt(subpos[1]+4,pos(17),0, WEAPON_IMAGES["AASHOOT"][0],WEAPON_IMAGES["AASHOOT"][1], 8,8, pyxel.COLOR_BLACK)
                pyxel.blt(subpos[1]+8,pos(17),0, WEAPON_IMAGES["AASHOOT"][0],WEAPON_IMAGES["AASHOOT"][1], 8,8, pyxel.COLOR_BLACK)
                pyxel.blt(subpos[1],pos(18),0, WEAPON_IMAGES["AASHOOT"][0],WEAPON_IMAGES["AASHOOT"][1], 8,8, pyxel.COLOR_BLACK)
                pyxel.blt(subpos[1]+4,pos(18),0, WEAPON_IMAGES["AASHOOT"][0],WEAPON_IMAGES["AASHOOT"][1], 8,8, pyxel.COLOR_BLACK)
            else:
                pyxel.blt(subpos[1],pos(18),0, WEAPON_IMAGES["DEPTHCHARGE"][0],WEAPON_IMAGES["DEPTHCHARGE"][1], 8,8, pyxel.COLOR_BLACK)
                pyxel.blt(subpos[1]+8,pos(18),0, WEAPON_IMAGES["DEPTHCHARGE"][0],WEAPON_IMAGES["DEPTHCHARGE"][1], 8,8, pyxel.COLOR_BLACK)
        elif self.select == "img_ca": #---CA
            pyxel.text(pos(1),pos(18),"Main:",pyxel.COLOR_WHITE)
            pyxel.blt(pos(4),pos(17),0, WEAPON_IMAGES["GUN"][0],WEAPON_IMAGES["GUN"][1], 8,8, pyxel.COLOR_BLACK)
            pyxel.blt(pos(5),pos(17),0, WEAPON_IMAGES["GUN"][0],WEAPON_IMAGES["GUN"][1], 8,8, pyxel.COLOR_BLACK)
            pyxel.blt(pos(4),pos(18),0, WEAPON_IMAGES["GUN"][0],WEAPON_IMAGES["GUN"][1], 8,8, pyxel.COLOR_BLACK)
            pyxel.blt(pos(5),pos(18),0, WEAPON_IMAGES["GUN"][0],WEAPON_IMAGES["GUN"][1], 8,8, pyxel.COLOR_BLACK)
            pyxel.text(subpos[0],pos(18),"Sub:",pyxel.COLOR_WHITE)
            pyxel.blt(subpos[1],pos(17),0, WEAPON_IMAGES["AASHOOT"][0],WEAPON_IMAGES["AASHOOT"][1], 8,8, pyxel.COLOR_BLACK)
            pyxel.blt(subpos[1]+4,pos(17),0, WEAPON_IMAGES["AASHOOT"][0],WEAPON_IMAGES["AASHOOT"][1], 8,8, pyxel.COLOR_BLACK)
            pyxel.blt(subpos[1]+8,pos(17),0, WEAPON_IMAGES["AASHOOT"][0],WEAPON_IMAGES["AASHOOT"][1], 8,8, pyxel.COLOR_BLACK)
            pyxel.blt(subpos[1],pos(18),0, WEAPON_IMAGES["AASHOOT"][0],WEAPON_IMAGES["AASHOOT"][1], 8,8, pyxel.COLOR_BLACK)
            pyxel.blt(subpos[1]+4,pos(18),0, WEAPON_IMAGES["AASHOOT"][0],WEAPON_IMAGES["AASHOOT"][1], 8,8, pyxel.COLOR_BLACK)
        elif self.select == "img_cvl": #---CVL
            pyxel.text(pos(1),pos(18),"Main:",pyxel.COLOR_WHITE)
            pyxel.blt(pos(4),pos(18),0, WEAPON_IMAGES["AIRCRAFT"][0],WEAPON_IMAGES["AIRCRAFT"][1], 8,8, pyxel.COLOR_BLACK)
            pyxel.blt(pos(5),pos(18),0, WEAPON_IMAGES["AIRCRAFT"][0],WEAPON_IMAGES["AIRCRAFT"][1], 8,8, pyxel.COLOR_BLACK)            
            pyxel.text(subpos[0],pos(18),"Sub:",pyxel.COLOR_WHITE)
            if self.equiptype == 0:
                pyxel.blt(subpos[1],pos(17),0, WEAPON_IMAGES["AASHOOT"][0],WEAPON_IMAGES["AASHOOT"][1], 8,8, pyxel.COLOR_BLACK)
                pyxel.blt(subpos[1]+4,pos(17),0, WEAPON_IMAGES["AASHOOT"][0],WEAPON_IMAGES["AASHOOT"][1], 8,8, pyxel.COLOR_BLACK)
                pyxel.blt(subpos[1]+8,pos(17),0, WEAPON_IMAGES["AASHOOT"][0],WEAPON_IMAGES["AASHOOT"][1], 8,8, pyxel.COLOR_BLACK)
                pyxel.blt(subpos[1],pos(18),0, WEAPON_IMAGES["AASHOOT"][0],WEAPON_IMAGES["AASHOOT"][1], 8,8, pyxel.COLOR_BLACK)
                pyxel.blt(subpos[1]+4,pos(18),0, WEAPON_IMAGES["AASHOOT"][0],WEAPON_IMAGES["AASHOOT"][1], 8,8, pyxel.COLOR_BLACK)
                
            else:
                pyxel.blt(subpos[1],pos(18),0, WEAPON_IMAGES["DEPTHCHARGE"][0],WEAPON_IMAGES["DEPTHCHARGE"][1], 8,8, pyxel.COLOR_BLACK)
                pyxel.blt(subpos[1]+8,pos(18),0, WEAPON_IMAGES["DEPTHCHARGE"][0],WEAPON_IMAGES["DEPTHCHARGE"][1], 8,8, pyxel.COLOR_BLACK)
        elif self.select == "img_cv": #---CV
            pyxel.text(pos(1),pos(18),"Main:",pyxel.COLOR_WHITE)
            pyxel.blt(pos(4),pos(18),0, WEAPON_IMAGES["AIRCRAFT"][0],WEAPON_IMAGES["AIRCRAFT"][1], 8,8, pyxel.COLOR_BLACK)
            pyxel.blt(pos(5),pos(18),0, WEAPON_IMAGES["AIRCRAFT"][0],WEAPON_IMAGES["AIRCRAFT"][1], 8,8, pyxel.COLOR_BLACK)
            pyxel.blt(pos(6),pos(18),0, WEAPON_IMAGES["AIRCRAFT"][0],WEAPON_IMAGES["AIRCRAFT"][1], 8,8, pyxel.COLOR_BLACK)
            pyxel.text(subpos[0],pos(18),"Sub:",pyxel.COLOR_WHITE)
            pyxel.blt(subpos[1],pos(17),0, WEAPON_IMAGES["AASHOOT"][0],WEAPON_IMAGES["AASHOOT"][1], 8,8, pyxel.COLOR_BLACK)
            pyxel.blt(subpos[1]+4,pos(17),0, WEAPON_IMAGES["AASHOOT"][0],WEAPON_IMAGES["AASHOOT"][1], 8,8, pyxel.COLOR_BLACK)
            pyxel.blt(subpos[1]+8,pos(17),0, WEAPON_IMAGES["AASHOOT"][0],WEAPON_IMAGES["AASHOOT"][1], 8,8, pyxel.COLOR_BLACK)
            pyxel.blt(subpos[1],pos(18),0, WEAPON_IMAGES["AASHOOT"][0],WEAPON_IMAGES["AASHOOT"][1], 8,8, pyxel.COLOR_BLACK)
            pyxel.blt(subpos[1]+4,pos(18),0, WEAPON_IMAGES["AASHOOT"][0],WEAPON_IMAGES["AASHOOT"][1], 8,8, pyxel.COLOR_BLACK)
        elif self.select == "img_bc": #---BC,BB
            pyxel.text(pos(1),pos(18),"Main:",pyxel.COLOR_WHITE)
            pyxel.blt(pos(4),pos(17)+4,0, WEAPON_IMAGES["BBGUN"][0],WEAPON_IMAGES["BBGUN"][1], 8,16, pyxel.COLOR_BLACK)
            pyxel.text(subpos[0],pos(18),"Sub:",pyxel.COLOR_WHITE)
            pyxel.blt(subpos[1],pos(17),0, WEAPON_IMAGES["AASHOOT"][0],WEAPON_IMAGES["AASHOOT"][1], 8,8, pyxel.COLOR_BLACK)
            pyxel.blt(subpos[1]+4,pos(17),0, WEAPON_IMAGES["AASHOOT"][0],WEAPON_IMAGES["AASHOOT"][1], 8,8, pyxel.COLOR_BLACK)
            pyxel.blt(subpos[1]+8,pos(17),0, WEAPON_IMAGES["AASHOOT"][0],WEAPON_IMAGES["AASHOOT"][1], 8,8, pyxel.COLOR_BLACK)
            pyxel.blt(subpos[1],pos(18),0, WEAPON_IMAGES["AASHOOT"][0],WEAPON_IMAGES["AASHOOT"][1], 8,8, pyxel.COLOR_BLACK)
            pyxel.blt(subpos[1]+4,pos(18),0, WEAPON_IMAGES["AASHOOT"][0],WEAPON_IMAGES["AASHOOT"][1], 8,8, pyxel.COLOR_BLACK)"""