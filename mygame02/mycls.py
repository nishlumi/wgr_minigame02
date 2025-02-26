import pyxel
import copy
from appconst import PLAYER_MOTION, ShipKind, CSV_ATTACKWEAK, CIP
from imgbnk import IBNK, BankImageElement
from myconfig import GameOperator

def pos(x):
    return 8 * x

def center_x():
    return pyxel.width // 2

def center_y():
    return pyxel.height // 2

def check_mouse_playscreen(offset_x = 0, offset_y = 0):
        return (0 <= pyxel.mouse_x <= pyxel.width - offset_x) and (0 <= pyxel.mouse_y <= pyxel.height - offset_y)

def check_object_playscreen(x, y, offset_x = 0, offset_y = 0):
        return (0 <= x <= pyxel.width - offset_x) and (0 <= y <= pyxel.height - offset_y)


def check_touch_area(startx:int, starty:int, endx:int, endy:int):
    return (
        (startx <= pyxel.mouse_x <= endx)
        and
        (starty <= pyxel.mouse_y <= endy)
    )
        
def calc_collision(myleft, myright, mytop, mybottom, moveleft, moveright, movetop, movebottom):
    if myleft > moveright:
        return False
    if myright < moveleft:
        return False
    if mytop > movebottom:
        return False
    if mybottom < movetop:
        return False
    return True
    
def draw_select_cursor(cursor, cursor10w, cursor10h, offset_x = 0, offset_y = 0):
    curcur_x = cursor.x + offset_x
    curcur_y = cursor.y + offset_y
    #---top
    top_x = 0
    left_y = 0
    bottom_y = curcur_y+2+ 1*cursor10h
    right_x = curcur_x+2+ 1*cursor10w
    
    pyxel.blt(curcur_x, curcur_y, 0, 0, 80, 2, 2, pyxel.COLOR_BLACK)
    for i in range(0, cursor10w):
        pyxel.blt(curcur_x+2+top_x, curcur_y, 0, CIP.top.x, CIP.top.y, 1, 2, pyxel.COLOR_BLACK)
        top_x += 1
        #pyxel.blt(curcur_x+2+10, curcur_y, 0, CIP.top.x, CIP.top.y, 10, 2, pyxel.COLOR_BLACK)
    pyxel.blt(curcur_x+2+top_x, curcur_y, 0, 14, 80, 2, 2, pyxel.COLOR_BLACK)
    #---left
    for i in range(0, cursor10h):
        pyxel.blt(curcur_x, curcur_y+2+left_y, 0, CIP.left.x, CIP.left.y, 2, 1, pyxel.COLOR_BLACK)
        left_y += 1
        #pyxel.blt(curcur_x, curcur_y+2+10, 0, CIP.left.x, CIP.left.y, 2, 10, pyxel.COLOR_BLACK)
    pyxel.blt(curcur_x, curcur_y+2+left_y, 0, 0, 94, 2, 2, pyxel.COLOR_BLACK)
    #---bottom
    bottom_x = 0
    for i in range(0, cursor10w):
        pyxel.blt(curcur_x+2+bottom_x, bottom_y, 0, CIP.bottom.x, CIP.bottom.y, 1, 2, pyxel.COLOR_BLACK)
        bottom_x += 1
        #pyxel.blt(curcur_x+2+10, bottom_y, 0, CIP.bottom.x, CIP.bottom.y, 10, 2, pyxel.COLOR_BLACK)
    pyxel.blt(right_x, bottom_y, 0, 14, 94, 2, 2, pyxel.COLOR_BLACK)
    #---right
    right_y = 0
    for i in range(0, cursor10h):
        pyxel.blt(right_x, curcur_y+2+right_y, 0, CIP.right.x, CIP.right.y, 2, 1, pyxel.COLOR_BLACK)
        right_y += 1
        #pyxel.blt(right_x, curcur_y+2+10, 0, CIP.right.x, CIP.right.y, 2, 10, pyxel.COLOR_BLACK)
    #pyxel.blt(right_x, curcur_y+2+20, 0, 14, 94, 2, 2, pyxel.COLOR_BLACK)
    
