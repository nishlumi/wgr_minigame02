import pyxel
import copy
import json
from typing import TypedDict
from myscene import GameScene
from myconfig import GameOperator
from mycls import ShipJob, AttackCommand, BaseEffect, ExplodeEffect, ItemEffect, LevelEffect, Bounds, pos, center_x, check_mouse_playscreen, GamePoint, Vector2, Item
from enemycls import Enemy
from player import Player
from appconst import SINGLE_FONTSIZE, MAP_SEA1, ShipKind, GameMode, CSV_RANK_IMAGE, CSV_TIMEATTACK_APPEAR_RATE, CSV_TIMEATTACK_APPEAR_LV, CSV_TIMEATTACK_TIME
from myui import GameUI, GUIText, GUIImage, GUICheckbox, GUIButton, GUIPauseButton
from imgbnk import IBNK

class MainStageScene(GameScene):
    def __init__(self, app: GameOperator):
        super().__init__(app)
        self.player = Player(app, 0, 0)
        
        
        self.reset_game(0)
        self.setup_ui()
        #self.sound = SoundManager()
    
    def setup_ui(self):
        retimg = self.parent.imgbnk.get("larrow")
        curry1 = IBNK.get("curry1")
        curry2= IBNK.get("curry2")
        rader1 = IBNK.get("rader1")
        rader2 = IBNK.get("rader2")
        shield = IBNK.get("shield")
        self.ui = {
            "return": GUIImage(pos(0)+4,pos(0)+4,retimg.page, Bounds(retimg.x, retimg.y, retimg.w, retimg.h),pyxel.COLOR_BLACK),
            "txt_point": GUIText(f"Point:",pos(1),pos(1),color1=pyxel.COLOR_WHITE,color2=pyxel.COLOR_BLACK,shifted_x=1),
            "inp_point": GUIText("0",pos(4),pos(1),color1=pyxel.COLOR_WHITE,color2=pyxel.COLOR_BLACK,shifted_x=1),
            "txt_time": GUIText(f"Time:",pos(9),pos(1),color1=pyxel.COLOR_WHITE,color2=pyxel.COLOR_BLACK,shifted_x=1),
            "inp_time": GUIText("0",pos(12),pos(1),color1=pyxel.COLOR_WHITE,color2=pyxel.COLOR_BLACK,shifted_x=1),
            "txt_hp": GUIText(f"HP:",pos(8),pos(18)+4,color1=pyxel.COLOR_WHITE, font=self.parent.jp_font10),
            "inp_hp": GUIText("",pos(10),pos(18)+4,color1=pyxel.COLOR_WHITE, font=self.parent.jp_font10),
            "inp_maxhp": GUIText("",pos(12),pos(18)+4,color1=pyxel.COLOR_WHITE, font=self.parent.jp_font10),
            "txt_lv": GUIText(f"Lv:",pos(8),pos(18),color1=pyxel.COLOR_WHITE),
            "inp_lv": GUIText(f"",pos(10),pos(18),color1=pyxel.COLOR_WHITE),
            "img_buffboost" : GUIImage(pos(0), pos(18), curry1.page, Bounds(curry1),pyxel.COLOR_BLACK),
            "inp_buffboost": GUIText("0",pos(1),pos(18),color1=pyxel.COLOR_RED),
            "img_buffinvincible" : GUIImage(pos(0), pos(19), curry2.page, Bounds(curry2),pyxel.COLOR_BLACK),
            "inp_buffinvincible": GUIText("0",pos(1),pos(19),color1=pyxel.COLOR_RED),
            "img_buffrader1" : GUIImage(pos(2)+4, pos(18), rader1.page, Bounds(rader1),pyxel.COLOR_BLACK),
            "inp_buffrader1": GUIText("0",pos(3)+4,pos(18),color1=pyxel.COLOR_RED),
            "img_buffrader2" : GUIImage(pos(2)+4, pos(19), rader2.page, Bounds(rader2),pyxel.COLOR_BLACK),
            "inp_buffrader2": GUIText("0",pos(3)+4,pos(19),color1=pyxel.COLOR_RED),
            "img_buffshield" : GUIImage(pos(5)+4, pos(18), shield.page, Bounds(shield),pyxel.COLOR_BLACK),
            "inp_buffshield": GUIText("0",pos(6)+4,pos(18),color1=pyxel.COLOR_RED),
            "btn_pause" : GUIButton("=", pos(14), pos(0)+4, 8, 8, font=self.parent.jp_fontmisaki)
        }
        
        super().setup_ui()
        self.ui["return"].selectable = True
        
        self.ui["inp_point"].is_wrap = False
        self.ui["img_buffboost"].img_bnd.w = 8
        self.ui["img_buffinvincible"].img_bnd.w = 8
        self.ui["img_buffrader2"].img_bnd.w = 8
        self.ui["img_buffrader2"].img_bnd.h = 8
        
            
    def setup_player(self, job: int, equiptype: int = 0):
        print("job=",job)
        self.player.setup_job(job, equiptype)
        self.player.shots_main.clear()
        self.player.shots_sub.clear()
        self.player.x = center_x()-self.player.w // 2
        self.player.y = pos(16)-2
        self.player.reset_states()
        print("x=", self.player.x)
        print("y=", self.player.y)
        
    def reset_game(self, gamemode: int):
        self.gamemode = gamemode
        if self.gamemode == GameMode.TYPE_TIMEATTACK:
            #self.enemydata = CSV_TIMEATTACK_APPEAR_RATE
            #self.enemylvdata = CSV_TIMEATTACK_APPEAR_LV
            self.play_time_dir = -1
            self.play_time = CSV_TIMEATTACK_TIME[self.parent.states.timeattack_time]
            #---new code
            tmdt = self.parent.data_man.timeattack_data["appear"][self.parent.states.timeattack_enemies]
            ##---{id: str, wave: [{time: int, frame_interval: int, eachtype: {...}, eachclass: {...} } ] }
            self.enemydata = tmdt
            self.enemylvdata = self.parent.data_man.timeattack_data["lv"]
        elif self.gamemode == GameMode.TYPE_SURVIVAL:
            #print(self.parent.states.survival_enemies)
            #print(self.enemydata)
            self.enemydata = self.parent.data_man.survival_data["appear"][self.parent.states.survival_enemies]
            self.enemylvdata = CSV_TIMEATTACK_APPEAR_LV
            self.play_time = 0
            self.play_time_dir = 1
            self.play_wave = 0
            self.play_wave_time = self.enemydata["wave"][0]["time"]
            self.summary_wave_count = 0
        self.states = TypedDict
        self.states.is_gameend = False
        self.states.is_pause = False
        self.states.gameend_interval = 0
        self.states.is_success = False
        self.states.is_fail = False
        self.states.debuff_appear = {
            "enabled" : False,
            "remain_time" : 10,
        }
        self.states.result = {
            "drawtime" : 15,
            "ranktime" : 30,
            "curdraw" : 0,
            "is_drawend" : False,
            "is_rankend" : False,
            "classpoint" : [],
            "userrank" : 0,
        }
        self.points = GamePoint()
        for i in range(0, len(ShipKind.LIST)):
            self.states.result["classpoint"].append([
                [0, 0], #---normal(cur, max)
                [0, 0], #---enhanced(cur, max)
                [0, 0]  #---super(cur, max)
            ])
        
        self.damecons: list[Item] = []
        self.enemies: list[Enemy] = []
        self.explodes: list[BaseEffect] = []
        #---player shots
        #self.shots_main: list[AttackCommand] = []
        #self.shots_sub: list[AttackCommand] = []
        #---map wave effect
        maxline = 19
        self.waves = []
        self.scroll_waves = []
        for i in enumerate("a"*maxline):
            ln = []
            lnrnd = pyxel.rndi(1, 100)
            #---randomize line
            if lnrnd > 50:
                for j in enumerate("b"*16):
                    jhit_wave = pyxel.rndi(1, 100)
                    #---randomize cell
                    if len(ln) < 15:
                        if jhit_wave > 30:
                            ln.append((0,0))
                        else:
                            ln.append((8,32))
            self.scroll_waves.append(0)
            self.waves.append({
                "massy" : i[0],
                "dotty" : 8 * i[0],
                "animate" : 0,
                "animate_dir" : 1,
                "csv" : ln
            })
        self.missile_cursor = Vector2(0, 0)
    
    def generate_item(self):
        if len(self.damecons) > 0:
            return
        
        rndx = pyxel.rndi(0, pyxel.width - 8)
        if (self.player.hp / self.player.maxhp) < 0.4:
            rnd_hpfull = pyxel.rndi(1, 100)
            rndmax = self.parent.states.appear_damecon[1]
            if self.parent.states.current_gamemode == GameMode.TYPE_SURVIVAL:
                rndmax = 1
            if self.parent.states.appear_damecon[0] <= rnd_hpfull <= rndmax:
                self.damecons.append(Item(self, Item.TYPE_HPFULL, rndx, 0))
                return
            
        rndx = pyxel.rndi(0, pyxel.width - 8)
        if (self.player.hp / self.player.maxhp) < 0.7:
            rnd_hphalf = pyxel.rndi(1, 100)
            rndmax = self.parent.states.appear_juice[1]
            if self.parent.states.current_gamemode == GameMode.TYPE_SURVIVAL:
                rndmax = 5
            if self.parent.states.appear_juice[0] <= rnd_hphalf <= rndmax:
                print("    juice!")
                self.damecons.append(Item(self, Item.TYPE_HPHALF, rndx, 0))
                return
        
        rndx = pyxel.rndi(0, pyxel.width - 8)
        rnd_boost = pyxel.rndi(1, 100)
        if self.parent.states.appear_curry[0] <= rnd_boost <= self.parent.states.appear_curry[1]:
            self.damecons.append(Item(self, Item.TYPE_BOOST, rndx, 0))
            return
        
        rndx = pyxel.rndi(0, pyxel.width - 8)
        rnd_invincible = pyxel.rndi(1, 100)
        if self.parent.states.appear_redcurry[0] <= rnd_invincible <= self.parent.states.appear_redcurry[1]:
            self.damecons.append(Item(self, Item.TYPE_INVINCIBLE, rndx, 0))
            return
        
        rndx = pyxel.rndi(0, pyxel.width - 8)
        rnd_rader = pyxel.rndi(1, 100)
        if self.parent.states.appear_rader1[0] <= rnd_rader <= self.parent.states.appear_rader1[1]:
            self.damecons.append(Item(self, Item.TYPE_RADER_1, rndx, 0))
            return
        
        rndx = pyxel.rndi(0, pyxel.width - 8)
        rnd_rader = pyxel.rndi(1, 100)
        if self.parent.states.appear_rader2[0] <= rnd_rader <= self.parent.states.appear_rader2[1]:
            self.damecons.append(Item(self, Item.TYPE_RADER_2, rndx, 0))
            
        rndx = pyxel.rndi(0, pyxel.width - 8)
        rnd_shield = pyxel.rndi(1, 100)
        if self.parent.states.appear_shield1[0] <= rnd_shield <= self.parent.states.appear_shield1[1]:
            self.damecons.append(Item(self, Item.TYPE_SHIELD, rndx, 0))

        rndx = pyxel.rndi(0, pyxel.width - 8)
        rnd_cat = pyxel.rndi(1, 100)
        if self.parent.states.appear_cat[0] <= rnd_cat <= self.parent.states.appear_cat[1]:
            self.damecons.append(Item(self, Item.TYPE_LEVELUP, rndx, 0))
            
        if not self.states.debuff_appear["enabled"]:
            rndx = pyxel.rndi(0, pyxel.width - 8)
            rnd_gold = pyxel.rndi(1, 100)
            if self.parent.states.appear_goldbox[0] <= rnd_gold <= self.parent.states.appear_goldbox[1]:
                self.damecons.append(Item(self, Item.TYPE_GOLDBOX, rndx, 0))
        
    def generate_enemy_each(self, ratevalue: int, appearlv: int, rnx: float, rny: float, csvkey: list, lencsv: int, wavedict: dict):
        for e in range(0, lencsv):
            erate = wavedict["eachtype"][csvkey[e]]
            
            #---judge class (each type loop...)
            classrate = wavedict["eachclass"][csvkey[e]]
            clsrnd = pyxel.rndi(1, 100)
            clstype = -1
            if classrate[Enemy.TYPE_NORMAL][0] <= clsrnd <= classrate[Enemy.TYPE_NORMAL][1]:
                clstype = Enemy.TYPE_NORMAL
            elif classrate[Enemy.TYPE_ENHANCED][0] <= clsrnd <= classrate[Enemy.TYPE_ENHANCED][1]:
                clstype = Enemy.TYPE_ENHANCED
            elif classrate[Enemy.TYPE_SUPER][0] <= clsrnd <= classrate[Enemy.TYPE_SUPER][1]:
                clstype = Enemy.TYPE_SUPER
            
            strate = erate[0]
            edrate = erate[1]
            
            if strate <= ratevalue <= edrate:
                #print(f"appear rate={cnt} ... {csvkey[e]} by {pyxel.frame_count}")
                finaltype = -1
                if csvkey[e] == "CL":
                    finaltype = ShipKind.TYPE_CL
                elif csvkey[e] == "CA":
                    finaltype = ShipKind.TYPE_CA
                elif csvkey[e] == "CVL":
                    finaltype = ShipKind.TYPE_CVL
                elif csvkey[e] == "CV":
                    finaltype = ShipKind.TYPE_CV
                elif csvkey[e] == "BC":
                    finaltype = ShipKind.TYPE_BC
                elif csvkey[e] == "BB":
                    finaltype = ShipKind.TYPE_BB
                elif csvkey[e] == "SS":
                    finaltype = ShipKind.TYPE_SS
                elif csvkey[e] == "DD":
                    finaltype = ShipKind.TYPE_DD
                    
                cntchke = 0
                for chke in self.enemies:
                    if chke.jobtype == finaltype:
                        cntchke += 1
                em = Enemy(self.parent, finaltype, clstype, appearlv, rnx, rny)
                if em.max_count > 0:
                    if cntchke > em.max_count:
                        return
                self.enemies.append(em)
                self.points.eachtype[finaltype].add_max(em.jobclass, em.lv-1, 1)
        
    def generate_enemy(self):
        #---new code
        if self.parent.states.current_gamemode == GameMode.TYPE_TIMEATTACK:
            #---remain time is less than 3, don't appear an enemy.
            if self.play_time < 3:
                return

            finterval = self.enemydata["wave"][0]["frame_interval"]
            if self.states.debuff_appear["enabled"]:
                finterval /= 2
                
            #--- timeattack is wave 0
            if pyxel.frame_count % finterval == 0:
                typernd = pyxel.rndi(1, 100)
                rnx = pyxel.rndi(8, pyxel.width-8)
                rny = pyxel.rndi(1, 3) * 8
                lvrnd = pyxel.rndi(1, 100)
                lvcheck = self.enemylvdata[self.parent.states.timeattack_firstlv]
                
                #---judge lv
                appearlv = 1
                for l in enumerate(lvcheck):
                    if l[1][0] <= lvrnd <= l[1][1]:
                        appearlv = l[0] + 1
                
                #---judge ship type
                csvkey = list(self.enemydata["wave"][0]["eachtype"].keys())
                lencsv = len(csvkey)
                self.generate_enemy_each(typernd, appearlv, rnx, rny, csvkey, lencsv, self.enemydata["wave"][0])
        elif self.parent.states.current_gamemode == GameMode.TYPE_SURVIVAL:
            wave = self.enemydata["wave"][self.play_wave]
            #---if wave finish, go to next wave
            if self.play_time > self.play_wave_time:
                self.play_wave += 1
                self.summary_wave_count += 1
                #---data is defined last wave only.
                if self.play_wave >= len(self.enemydata["wave"]):
                    self.play_wave = len(self.enemydata["wave"]) - 1
                self.play_wave_time += wave["time"]
                
                self.player.level_up()
                self.parent.sound.play_levelup()
                self.explodes.append(LevelEffect(self.player.x, self.player.y))
            

            finterval = wave["frame_interval"]
            if self.states.debuff_appear["enabled"]:
                finterval /= 2
                
            if pyxel.frame_count % finterval == 0:
                typernd = pyxel.rndi(1, 100)
                rnx = pyxel.rndi(8, pyxel.width-8)
                rny = pyxel.rndi(1, 3) * 8
                lvrnd = pyxel.rndi(1, 100)
                lvcheck = wave["eachlv"]
                
                #---judge lv
                appearlv = 1
                for l in enumerate(lvcheck):
                    if l[1][0] <= lvrnd <= l[1][1]:
                        appearlv = l[0] + 1
                
                #---judge ship type
                csvkey = list(wave["eachtype"].keys())
                lencsv = len(csvkey)
                self.generate_enemy_each(typernd, appearlv, rnx, rny, csvkey, lencsv, wave)
        return
        if pyxel.frame_count % self.parent.states.timeattack_appear_interval == 0:
            cnt = pyxel.rndi(1, 100)
            
            rnx = pyxel.rndi(8, pyxel.width-8)
            rny = pyxel.rndi(1, 3) * 8
            
            #---code
            lvrnd = pyxel.rndi(1, 100)
            lvcheck = self.enemylvdata[self.parent.states.timeattack_firstlv]
            appearlv = 1
            for l in enumerate(lvcheck):
                if l[1][0] <= lvrnd <= l[1][1]:
                    appearlv = l[0] + 1
            
            csvkey = list(self.enemydata.keys())
            lencsv = len(csvkey)
            strate = 0
            edrate = 0
            for e in range(0, lencsv):
                erate = self.enemydata[csvkey[e]]
                
                strate = erate[self.parent.states.timeattack_enemies][0]
                edrate = erate[self.parent.states.timeattack_enemies][1]
                
                if strate <= cnt <= edrate:
                    #print(f"appear rate={cnt} ... {csvkey[e]} by {pyxel.frame_count}")
                    if csvkey[e] == "CL":
                        em = Enemy(self.parent, ShipKind.TYPE_CL, Enemy.TYPE_NORMAL, appearlv, rnx, rny)
                        self.enemies.append(em)
                        self.points.eachtype[ShipKind.TYPE_CL].add_max(em.jobclass, em.lv-1, 1)
                    elif csvkey[e] == "CA":
                        em = Enemy(self.parent, ShipKind.TYPE_CA, Enemy.TYPE_NORMAL, appearlv, rnx, rny)
                        self.enemies.append(em)                        
                        self.points.eachtype[ShipKind.TYPE_CA].add_max(em.jobclass, em.lv-1, 1)
                    elif csvkey[e] == "CVL":
                        em = Enemy(self.parent, ShipKind.TYPE_CVL, Enemy.TYPE_NORMAL, appearlv, rnx, rny)
                        self.enemies.append(em)
                        self.points.eachtype[ShipKind.TYPE_CVL].add_max(em.jobclass, em.lv-1, 1)
                    elif csvkey[e] == "CV":
                        em = Enemy(self.parent, ShipKind.TYPE_CV, Enemy.TYPE_NORMAL, appearlv, rnx, rny)
                        self.enemies.append(em)
                        self.points.eachtype[ShipKind.TYPE_CV].add_max(em.jobclass, em.lv-1, 1)
                    elif csvkey[e] == "BC":
                        em = Enemy(self.parent, ShipKind.TYPE_BC, Enemy.TYPE_NORMAL, appearlv, rnx, rny)
                        self.enemies.append(em)
                        self.points.eachtype[ShipKind.TYPE_BC].add_max(em.jobclass, em.lv-1, 1)
                    elif csvkey[e] == "BB":
                        em = Enemy(self.parent, ShipKind.TYPE_BB, Enemy.TYPE_NORMAL, appearlv, rnx, rny)
                        self.enemies.append(em)
                        self.points.eachtype[ShipKind.TYPE_BC].add_max(em.jobclass, em.lv-1, 1)
                    elif csvkey[e] == "SS":
                        em = Enemy(self.parent, ShipKind.TYPE_SS, Enemy.TYPE_NORMAL, appearlv, rnx, rny)
                        self.enemies.append(em)
                        self.points.eachtype[ShipKind.TYPE_SS].add_max(em.jobclass, em.lv-1, 1)
                    elif csvkey[e] == "DD":
                        clsrnd = pyxel.rndi(1, 100)
                        clstype = Enemy.TYPE_NORMAL
                        if clsrnd < 40:
                            clstype = Enemy.TYPE_ENHANCED
                        em = Enemy(self.parent, ShipKind.TYPE_DD, clstype, appearlv, rnx, rny)
                        self.enemies.append(em)
                        self.points.eachtype[ShipKind.TYPE_DD].add_max(em.jobclass, em.lv-1, 1)
            

    
    def check_shot(self, enemy: Enemy, shots: list[AttackCommand]):
        """Collision check of Shot and Enemy 
        
            args:
                enemy: Enemy current enemy
                
                shots: list[AttackCommand] target shots list
                
        """
        for shot in shots.copy():
            #---cancel shot
            for es in enemy.shots_main.copy():
                eshit = shot.receive_attack(es)
                if eshit["main"]:
                    self.explodes.append(ExplodeEffect(shot.x, shot.y))
                    self.parent.sound.play_damage()
                    #shots.remove(shot)
                    shot.destroy()
                    break
            
            #print("===========================================================")
            ishit = enemy.receive_attack(shot)
            #print(f"    enemy id={id(enemy)}, shot id={id(shot)}")
            if not enemy.will_destroy and (ishit["main"] or ishit["blast"]):
                enemy.damage(ishit["main"], ishit["blast"], shot)
                self.parent.sound.play_damage()
                self.explodes.append(ExplodeEffect(shot.x, shot.y))
                if enemy.is_defeat():
                    enemy.death()
                    self.points.summary += enemy.point
                    self.points.eachtype[enemy.jobtype].add_cur(enemy.jobclass, enemy.lv-1,1)
                    #if self.enemies.count(enemy) > 0:
                    #    self.enemies.remove(enemy)
                if not shot.is_penetrate and ishit["main"]:
                    #---hit main weapon, destroy when collision
                    #shots.remove(shot)
                    shot.destroy()
                else:
                    #---not blast damage, enable penetrate
                    if not ishit["blast"] or (shot.is_destroy_blast and ishit["blast"]):
                        if not shot.is_penetrate:
                            #if shots.count(shot) > 0:
                            #    shots.remove(shot)
                            shot.destroy()
            
            #---additional explode effect
            if shot.type == AttackCommand.TYPE_MISSILE and shot.was_impacted:
                #---explode for missle
                poss = shot.impactarea_missile()
                #print(poss)
                for p in poss:
                    self.explodes.append(ExplodeEffect(p.x, p.y))
                #if shots.count(shot) > 0:
                #    shots.remove(shot)
                shot.destroy()
                self.parent.sound.play_blank_explode()
            elif shot.type == AttackCommand.TYPE_DEPTHCHARGE and (ishit["main"] or ishit["blast"]):
                self.explodes.append(ExplodeEffect(shot.x-shot.img_bnd.w, shot.y))
                self.explodes.append(ExplodeEffect(shot.x+shot.img_bnd.w, shot.y))
    
    def check_enemy_shot(self, shots: list[AttackCommand]):
        for shot in shots.copy():
            #---shot and shot cancel ??? (ex: air craft, asa craft, aashoot vs both craft)
            for ms in self.player.shots_main:
                mshit = shot.receive_attack(ms)
                if mshit["main"] or mshit["blast"]:
                    self.explodes.append(ExplodeEffect(shot.x, shot.y))
                    self.parent.sound.play_damage()
                    #shots.remove(shot)
                    shot.destroy()
                    ms.destroy()
                    break
            if not shot.will_destroy:
                for ss in self.player.shots_sub:
                    sshit = shot.receive_attack(ss)
                    if sshit["main"] or sshit["blast"]:
                        self.explodes.append(ExplodeEffect(shot.x, shot.y))
                        self.parent.sound.play_damage()
                        #shots.remove(shot)
                        shot.destroy()
                        ss.destroy()
                        break
            if not shot.will_destroy:
                ishit = self.player.receive_attack(shot)
                #---submarine is no damage other than Aircraft
                #if self.player.job.type == ShipKind.TYPE_SS:
                #   if shot.type != AttackCommand.TYPE_AIRCRAFT:
                #        ishit["main"] = False
                #        ishit["blast"] = False
                if not self.player.is_dead() and (ishit["main"] or ishit["blast"]):
                    self.player.damage(ishit["main"], ishit["blast"], shot)
                    self.parent.sound.play_damage()
                    if self.player.is_dead():
                        self.player.death()
                    if not shot.is_penetrate:
                        #shots.remove(shot)
                        shot.destroy()
    
    def check_prepare_gameend(self):
        flag = False
        if self.gamemode == GameMode.TYPE_TIMEATTACK:
            if (self.play_time < 0) or (self.player.is_dead() and not self.parent.is_test):
                if not self.states.is_gameend:
                    self.parent.sound.play_gameclear()
                    #---copy to draw result
                    for cls in enumerate(self.points.eachtype):
                        for i in range(0, 3): #classtype: normal, enhanced, super
                            self.states.result["classpoint"][cls[0]][i][0] = cls[1].summary_cur(i)
                            self.states.result["classpoint"][cls[0]][i][1] = cls[1].summary_max(i)
                    self.states.result["userrank"] = self.points.judgement(self.player.is_dead())
                    print(f"commands len={len(self.player.job.commands)}")
                    serjs = self.points.serialize(
                        self.parent.states.current_gamemode,
                        {
                            "lv" : self.player.lv,
                            "hp" : self.player.hp,
                            "maxhp" : self.player.maxhp,
                            "mainwpn" : self.player.job.commands[0].type,
                            "subwpn" : self.player.job.commands[1].type,
                            "time": self.parent.states.timeattack_time,
                            "forces" : self.parent.states.timeattack_enemies,
                            "freqlv" : self.parent.states.timeattack_firstlv,
                        }, self.parent.states.current_date,
                        self.parent.states.current_player,
                        self.player.is_death, self.states.result["userrank"]
                    )
                    self.parent.data_man.set_timeattack_cleardata(self.parent.states.timeattack_time,self.parent.states.timeattack_enemies,serjs)
                    if self.parent.config["save_score"]:
                        self.parent.data_man.save_result()
                    
                self.states.is_gameend = True
                
                
                flag = True
                
                
        elif self.gamemode == GameMode.TYPE_SURVIVAL:
            if self.player.is_dead():
                if not self.states.is_gameend:
                    self.parent.sound.play_gameclear()
                    #---copy to draw result
                    for cls in enumerate(self.points.eachtype):
                        for i in range(0, 3): #classtype: normal, enhanced, super
                            self.states.result["classpoint"][cls[0]][i][0] = cls[1].summary_cur(i)
                            self.states.result["classpoint"][cls[0]][i][1] = cls[1].summary_max(i)
                    self.states.result["userrank"] = self.points.judgement()
                    if self.summary_wave_count < 1:
                        self.states.result["userrank"] = GamePoint.RANK_C
                    elif self.summary_wave_count == 1:
                        self.states.result["userrank"] -= 1
                        if self.states.result["userrank"] < 0:
                            self.states.result["userrank"] = GamePoint.RANK_C
                    serjs = self.points.serialize(
                        self.parent.states.current_gamemode,
                        {
                            "lv" : self.player.lv,
                            "hp" : self.player.hp,
                            "maxhp" : self.player.maxhp,
                            "mainwpn" : self.player.job.commands[0].type,
                            "subwpn" : self.player.job.commands[1].type,
                            "play_time": self.play_time,
                            "wave" : self.summary_wave_count,
                        }, self.parent.states.current_date,
                        self.parent.states.current_player,
                        self.player.is_death, self.states.result["userrank"]
                    )
                    self.parent.data_man.set_survival_cleardata(self.parent.states.survival_enemies, serjs)
                    if self.parent.config["save_score"]:
                        self.parent.data_man.save_result()
                self.states.is_gameend = True
                flag = True
        return flag
    
    def update_status(self):
        self.ui["inp_point"].set_text(f"{self.points.summary}")
        self.ui["inp_time"].set_text(f"{self.play_time}")
        self.ui["inp_hp"].set_text(f"{pyxel.floor(self.player.hp)}")
        self.ui["inp_maxhp"].set_text(f"/ {self.player.maxhp}")
        self.ui["inp_lv"].set_text(f"{self.player.lv}")
        if self.player.buff["boost"] > 0:
            if self.player.buff["boost"] > 3:
                self.ui["inp_buffboost"].color1 = pyxel.COLOR_WHITE
            else:
                self.ui["inp_buffboost"].color1 = pyxel.COLOR_RED
            self.ui["inp_buffboost"].set_text(f"{self.player.buff['boost']:>2}")
        else:
            self.ui["inp_buffboost"].set_text(" 0")
        if self.player.buff["invincible"] > 0:
            if self.player.buff["invincible"] > 3:
                self.ui["inp_buffinvincible"].color1 = pyxel.COLOR_WHITE
            else:
                self.ui["inp_buffinvincible"].color1 = pyxel.COLOR_RED
            self.ui["inp_buffinvincible"].set_text(f"{self.player.buff['invincible']:>2}")
        else:
            self.ui["inp_buffinvincible"].set_text(" 0")
        if self.player.buff["rader1"] > 0:
            if self.player.buff["rader1"] > 3:
                self.ui["inp_buffrader1"].color1 = pyxel.COLOR_WHITE
            else:
                self.ui["inp_buffrader1"].color1 = pyxel.COLOR_RED
            self.ui["inp_buffrader1"].set_text(f"{self.player.buff['rader1']:>2}")
        else:
            self.ui["inp_buffrader1"].set_text(" 0")
        if self.player.buff["rader2"] > 0:
            if self.player.buff["rader2"] > 3:
                self.ui["inp_buffrader2"].color1 = pyxel.COLOR_WHITE
            else:
                self.ui["inp_buffrader2"].color1 = pyxel.COLOR_RED
            self.ui["inp_buffrader2"].set_text(f"{self.player.buff['rader2']:>2}")
        else:
            self.ui["inp_buffrader2"].set_text(" 0")
        if self.player.buff["shield"] > 0:
            if self.player.buff["rader1"] > 3:
                self.ui["inp_buffshield"].color1 = pyxel.COLOR_WHITE
            else:
                self.ui["inp_buffshield"].color1 = pyxel.COLOR_RED
            self.ui["inp_buffshield"].set_text(f"{self.player.buff['shield']:>2}")
        else:
            self.ui["inp_buffshield"].set_text(" 0")
        
    def update(self):
        for u in self.ui:
            self.ui[u].update()

        #---pause button
        if not self.states.is_gameend and (self.ui["btn_pause"].pressed or self.keyman.is_startpose()):
            print("btn_pause=",self.ui["btn_pause"].pressed)
            self.parent.sound.play_pause()
            self.states.is_pause = not self.states.is_pause
            self.ui["btn_pause"].pressed = False
            if self.states.is_pause:
                self.parent.sound.stop_music()
            else:
                self.parent.sound.play_mainstage()

        if self.states.is_pause:
            return

        #---count play time
        if pyxel.frame_count % 30 == 0 and not self.states.is_gameend:
            self.play_time += self.play_time_dir
            """if self.gamemode == GameMode.TYPE_TIMEATTACK:
                self.play_time -= 1
            elif self.gamemode == GameMode.TYPE_SURVIVAL:
                self.play_time += 1"""
        
        
        #---animate wave
        for s in enumerate("a"*len(self.waves)):
            inx = s[0]
            
            if pyxel.frame_count % 2 == 0:
                self.waves[inx]["dotty"] += 1
                self.waves[inx]["animate"] += self.waves[inx]["animate_dir"]
                if self.waves[inx]["animate"] > 8:
                    self.waves[inx]["animate"] = 8
                    self.waves[inx]["animate_dir"] = -1
                elif self.waves[inx]["animate"] < 0:
                    self.waves[inx]["animate"] = 0
                    self.waves[inx]["animate_dir"] = 1
            if self.waves[inx]["dotty"] >= pos(18):
                self.waves[inx]["dotty"] = 0
        
        #---operation for system
        if pyxel.btnp(pyxel.KEY_Q):
            self.parent.current_scene = "playerselect"
            self.parent.setup_selectplayer()
            
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            #---return button
            if self.ui["return"].check_touch_area(pyxel.mouse_x, pyxel.mouse_y):
                self.parent.current_scene = "playerselect"
                self.parent.setup_selectplayer()
                return
            
            if not self.states.is_gameend:
                #---missile focus
                if self.player.job.type == ShipKind.TYPE_ASDG:
                    self.missile_cursor.x = pyxel.mouse_x - 4
                    self.missile_cursor.y = pyxel.mouse_y - 4
                    self.player.job.commands[0].focus.x = self.missile_cursor.x
                    self.player.job.commands[0].focus.y = self.missile_cursor.y
        
        #---start update for result window
        if self.states.gameend_interval > 50:
            #---during to draw result window
            if not self.states.result["is_drawend"] and self.states.is_gameend:
                if self.states.result["curdraw"]  <= self.states.result["drawtime"]:
                    self.states.result["curdraw"] += 1
                else:
                    self.states.result["is_drawend"] =  True
                    self.states.result["curdraw"] = 0
            elif not self.states.result["is_rankend"] and self.states.result["is_drawend"] and self.states.is_gameend:
                if self.states.result["curdraw"] <= self.states.result["ranktime"]:
                    self.states.result["curdraw"] += 1
                else:
                    self.states.result["is_rankend"] = True
                    self.parent.sound.play_showrank()
                
                
                
        if self.states.result["is_drawend"]:
            if self.keyman.is_cancel() or pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                self.parent.current_scene = "playerselect"
                self.parent.setup_selectplayer()

        if self.states.gameend_interval == 3:
            self.player.update()
        
        #---check game end
        if self.check_prepare_gameend():
            self.states.gameend_interval += 1
            self.player.dir.x = 0
            self.player.update()
            return                    
        

        #### below is active game elements #################################################
        #---move player
        #if (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)) and self.player.x < pyxel.width - 14:
        

        if self.keyman.release_right():
            self.keyman.left_pressed = False
            self.keyman.second_right_pressed = False
            self.keyman.right_pressed = not self.keyman.right_pressed
            self.keyman.right_pressframe = pyxel.frame_count
        
        if self.keyman.release_left():
            self.keyman.right_pressed = False
            self.keyman.second_left_pressed = False
            self.keyman.left_pressed = not self.keyman.left_pressed
            self.keyman.left_pressframe = pyxel.frame_count

        if self.keyman.is_right(True):
            self.player.dir.x = 1
            if not self.keyman.second_right_pressed:
                self.keyman.second_right_pressed = True
                if abs(pyxel.frame_count - self.keyman.right_pressframe) >= 7:
                    self.keyman.right_pressed = False
                    self.keyman.second_right_pressed = False
                    self.keyman.right_pressframe = 0
            
            if (
                (self.keyman.right_pressed and self.keyman.second_right_pressed)
                or
                (self.keyman.is_dashaction(True))
            ):
                self.player.dir.x = 3
        #elif (pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)) and self.player.x > -2:
        elif self.keyman.is_left(True):
            self.player.dir.x = -1
            if not self.keyman.second_left_pressed:
                self.keyman.second_left_pressed = True
                if abs(pyxel.frame_count - self.keyman.left_pressframe) >= 7:
                    self.keyman.left_pressed = False
                    self.keyman.second_left_pressed = False
                    self.keyman.left_pressframe = 0
            
            if (
                (self.keyman.left_pressed and self.keyman.second_left_pressed)
                or
                (self.keyman.is_dashaction(True))
            ):
                self.player.dir.x = -3
        else:
            self.player.dir.x = 0
        self.player.update()
        
        #---action player
        ##---main weapon
        if self.keyman.is_mainaction(True): #(pyxel.btnp(pyxel.KEY_E) or pyxel.btnp(pyxel.KEY_KP_1) or (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and check_mouse_playscreen(offset_y=16)) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A)):
            if pyxel.frame_count % 3 == 0:
                opt = {}
                if self.player.job.commands[0].type == AttackCommand.TYPE_MISSILE:
                    opt["missile_cursor"] = self.missile_cursor
                if self.player.shooting_main(opt):
                    self.parent.sound.play_shoot(self.player.job.commands[0].type)
            
        ##---sub weapon
        if self.keyman.is_subaction(True): # (pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.KEY_KP_2) or (pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT) and check_mouse_playscreen(offset_y=16)) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_B)):
            if pyxel.frame_count % 3 == 0:
                if self.player.shooting_sub():
                    self.parent.sound.play_shoot(self.player.job.commands[1].type)
        
        #---generate an enemy
        self.generate_enemy()
        
        if pyxel.frame_count % 30 == 0:
            self.generate_item()
        
                    
        
        #---loop enemies
        lenenemy = len(self.enemies)
        for ie in range(0, lenenemy):
            enemy = self.enemies[ie]
            #print(f"cur enemy id={id(enemy)}")
            
            #---check collision to player 
            if enemy.check_collision(self.player):
                fnlcollidered = False
                #---if Player is Submarine, collision damage by DD, CL, CVL
                if self.player.job.type == ShipKind.TYPE_SS and (enemy.jobtype == ShipKind.TYPE_DD or enemy.jobtype == ShipKind.TYPE_CL or enemy.jobtype == ShipKind.TYPE_CVL):
                    fnlcollidered = True
                else:
                    fnlcollidered = True
                    if self.player.check_buff("invincible"):
                        fnlcollidered = False
                if fnlcollidered:
                    self.player.damage(True,False)
                    self.parent.sound.play_damage()
                    #---collided enemy ?
                    enemy.death()
                    #if self.enemies.count(enemy) > 0:
                    #    self.enemies.remove(enemy)
            
            #---enemy is screen out ?
            if not enemy.will_destroy and (enemy.y >= pyxel.height // 20 * 17):
                try:
                    enemy.death()
                    #if self.enemies.count(enemy) > 0:
                    #    self.enemies.remove(enemy)
                except Exception as e:
                    print(e)
            
            #---check shooting
            for shots in enemy.cur_shots:
                self.check_enemy_shot(shots)
            #self.check_enemy_shot(enemy.shots_main)
            #self.check_enemy_shot(enemy.shots_sub)
            ##---main shot
            self.check_shot(self.enemies[ie], self.player.shots_main)
            ##---sub shot
            self.check_shot(self.enemies[ie], self.player.shots_sub)
            
            #---update
            enemy.update(self.player)

        self.player.update_shots()
        
        #---loop damecon
        for dame in self.damecons:
            dame.update()
            if dame.check_collision(self.player):
                if dame.type == Item.TYPE_LEVELUP:
                    self.parent.sound.play_levelup()
                elif dame.type == Item.TYPE_GOLDBOX:
                    self.parent.sound.play_debuff()
                    self.states.debuff_appear["enabled"] = True
                    self.states.debuff_appear["remain_time"] = 10
                    self.ui["inp_time"].color1 = pyxel.COLOR_RED
                else:
                    self.parent.sound.play_getitem()
                dame.effect(self.player)
                self.explodes.append(ItemEffect(self.player.x, self.player.y))
                dame.will_destroy = True
                
        #---loop explode effect
        for explode in self.explodes.copy():
            explode.update()
            if explode.is_explode:
                self.explodes.remove(explode)
            
        #---debuff effect
        if self.states.debuff_appear["enabled"]:
            if pyxel.frame_count % 30 == 0:
                self.states.debuff_appear["remain_time"] -= 1
            if self.states.debuff_appear["remain_time"] <= 0:
                self.states.debuff_appear["enabled"] = False
                self.ui["inp_time"].color1 = pyxel.COLOR_WHITE
        
        self.update_status()
            
        
        #---GC object
        for d in self.damecons.copy():
            if d.will_destroy:
                self.damecons.remove(d)
        
        for e in self.enemies.copy():
            if e.will_destroy:
                self.enemies.remove(e)
    
    
    def draw_resultwindow(self):
        if not self.states.result["is_drawend"]:
            pyxel.rect(0, pos(0), pos(self.states.result["curdraw"]), pos(20), pyxel.COLOR_BLACK)
        else:
            pyxel.rect(0, pos(0), pos(15), pos(20), pyxel.COLOR_BLACK)
            #---summary point
            pyxel.text(pos(1), pos(1), f"Point:{self.points.summary}", pyxel.COLOR_WHITE, font=self.parent.jp_fontmisaki)
            if self.parent.states.current_gamemode == GameMode.TYPE_TIMEATTACK:
                if self.player.is_dead():
                    pyxel.text(pos(2), pos(2), f"{self.parent.t('txt_resultremaintime')}{self.play_time}", pyxel.COLOR_WHITE, font=self.parent.jp_fontmisaki)

                    
            if self.parent.states.current_gamemode == GameMode.TYPE_SURVIVAL:
                pyxel.text(pos(2), pos(2), f"Time:{self.play_time}", pyxel.COLOR_WHITE)
                pyxel.text(pos(2), pos(3), f"Wave:{self.summary_wave_count+1}", pyxel.COLOR_WHITE)
                
            if self.states.result["is_rankend"]:
                cri = CSV_RANK_IMAGE[self.states.result["userrank"]]
                pyxel.blt(pos(10), pos(0), 0, cri[0],cri[1],cri[2],cri[3],pyxel.COLOR_BLACK)
            
            #---each class
            #==========================================================
            ## SS
            ssp = self.states.result["classpoint"][ShipKind.TYPE_SS][Enemy.TYPE_NORMAL]
            sscur = ssp[0]
            ssmax = ssp[1]            
            if ssmax > 0:
                ssi = IBNK.get("eSS_a")
                pyxel.blt(pos(0)+4, pos(5), ssi.page, ssi.x, ssi.y, ssi.w, ssi.h, pyxel.COLOR_BLACK)            
                pyxel.text(pos(0)+4, pos(7), "SS", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
                pyxel.text(pos(0)+4, pos(8), f"{sscur}/{ssmax}", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
            #==========================================================
            ## DD
            ddp = self.states.result["classpoint"][ShipKind.TYPE_DD][Enemy.TYPE_NORMAL]
            ddcur = ddp[0]
            ddmax = ddp[1]
            #---class: N
            if ddmax > 0:
                ddi = IBNK.get("eDD1_a")
                pyxel.blt(pos(4), pos(5), ddi.page, ddi.x, ddi.y, ddi.w, ddi.h, pyxel.COLOR_BLACK)
                pyxel.text(pos(4), pos(7), f"DD-N", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
                pyxel.text(pos(4), pos(8), f"{ddcur}/{ddmax}", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
            #---class: E
            ddp = self.states.result["classpoint"][ShipKind.TYPE_DD][Enemy.TYPE_ENHANCED]
            ddcur = ddp[0]
            ddmax = ddp[1]
            if ddmax > 0:
                ddi = IBNK.get("eDDE_a")
                pyxel.blt(pos(8), pos(5), ddi.page, ddi.x, ddi.y, ddi.w, ddi.h, pyxel.COLOR_BLACK)
                pyxel.text(pos(8), pos(7), "DD-E", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
                pyxel.text(pos(8), pos(8), f"{ddcur}/{ddmax}", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
            #==========================================================
            ## CL
            clp = self.states.result["classpoint"][ShipKind.TYPE_CL][Enemy.TYPE_NORMAL]
            clcur = clp[0]
            clmax = clp[1]
            if clmax > 0:
                cli = IBNK.get("eCL_a")
                pyxel.blt(pos(11)+4, pos(5), cli.page, cli.x, cli.y, cli.w, cli.h, pyxel.COLOR_BLACK)            
                pyxel.text(pos(11)+4, pos(7), "CL-N", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
                pyxel.text(pos(11)+4, pos(8), f"{clcur}/{clmax}", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
            #==========================================================
            ## CA
            cap = self.states.result["classpoint"][ShipKind.TYPE_CA][Enemy.TYPE_NORMAL]
            cacur = cap[0]
            camax = cap[1]
            if camax > 0:
                cai = IBNK.get("eCA_a")
                pyxel.blt(pos(0)+4, pos(10), cai.page, cai.x, cai.y, cai.w, cai.h, pyxel.COLOR_BLACK)            
                pyxel.text(pos(0)+4, pos(12), "CA-N", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
                pyxel.text(pos(0)+4, pos(13), f"{cacur}/{camax}", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
            #==========================================================
            ## CVL
            cvlp = self.states.result["classpoint"][ShipKind.TYPE_CVL][Enemy.TYPE_NORMAL]
            cvlcur = cvlp[0]
            cvlmax = cvlp[1]
            if cvlmax > 0:
                cvli = IBNK.get("eCVL_a")
                pyxel.blt(pos(5), pos(10), cvli.page, cvli.x, cvli.y, cvli.w, cvli.h, pyxel.COLOR_BLACK)
                pyxel.text(pos(5), pos(12), f"CVL-N", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
                pyxel.text(pos(5), pos(13), f"{cvlcur}/{cvlmax}", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
            #==========================================================
            ## CV
            cvp = self.states.result["classpoint"][ShipKind.TYPE_CV][Enemy.TYPE_NORMAL]
            cvcur = cvp[0]
            cvmax = cvp[1]
            if cvmax > 0:
                cvi = IBNK.get("eCV_a")
                pyxel.blt(pos(9), pos(10), cvi.page, cvi.x, cvi.y, cvi.w, cvi.h, pyxel.COLOR_BLACK)
                pyxel.text(pos(10), pos(12), f"CV-N", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
                pyxel.text(pos(10), pos(13), f"{cvcur}/{cvmax}", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
            #==========================================================
            ## BC
            bcp = self.states.result["classpoint"][ShipKind.TYPE_BC][Enemy.TYPE_NORMAL]
            bccur = bcp[0]
            bcmax = bcp[1]
            if bcmax > 0:
                bci = IBNK.get("eBC_a")
                pyxel.blt(pos(2), pos(15), bci.page, bci.x, bci.y, bci.w, bci.h, pyxel.COLOR_BLACK)            
                pyxel.text(pos(5), pos(15), "BC-N", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
                pyxel.text(pos(5), pos(16), f"{bccur}/{bcmax}", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
            #==========================================================
            ## BB
            bbp = self.states.result["classpoint"][ShipKind.TYPE_BB][Enemy.TYPE_NORMAL]
            bbcur = bbp[0]
            bbmax = bbp[1]
            if bbmax > 0:
                bbi = IBNK.get("eBB_a")
                pyxel.blt(pos(8), pos(15), bbi.page, bbi.x, bbi.y, bbi.w, bbi.h, pyxel.COLOR_BLACK)            
                pyxel.text(pos(11), pos(15), "BB-N", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
                pyxel.text(pos(11), pos(16), f"{bbcur}/{bbmax}", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)
        #pyxel.bltm(0, 0, MAP_SEA1["page"], MAP_SEA1["x"], MAP_SEA1["y"], MAP_SEA1["w"], MAP_SEA1["h"])
        pyxel.rect(0, 0, 8*15, 8*20, pyxel.COLOR_LIGHT_BLUE)
        #---calc waves
        for wav in enumerate(self.waves):
            for w in enumerate(wav[1]["csv"]):
                if w[1][0] != 0 and w[1][1] != 0:
                    fnly = wav[1]["dotty"]
                    
                    pyxel.blt(8*w[0], fnly,
                              0, w[1][0], w[1][1], 8, wav[1]["animate"], pyxel.COLOR_LIGHT_BLUE
                    )
        pyxel.rect(0, pos(18), 8*15, 8*2, pyxel.COLOR_BLACK)
        
        # return button
        #pyxel.blt(pos(0), pos(0), 0, 0, 72, 8, 8, pyxel.COLOR_BLACK)
        
        
        #---Drawing game elements
        # missile cursor
        if self.player.job.type == ShipKind.TYPE_ASDG:
            pyxel.blt(self.missile_cursor.x, self.missile_cursor.y, 0, 8, 0, 8, 8, pyxel.COLOR_BLACK)
        
        #---enemies
        for enemy in self.enemies:
            enemy.draw()
        
        
        #---item
        for dame in self.damecons:
            dame.draw()
        
        for explode in self.explodes.copy():
            explode.draw()
                
        #---player
        self.player.draw()

        #---UI----------------------------------------
        for u in self.ui:
            if u in ["txt_point","inp_point","txt_time","inp_time"]:
                if not self.states.result["is_drawend"]:
                    self.ui[u].draw()
            else:
                self.ui[u].draw()
        ##---top
        ###---point
        #pyxel.text(pos(1)+1, pos(1), f"Point: {self.points.summary}", pyxel.COLOR_BLACK)
        #pyxel.text(pos(1), pos(1), f"Point: {self.points.summary}", pyxel.COLOR_WHITE)
        ###---timer
        #pyxel.text(pos(10)+1, pos(1), f"Limit: {self.play_time}", pyxel.COLOR_BLACK)
        #pyxel.text(pos(10), pos(1), f"Limit: {self.play_time}", pyxel.COLOR_WHITE)
        
        ##---bottom
        #pyxel.text(pos(8), pos(19), f"HP: {pyxel.floor(self.player.hp)} / {self.player.maxhp}", pyxel.COLOR_WHITE)
        
        if self.states.is_gameend:
            self.draw_resultwindow()
        
        if self.states.is_pause:
            pyxel.dither(0.2)
            pyxel.rect(0, 0, pyxel.width, pyxel.height, pyxel.COLOR_BLACK)
            pyxel.dither(1.0)
            self.ui["btn_pause"].draw()