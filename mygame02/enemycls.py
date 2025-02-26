from myconfig import GameOperator
from mycls import GameObject, Vector2, EffectiveArea, ShipJob, AttackCommand, calc_collision, Bounds
from imgbnk import IBNK
from appconst import ShipKind
import pyxel
import copy

class Enemy(GameObject):
    TYPE_NORMAL = 0
    TYPE_ENHANCED = 1
    TYPE_SUPER = 2
    def __init__(self, app: GameOperator, job: int, jobclass: int = 0, lv: int = 1, x = 0, y = 0):
        super().__init__(app, x, y)
        self.jobtype = job
        self.jobclass = jobclass
        self.lv = lv
        self.point = 0
        self.commands: list[AttackCommand] = []
        self.shots_main: list[AttackCommand] = []
        self.shots_sub: list[AttackCommand] = []
        self.cur_shots: list[list[AttackCommand]] = []
        self.mainattack_interval = 0
        self.subattack_interval = 0
        self.move_interval = 1
        self.move_additional_area = EffectiveArea()
        self.is_moving = EffectiveArea()
        self.move_additional_frame_time = 15
        self.move_additional_current_frame = 0
        self.motionlst = []
        self.motioninx = 0
        self.max_count = 0
        
        #---new code: load from json
        self.load(job, app.data_man.get_enemydata(job, jobclass, lv))
        
        """
        if job == ShipKind.TYPE_DD:
            if jobclass == self.TYPE_NORMAL:
                self.dir.y = 1
                self.motionlst.append(IBNK.get("eDD1_a")) # (160,0))
                self.motionlst.append(IBNK.get("eDD1_b")) # (160,8))
                self.img_bnd.w = IBNK.get("eDD1_a").w
                self.img_bnd.h = IBNK.get("eDD1_a").h
                self.maxhp = 2
                if self.lv == 1:
                    self.move_interval = 3
                    self.point = 1
                elif self.lv == 2:
                    self.maxhp = 2
                    self.move_interval = 2
                    self.movespeed = 1
                    self.move_additional_area.left = True
                    self.move_additional_area.right =  True
                    self.move_additional_area.frequency = pyxel.rndi(100, 150)
                    self.point = 1
                elif self.lv == 3:
                    self.maxhp = 4
                    self.movespeed = 1
                    self.move_additional_area.left = True
                    self.move_additional_area.right =  True
                    self.move_additional_area.front = True
                    self.move_additional_area.back =  True
                    self.move_additional_area.frequency = pyxel.rndi(60, 90)
                    self.point = 1
            if self.jobclass == self.TYPE_ENHANCED:
                self.dir.y = 1
                self.maxhp = 3
                self.motionlst.append(IBNK.get("eDDE_a")) # #(160,32))
                self.motionlst.append(IBNK.get("eDDE_b")) #(160,48))
                self.img_bnd.w = IBNK.get("eDDE_a").w
                self.img_bnd.h = IBNK.get("eDDE_a").h
                
                if self.lv == 1:
                    self.movespeed = 2
                    self.move_interval = 2
                    self.mainattack_interval = pyxel.rndi(90, 120)
                    self.subattack_interval = pyxel.rndi(100, 150)
                    self.commands.append(AttackCommand(AttackCommand.TYPE_AASHOOT))
                    self.commands.append(AttackCommand(AttackCommand.TYPE_DEPTHCHARGE))
                    self.commands[0].dir.y = 1
                    self.commands[1].dir.y = 1
                    self.point = 2
                elif self.lv == 2:
                    self.maxhp = 5
                    self.movespeed = 2
                    self.move_interval = 1
                    self.move_additional_area.left = True
                    self.move_additional_area.right =  True
                    self.move_additional_area.frequency = pyxel.rndi(100, 150)
                    self.mainattack_interval = pyxel.rndi(80, 110)
                    self.subattack_interval = pyxel.rndi(100, 150)
                    self.commands.append(AttackCommand(AttackCommand.TYPE_TORPEDO))
                    self.commands.append(AttackCommand(AttackCommand.TYPE_DEPTHCHARGE))
                    self.commands[0].dir.y = 1
                    self.commands[1].dir.y = 1
                    self.commands[1].blastpower = 0.5
                    self.commands[1].area.left = True
                    self.commands[1].area.right = True
                    self.point = 2
                elif self.lv == 3:
                    self.maxhp = 6
                    self.movespeed = 2
                    self.move_interval = 1
                    self.move_additional_area.left = True
                    self.move_additional_area.right =  True
                    self.move_additional_area.frequency = pyxel.rndi(90, 120)
                    self.mainattack_interval = pyxel.rndi(80, 110)
                    self.subattack_interval = pyxel.rndi(100, 150)
                    self.commands.append(AttackCommand(AttackCommand.TYPE_TORPEDO))
                    self.commands.append(AttackCommand(AttackCommand.TYPE_DEPTHCHARGE))
                    self.commands[0].dir.y = 1
                    self.commands[1].dir.y = 1
                    self.commands[1].blastpower = 0.5
                    self.commands[1].area.left = True
                    self.commands[1].area.right = True
                    self.point = 2
        elif job == ShipKind.TYPE_SS:
            if self.jobclass == self.TYPE_NORMAL:
                self.motionlst.append(IBNK.get("eSS_a")) #(176,32))
                self.motionlst.append(IBNK.get("eSS_b")) #(176,48))
                self.img_bnd.w = IBNK.get("eSS_a").w
                self.img_bnd.h = IBNK.get("eSS_a").h
                self.movespeed = 1
                self.move_interval = 3                
                self.point = 100
                self.maxhp = 3
                self.dir.y = 1
                if self.lv == 1:
                    self.mainattack_interval = pyxel.rndi(100, 150)
                    self.commands.append(AttackCommand(AttackCommand.TYPE_TORPEDO))
                    self.commands[0].dir.y = 1
                elif self.lv == 2:
                    self.maxhp = 4
                    self.point = 200
                    self.mainattack_interval = pyxel.rndi(90, 120)
                    self.commands.append(AttackCommand(AttackCommand.TYPE_TORPEDO))
                    self.commands[0].dir.y = 1
                elif self.lv == 3:
                    self.maxhp = 6
                    self.point = 300
                    self.move_additional_area.left = True
                    self.move_additional_area.right =  True
                    self.move_additional_area.frequency = pyxel.rndi(90, 120)
                    self.mainattack_interval = pyxel.rndi(90, 120)
                    self.commands.append(AttackCommand(AttackCommand.TYPE_TORPEDO))
                    self.commands[0].dir.y = 1
        elif job == ShipKind.TYPE_CL:
            if self.jobclass == self.TYPE_NORMAL:
                self.dir.y = 1
                self.motionlst.append(IBNK.get("eCL_a")) #(176,0))
                self.motionlst.append(IBNK.get("eCL_b")) #(176,16))
                self.img_bnd.w = IBNK.get("eCL_a").w
                self.img_bnd.h = IBNK.get("eCL_a").h
                self.maxhp = 4
                self.move_interval = 2
                self.move_additional_frame_time = 30
                self.move_additional_area.left = True
                self.move_additional_area.right =  True
                self.move_additional_area.frequency = pyxel.rndi(100, 150)
                self.mainattack_interval = pyxel.rndi(80, 120)
                self.commands.append(AttackCommand(AttackCommand.TYPE_GUN))
                self.commands[0].dir.y = 1
                self.point = 5
                if self.lv == 2:
                    self.maxhp = 6
                    self.point = 10
                    self.move_additional_area.frequency = pyxel.rndi(90, 120)
                    self.subattack_interval = pyxel.rndi(100, 150)
                    self.commands.append(AttackCommand(AttackCommand.TYPE_DEPTHCHARGE))
                    self.commands[1].dir.y = 1
                elif self.lv == 3:
                    self.maxhp = 8
                    self.point = 15
                    self.move_additional_area.frequency = pyxel.rndi(90, 120)
                    self.subattack_interval = pyxel.rndi(50, 80)
                    self.commands.append(AttackCommand(AttackCommand.TYPE_AASHOOT))
                    self.commands[1].dir.y = 1
        elif job == ShipKind.TYPE_CA:
            if self.jobclass == self.TYPE_NORMAL:
                self.dir.y = 1
                self.motionlst.append(IBNK.get("eCA_a")) #(192,0))
                self.motionlst.append(IBNK.get("eCA_b")) #(192,16))
                self.img_bnd.w = IBNK.get("eCA_a").w
                self.img_bnd.h = IBNK.get("eCA_a").h
                self.maxhp = 6
                self.move_interval = 2
                self.move_additional_area.left = True
                self.move_additional_area.right =  True
                self.move_additional_area.frequency = pyxel.rndi(90, 120)
                self.mainattack_interval = pyxel.rndi(50, 100) 
                self.commands.append(AttackCommand(AttackCommand.TYPE_GUN))
                self.commands[0].dir.y = 1
                self.point = 10
                if self.lv == 2:
                    self.maxhp = 8
                    self.point = 20
                elif self.lv == 3:
                    self.maxhp = 10
                    self.point = 25
                    self.subattack_interval = pyxel.rndi(50, 80)
                    self.commands.append(AttackCommand(AttackCommand.TYPE_AASHOOT))
                    self.commands[1].dir.y = 1
        elif job == ShipKind.TYPE_CVL:
            self.dir.y = 0
            self.move_interval = 0
            if self.jobclass == self.TYPE_NORMAL:
                self.motionlst.append(IBNK.get("eCVL_a")) #(208,0))
                self.motionlst.append(IBNK.get("eCVL_b")) #(208,16))
                self.img_bnd.w = IBNK.get("eCVL_a").w
                self.img_bnd.h = IBNK.get("eCVL_a").h
                self.maxhp = 5
                self.move_additional_area.left = True
                self.move_additional_area.right =  True
                self.move_additional_area.frequency = pyxel.rndi(100, 120)
                self.move_additional_frame_time = 30
                self.mainattack_interval = pyxel.rndi(90, 120)
                self.subattack_interval = pyxel.rndi(100, 150)
                self.commands.append(AttackCommand(AttackCommand.TYPE_AIRCRAFT))                
                self.commands[0].blastpower = 0.01
                self.commands[0].dir.y = 1
                self.commands[0].img_bnd.x = 24
                
                self.point = 20
                self.alive_time = 30 * 15
                if self.lv == 1:
                    self.move_additional_area.front = True
                    self.move_additional_area.back = True
                    self.commands.append(AttackCommand(AttackCommand.TYPE_DEPTHCHARGE))
                    self.commands[1].dir.y = 1
                elif self.lv == 2:
                    self.maxhp = 8
                    self.point = 30
                    self.move_additional_frame_time = 40
                    self.subattack_interval = pyxel.rndi(50, 100)
                    self.commands.append(AttackCommand(AttackCommand.TYPE_ASA_AIRCRAFT))
                    self.commands[1].dir.y = 1
                    self.commands[1].blastpower = 0.01
                elif self.lv == 3:
                    self.maxhp = 10
                    self.point = 40
                    self.move_additional_frame_time = 40
                    self.subattack_interval = pyxel.rndi(50, 70)
                    self.commands.append(AttackCommand(AttackCommand.TYPE_ASA_AIRCRAFT))
                    self.commands[1].dir.y = 1
                    self.commands[1].blastpower = 0.01
        elif job == ShipKind.TYPE_CV:
            self.dir.y = 0
            self.move_interval = 0
            if self.jobclass == self.TYPE_NORMAL:
                self.motionlst.append(IBNK.get("eCV_a")) #(224,0))
                self.motionlst.append(IBNK.get("eCV_b")) #(224,16))
                self.img_bnd.w = IBNK.get("eCV_a").w
                self.img_bnd.h = IBNK.get("eCV_a").h
                self.maxhp = 8
                self.movespeed = 0.75
                self.move_additional_area.left = True
                self.move_additional_area.right =  True
                self.move_additional_area.frequency = pyxel.rndi(100, 150)
                self.move_additional_frame_time = 15
                self.mainattack_interval = pyxel.rndi(100, 120)
                self.commands.append(AttackCommand(AttackCommand.TYPE_AIRCRAFT))
                self.commands[0].blastpower = 0.01
                self.commands[0].dir.y = 1
                self.commands[0].img_bnd.x = 24  
                self.point = 100
                self.alive_time = 30 * 10
                if self.lv == 1:
                    self.move_additional_area.front = True
                    self.move_additional_area.back = True
                elif self.lv == 2:
                    self.maxhp = 10
                    self.point = 150
                    self.mainattack_interval = pyxel.rndi(70, 100)
                    self.commands[0].blastpower = 0.02
                    self.subattack_interval = pyxel.rndi(80, 100)
                    self.commands.append(AttackCommand(AttackCommand.TYPE_AASHOOT))
                    self.commands[1].dir.y = 1
                    self.commands[1].range = 15
                elif self.lv == 3:
                    self.maxhp = 15
                    self.point = 200
                    self.mainattack_interval = pyxel.rndi(50, 100)
                    self.subattack_interval = pyxel.rndi(40, 60)
                    self.commands[0].blastpower = 0.05
                    self.commands.append(AttackCommand(AttackCommand.TYPE_AASHOOT))
                    self.commands[1].dir.y = 1
                    self.commands[1].range = 15
        elif job == ShipKind.TYPE_BC:
            if self.jobclass == self.TYPE_NORMAL:
                self.dir.y = 0
                self.motionlst.append(IBNK.get("eBC_a")) #(208,32))
                self.motionlst.append(IBNK.get("eBC_b")) #(208,64))
                self.img_bnd.w = IBNK.get("eBC_a").w
                self.img_bnd.h = IBNK.get("eBC_a").h
                self.maxhp = 8
                self.move_interval = 0
                self.movespeed = 0.75
                self.move_additional_area.left = True
                self.move_additional_area.right =  True
                self.move_additional_area.front = True
                self.move_additional_area.back = True
                self.move_additional_area.frequency = pyxel.rndi(90, 100)
                self.move_additional_frame_time = 15
                self.mainattack_interval = pyxel.rndi(70, 90)
                self.commands.append(AttackCommand(AttackCommand.TYPE_BBGUN))
                self.commands[0].dir.y = 1
                self.commands[0].power = 2
                self.commands[0].blastpower = 0.01
                self.commands[0].area.left = False
                self.commands[0].area.right = False
                self.point = 80
                self.alive_time = 30 * 15
                if self.lv == 2:
                    self.maxhp = 12
                    self.point = 150
                    self.subattack_interval = pyxel.rndi(100, 150)
                    self.commands.append(AttackCommand(AttackCommand.TYPE_AASHOOT))
                    self.commands[1].dir.y = 1
                elif self.lv == 3:
                    self.maxhp = 15
                    self.point = 220
                    self.subattack_interval = pyxel.rndi(60, 90)
                    self.commands.append(AttackCommand(AttackCommand.TYPE_AASHOOT))
                    self.commands[1].dir.y = 1
        elif job == ShipKind.TYPE_BB:
            if self.jobclass == Enemy.TYPE_NORMAL:
                self.dir.y = 0
                self.motionlst.append(IBNK.get("eBB_a")) #(224,32))
                self.motionlst.append(IBNK.get("eBB_b")) #(224,64))
                self.img_bnd.w = IBNK.get("eBB_a").w
                self.img_bnd.h = IBNK.get("eBB_a").h
                self.maxhp = 10
                self.move_interval = 0
                self.movespeed = 0.5
                self.move_additional_area.left = True
                self.move_additional_area.right =  True
                self.move_additional_area.front = True
                self.move_additional_area.back = True
                self.move_additional_area.frequency = pyxel.rndi(100, 120)
                self.move_additional_frame_time = 10
                self.mainattack_interval = pyxel.rndi(90, 120)
                self.commands.append(AttackCommand(AttackCommand.TYPE_BBGUN))
                self.commands[0].dir.y = 1
                self.commands[0].power = 2
                self.commands[0].blastpower = 0.01
                self.point = 150
                self.alive_time = 30 * 10
                if self.lv == 2:
                    self.maxhp = 15
                    self.point = 250
                    self.commands[0].blastpower = 0.02
                    self.alive_time = 30 * 15
                elif self.lv == 3:
                    self.maxhp = 20
                    self.point = 300
                    self.commands[0].blastpower = 0.05
                    self.alive_time = 30 * 15"""
        
        #--finalize
        if self.lv > 1:
            self.maxhp += self.maxhp // 2 * (self.lv - 1)
        self.hp = self.maxhp
    
    def load(self, typeid: int, data: dict):
        """load enemy data from json
            data - ['eachclass']['normal'][0]
        """
        self.jobtype = typeid
        self.jobclass = data["class"] if "class" in data else self.TYPE_NORMAL
        self.lv = data["lv"] if "lv" in data else 1
        self.maxhp = data["maxhp"] if "maxhp" in data else 1
        if "motionlst" in data:
            for m in data["motionlst"]:
                self.motionlst.append(IBNK.get(m))
            self.img_bnd.w = self.motionlst[0].w
            self.img_bnd.h = self.motionlst[0].h
        self.move_interval = data["move_interval"] if "move_interval" in data else 1
        self.movespeed = data["movespeed"] if "movespeed" in data else 1
        self.dir.x = data["dir"]["x"] if "dir" in data else 0
        self.dir.y = data["dir"]["y"] if "dir" in data else 0
        self.point = data["point"] if "point" in data else 1
        if "move_additional" in data:
            tmp_add = data["move_additional"]
            if "area" in tmp_add:
                tmp_area = tmp_add["area"]
                self.move_additional_area.front = tmp_area["front"] if "front" in tmp_area else False
                self.move_additional_area.front_left = tmp_area["front_left"] if "front_left" in tmp_area else False
                self.move_additional_area.front_right = tmp_area["front_right"] if "front_right" in tmp_area else False
                self.move_additional_area.back = tmp_area["back"] if "back" in tmp_area else False
                self.move_additional_area.back_left = tmp_area["back_left"] if "back_left" in tmp_area else False
                self.move_additional_area.back_right = tmp_area["back_right"] if "back_right" in tmp_area else False
                self.move_additional_area.left = tmp_area["left"] if "left" in tmp_area else False
                self.move_additional_area.right = tmp_area["right"] if "right" in tmp_area else False
            if "frequency" in tmp_add:
                self.move_additional_area.frequency = pyxel.rndi(tmp_add["frequency"][0], tmp_add["frequency"][1])
            else:
                self.move_additional_area.frequency = pyxel.rndi(90, 120)
            if "frame_time" in tmp_add:
                self.move_additional_frame_time = tmp_add["frame_time"]
            else:
                self.move_additional_frame_time = 30
        if "commands" in data:
            cmds = data["commands"]
            for cmd in cmds:
                if "command" in cmd:
                    tmpcmd = cmd["command"] 
                    tmpatc = AttackCommand(tmpcmd["type"])
                    
                    #---change an air craft image
                    if tmpatc.type == AttackCommand.TYPE_AIRCRAFT:
                        tmpatc.img_bnd.x = 24
                    
                    if "interval" in cmd:
                        tmpatc.interval = pyxel.rndi(cmd["interval"][0],cmd["interval"][1])  
                    else:
                        tmpatc.interval = pyxel.rndi(100, 120)
                    #---below is optional edit
                    if "power" in tmpcmd:
                        tmpatc.power = tmpcmd["power"]
                    if "blastpower" in tmpcmd:
                        tmpatc.blastpower = tmpcmd["blastpower"]
                    if "dir" in tmpcmd:
                        tmpatc.dir.x = tmpcmd["dir"]["x"] if "x" in tmpcmd["dir"] else 0
                        tmpatc.dir.y = tmpcmd["dir"]["y"] if "y" in tmpcmd["dir"] else 0
                    if "range" in tmpcmd:
                        tmpatc.range = tmpcmd["range"]
                    if "area" in tmpcmd:
                        tpcmda = tmpcmd["area"]
                        if "left" in tpcmda:
                            tmpatc.area.left = tpcmda["left"]
                        if "right" in tpcmda:
                            tmpatc.area.right = tpcmda["right"]
                        if "front" in tpcmda:
                            tmpatc.area.front = tpcmda["front"]
                        if "front_left" in tpcmda:
                            tmpatc.area.front_left = tpcmda["front_left"]
                        if "front_right" in tpcmda:
                            tmpatc.area.front_right = tpcmda["front_right"]
                        if "back" in tpcmda:
                            tmpatc.area.back = tpcmda["back"]
                        if "back_left" in tpcmda:
                            tmpatc.area.back_left = tpcmda["back_left"]
                        if "back_right" in tpcmda:
                            tmpatc.area.back_right = tpcmda["back_right"]
                    self.commands.append(tmpatc)
                    self.cur_shots.append([])
        self.alive_time = data["alive_time"] * 30 if "alive_time" in data else 0
        self.max_count = data["max_count"] if "max_count" in data else 0
        
    def damage(self, ismain:bool, isblast:bool, shot: AttackCommand = None):
        if shot is not None:
            if ismain:
                self.hp -= shot.power
            if isblast:
                self.hp -= shot.blastpower
        else:
            #---collision damage
            self.hp -= 0.5
            
        self.is_halftransparency = True
        self.start_transparency = pyxel.frame_count
        
    def is_defeat(self):
        if self.hp <= 0:
            return True
        else:
            return False
        
    def receive_attack(self, shot: AttackCommand):
        ishit = {
            "main" : False,
            "blast" : False
        }
        fnlhit = False
        #---shot's collision area
        tmpshot = Bounds(shot.x, shot.y, shot.x+shot.img_bnd.w, shot.y+shot.img_bnd.h)
        if shot.type == AttackCommand.TYPE_MISSILE:
            #print(f"IMPACT missile attack id={id(shot)}")
            fnlhit = shot.impact_missle()
            #if fnlhit:
            #    print(f"IMPACT enemy id={id(self)}, x={self.x}, y={self.y}, w={self.x + self.img_bnd.w}, h={self.y + self.img_bnd.h}")
            #    print(f"IMPACT    shot x={tmpshot.x},y={tmpshot.y},w={tmpshot.w},h={tmpshot.h}")        
        else:
            fnlhit = True
            fnlhit = shot.effective_against(self.jobtype)
            

        if fnlhit:
            #---directly hit
            selfleft = self.x
            selfright = self.x + self.img_bnd.w
            selftop = self.y
            selfbottom = self.y + self.img_bnd.h
            #if shot.x+shot.img_bnd.w > selfleft and selfright > shot.x and shot.y+shot.img_bnd.h > selftop and selfbottom > shot.y:
            if calc_collision(selfleft, selfright, selftop, selfbottom, 
                              shot.x, shot.x+shot.img_bnd.w, shot.y, shot.y+shot.img_bnd.h
            ):
                ishit["main"] = True
            #if (abs(shot.x - self.x) < self.img_bnd.w and abs(shot.y - self.y) < self.img_bnd.h):
            #    ishit["main"] = True
            
            #---blast hit
            newpos = Vector2(shot.x, shot.y)
            if shot.area.front:
                newpos.x = shot.x
                newpos.y = shot.y + shot.img_bnd.h * shot.dir.y
                #ishit["blast"] = (abs(newpos.x - self.x) < self.img_bnd.w and abs(newpos.y - self.y) < self.img_bnd.h)
                ishit["blast"] = calc_collision(selfleft, selfright, selftop, selfbottom, 
                              newpos.x, newpos.x+shot.img_bnd.w, newpos.y, newpos.y+shot.img_bnd.h
                )
                if ishit["blast"]:
                    print("front hit!")
            
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
    
    def death(self):
        self.shots_main.clear()
        self.commands.clear()
        self.will_destroy = True
        
    def update(self, player):
        #---normally moving
        if self.move_interval > 0:
            if pyxel.frame_count % self.move_interval == 0:
                self.y += (self.dir.y * self.movespeed)
                self.x += (self.dir.x * self.movespeed)
        
        if pyxel.frame_count % 15 == 0:
            self.motioninx += 1
            if self.motioninx > 1:
                self.motioninx = 0
        
        #---additional moving
        topdown = pyxel.rndi(0, 2)
        if topdown == 1 and not self.is_moving.front and self.move_additional_area.front and pyxel.frame_count % self.move_additional_area.frequency == 0:
            self.is_moving.clear_dir()
            self.is_moving.front = True
            self.move_additional_current_frame = 0
        if topdown == 2 and not self.is_moving.back and self.move_additional_area.back and pyxel.frame_count % self.move_additional_area.frequency == 0:
            self.is_moving.clear_dir()
            self.is_moving.back = True
            self.move_additional_current_frame = 0
            
        leftright = pyxel.rndi(0, 2)
        if leftright == 1 and not self.is_moving.left and self.move_additional_area.left and pyxel.frame_count % self.move_additional_area.frequency == 0:
            self.is_moving.clear_dir()
            self.is_moving.left = True
            self.move_additional_current_frame = 0
        if leftright == 2 and not self.is_moving.right and self.move_additional_area.right and pyxel.frame_count % self.move_additional_area.frequency == 0:
            self.is_moving.clear_dir()
            self.is_moving.right = True
            self.move_additional_current_frame = 0
        #---additional move effective calc
        if self.is_moving.front:
            if self.move_additional_current_frame <= self.move_additional_frame_time:
                self.y += (1 * self.movespeed)
            else:
                self.is_moving.front = False
            self.move_additional_current_frame += 1
        elif self.is_moving.back:
            if self.move_additional_current_frame <= self.move_additional_frame_time:
                self.y += (-1 * self.movespeed)
            else:
                self.is_moving.back = False
            self.move_additional_current_frame += 1
            
        if self.is_moving.right:
            if self.move_additional_current_frame <= self.move_additional_frame_time:
                self.x += (1 * self.movespeed)
            else:
                self.is_moving.right = False
            self.move_additional_current_frame += 1
        elif self.is_moving.left:
            if self.move_additional_current_frame <= self.move_additional_frame_time:
                self.x += (-1 * self.movespeed)
            else:
                self.is_moving.left = False
            self.move_additional_current_frame += 1
                  
        if self.x < -4:
            self.x = -4
        if self.x > pyxel.width - 4 :
            self.x = pyxel.width - 4
            
          
        #---attack
        """if len(self.commands) > 0:
            if pyxel.frame_count % self.mainattack_interval == 0 and len(self.shots_main) < self.commands[0].max_count:
                shot = copy.deepcopy(self.commands[0])
                shot.x = self.x + self.w // 2
                shot.y = self.y + self.h + shot.img_bnd.h
                shot.init_pos(shot.x, shot.y)
                #print(shot.x, shot.y)
                self.shots_main.append(shot)
            if len(self.commands) > 1:
                if pyxel.frame_count % self.subattack_interval == 0 and len(self.shots_sub) < self.commands[1].max_count:
                    shot = copy.deepcopy(self.commands[1])
                    isshot = True
                    #---enemy sub weapon is depth charge, fire only player is submarine.
                    if shot.type == AttackCommand.TYPE_DEPTHCHARGE and player.job.type != ShipKind.TYPE_SS:
                        isshot = False
                    if isshot:
                        shot.x = self.x + self.w // 2
                        shot.y = self.y + self.h + shot.img_bnd.h
                        shot.init_pos(shot.x, shot.y)
                        #print(shot.x, shot.y)
                        self.shots_sub.append(shot)"""
        #---new code: attack
        if len(self.commands) > 0:
            for cmds in enumerate(self.commands):
                inx = cmds[0]
                cmd = cmds[1]
                if pyxel.frame_count % cmd.interval == 0 and len(self.cur_shots[inx]) < cmd.max_count:
                    shot = copy.deepcopy(cmd)
                    isshot = True
                    #---enemy sub weapon is depth charge, fire only player is submarine.
                    if shot.type == AttackCommand.TYPE_DEPTHCHARGE and player.job.type != ShipKind.TYPE_SS:
                        isshot = False
                    if isshot:
                        shot.x = self.x + self.w // 2
                        shot.y = self.y + self.h + shot.img_bnd.h
                        shot.init_pos(shot.x, shot.y)
                        self.cur_shots[inx].append(shot)
                    
                
            
        #---update shots
        self.update_shots()
        
        #---aliving check
        if self.alive_time > 0:
            if (pyxel.frame_count - self.cur_alive_time_diff) > self.alive_time:
                self.will_destroy = True
        
        return super().update()
    
    def update_shots(self):
        #---this enemy's shot dead or alive ?
        """for shot in self.shots_main.copy():
            shot.update()
            if shot.check_range():
                #self.shots.remove(shot)
                shot.destroy()
        
        #---this enemy's shot dead or alive ?
        for shot in self.shots_sub.copy():
            shot.update()
            if shot.check_range():
                #self.shots.remove(shot)
                shot.destroy()"""
        
        for shots in self.cur_shots:
            for shot in shots.copy():
                shot.update()
                if shot.check_range():
                    shot.destroy()
        
        #---GC shot
        """for s in self.shots_main.copy():
            if s.will_destroy:
                self.shots_main.remove(s)
                
        for s in self.shots_sub.copy():
            if s.will_destroy:
                self.shots_sub.remove(s)"""
        
        for shots in self.cur_shots:
            for s in shots.copy():
                if s.will_destroy:
                    shots.remove(s)
        
    def draw(self):
        if self.is_halftransparency:
            if abs(pyxel.frame_count - self.start_transparency) <= self.during_transparency:
                if pyxel.frame_count % 2 == 0:
                    pyxel.dither(0.5)
                else:
                    pyxel.dither(1.0)
            else:
                self.is_halftransparency = False
                pyxel.dither(1.0)
                
        motpage = self.motionlst[self.motioninx]
        if self.lv == 2:
            pyxel.pal(pyxel.COLOR_PURPLE, pyxel.COLOR_YELLOW)
        elif self.lv == 3:
            pyxel.pal(pyxel.COLOR_PURPLE, pyxel.COLOR_RED)
        pyxel.blt(self.x, self.y, self.img_page, motpage.x, motpage.y, self.img_bnd.w, self.img_bnd.h, pyxel.COLOR_GREEN)
        pyxel.dither(1.0)
        pyxel.pal()
        
        
        
        """for shot in self.shots_main:
            shot.draw()
            
        for shot in self.shots_sub:
            shot.draw()"""
        
        for shots in self.cur_shots:
            for shot in shots:
                shot.draw()
            
        return super().draw()