class GamePoint:
    RANK_C = 0
    RANK_B = 1
    RANK_A = 2
    RANK_S = 3
    LV1 = 0
    LV2 = 1
    LV3 = 2
    CNT_CUR = 0
    CNT_MAX = 1
    class ClassPoint:
        def __init__(self, job):
            self.job = job
            self.clear()
        
        def clear(self):
            self.cur = [
                [0, 0, 0], #---normal
                [0, 0, 0], #---enhanced
                [0, 0, 0], #---super
                [0, 0, 0]  #---boss
            ]
            self.max = [
                [0, 0, 0], #---normal
                [0, 0, 0], #---enhanced
                [0, 0, 0], #---super
                [0, 0, 0]  #---boss
            ]
        
        def add_max(self, classtype, lv, val):
            self.max[classtype][lv] += val
        
        def add_cur(self, classtype, lv, val):
            self.cur[classtype][lv] += val
        
        def summary_cur(self, classtype = 0):
            ret = 0
            for c in self.cur[classtype]:
                ret += c
            return ret
        
        def summary_max(self, classtype = 0):
            ret = 0
            for c in self.max[classtype]:
                ret += c
            return ret

    def __init__(self):
        self.clear()

    def clear(self):
        self.summary = 0
        self.eachtype = [
            #Lv.1    2       3
            #  defeat count, all count
            self.ClassPoint(ShipKind.TYPE_SS), #---0: SS
            self.ClassPoint(ShipKind.TYPE_DD), #---1: DD
            self.ClassPoint(ShipKind.TYPE_ASDG), #---2: ASDG
            self.ClassPoint(ShipKind.TYPE_CL), #---3: CL
            self.ClassPoint(ShipKind.TYPE_CA), #---4: CA
            self.ClassPoint(ShipKind.TYPE_CVL), #---5: CVL
            self.ClassPoint(ShipKind.TYPE_CV), #---6: CV
            self.ClassPoint(ShipKind.TYPE_BC), #---7: BC
            self.ClassPoint(ShipKind.TYPE_BC), #---8: BB
        ]
    
    def judgement(self):
        CLSN = 0
        CLSE = 1
        CLSS = 2
        rank = self.RANK_C
        appear_kind_cnt = 0
        resultlist = []
        #---SS
        eachcls = self.eachtype[ShipKind.TYPE_SS]
        ssnresult = 0
        if eachcls.summary_max(CLSN) > 0:
            appear_kind_cnt += 1
            ssnresult = eachcls.summary_cur(CLSN) / eachcls.summary_max(CLSN)
            resultlist.append(ssnresult)
        #---DD
        eachcls = self.eachtype[ShipKind.TYPE_DD]
        ddnresult = 0
        dderesult = 0
        if eachcls.summary_max(CLSN) > 0:
            appear_kind_cnt += 1
            ddnresult = eachcls.summary_cur(CLSN) / eachcls.summary_max(CLSN)
            resultlist.append(ddnresult)
        if eachcls.summary_max(CLSE) > 0:
            appear_kind_cnt += 1
            dderesult = eachcls.summary_cur(CLSE) / eachcls.summary_max(CLSE)
            resultlist.append(dderesult)
        #---CL
        eachcls = self.eachtype[ShipKind.TYPE_CL]
        clnresult = 0
        if eachcls.summary_max(CLSN) > 0:
            appear_kind_cnt += 1
            clnresult = eachcls.summary_cur(CLSN) / eachcls.summary_max(CLSN)
            resultlist.append(clnresult)
        #---CA
        eachcls = self.eachtype[ShipKind.TYPE_CA]
        canresult = 0
        if eachcls.summary_max(CLSN) > 0:
            appear_kind_cnt += 1
            canresult = eachcls.summary_cur(CLSN) / eachcls.summary_max(CLSN)
            resultlist.append(canresult)
        #---CVL
        eachcls = self.eachtype[ShipKind.TYPE_CVL]
        cvlnresult = 0
        if eachcls.summary_max(CLSN) > 0:
            appear_kind_cnt += 1
            cvlnresult = eachcls.summary_cur(CLSN) / eachcls.summary_max(CLSN)
            resultlist.append(cvlnresult)
        #---CVL
        eachcls = self.eachtype[ShipKind.TYPE_CV]
        cvnresult = 0
        if eachcls.summary_max(CLSN) > 0:
            appear_kind_cnt += 1
            cvnresult = eachcls.summary_cur(CLSN) / eachcls.summary_max(CLSN)
            resultlist.append(cvnresult)
        #---BC
        eachcls = self.eachtype[ShipKind.TYPE_BC]
        bcnresult = 0
        if eachcls.summary_max(CLSN) > 0:
            appear_kind_cnt += 1
            bcnresult = eachcls.summary_cur(CLSN) / eachcls.summary_max(CLSN)
            resultlist.append(bcnresult)
        #---BB
        eachcls = self.eachtype[ShipKind.TYPE_BB]
        bbnresult = 0
        if eachcls.summary_max(CLSN) > 0:
            appear_kind_cnt += 1
            bbnresult = eachcls.summary_cur(CLSN) / eachcls.summary_max(CLSN)
            resultlist.append(bbnresult)
        
        #---judge
        b_cnt = 0
        a_cnt = 0
        s_cnt = 0
        for res in resultlist:
            #---defeat count of each class
            if res >= 0.5:
                b_cnt += 1
            if res >= 0.7:
                a_cnt += 1
            if res >= 0.9:
                s_cnt += 1
        #---defeat rate of all class
        if b_cnt / appear_kind_cnt >= 0.5:
            rank = self.RANK_B
        if a_cnt / appear_kind_cnt >= 0.8:
            rank = self.RANK_A
        if s_cnt / appear_kind_cnt >= 0.9:
            rank = self.RANK_S
        
        return rank

        
class GameObject:
    def __init__(self, app: GameOperator, x, y):
        self.parent: GameOperator = app
        self.x = x
        self.y = y
        self.w = 8
        self.h = 8
        self.dir = Vector2(0, 0)
        self.movespeed = 1
        self.img_page = 0
        self.img_bnd = Bounds(0, 0, 0, 0)
        self.img_transparent = pyxel.COLOR_BLACK
        self.is_halftransparency = False
        self.during_transparency = 10
        self.start_transparency = 0
        #---aliving time
        self.alive_time = 0
        self.cur_alive_time_diff = pyxel.frame_count
        
        self.will_destroy = False
    
    def update(self):
        pass

    def draw(self):
        pass
    
    def check_collision(self, target, offset_x = 0, offset_y = 0):
        return (abs(target.x - self.x) < (self.w - offset_x) and abs(target.y - self.y) < (self.h - offset_y))

class KeyManager:
    def __init__(self):
        pass

    def _basic_judge(self, keys: list, pressing: bool = False):
        ishit = False
        for k in keys:
            if pressing:
                if pyxel.btn(k):
                    if (pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT) or pyxel.btn(pyxel.MOUSE_BUTTON_MIDDLE)) and check_mouse_playscreen(offset_y=16):
                        ishit = True
                    else:
                        ishit = True
            else:
                if pyxel.btnp(k):
                    if (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT) or pyxel.btnp(pyxel.MOUSE_BUTTON_MIDDLE)) and check_mouse_playscreen(offset_y=16):
                        ishit = True
                    else:
                        ishit = True
        return ishit
    def is_enter(self):
        return self._basic_judge([pyxel.KEY_RETURN,pyxel.KEY_F, pyxel.KEY_SPACE,pyxel.KEY_KP_1,pyxel.GAMEPAD1_BUTTON_A])
    
    def is_cancel(self):
        return self._basic_judge([pyxel.KEY_G,pyxel.KEY_KP_2,pyxel.GAMEPAD1_BUTTON_B])
    
    def is_left(self):
        return self._basic_judge([pyxel.KEY_LEFT, pyxel.KEY_A, pyxel.GAMEPAD1_BUTTON_DPAD_LEFT])
    
    def is_right(self):
        return self._basic_judge([pyxel.KEY_RIGHT, pyxel.KEY_D, pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT])
    
    def is_up(self):
        return self._basic_judge([pyxel.KEY_UP, pyxel.KEY_W, pyxel.GAMEPAD1_BUTTON_DPAD_UP])
    
    def is_down(self):
        return self._basic_judge([pyxel.KEY_DOWN, pyxel.KEY_S, pyxel.GAMEPAD1_BUTTON_DPAD_DOWN])

    def is_mainaction(self, pressing: bool = False):
        keys = [
            pyxel.KEY_E,pyxel.KEY_KP_1,
            pyxel.MOUSE_BUTTON_LEFT,pyxel.GAMEPAD1_BUTTON_A
        ]
        return self._basic_judge(keys, pressing)
    
    def is_subaction(self, pressing: bool = False):
        keys = [
            pyxel.KEY_G,pyxel.KEY_KP_2,
            pyxel.MOUSE_BUTTON_RIGHT,pyxel.GAMEPAD1_BUTTON_B
        ]
        return self._basic_judge(keys, pressing)

    def is_thirdaction(self, pressing: bool = False):
        keys = [pyxel.KEY_R, pyxel.KEY_KP_4, pyxel.GAMEPAD1_BUTTON_X, pyxel.MOUSE_BUTTON_MIDDLE]
        return self._basic_judge(keys,pressing)
    
    def is_fourthaction(self, pressing: bool = False):
        keys = [pyxel.KEY_T, pyxel.KEY_KP_5, pyxel.GAMEPAD1_BUTTON_Y]
        return self._basic_judge(keys,pressing)

    def is_startpose(self, pressing: bool = False):
        keys = [pyxel.KEY_P, pyxel.GAMEPAD1_BUTTON_START]
        return self._basic_judge(keys,pressing)
    
