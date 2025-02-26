import copy
import pyxel
from mycls import GameObject, ShipJob, AttackCommand, BaseEffect, Bounds,  calc_collision, Vector2, Item
from appconst import PLAYER_MOTION

MAXLV = 4

class Player(GameObject):    
    def __init__(self, app, x, y):
        super().__init__(app, x, y)
        self.lv = 1
        self.hp = 0
        self.maxhp = 0
        self.is_middamage = False
        self.is_death = False
        self.movespeed = 1
        self.job: ShipJob = None
        self.shots_main: list[AttackCommand] = []
        self.shots_sub: list[AttackCommand] = []
        self.motionlst = PLAYER_MOTION
        self.buff = {
            "boost" : 0,
            "invincible" : 0,
            "rader1" : 0,
            "rader2" : 0,
            "shield" : 0
        }
        self.invincible_effect = BaseEffect(self.x, self.y-16)
        self.invincible_effect.motionlst = [Bounds(16,40,16,16),Bounds(14,48,16,16)]
    
    def reset_states(self):
        self.buff = {
            "boost" : 0,
            "invincible" : 0,
            "rader1" : 0,
            "rader2" : 0,
            "shield" : 0
        }
        self.is_middamage = False
        self.is_death = False
        
    def setup_job(self,job: int, equiptype: int = 0):
        self.job = ShipJob(job, equiptype)
        self.lv = 1
        self.img_bnd.x = self.job.img_bnd.x
        self.img_bnd.w = 16
        self.img_bnd.h = 16
        self.hp = self.job.maxhp
        self.maxhp = self.job.maxhp
        self.is_middamage = False
    
    def level_up(self):
        if self.lv < MAXLV:
            self.lv += 1
            self.maxhp = self.maxhp + pyxel.rndi(1, 5)
            if self.maxhp >= 100:
                self.maxhp = 99
            self.job.movespeed += 0.25
            #self.job.commands[0].power += 0.5
            #self.job.commands[1].power += 0.25
            self.job.level_up(self.lv)
    
    def healing(self, value):
        self.hp += value
        if self.hp > self.maxhp:
            self.hp = self.maxhp
        if (self.hp / self.maxhp) <= 0.5:
            self.is_middamage = True
        else:
            self.is_middamage = False
        
    def damage(self, ismain:bool, isblast:bool, shot: AttackCommand = None):
        if self.hp == 0:
            return

        if shot is not None:
            if ismain:
                if self.check_buff("shield"):
                    self.hp -= (shot.power / 2)
                else:    
                    self.hp -= shot.power
            if isblast:
                if self.check_buff("shield"):
                    self.hp -= (shot.blastpower / 2)
                else:
                    self.hp -= shot.blastpower
        else:
            self.hp -= 1
        
        
        
        self.is_halftransparency = True
        self.start_transparency = pyxel.frame_count
        
        if self.hp > 0:
            if (self.hp / self.maxhp) <= 0.5:
                self.is_middamage = True
            else:
                self.is_middamage = False
        elif self.hp < 0:
            self.hp = 0
        
    def is_dead(self):
        if self.hp <= 0:
            self.is_death = True
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
            fnlhit = shot.effective_against(self.job.type)
            
            #---buff:invincible
            if self.check_buff("invincible"):
                fnlhit = False

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
        if not self.parent.is_test:
            self.job.destroy()
    
    def set_buff(self, bufftype, bufftime):
        if bufftype == Item.TYPE_BOOST:
            self.buff["boost"] = bufftime
        elif bufftype == Item.TYPE_INVINCIBLE:
            self.buff["invincible"] = bufftime
        elif bufftype == Item.TYPE_RADER_1:
            self.buff["rader1"] = bufftime
        elif bufftype == Item.TYPE_RADER_2:
            self.buff["rader2"] = bufftime
        elif bufftype == Item.TYPE_SHIELD:
            self.buff["shield"] = bufftime
    
    def count_buff(self, bufname):
        if bufname in self.buff:
            if pyxel.frame_count % 30 == 0:
                self.buff[bufname] -= 1
                
            if self.buff[bufname] <= 0:
                self.buff[bufname] = 0
        
    def check_buff(self, bufname):
        if bufname in self.buff:
            if self.buff[bufname] <= 0:
                return False
            else:
                return True
        else:
            return False
        
    def shooting_main(self, option: dict = {}):
        if len(self.shots_main) < self.job.commands[0].max_count:
            shot: AttackCommand = copy.deepcopy(self.job.commands[0])
            shot.x = self.x + self.w // 2
            shot.y = self.y - shot.h
            shot.init_pos(shot.x, shot.y)
            
            if shot.first_x[0] != 0 and shot.first_x[2] != 0:
                if len(self.shots_main) > 0:
                    rndi = pyxel.rndi(shot.first_x[0],shot.first_x[2]) * 4
                    shot.x += rndi
                    shot.init_pos(shot.x, shot.y)
                print(f"{shot.x}:{shot.y}")
            
            if shot.fired_x[0] != 0 and shot.fired_x[1] != 0:
                shot.dir.x = pyxel.rndf(shot.fired_x[0], shot.fired_x[1])
            
            if shot.type == AttackCommand.TYPE_MISSILE:
                if "missile_cursor" in option:
                    shot.focus.x = option["missile_cursor"].x
                    shot.focus.y = option["missile_cursor"].y
                    #print(shot.focus.x, shot.focus.y)
                if len(self.shots_main) > 0:
                    rndi = shot.fired_x.copy()
                    shot.focus.x += (rndi[pyxel.rndi(0,2)] * 8)
                    shot.focus.y += (rndi[pyxel.rndi(0,2)] * 8)
                    #print("   ->",shot.focus.x, shot.focus.y)
            self.shots_main.append(shot)
            return True
        else:
            return False
    
    def shooting_sub(self):
        if len(self.shots_sub) < self.job.commands[1].max_count:
            shot: AttackCommand = copy.deepcopy(self.job.commands[1])
            shot.x = self.x + self.w // 2
            shot.y = self.y - shot.h
            shot.init_pos(shot.x, shot.y)
            
            #if shot.type == AttackCommand.TYPE_AASHOOT:
            if shot.fired_x[0] != 0 and shot.fired_x[1] != 0:
                shot.dir.x = pyxel.rndf(shot.fired_x[0], shot.fired_x[1])
            self.shots_sub.append(shot)
            return True
        else:
            return False

    def update(self):
        
        if self.dir.x == 1:
            self.img_bnd.y = self.motionlst["right_move"]
        elif self.dir.x == -1:
            self.img_bnd.y = self.motionlst["left_move"]
        else:
            self.img_bnd.y = self.motionlst["down"]
        
        #---change normal/damaged image index
        if self.is_middamage and not self.is_death:
            self.img_bnd.y += 96
        
        if self.is_death and not self.parent.is_test:
            self.img_bnd.y = self.motionlst["dead"]
        
        self.x += (self.job.movespeed *  self.dir.x)
        self.y += (self.job.movespeed * self.dir.y)
        if self.check_buff("boost"):
            #---first effect: speed up
            self.x += (self.job.movespeed *  self.dir.x)
            self.y += (self.job.movespeed * self.dir.y)

            
        if self.check_buff("invincible"):
            self.invincible_effect.motioninx += 1
            if self.invincible_effect.motioninx > 1:
                self.invincible_effect.motioninx = 0
            
        self.count_buff("boost")
        self.count_buff("invincible")
        self.count_buff("rader1")
        self.count_buff("rader2")
        self.count_buff("shield")
        
    def update_shots(self):
        #---loop shot
        for shot in self.shots_main.copy():
            shot.update()
            if shot.y <= 0 or shot.check_range():
                #self.shots_main.remove(shot)
                shot.destroy()
            
            shot.effect_buff("boost", self.buff["boost"])
            shot.effect_buff("rader1", self.buff["rader1"])
                
        for shot in self.shots_sub.copy():
            shot.update()
            if shot.y <= 0 or shot.check_range():
                #self.shots_sub.remove(shot)
                shot.destroy()
            shot.effect_buff("boost", self.buff["boost"])            
            shot.effect_buff("rader2", self.buff["rader2"])

        #---GC shot
        for s in self.shots_main.copy():
            if s.will_destroy:
                self.shots_main.remove(s)
        for s in self.shots_sub.copy():
            if s.will_destroy:
                self.shots_sub.remove(s)
        
        return super().update()
        
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
        pyxel.blt(
            self.x, self.y,
            self.img_page,
            self.img_bnd.x, self.img_bnd.y, self.img_bnd.w, self.img_bnd.h,
            self.img_transparent
        )
        pyxel.dither(1.0)
        
        if self.check_buff("invincible"):
            inv: Bounds = self.invincible_effect.motionlst[self.invincible_effect.motioninx]
            pyxel.blt(self.x, self.y - 8, 0, inv.x, inv.y, inv.w, inv.h, pyxel.COLOR_BLACK)
        
        for shot in self.shots_main:
            shot.draw()
        
        for shot in self.shots_sub:
            shot.draw()
