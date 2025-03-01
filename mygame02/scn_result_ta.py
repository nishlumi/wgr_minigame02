import pyxel
from myscene import GameScene
from myconfig import GameOperator
from mycls import Bounds, GameMode, GamePoint, pos, draw_select_cursor
from enemycls import Enemy
from appconst import ShipKind, TimeAttackRule, CSV_PLAYABLE, WEAPON_IMGKEY
from myui import GameUI, GUIText, GUIImage, GUICheckbox, GUIScrollArea, GUIResultCard
from imgbnk import IBNK


TIME_REAL = [60, 120, 180]
LIMIT_TIME_STR = ["chk_time_short","chk_time_mid","chk_time_long"]
ENEMY_FORCE_STR = ["chk_enemy_all","chk_enemy_vanguard","chk_enemy_smallship","chk_enemy_airforce","chk_enemy_highfire"]
ENEMY_FREQ_STR = ["chk_lv1only","chk_lv2only","chk_lv3only","chk_lv1_2",
            "chk_lv1lots","chk_lv2lots","chk_lv3lots"]

class ResultTimeAttackScene(GameScene):
    def __init__(self, app: GameOperator):
        super().__init__(app)
        self.cursor = Bounds(pos(1), pos(4), 8, 8)
        self.select = "return"
        self.rule_select = {
            "time" : TimeAttackRule.TYPE_TIME_SHORT,
            "forces" : TimeAttackRule.TYPE_FORCES_ALL
        }
        
        self.setup_ui()
        
        self.uikeys = list(self.ui.keys())
        self.lenui = len(self.uikeys)
        
        self.states = {
            "is_startdraw" : False,
            "drawtime" : 15,
            "curdraw" : 0,
            "is_drawend" : False,
            "detailpage" : 0,
        }
        self.basedata = []
        self.select_data = {}
        
    def reset_select(self):
        self.cursor.x = self.ui["return"].bounds.x
        self.cursor.y = self.ui["return"].bounds.y

    def change_locale(self):
        targets = [
           
        ]
        for t in targets:
            if self.ui[t].type == GameUI.TYPE_TEXT:
                self.ui[t].set_text(self.parent.t(t))
            elif self.ui[t].type == GameUI.TYPE_CHECKBOX:
                self.ui[t].text.set_text(self.parent.t(t))
        
        self.ui["condition"].set_text(f"{self.parent.t('txt_enemy')} {TimeAttackRule.FORCE_LIST[self.parent.states.timeattack_enemies]}")
        
    def setup_ui(self):
        retimg = self.parent.imgbnk.get("larrow")
        self.ui = {
            "return": GUIImage(pos(0)+4,pos(0)+4,retimg.page, Bounds(retimg.x, retimg.y, retimg.w, retimg.h),pyxel.COLOR_BLACK),
            "condition" : GUIText("", pos(3), pos(0)+4,font=self.parent.jp_fontmisaki, color1=pyxel.COLOR_WHITE),
            "result" : GUIScrollArea(0, pos(2), pos(15), pos(17),{})
        }
        
        self.setup_listdata()
            
        super().setup_ui()
        
        self.ui["return"].selectable = True
        self.ui["return"].set_round(
            #bottomui=self.ui["chk_time_short"]
        )

                
        self.reset_select()

    def setup_listdata(self):
        self.ui["result"].contents.clear()
        data = self.parent.data_man.get_timeattack_cleardata(self.parent.states.timeattack_time, self.parent.states.timeattack_enemies)
        self.basedata = data
        tmpy = 0
        #print(data)
        respar: GUIScrollArea = self.ui["result"]
        for i,dt in enumerate(data):
            #print("dt=",dt)
            card1: GUIResultCard = GUIResultCard(0, pos(tmpy), pos(15), pos(5)-2, IBNK.get(CSV_PLAYABLE[dt["player"]].previewkey), pyxel.COLOR_WHITE, pyxel.COLOR_DARK_BLUE, font1=self.parent.jp_font10, font2=self.parent.jp_fontmisaki)
            card1.set_playername(CSV_PLAYABLE[dt["player"]].title)
            card1.set_condition(1, f"{self.parent.t('txt_time')} {TimeAttackRule.TIME_LIST[dt['condition_time']]}")
            card1.set_condition(2, f"Point: {dt['point']}")
            card1.set_condition(3, f"C: {dt['summary']['cnt']}")
            card1.set_condition(4, f"/  {dt['summary']['max']}")
            card1.set_rank(GamePoint.RANK_LIST[dt["rank"]])
            if i == 0:
                card1.set_round(
                    upui="return"
                )
            card1.referlist = self.ui
            self.ui["result"].append(dt["player"]+"%"+dt["play_date"], card1)
            tmpy += 5
        self.ui["result"].calculate_pos()
        if len(self.ui["result"].contents.keys()) > 0:
            self.ui["return"].set_round(
                bottomui=self.ui["result"].first_content.name
            )
            ckeys = list(self.ui["result"].contents.keys())
            for i,ci in enumerate(ckeys):
                nextui = None
                prevui = None
                if i > 0:
                    prevui = self.ui["result"].contents[ckeys[i-1]]
                elif i == 0:
                    prevui = self.ui["return"]
                if i < len(ckeys)-1:
                    nextui = self.ui["result"].contents[ckeys[i+1]]
                #print("current=",self.ui["result"].contents[ci],ci)
                #print("prevui=",prevui)
                #print("nextui=",nextui)
                self.ui["result"].contents[ci].set_round(
                    upui=prevui,
                    bottomui=nextui
                )
    
    def get_selectdata(self):
        key_player = self.select.split("%")[0]
        key_datetime = self.select.split("%")[1]
        self.select_data = {}
        for l in self.basedata:
            if (l["player"] == key_player) and (l["play_date"] == key_datetime):
                self.select_data = l
                break
                
        
    def check_and_config(self, is_decide = False):
        if self.select == "return":
            self.parent.current_scene = "timeattack"
            #self.parent.setup_start()
            self.parent.setup_timeattack_rule()
        elif self.select == "result":
            pass
        else:
            #print(self.select)
            if is_decide:
                self.decide_select()
            
            
    def decide_select(self):
        if self.select == "return":
            self.parent.current_scene = "timeattack"
            self.parent.setup_timeattack_rule()
        elif self.select == "result":
            pass
        else:
            self.get_selectdata()
            self.parent.sound.play_select()
            #print(self.select_data)
            self.states["is_startdraw"] =  True
            self.states["detailpage"] = 0
        
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            self.parent.current_scene = "timeattack"
            self.parent.setup_timeattack_rule()
            return
        
        if self.states["is_drawend"]:
            if self.keyman.is_cancel() or self.keyman.is_subaction(): 
                if self.states["detailpage"] == 1:
                    self.states["detailpage"] = 0
                else:
                    self.states["is_drawend"] = False
                    self.states["is_startdraw"] = False
                
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) or self.keyman.is_mainaction():
                self.states["detailpage"] = 1
            
            return
        
        if self.states["is_startdraw"]:
            if not self.states["is_drawend"]:
                if self.states["curdraw"]  <= self.states["drawtime"]:
                    self.states["curdraw"] += 1
                else:
                    self.states["is_drawend"] =  True
                    self.states["curdraw"] = 0
        
        keystr = ""
        if self.keyman.is_up():
            keystr = "up"
        elif self.keyman.is_down():
            keystr = "bottom"
        elif self.keyman.is_left():
            keystr = "left"
        elif self.keyman.is_right():
            keystr = "right"
        
        uoc = self.ui_operation_check2(keystr)
        if uoc["mouse"]:
            self.check_and_config()
        if uoc["mouse_already"]:
            self.check_and_config(True)
        
        if not uoc["cursor"] and uoc["virtual_roundui"]:
            vui = uoc["virtual_roundui"]
            if self.get_ui(self.select):
                thisui = self.get_ui(self.select)
                if thisui.parent and thisui.parent.type == GameUI.TYPE_SCROLLAREA:
                    if keystr == "bottom":
                        #print("->this=",thisui.name,"bottom=",thisui.roundui["up"].name)
                        thisui.parent.scroll_y(-vui.bounds.h)
                        self.cursor.x = vui.bounds.x
                        self.cursor.y = vui.bounds.y
                        self.select = vui.name
                    elif keystr == "up":
                        #print("->this=",thisui.name,"up=",thisui.roundui["bottom"].name)
                        thisui.parent.scroll_y(vui.bounds.h)
                        self.cursor.x = vui.bounds.x
                        self.cursor.y = vui.bounds.y
                        self.select = vui.name
                
            
        if self.keyman.is_enter():
            self.decide_select()
            
        if self.keyman.is_cancel():
            self.parent.current_scene = "timeattack"
            self.parent.setup_timeattack_rule()
            self.select = "return"
        
        for u in self.ui:
            self.ui[u].update()
        
        return super().update()
    
    def draw_resultlist(self):
        if not self.states["is_drawend"]:
            pyxel.rect(0, pos(0), pos(self.states["curdraw"]), pos(20), pyxel.COLOR_BLACK)
        else:
            pyxel.rect(0, pos(0), pos(15), pos(20), pyxel.COLOR_BLACK)
            
            player = CSV_PLAYABLE[self.select_data['player']]
            pimg = IBNK.get(player.previewkey)
            if self.states["detailpage"] == 0:
                #---player info
                pyxel.rect(pos(0),pos(0),pos(15),pos(7),pyxel.COLOR_DARK_BLUE)
                pyxel.rect(pos(0)+4, pos(0)+4, pimg.w+2, pimg.h+2, pyxel.COLOR_WHITE)
                pyxel.rect(pos(0)+3, pos(0)+3, pimg.w+2, pimg.h+2, pyxel.COLOR_BLACK)
                #pyxel.rectb(pos(0)+3, pos(0)+3, pimg.w+2, pimg.h+2, pyxel.COLOR_WHITE)
                pyxel.blt(pos(0)+4, pos(0)+4, pimg.page, pimg.x, pimg.y, pimg.w, pimg.h, pyxel.COLOR_BLACK)
                pyxel.text(pos(3), pos(0), f"{player.title}", pyxel.COLOR_WHITE, font=self.parent.jp_font10)
                #---
                pyxel.text(pos(4),pos(2),f"Lv: {self.select_data['lv']}", pyxel.COLOR_WHITE, font=self.parent.jp_fontmisaki)
                pyxel.text(pos(4),pos(3),f"HP: {pyxel.floor(self.select_data['hp'])} / {self.select_data['maxhp']}", pyxel.COLOR_WHITE, font=self.parent.jp_fontmisaki)
                
                #---weapon
                mainw = IBNK.get(WEAPON_IMGKEY[self.select_data["weapon"]["main"]])
                subw = IBNK.get(WEAPON_IMGKEY[self.select_data["weapon"]["sub"]])
                pyxel.rect(pos(5),pos(5)-2, mainw.w+2, mainw.h+2, pyxel.COLOR_WHITE)
                pyxel.rect(pos(5)-1,pos(5)-3, mainw.w+2, mainw.h+2, pyxel.COLOR_BLACK)
                #pyxel.rectb(pos(5)-1,pos(5)-2, mainw.w+2, mainw.h+2, pyxel.COLOR_WHITE)
                pyxel.text(pos(1),pos(5),f"Main: ", pyxel.COLOR_WHITE, font=self.parent.jp_fontmisaki)
                pyxel.blt(pos(5),pos(5)-2,mainw.page, mainw.x, mainw.y, mainw.w, mainw.h, pyxel.COLOR_BLACK)
                
                pyxel.rect(pos(11),pos(5)-2, subw.w+2, subw.h+2, pyxel.COLOR_WHITE)
                pyxel.rect(pos(11)-1,pos(5)-3, subw.w+2, subw.h+2, pyxel.COLOR_BLACK)
                #pyxel.rectb(pos(11)-1,pos(5)-2, subw.w+2, subw.h+2, pyxel.COLOR_WHITE)
                pyxel.text(pos(8),pos(5),f"Sub: ", pyxel.COLOR_WHITE, font=self.parent.jp_fontmisaki)
                pyxel.blt(pos(11),pos(5)-2,subw.page, subw.x, subw.y, subw.w, subw.h, pyxel.COLOR_BLACK)
                #---divide
                pyxel.text(pos(4)+4,pos(7),self.parent.t("txt_resultmode"),pyxel.COLOR_WHITE, font=self.parent.jp_font10)
                #---enemy info
                pyxel.rect(pos(0),pos(8)+4,pos(15),pos(8),pyxel.COLOR_DARK_BLUE)
                pyxel.text(pos(1),pos(9),self.select_data["play_date"], pyxel.COLOR_WHITE)
                pyxel.text(pos(1),pos(10),f"Mode: {self.parent.t('txt_timeattack')}", pyxel.COLOR_WHITE, font=self.parent.jp_fontmisaki)
                pyxel.text(pos(1),pos(11),f"{self.parent.t('txt_enemy2')} {TimeAttackRule.FORCE_LIST[self.parent.states.timeattack_enemies]}", pyxel.COLOR_WHITE, font=self.parent.jp_fontmisaki)
                pyxel.text(pos(1),pos(12),f"{self.parent.t('txt_time')} {TimeAttackRule.TIME_LIST[self.select_data['condition_time']]}", pyxel.COLOR_WHITE, font=self.parent.jp_fontmisaki)
                pyxel.text(pos(1),pos(13),f"{self.parent.t('txt_totalkills')}", pyxel.COLOR_WHITE, font=self.parent.jp_fontmisaki)
                pyxel.text(pos(4),pos(14),f"{self.select_data['summary']['cnt']} / {self.select_data['summary']['max']}", pyxel.COLOR_WHITE, font=self.parent.jp_fontmisaki)
                pyxel.text(pos(1),pos(15),f"Point: {self.select_data['point']}", pyxel.COLOR_WHITE, font=self.parent.jp_fontmisaki)
                #---
                cri = IBNK.get(GamePoint.RANK_IMAGE[self.select_data['rank']])
                pyxel.rect(pos(10)+4, pos(12)+1, cri.w+2,cri.h+2, pyxel.COLOR_WHITE)
                pyxel.rect(pos(10)+3, pos(12), cri.w+2,cri.h+2, pyxel.COLOR_BLACK)
                #pyxel.rectb(pos(10)+3, pos(12), cri.w+2, cri.h+2, pyxel.COLOR_WHITE)
                pyxel.blt(pos(10)+4, pos(12), cri.page, cri.x,cri.y,cri.w,cri.h,pyxel.COLOR_BLACK)
                #---
                pyxel.text(pos(9),pos(18),"Next page...",pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
                
            elif self.states["detailpage"] == 1:
            
                #---summary point
                pyxel.text(pos(1), pos(1), f"Point:{self.select_data['point']}", pyxel.COLOR_WHITE, font=self.parent.jp_fontmisaki)
                if self.parent.states.current_gamemode == GameMode.TYPE_TIMEATTACK:
                    if not self.select_data["complete"]:
                        pyxel.text(pos(2), pos(2), "Defeat...", pyxel.COLOR_WHITE, font=self.parent.jp_fontmisaki)

                pyxel.text(pos(1), pos(3), f"{self.parent.t('txt_totalkills')} {self.select_data['summary']['cnt']}/{self.select_data['summary']['max']}", pyxel.COLOR_WHITE, font=self.parent.jp_fontmisaki)
                        
                """if self.parent.states.current_gamemode == GameMode.TYPE_SURVIVAL:
                    pyxel.text(pos(2), pos(2), f"Time:{self.play_time}", pyxel.COLOR_WHITE)
                    pyxel.text(pos(2), pos(3), f"Wave:{self.summary_wave_count+1}", pyxel.COLOR_WHITE)"""
                    
                
                cri = IBNK.get(GamePoint.RANK_IMAGE[self.select_data['rank']])
                pyxel.blt(pos(11), pos(0), cri.page, cri.x,cri.y,cri.w,cri.h,pyxel.COLOR_BLACK)
                
                #---each class
                enemies: list = self.select_data["enemies"]
                #==========================================================
                ## SS
                ssp = self.parent.data_man.get_enemy_summary(enemies,ShipKind.TYPE_SS,Enemy.TYPE_NORMAL)
                sscur = ssp[0]
                ssmax = ssp[1]            
                if ssmax > 0:
                    ssi = IBNK.get("eSS_a")
                    pyxel.blt(pos(0)+4, pos(5), ssi.page, ssi.x, ssi.y, ssi.w, ssi.h, pyxel.COLOR_BLACK)            
                    pyxel.text(pos(0)+4, pos(7), "SS", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
                    pyxel.text(pos(0)+4, pos(8), f"{sscur}/{ssmax}", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
                #==========================================================
                ## DD
                ddp = self.parent.data_man.get_enemy_summary(enemies,ShipKind.TYPE_DD,Enemy.TYPE_NORMAL)
                ddcur = ddp[0]
                ddmax = ddp[1]
                #---class: N
                if ddmax > 0:
                    ddi = IBNK.get("eDD1_a")
                    pyxel.blt(pos(4), pos(5), ddi.page, ddi.x, ddi.y, ddi.w, ddi.h, pyxel.COLOR_BLACK)
                    pyxel.text(pos(4), pos(7), f"DD-N", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
                    pyxel.text(pos(4), pos(8), f"{ddcur}/{ddmax}", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
                #---class: E
                ddp = self.parent.data_man.get_enemy_summary(enemies,ShipKind.TYPE_DD,Enemy.TYPE_ENHANCED)
                ddcur = ddp[0]
                ddmax = ddp[1]
                if ddmax > 0:
                    ddi = IBNK.get("eDDE_a")
                    pyxel.blt(pos(8), pos(5), ddi.page, ddi.x, ddi.y, ddi.w, ddi.h, pyxel.COLOR_BLACK)
                    pyxel.text(pos(8), pos(7), "DD-E", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
                    pyxel.text(pos(8), pos(8), f"{ddcur}/{ddmax}", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
                #==========================================================
                ## CL
                clp = self.parent.data_man.get_enemy_summary(enemies,ShipKind.TYPE_CL,Enemy.TYPE_NORMAL)
                clcur = clp[0]
                clmax = clp[1]
                if clmax > 0:
                    cli = IBNK.get("eCL_a")
                    pyxel.blt(pos(11)+4, pos(5), cli.page, cli.x, cli.y, cli.w, cli.h, pyxel.COLOR_BLACK)            
                    pyxel.text(pos(11)+4, pos(7), "CL-N", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
                    pyxel.text(pos(11)+4, pos(8), f"{clcur}/{clmax}", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
                #==========================================================
                ## CA
                cap = self.parent.data_man.get_enemy_summary(enemies,ShipKind.TYPE_CA,Enemy.TYPE_NORMAL)
                cacur = cap[0]
                camax = cap[1]
                if camax > 0:
                    cai = IBNK.get("eCA_a")
                    pyxel.blt(pos(0)+4, pos(10), cai.page, cai.x, cai.y, cai.w, cai.h, pyxel.COLOR_BLACK)            
                    pyxel.text(pos(0)+4, pos(12), "CA-N", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
                    pyxel.text(pos(0)+4, pos(13), f"{cacur}/{camax}", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
                #==========================================================
                ## CVL
                cvlp = self.parent.data_man.get_enemy_summary(enemies,ShipKind.TYPE_CVL,Enemy.TYPE_NORMAL)
                cvlcur = cvlp[0]
                cvlmax = cvlp[1]
                if cvlmax > 0:
                    cvli = IBNK.get("eCVL_a")
                    pyxel.blt(pos(5), pos(10), cvli.page, cvli.x, cvli.y, cvli.w, cvli.h, pyxel.COLOR_BLACK)
                    pyxel.text(pos(5), pos(12), f"CVL-N", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
                    pyxel.text(pos(5), pos(13), f"{cvlcur}/{cvlmax}", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
                #==========================================================
                ## CV
                cvp = self.parent.data_man.get_enemy_summary(enemies,ShipKind.TYPE_CV,Enemy.TYPE_NORMAL)
                cvcur = cvp[0]
                cvmax = cvp[1]
                if cvmax > 0:
                    cvi = IBNK.get("eCV_a")
                    pyxel.blt(pos(9), pos(10), cvi.page, cvi.x, cvi.y, cvi.w, cvi.h, pyxel.COLOR_BLACK)
                    pyxel.text(pos(10), pos(12), f"CV-N", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
                    pyxel.text(pos(10), pos(13), f"{cvcur}/{cvmax}", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
                #==========================================================
                ## BC
                bcp = self.parent.data_man.get_enemy_summary(enemies,ShipKind.TYPE_BC,Enemy.TYPE_NORMAL)
                bccur = bcp[0]
                bcmax = bcp[1]
                if bcmax > 0:
                    bci = IBNK.get("eBC_a")
                    pyxel.blt(pos(2), pos(15), bci.page, bci.x, bci.y, bci.w, bci.h, pyxel.COLOR_BLACK)            
                    pyxel.text(pos(5), pos(15), "BC-N", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
                    pyxel.text(pos(5), pos(16), f"{bccur}/{bcmax}", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
                #==========================================================
                ## BB
                bbp = self.parent.data_man.get_enemy_summary(enemies,ShipKind.TYPE_BB,Enemy.TYPE_NORMAL)
                bbcur = bbp[0]
                bbmax = bbp[1]
                if bbmax > 0:
                    bbi = IBNK.get("eBB_a")
                    pyxel.blt(pos(8), pos(15), bbi.page, bbi.x, bbi.y, bbi.w, bbi.h, pyxel.COLOR_BLACK)            
                    pyxel.text(pos(11), pos(15), "BB-N", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
                    pyxel.text(pos(11), pos(16), f"{bbcur}/{bbmax}", pyxel.COLOR_WHITE,font=self.parent.jp_fontmisaki)
            
            
        
    def draw(self):
        pyxel.cls(pyxel.COLOR_BLACK)
        for u in self.ui:
            self.ui[u].draw()
        
        #---cursor
        if pyxel.frame_count % 15 == 0:
            pyxel.dither(0.25)
        elif pyxel.frame_count % 30 == 0:
            pyxel.dither(0.5)
        
        curcur = self.get_ui(self.select)
        if curcur:
            draw_select_cursor(self.cursor, curcur.bounds.w-2, curcur.bounds.h-2, offset_x=-1, offset_y=-1)
            #pyxel.rect(self.cursor.x, self.cursor.y, self.cursor.w, self.cursor.h, pyxel.COLOR_PINK)
        pyxel.dither(1.0)
        
        if self.states["is_startdraw"]:
            self.draw_resultlist()
        
        return super().draw()