class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Bounds:
    def __init__(self, x, y = 0, w = 0, h = 0):
        if type(x) == BankImageElement:
            self.x = x.x
            self.y = x.y
            self.w = x.w
            self.h = x.h
        else:
            self.x = x
            self.y = y
            self.w = w
            self.h = h
        
    
class EffectiveArea:
    def __init__(self):
        self.clear_dir()
        
        self.frequency = 0
    
    def clear_dir(self):
        self.front = False
        self.left = False
        self.right = False
        self.back = False
        self.center = True
        
        self.front_left = False
        self.front_right = False
        self.back_left = False
        self.back_right = False
    

class BaseEffect:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 8
        self.h = 8
        self.img_page = 0
        self.img_bnd = Bounds(0, 0, 8, 8)
        self.is_explode = False
        self.during_explode = 15
        self.start_explode = 0
        self.motioninx = 0
        self.motionlst = []
    
    def update(self):
        pass

    def draw(self):
        pass

class ExplodeEffect(BaseEffect):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.motionlst = [Bounds(IBNK.get("blast1")),Bounds(IBNK.get("blast2")),Bounds(IBNK.get("blast3")),Bounds(IBNK.get("blast4"))]
        self.motioninx = 0
    
    def update(self):
        self.img_bnd.x = self.motionlst[self.motioninx].x
        self.img_bnd.y = self.motionlst[self.motioninx].y
        self.img_bnd.w = self.motionlst[self.motioninx].w
        self.img_bnd.h = self.motionlst[self.motioninx].h
        self.motioninx += 1
        
        if self.motioninx > 3:
            self.is_explode = True
            
        return super().update()

    def draw(self):
        offsetx = 0
        offsety = 0
        if self.motioninx == 2:
            offsetx =  -2
        elif self.motioninx == 3:
            offsetx = -8
            offsety = -8
        
        if self.motioninx <= 2:
            pyxel.blt(
                self.x + offsetx, self.y + offsety, 
                self.img_page, self.img_bnd.x,self.img_bnd.y,self.img_bnd.w,self.img_bnd.h,
                pyxel.COLOR_BLACK
            )
        return super().draw()

class ItemEffect(BaseEffect):
    def __init__(self, x, y):
        super().__init__(x, y)
        
        self.img_bnd = Bounds(IBNK.get("effect1"))
        self.scale = 0
        self.motionlst = [0, 0.5, 0.75, 1.0, 1.25, 1.5 ]
    
    def update(self):
        self.scale = self.motionlst[self.motioninx]
        self.motioninx += 1
        
        if self.motioninx > 5:
            self.is_explode = True
        
        return super().update()

    def draw(self):
        offsetx = 0
        offsety = 0
        
        if self.motioninx <= 5:
            pyxel.blt(
                self.x + offsetx, self.y + offsety, 
                self.img_page, self.img_bnd.x,self.img_bnd.y,self.img_bnd.w,self.img_bnd.h,
                pyxel.COLOR_BLACK, scale=self.scale
            )
        
        return super().draw()

class LevelEffect(BaseEffect):
    def __init__(self, x, y):
        super().__init__(x, y)
        
        self.img_bnd = Bounds(IBNK.get("effect1"))
        self.scale = 0
        self.motionlst = [0, 0.5, 0.75, 1.0, 1.25, 1.5]
    
    def update(self):
        self.scale = self.motionlst[self.motioninx]
        self.motioninx += 1
        
        if self.motioninx > 5:
            self.is_explode = True
        
        return super().update()

    def draw(self):
        offsetx = 0
        offsety = 0
        
        if self.motioninx <= 5:
            pyxel.blt(
                self.x + offsetx, self.y + offsety - 0.25, 
                self.img_page, self.img_bnd.x,self.img_bnd.y,self.img_bnd.w,self.img_bnd.h,
                pyxel.COLOR_BLACK, scale=self.scale
            )
        
        return super().draw()

