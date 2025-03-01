import pyxel
import datetime
from typing import NamedTuple
from soundman import SoundManager
from appconst import CSV_ENEMY_APPEAR_RATE
from apptranslate import LOCALE_EN, LOCALE_JA, LOCALE_STRING
from dataman import DataManager
from imgbnk import IBNK

class AppMeta(NamedTuple):
    author: str

class GameOperator:
    def __init__(self, app):
        self.parent = app
        self.imgbnk = IBNK
        self.jp_font10 = pyxel.Font("assets/fonts/umplus_j10r.bdf")
        self.jp_font12 = pyxel.Font("assets/fonts/umplus_j12r.bdf")
        self.jp_fontmisaki = pyxel.Font("assets/fonts/misaki_gothic_2nd.bdf")
        self.jp_font8 = pyxel.Font("assets/fonts/k8x12.bdf")
        self.jp_font8s = pyxel.Font("assets/fonts/k8x12S.bdf")
        
        self.is_test = False
        self.meta = AppMeta("lumidina")
        self.sound = SoundManager()
        #---savable settings
        self.config = {
            "use_bgm" : False,
            "use_se" : True,
            "locale" : LOCALE_EN,
            "save_score" : True
        }
        #---not savbale, temporary settings and status
        self.states = GameState()
        self.current_scene = "start"        
        
        self.data_man = DataManager()
        self.load()
        self.setup_config()
        self.sound.play_title()
        
    def load(self):
        if self.data_man.load():
            self.config = self.data_man.data.copy()
        self.data_man.load_timeattack_data()
        self.data_man.load_survival_data()
        self.data_man.load_enemy_data()
        
    def save(self):
        self.data_man.data = self.config.copy()
        self.data_man.save()
    
    def setup_config(self):
        self.sound.use_bgm = self.config["use_bgm"]
        self.sound.use_se = self.config["use_se"]
        
        self.mode_each = CSV_ENEMY_APPEAR_RATE
        
    
    def get_each_mode(self, name):
        return self.mode_each[name][self.config.mode]

    def t(self, locstr):
        l = LOCALE_STRING.get(locstr)
        if l:
            return l[self.config["locale"]]
        else:
            return ""
        
    def setup_start(self):
        self.parent.scenes["start"].change_locale()
        self.sound.stop_music()
        self.sound.play_title()
        
    def setup_option(self):
        self.parent.scenes["option"].setup_config()
        
    def setup_help(self):
        self.parent.scenes["help"].change_locale()

    def setup_mainstage(self, selectchara, equiptype: int = 0):
        self.parent.scenes["mainstage"].reset_game(self.states.current_gamemode)
        self.parent.scenes["mainstage"].setup_player(selectchara, equiptype)
        self.states.current_date = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
        self.sound.stop_music()
        self.sound.play_mainstage()

    def setup_selectplayer(self):
        self.parent.scenes["playerselect"].reset_select()
        self.sound.stop_music()
        self.sound.play_playerselect()
    
    def setup_gamemode(self):
        self.parent.scenes["gamemode"].change_locale()
        self.sound.play_modeselect()
        
    def setup_start(self):
        self.parent.scenes["start"].change_locale()
        self.sound.stop_music()
        self.sound.play_title()
        
    def setup_timeattack_rule(self):
        self.parent.scenes["timeattack"].reset_select()
        self.parent.scenes["timeattack"].change_locale()
        self.sound.stop_music()
        self.sound.play_modeselect()
        
    
    def setup_survival_rule(self):
        self.parent.scenes["survival"].reset_select()
        self.parent.scenes["survival"].change_locale()
        self.sound.stop_music()
        self.sound.play_modeselect()
        
    def setup_resultmode(self):
        self.parent.scenes["resultmode"].change_locale()
        #self.sound.play_modeselect()
    
    def setup_timeattack_result(self):
        self.parent.scenes["resulttimeattack"].reset_select()
        self.parent.scenes["resulttimeattack"].change_locale()
        self.parent.scenes["resulttimeattack"].setup_listdata()
        self.sound.stop_music()
        self.sound.play_history()
        
    def setup_survival_result(self):
        self.parent.scenes["resultsurvival"].reset_select()
        self.parent.scenes["resultsurvival"].change_locale()
        self.parent.scenes["resultsurvival"].setup_listdata()
        self.sound.stop_music()
        self.sound.play_history()

class GameConfig:
    def __init__(self):
        self.reset_config()

    def reset_config(self):
        self.use_bgm = False
        self.use_se = True
        self.locale = LOCALE_EN
        self.save_score = True
    
    def to_raw(self):
        return {
            "use_bgm" : self.use_bgm,
            "use_se" : self.use_se,
            "locale" : self.locale,
            "save_score" : self.save_score
        }

class GameState:
    def __init__(self):
        self.reset_states()
    
    def reset_states(self):
        self.current_gamemode = 0
        self.current_player = ""
        self.current_date = None
        self.godmode = True
        self.appear_damecon = [1, 10]
        self.appear_juice = [1, 30]
        self.appear_curry = [1, 10]
        self.appear_redcurry = [1, 5]
        self.appear_rader1 = [1, 20]
        self.appear_rader2 = [1, 10]
        self.appear_shield1 = [1, 30]
        self.appear_cat = [1, 5]
        self.appear_goldbox = [1,3]
        self.timeattack_appear_interval = 40
        self.timeattack_time = 0
        self.timeattack_enemies = 0
        self.timeattack_firstlv = 0
        self.survival_enemies = 0