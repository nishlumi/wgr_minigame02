import pyxel

class SoundManager:
    def __init__(self, use_bgm: bool = True, use_se: bool = True):
        self.use_bgm: bool = use_bgm
        self.use_se: bool = use_se
        
        self.bgm_ch0 = 0
        self.bgm_ch1 = 1
        self.defeat_enemy = 2
        self.shoot_battleship = 3
        self.shoot_gun = 4
        self.healing = 5
        self.player_damage = 6
        self.bgm_gameover = 7
        self.bgm_finish_ch0 = 8
        self.bgm_finish_ch1 = 9
        self.show_rank = 10
        self.torpedo = 11
        self.aircraft = 12
        self.aashoot = 13
        self.damage = 14
        self.bgm_select = 15
        self.decide = 16
        self.missile = 17
        self.disable_action = 18
        self.change_action = 19
        self.depthcharge = 20
        self.pause = 23
        self.levelup = 24
        self.debuff = 29
        
    def stop_music(self):
        pyxel.stop(0)
        pyxel.stop(1)
    
    def play_title(self):
        if not self.use_bgm:
            return
        pyxel.playm(4, loop=True)
    
    def play_history(self):
        if not self.use_bgm:
            return
        pyxel.playm(5, loop=True)
    
    def play_shoot(self,cmdtype:int):
        if not self.use_se:
            return
        
        from mycls import AttackCommand
        if cmdtype == AttackCommand.TYPE_GUN:
            pyxel.play(2, self.shoot_gun)
        elif cmdtype == AttackCommand.TYPE_TORPEDO:
            pyxel.play(2, self.torpedo)
        elif (cmdtype == AttackCommand.TYPE_AIRCRAFT or cmdtype == AttackCommand.TYPE_ASA_AIRCRAFT):
            pyxel.play(2, self.aircraft)
        elif cmdtype == AttackCommand.TYPE_AASHOOT:
            pyxel.play(2, self.aashoot)
        elif cmdtype == AttackCommand.TYPE_BBGUN:
            pyxel.play(2, self.shoot_battleship)
        elif cmdtype == AttackCommand.TYPE_MISSILE:
            pyxel.play(2, self.missile)
        elif cmdtype == AttackCommand.TYPE_DEPTHCHARGE:
            pyxel.play(2, self.depthcharge)
    
    def play_blank_explode(self):
        if not self.use_se:
            return
        pyxel.play(3, self.defeat_enemy)
    
    def play_select(self):
        if not self.use_se:
            return
        pyxel.play(2, self.decide)
        
    def play_pause(self):
        if not self.use_se:
            return
        pyxel.play(2, self.pause)
    
    def play_disable(self):
        if not self.use_se:
            return
        pyxel.play(2, self.disable_action)
    
    def play_change_action(self):
        print("flag=",self.use_se)
        if not self.use_se:
            return
        pyxel.play(2, self.change_action)
    
    def play_getitem(self):
        if not self.use_se:
            return
        pyxel.play(2, self.healing)
    
    def play_damage(self):
        if not self.use_se:
            return
        pyxel.play(2, self.damage)
    
    def play_levelup(self):
        if not self.use_se:
            return
        pyxel.play(2, self.levelup)
    
    def play_debuff(self):
        if not self.use_se:
            return
        pyxel.play(2, self.debuff)
    
    def play_modeselect(self):
        if not self.use_bgm:
            return
        pyxel.playm(3,loop=True)

    def play_playerselect(self):
        if not self.use_bgm:
            return
        pyxel.playm(2,loop=True)
    
    def play_mainstage(self):
        if not self.use_bgm:
            return
        pyxel.playm(0, loop=True)
    
    def play_gameclear(self):
        if not self.use_bgm:
            return
        pyxel.stop(0)
        pyxel.stop(1)
        pyxel.stop(2)
        pyxel.stop(3)
        pyxel.playm(1,loop=False)

    def play_showrank(self):
        if not self.use_se:
            return
        pyxel.stop(0)
        pyxel.stop(1)
        pyxel.stop(2)
        pyxel.stop(3)
        pyxel.play(2, self.show_rank)