class AttackCommand:
    TYPE_GUN = 0
    TYPE_TORPEDO = 1
    TYPE_AIRCRAFT = 2
    TYPE_BBGUN = 3
    TYPE_AASHOOT = 4
    TYPE_MISSILE = 5
    TYPE_DEPTHCHARGE = 6
    TYPE_ASA_AIRCRAFT = 7
    def __init__(self, thistype: int):
        self.will_destroy = False
        
        self.x = 0
        self.y = 0
        self.first = Vector2(0, 0)
        self.w = 8
        self.h = 8
        self.dir = Vector2(0, -1)
        self.img_page = 0
        self.img_bnd = Bounds(0, 0, 8, 8)
        self.img_transparent = pyxel.COLOR_BLACK
        self.type = thistype
        self.power = 2
        self.blastpower = 0
        self.speed = 30
        self.max_count = 3
        self.area = EffectiveArea()
        self.range = 0 #---: 0 = max, 1~20 = specified tile count
        self.focus = Vector2(0, 0) #---missile focus position
        self.flight_time = 0
        self.focus_degree = 0
        #                  SS     DD     ADSG   CL     CA     CVL    CV     BC,    BB
        self.effectable = [False, True,  True,  True,  True,  True,  True,  True,  True]
        # first shot direction, fired direction
        self.first_x = [0, 0, 0] #left, middle, right
        self.fired_x = [0, 0] #left, right
        
        #---for enemy only
        self.interval = 0
        
        #---kantuu suru ka ?
        self.is_penetrate = False
        #---disappear by the blast
        self.is_destroy_blast = True
        #---delete when screen out ?
        self.is_screenout = True
        #---delete when hit with an object ?
        self.is_hitobject = True
        self.was_impacted = False
        #---for motion
        self.is_explode = False
        self.during_explode = 15
        self.start_explode = 0
        self.is_blast_depthcharge = False
        
        if thistype == AttackCommand.TYPE_GUN:
            self.speed = 2
            self.img_bnd = Bounds(IBNK.get("gun"))
            
        elif thistype == AttackCommand.TYPE_TORPEDO:
            self.speed = 2.5
            self.power = 3
            self.blastpower = 1.5
            self.area.left = True
            self.area.right = True
            self.max_count = 2
            self.img_bnd = Bounds(IBNK.get("torpedo"))
            
            self.is_destroy_blast = False
        elif thistype == AttackCommand.TYPE_AASHOOT:
            self.speed = 5
            self.power = 1
            self.range = 5
            self.max_count = 5
            self.img_bnd = Bounds(IBNK.get("aashoot"))
            
        elif thistype == AttackCommand.TYPE_AIRCRAFT:
            self.speed = 2.5
            self.power = 2
            self.blastpower = 1
            self.area.left = True
            self.area.right = True
            self.max_count = 2
            self.img_bnd = Bounds(IBNK.get("jet1"))
            
            self.is_penetrate = True
        elif thistype == AttackCommand.TYPE_BBGUN:
            self.speed = 3
            self.power = 4
            self.blastpower = 1
            self.area.left = True
            self.area.right = True
            self.img_bnd = Bounds(IBNK.get("bbgun1"))
            
            self.max_count = 1
            self.is_penetrate = True
        elif thistype == AttackCommand.TYPE_MISSILE:
            self.speed = 15
            self.power = 3
            self.blastpower = 1.5
            self.max_count = 2
            self.img_bnd = Bounds(IBNK.get("missile"))            
            self.area.front = True
            self.area.front_left = True
            self.area.front_right = True
            self.area.back = True
            self.area.back_left = True
            self.area.back_right =True
            self.area.left = True
            self.area.right = True
            self.fired_x = [-2, 0, 2]
        elif thistype == AttackCommand.TYPE_DEPTHCHARGE:
            self.speed = 1
            self.power = 3
            self.blastpower = 1.5
            self.max_count = 2
            self.img_bnd = Bounds(IBNK.get("depthcharge"))
            
            self.dir.x = 1
            self.effectable = [True,  False, False, False, False, False, False, False, False]
            
            self.area.front = True
            self.area.front_left = True
            self.area.front_right = True
            self.area.back = True
            self.area.back_left = True
            self.area.back_right =True
            self.area.left = True
            self.area.right = True
        
        elif thistype == AttackCommand.TYPE_ASA_AIRCRAFT:
            self.speed = 1.75
            self.power = 0.5
            self.blastpower = 0.25
            self.area.left = True
            self.area.right = True
            self.area.front_left = True
            self.area.front_right = True
            self.max_count = 2
            self.img_bnd = Bounds(IBNK.get("asa_acraft"))
            
            self.is_penetrate = True
            self.effectable = [True,  True,  True,  True,  True,  True,  True,  True,  True]
            
        #---buff
        self.buff = {
            "boost": False,
            "rader1" : False,
            "rader2" : False
        }
    def destroy(self):
        self.will_destroy = True
    
    def init_pos(self, x, y):
        self.x = x
        self.y = y
        self.first.x = x
        self.first.y = y
    
    def check_range(self):
        if self.range > 0:
            #---shot is range out
            if abs(self.first.x - self.x) > (self.range * 8):
                return  True
            if abs(self.first.y - self.y) > (self.range * 8):
                return  True
        else:
            #---shot is screen out
            if self.y  ==  pos(18):
                return True
            if self.x <= pos(0) or self.x > pos(15):
                return True
        
        return False
    
    def impact_missle(self): 
        x = (abs(self.x - self.focus.x))
        y = (abs(self.y - self.focus.y))
        
#        print(f"x={x}, y={y}")
        if x < 1 and y < 1:
            print(f"tyakudan! x={self.focus.x} y={self.focus.y}")
            self.was_impacted = True
            self.flight_time = 0
            return True
        else:
            if check_object_playscreen(x, y):
                return False
            else:
                #---screen out missile, forcely impact
                self.was_impacted = True
                self.flight_time = 0
                return True
        
    def impactarea_missile(self):
        poss = []
        if self.area.front:
            poss.append(Vector2(self.x, self.y + self.img_bnd.h * self.dir.y))
        if self.area.back:
            poss.append(Vector2(self.x, self.y + self.img_bnd.h * self.dir.y * self.dir.y))
        if self.dir.y == -1:
            if self.area.front_left:
                poss.append(Vector2(
                    self.x + (self.img_bnd.w * -1),
                    self.y + self.img_bnd.h * self.dir.y
                ))
            if self.area.front_right:
                poss.append(Vector2(
                    self.x + (self.img_bnd.w),
                    self.y + self.img_bnd.h * self.dir.y
                ))
            if self.area.back_left:
                poss.append(Vector2(
                    self.x + (self.img_bnd.w * -1),
                    self.y + self.img_bnd.h * self.dir.y * self.dir.y
                ))
            if self.area.back_right:
                poss.append(Vector2(
                    self.x + (self.img_bnd.w),
                    self.y + self.img_bnd.h * self.dir.y * self.dir.y
                ))
            if self.area.left:
                poss.append(Vector2(
                    self.x + (self.img_bnd.w * -1),
                    self.y
                ))
            if self.area.right:
                poss.append(Vector2(
                    self.x + (self.img_bnd.w),
                    self.y
                ))
        else:
            if self.area.front_left:
                poss.append(Vector2(
                    self.x + (self.img_bnd.w),
                    self.y + self.img_bnd.h * self.dir.y
                ))
            if self.area.front_right:
                poss.append(Vector2(
                    self.x + (self.img_bnd.w * -1),
                    self.y + self.img_bnd.h * self.dir.y
                ))
            if self.area.back_left:
                poss.append(Vector2(
                    self.x + (self.img_bnd.w),
                    self.y + self.img_bnd.h * self.dir.y * self.dir.y
                ))
            if self.area.back_right:
                poss.append(Vector2(
                    self.x + (self.img_bnd.w * -1),
                    self.y + self.img_bnd.h * self.dir.y * self.dir.y
                ))
            if self.area.left:
                poss.append(Vector2(
                    self.x + (self.img_bnd.w),
                    self.y
                ))
            if self.area.right:
                poss.append(Vector2(
                    self.x + (self.img_bnd.w * -1),
                    self.y
                ))
        return poss
    
    def effective_against(self, jobtype: int):
        #for cmd in enumerate(CSV_ATTACKWEAK):
        for shiptype in enumerate(self.effectable):
            if jobtype == shiptype[0]:
                return shiptype[1]
        return False
        
    def receive_attack(self, shot):
        """shot and other shot collidered?
        """
        ishit = {
            "main" : False,
            "blast" : False
        }
        #---directly hit
        #---anti aircraft shoot can defeat air craft
        if (
            ((self.type == AttackCommand.TYPE_AIRCRAFT or self.type == AttackCommand.TYPE_ASA_AIRCRAFT) and shot.type == AttackCommand.TYPE_AASHOOT)
            or
            (self.type == AttackCommand.TYPE_TORPEDO and shot.type == AttackCommand.TYPE_TORPEDO)
            or
            (self.type == AttackCommand.TYPE_AIRCRAFT and shot.type == AttackCommand.TYPE_AIRCRAFT)
            or
            (self.type == AttackCommand.TYPE_ASA_AIRCRAFT and shot.type == AttackCommand.TYPE_AIRCRAFT)
            or
            (self.type == AttackCommand.TYPE_AIRCRAFT and shot.type == AttackCommand.TYPE_AIRCRAFT)
            or
            (self.type == AttackCommand.TYPE_ASA_AIRCRAFT and shot.type == AttackCommand.TYPE_ASA_AIRCRAFT)
        ):
            if (abs(shot.x - self.x) < self.img_bnd.w and abs(shot.y - self.y) < self.img_bnd.h):
                ishit["main"] = True
                
            #---blast hit
            newpos = Vector2(shot.x, shot.y)
            selfleft = self.x
            selfright = self.x + self.img_bnd.w
            selftop = self.y
            selfbottom = self.y + self.img_bnd.h
            
            if shot.area.front:
                newpos.x = shot.x
                newpos.y = shot.y + shot.img_bnd.h * shot.dir.y
                #ishit["blast"] = (abs(newpos.x - self.x) < self.img_bnd.w and abs(newpos.y - self.y) < self.img_bnd.h)
                ishit["blast"] = calc_collision(selfleft, selfright, selftop, selfbottom, 
                              newpos.x, newpos.x+shot.img_bnd.w, newpos.y, newpos.y+shot.img_bnd.h
                )
                
            if not ishit["blast"] and shot.area.back:
                newpos.x = shot.x
                newpos.y = shot.y +  shot.img_bnd.h * shot.dir.y * shot.dir.y
                #ishit["blast"] = (abs(newpos.x - self.x) < self.img_bnd.w and abs(newpos.y - self.y) < self.img_bnd.h)
                ishit["blast"] = calc_collision(selfleft, selfright, selftop, selfbottom, 
                              newpos.x, newpos.x+shot.img_bnd.w, newpos.y, newpos.y+shot.img_bnd.h
                )
                if ishit["blast"]:
                    print("back hit!")
        
            if shot.dir.y == -1:
                if not ishit["blast"] and shot.area.front_left:
                    newpos.x = shot.x + (shot.img_bnd.w * -1)
                    newpos.y = shot.y + shot.img_bnd.h * shot.dir.y
                    #ishit["blast"] = (abs(newpos.x - self.x) < self.img_bnd.w and abs(newpos.y - self.y) < self.img_bnd.h)
                    ishit["blast"] = calc_collision(selfleft, selfright, selftop, selfbottom, 
                              newpos.x, newpos.x+shot.img_bnd.w, newpos.y, newpos.y+shot.img_bnd.h
                    )
                    if ishit["blast"]:
                        print("front left hit!")
                if not ishit["blast"] and shot.area.front_right:
                    newpos.x = shot.x + shot.img_bnd.w
                    newpos.y = shot.y + shot.img_bnd.h * shot.dir.y
                    #ishit["blast"] = (abs(newpos.x - self.x) < self.img_bnd.w and abs(newpos.y - self.y) < self.img_bnd.h)
                    ishit["blast"] = calc_collision(selfleft, selfright, selftop, selfbottom, 
                              newpos.x, newpos.x+shot.img_bnd.w, newpos.y, newpos.y+shot.img_bnd.h
                    )
                    if ishit["blast"]:
                        print("front right hit!")
                
                if not ishit["blast"] and shot.area.back_left:
                    newpos.x = shot.x + (shot.img_bnd.w * -1)
                    newpos.y = shot.y +  shot.img_bnd.h * shot.dir.y * shot.dir.y
                    #ishit["blast"] = (abs(newpos.x - self.x) < self.img_bnd.w and abs(newpos.y - self.y) < self.img_bnd.h)
                    ishit["blast"] = calc_collision(selfleft, selfright, selftop, selfbottom, 
                              newpos.x, newpos.x+shot.img_bnd.w, newpos.y, newpos.y+shot.img_bnd.h
                    )
                    if ishit["blast"]:
                        print("back left hit!")
                if not ishit["blast"] and shot.area.back_right:
                    newpos.x = shot.x + shot.img_bnd.w
                    newpos.y = shot.y +  shot.img_bnd.h * shot.dir.y * shot.dir.y
                    #ishit["blast"] = (abs(newpos.x - self.x) < self.img_bnd.w and abs(newpos.y - self.y) < self.img_bnd.h)
                    ishit["blast"] = calc_collision(selfleft, selfright, selftop, selfbottom, 
                              newpos.x, newpos.x+shot.img_bnd.w, newpos.y, newpos.y+shot.img_bnd.h
                    )
                    if ishit["blast"]:
                        print("back right hit!")
                
                if not ishit["blast"] and shot.area.left:
                    newpos.x = shot.x + (shot.img_bnd.w * -1)
                    newpos.y = shot.y
                    #ishit["blast"] = (abs(newpos.x - self.x) < self.img_bnd.w and abs(newpos.y - self.y) < self.img_bnd.h)
                    ishit["blast"] = calc_collision(selfleft, selfright, selftop, selfbottom, 
                              newpos.x, newpos.x+shot.img_bnd.w, newpos.y, newpos.y+shot.img_bnd.h
                    )
                    if ishit["blast"]:
                        print("left hit!")
                if not ishit["blast"] and shot.area.right:
                    newpos.x = shot.x + shot.img_bnd.w
                    newpos.y = shot.y
                    #ishit["blast"] = (abs(newpos.x - self.x) < self.img_bnd.w and abs(newpos.y - self.y) < self.img_bnd.h)
                    ishit["blast"] = calc_collision(selfleft, selfright, selftop, selfbottom, 
                              newpos.x, newpos.x+shot.img_bnd.w, newpos.y, newpos.y+shot.img_bnd.h
                    )
                    if ishit["blast"]:
                        print("right hit!")
            elif shot.dir.y == 1:
                if not ishit["blast"] and shot.area.front_left:
                    newpos.x = shot.x +  shot.img_bnd.w
                    newpos.y = shot.y + shot.img_bnd.h * shot.dir.y
                    #ishit["blast"] = (abs(newpos.x - self.x) < self.img_bnd.w and abs(newpos.y - self.y) < self.img_bnd.h)
                    ishit["blast"] = calc_collision(selfleft, selfright, selftop, selfbottom, 
                              newpos.x, newpos.x+shot.img_bnd.w, newpos.y, newpos.y+shot.img_bnd.h
                    )
                    if ishit["blast"]:
                        print("front left hit!")
                if not ishit["blast"] and shot.area.front_right:
                    newpos.x = shot.x + (shot.img_bnd.w * -1)
                    newpos.y = shot.y + shot.img_bnd.h * shot.dir.y
                    #ishit["blast"] = (abs(newpos.x - self.x) < self.img_bnd.w and abs(newpos.y - self.y) < self.img_bnd.h)
                    ishit["blast"] = calc_collision(selfleft, selfright, selftop, selfbottom, 
                              newpos.x, newpos.x+shot.img_bnd.w, newpos.y, newpos.y+shot.img_bnd.h
                    )
                    if ishit["blast"]:
                        print("front right hit!")
                
                if not ishit["blast"] and shot.area.back_left:
                    newpos.x = shot.x +  shot.img_bnd.w
                    newpos.y = shot.y +  shot.img_bnd.h * shot.dir.y * shot.dir.y
                    #ishit["blast"] = (abs(newpos.x - self.x) < self.img_bnd.w and abs(newpos.y - self.y) < self.img_bnd.h)
                    ishit["blast"] = calc_collision(selfleft, selfright, selftop, selfbottom, 
                              newpos.x, newpos.x+shot.img_bnd.w, newpos.y, newpos.y+shot.img_bnd.h
                    )
                    if ishit["blast"]:
                        print("back left hit!")
                if not ishit["blast"] and shot.area.back_right:
                    newpos.x = shot.x + (shot.img_bnd.w * -1)
                    newpos.y = shot.y +  shot.img_bnd.h * shot.dir.y * shot.dir.y
                    #ishit["blast"] = (abs(newpos.x - self.x) < self.img_bnd.w and abs(newpos.y - self.y) < self.img_bnd.h)
                    ishit["blast"] = calc_collision(selfleft, selfright, selftop, selfbottom, 
                              newpos.x, newpos.x+shot.img_bnd.w, newpos.y, newpos.y+shot.img_bnd.h
                    )
                    if ishit["blast"]:
                        print("back right hit!")
                
                if not ishit["blast"] and shot.area.left:
                    newpos.x = shot.x +  shot.img_bnd.w
                    newpos.y = shot.y
                    #ishit["blast"] = (abs(newpos.x - self.x) < self.img_bnd.w and abs(newpos.y - self.y) < self.img_bnd.h)
                    ishit["blast"] = calc_collision(selfleft, selfright, selftop, selfbottom, 
                              newpos.x, newpos.x+shot.img_bnd.w, newpos.y, newpos.y+shot.img_bnd.h
                    )
                    if ishit["blast"]:
                        print("left hit!")
                if not ishit["blast"] and shot.area.right:
                    newpos.x = shot.x + (shot.img_bnd.w * -1)
                    newpos.y = shot.y
                    #ishit["blast"] = (abs(newpos.x - self.x) < self.img_bnd.w and abs(newpos.y - self.y) < self.img_bnd.h)
                    ishit["blast"] = calc_collision(selfleft, selfright, selftop, selfbottom, 
                              newpos.x, newpos.x+shot.img_bnd.w, newpos.y, newpos.y+shot.img_bnd.h
                    )
                    if ishit["blast"]:
                        print("right hit!")
                
       
            
        return ishit
    
    def effect_buff(self, buff, time):
        if buff == "boost" and time > 0:
            self.buff["boost"] = True
            if self.type == AttackCommand.TYPE_MISSILE:
                self.power += 1
                self.blastpower += 1
            else: #if self.type == AttackCommand.TYPE_DEPTHCHARGE:
                self.speed += 1
                self.power *= 1.5
                self.blastpower *= 1.5
        elif buff == "rader1" and time > 0:
                self.buff["rader1"] = True
                self.speed += 0.5
        elif buff == "rader2" and time > 0:
            if self.type == AttackCommand.TYPE_AASHOOT:
                self.buff["rader2"] = True
                self.range *= 2
            
            
    def update(self):
        #if pyxel.frame_count % self.speed:
        if self.type == AttackCommand.TYPE_MISSILE and not self.was_impacted:
            asisdegree = 0
            if self.first.x < self.focus.x:
                self.x += (abs(self.focus.x - self.first.x) / self.speed)
                asisdegree = 1
            elif self.first.x > self.focus.x:
                self.x -= (abs(self.focus.x - self.first.x) / self.speed)
                asisdegree = -1
            
            if self.first.y < self.focus.y:
                self.y += (abs(self.focus.y - self.first.y) / self.speed)
            elif self.first.y > self.focus.y:
                self.y -= (abs(self.focus.y - self.first.y) / self.speed)
            
            self.flight_time += 1
            self.focus_degree = pyxel.atan2((self.focus.y - self.y), (self.focus.x - self.x))  * asisdegree
            
        elif self.type == AttackCommand.TYPE_DEPTHCHARGE:
            self.y += self.dir.y * self.speed            
            if self.x >= self.first.x + self.img_bnd.w:
                self.dir.x = -1
            elif self.x <= self.first.x - self.img_bnd.w:
                self.dir.x = 1
            #self.x += (abs(self.first.x - self.x) / 15) * self.dir.x
            self.x += 1 * self.dir.x
        else:
            self.focus_degree = 0
            self.x += self.dir.x * self.speed
            self.y += self.dir.y * self.speed

    def draw(self):
        pyxel.blt(
            self.x, self.y, 
            self.img_page, 
            self.img_bnd.x, self.img_bnd.y, self.img_bnd.w, self.img_bnd.h,
            self.img_transparent,
            rotate=self.focus_degree if self.dir.y == -1 else 180
        )

class ShipJob:
    TYPE_SS = 0
    TYPE_DD = 1
    TYPE_ASDG = 2
    TYPE_CL = 3
    TYPE_CA = 4
    TYPE_CVL = 5
    TYPE_CV = 6
    TYPE_BC = 7
    TYPE_BB = 8
    def __init__(self, job: int, equiptype = 0):
        self.type = job
        self.commands: list[AttackCommand] = []
        self.lv = 1
        self.maxhp = 0
        self.movespeed = 1
        self.img_page = 0
        self.img_bnd = Bounds(0, 0, 16, 16)
        
        if job == ShipKind.TYPE_SS:
            self.commands.append(AttackCommand(AttackCommand.TYPE_TORPEDO))
            self.commands.append(AttackCommand(AttackCommand.TYPE_TORPEDO))
            self.maxhp = 3
            self.img_bnd.x = IBNK.get("SS_front1").x
        elif job == ShipKind.TYPE_DD:
            self.commands.append(AttackCommand(AttackCommand.TYPE_TORPEDO))
            if equiptype == 0:
                self.commands.append(AttackCommand(AttackCommand.TYPE_AASHOOT))
            else:
                self.commands.append(AttackCommand(AttackCommand.TYPE_DEPTHCHARGE))
            self.maxhp = 6
            self.movespeed = 1.2
            self.img_bnd.x = IBNK.get("DD_front1").x
        elif job == ShipKind.TYPE_ASDG:
            self.commands.append(AttackCommand(AttackCommand.TYPE_MISSILE))
            self.commands.append(AttackCommand(AttackCommand.TYPE_AASHOOT))
            self.maxhp = 8
            self.img_bnd.x = IBNK.get("ASDG_front1").x
        elif job == ShipKind.TYPE_CL:
            self.commands.append(AttackCommand(AttackCommand.TYPE_GUN))
            if equiptype == 0:
                self.commands.append(AttackCommand(AttackCommand.TYPE_AASHOOT))
            else:
                self.commands.append(AttackCommand(AttackCommand.TYPE_DEPTHCHARGE))
            self.commands[0].speed += 0.5
            self.commands[0].max_count = 3
            self.commands[1].range = 10
            self.commands[1].fired_x = [-1,1]
            self.maxhp = 10
            self.img_bnd.x = IBNK.get("CL_front1").x
        elif job == ShipKind.TYPE_CA:
            self.commands.append(AttackCommand(AttackCommand.TYPE_GUN))
            self.commands.append(AttackCommand(AttackCommand.TYPE_AASHOOT))
            self.commands[0].max_count = 4
            self.commands[0].power = 3
            self.commands[0].area.left = True
            self.commands[0].area.right = True
            self.commands[0].blastpower = 0.25
            self.commands[0].first_x = [-1, 0, 1]            
            self.commands[1].range = 7
            self.maxhp = 14
            self.img_bnd.x = IBNK.get("CA_front1").x
        elif job == ShipKind.TYPE_CVL:
            self.commands.append(AttackCommand(AttackCommand.TYPE_AIRCRAFT))
            self.commands[0].is_blast_depthcharge = True
            if equiptype == 0:
                self.commands.append(AttackCommand(AttackCommand.TYPE_AASHOOT))
            elif equiptype == 1:
                self.commands.append(AttackCommand(AttackCommand.TYPE_DEPTHCHARGE))
            elif equiptype == 2:
                self.commands.append(AttackCommand(AttackCommand.TYPE_ASA_AIRCRAFT))
            self.maxhp = 8
            self.movespeed = 1.2
            self.img_bnd.x = IBNK.get("CVL_front1").x
        elif job == ShipKind.TYPE_CV:
            self.commands.append(AttackCommand(AttackCommand.TYPE_AIRCRAFT))
            if equiptype == 0:
                self.commands.append(AttackCommand(AttackCommand.TYPE_AASHOOT))
            elif equiptype == 1:
                self.commands.append(AttackCommand(AttackCommand.TYPE_ASA_AIRCRAFT))
                self.commands[1].effectable[0] = False
                self.commands[1].max_count = 3
            else:
                self.commands.append(AttackCommand(AttackCommand.TYPE_AASHOOT))
            self.commands[0].max_count = 3
            self.commands[0].first_x = [-2, 0, 2]
            self.maxhp = 16
            self.img_bnd.x = IBNK.get("CV_front1").x
        elif job == ShipKind.TYPE_BB:
            self.commands.append(AttackCommand(AttackCommand.TYPE_BBGUN))
            self.commands.append(AttackCommand(AttackCommand.TYPE_AASHOOT))
            self.maxhp = 20
            self.img_bnd.x = IBNK.get("BB_front1").x
        elif job == ShipKind.TYPE_BC:
            self.commands.append(AttackCommand(AttackCommand.TYPE_BBGUN))
            self.commands.append(AttackCommand(AttackCommand.TYPE_AASHOOT))
            self.maxhp = 18
            self.img_bnd.x = IBNK.get("BC_front1").x
        self.commands[0].dir.y = -1
        self.commands[1].dir.y = -1
    
    def destroy(self):        
        self.commands.clear()
        
    def level_up(self, playerlv: int):
        self.lv = playerlv
        self.commands[0].power += 0.25
        self.commands[1].power += 0.15
        if self.type == self.TYPE_SS:
            #main
            self.commands[0].max_count += 1
            self.commands[0].blastpower += 0.15
            #sub
            self.commands[1].max_count += 1
            self.commands[0].blastpower += 0.15
        elif self.type == self.TYPE_DD:
            #main
            if self.commands[0].max_count < 5:
                self.commands[0].max_count += 1
            self.commands[0].blastpower += 0.15
            #sub
            if self.commands[1].type == AttackCommand.TYPE_DEPTHCHARGE:
                if self.commands[1].max_count < 4:
                    self.commands[1].max_count += 1
            elif self.commands[1].type == AttackCommand.TYPE_AASHOOT:
                self.commands[1].range += 1
        elif self.type == self.TYPE_ASDG:
            #main
            if self.commands[0].max_count < 3:
                self.commands[0].max_count += 1
            self.commands[0].blastpower += 0.15
            #sub
            self.commands[1].range += 1

        elif self.type == self.TYPE_CL:
            #main
            if self.commands[0].max_count < 5:
                self.commands[0].max_count += 1
            if self.commands[0].speed < 2:
                self.commands[0].speed += 0.15
            #sub
            if self.commands[1].type == AttackCommand.TYPE_DEPTHCHARGE:
                if self.commands[1].max_count < 4:
                    self.commands[1].max_count += 1
            elif self.commands[1].type == AttackCommand.TYPE_AASHOOT:
                self.commands[1].range += 1
        elif self.type == self.TYPE_CA:
            #main
            if self.commands[0].max_count < 6:
                self.commands[0].max_count += 1
            self.commands[0].blastpower += 0.25
            if self.commands[0].speed < 2:
                self.commands[0].speed += 0.25
            #sub
            self.commands[1].range += 1
        elif self.type == self.TYPE_CVL:
            #main
            if self.lv >= 3:
                self.commands[0].max_count += 1
            self.commands[0].blastpower += 0.15
            #sub
            if self.commands[1].type == AttackCommand.TYPE_DEPTHCHARGE:
                if self.commands[1].max_count < 3:
                    self.commands[1].max_count += 1
            elif self.commands[1].type == AttackCommand.TYPE_ASA_AIRCRAFT:
                if self.commands[1].max_count < 3:
                    self.commands[1].max_count += 1
                self.commands[0].blastpower += 0.15
        elif self.type == self.TYPE_CV:
            #main
            if self.lv >= 3:
                if self.commands[0].max_count < 4:
                    self.commands[0].max_count += 1
            self.commands[0].blastpower += 0.15
            #sub
            if self.commands[1].type == AttackCommand.TYPE_ASA_AIRCRAFT:
                if self.commands[1].max_count < 4:
                    self.commands[1].max_count += 1
                self.commands[0].blastpower += 0.15
        elif self.type == self.TYPE_BC:
            #main
            if self.lv >= 3:
                if self.commands[0].max_count < 2:
                    self.commands[0].max_count += 1
            #sub
            self.commands[1].range += 1

class Item(GameObject):
    TYPE_HPFULL = 0
    TYPE_HPHALF = 1
    TYPE_BOOST = 2
    TYPE_INVINCIBLE = 3
    TYPE_RADER_1 = 4
    TYPE_RADER_2 = 5
    TYPE_SHIELD = 6
    TYPE_LEVELUP = 7
    def __init__(self, app, dtype, x, y):
        super().__init__(app, x, y)
        self.type = dtype
        self.dir.y = 1
        if dtype == Item.TYPE_HPFULL:
            self.img_bnd = Bounds(IBNK.get("damecon"))
            
        elif dtype == Item.TYPE_HPHALF:
            self.img_bnd = Bounds(IBNK.get("juice"))
            
        elif dtype == Item.TYPE_BOOST:
            self.img_bnd = Bounds(IBNK.get("curry1"))
            
            self.x = x - 4
        elif dtype == Item.TYPE_INVINCIBLE:
            self.img_bnd = Bounds(IBNK.get("curry2"))
            
            self.x = x - 4
        
        elif dtype == Item.TYPE_RADER_1:
            self.img_bnd = Bounds(IBNK.get("rader1"))
                
        elif dtype == Item.TYPE_RADER_2:
            self.img_bnd = Bounds(IBNK.get("rader2"))
            
        elif dtype == Item.TYPE_SHIELD:
            self.img_bnd = Bounds(IBNK.get("shield"))
            
        elif dtype == Item.TYPE_LEVELUP:
            self.img_bnd = Bounds(IBNK.get("ginger_fishcakes"))
            
    def effect(self, target):
        if self.type == Item.TYPE_HPFULL:
            target.healing(target.maxhp)
        elif self.type == Item.TYPE_HPHALF:
            target.healing(target.maxhp // 2)
        elif self.type == Item.TYPE_BOOST:
            target.set_buff(self.type,10)
        elif self.type == Item.TYPE_INVINCIBLE:
            target.set_buff(self.type,10)
        elif self.type == Item.TYPE_RADER_1:
            target.set_buff(self.type,10)
        elif self.type == Item.TYPE_RADER_2:
            target.set_buff(self.type,10)
        elif self.type == Item.TYPE_SHIELD:
            target.set_buff(self.type,10)
        elif self.type == Item.TYPE_LEVELUP:
            target.level_up()
        
    def update(self):
        if self.y < (pyxel.height - 16):
            self.y += self.dir.y * self.movespeed
        else:
            self.will_destroy = True
    
    def draw(self):
        pyxel.blt(self.x, self.y, self.img_page, self.img_bnd.x, self.img_bnd.y, self.img_bnd.w, self.img_bnd.h, pyxel.COLOR_BLACK)
        

class AnimationOnWave(GameObject):
    def __init__(self, app, x, y):
        super().__init__(app, x, y)
        self.bganime_cur = pos(15)
        self.bganime_img = (
            (Bounds(IBNK.get("ship")),0),
            (Bounds(IBNK.get("depthcharge")),0),
            (Bounds(IBNK.get("jet1")),90),
            (Bounds(IBNK.get("damecon")),0),
            (Bounds(IBNK.get("curry1")),0)
        )
        self.bga_img_index = 0
        
    
    def update(self):
        if self.bganime_cur < 0:
            self.bganime_cur = pos(20)
            irnd = pyxel.rndi(1, 100)
            if 1 <= irnd <= 50:
                self.bga_img_index = 0
            elif 51 <= irnd <= 70:
                self.bga_img_index = 1
            elif 71 <= irnd <= 85:
                self.bga_img_index = 2
            elif 86 <= irnd <= 95:
                self.bga_img_index = 3
            else:
                self.bga_img_index = 4
            self.movespeed = pyxel.rndf(0.5, 2)
            
        
        self.bganime_cur -= self.movespeed
        
            
        return super().update()
    
    def draw(self):
        pyxel.bltm(self.x,self.y,0,32*8,0, 16*8, 2*8,pyxel.COLOR_BLACK)
        pyxel.blt(self.bganime_cur,self.y, 0, 
                  self.bganime_img[self.bga_img_index][0].x, self.bganime_img[self.bga_img_index][0].y, self.bganime_img[self.bga_img_index][0].w, self.bganime_img[self.bga_img_index][0].h,
                  pyxel.COLOR_BLACK,
                  rotate=self.bganime_img[self.bga_img_index][1]
        )
        
        return super().draw()