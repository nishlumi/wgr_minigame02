# title: Warship-Girls R FAN Game 02
# author: lumis(lumidina)
# desc: Mini shooting game for Warship-Girls R
# license: MIT
# version: 1.0

import pyxel
from typing import TypedDict, NamedTuple
from mycls import GameObject, ShipJob
from myconfig import GameOperator, GameConfig, GameState
from appconst import CSV_ENEMY_APPEAR_RATE
from scn_start import StartScene
from scn_select import SelectScene
from scn_stage import MainStageScene
from scn_option import OptionScene
from scn_help import HelpScene
from scn_gamemode import GameModeScene
from scene_mode_ta import SceneModeTimeAttack
from scn_mode_surv import SceneModeSurvival
from scn_map import MapScene
from soundman  import SoundManager


class AppMeta(NamedTuple):
    author: str

class App:
    def __init__(self):
        pyxel.init(120, 160, title="Warship-Girls R FAN Game 02")
        pyxel.mouse(True)
        pyxel.load("my_resource.pyxres")

        self.ope = GameOperator(self)
        #self.jp_font10 = pyxel.Font("umplus_j10r.bdf")
        #self.jp_font12 = pyxel.Font("umplus_j12r.bdf")
        
        #self.is_test = True
        #self.meta = AppMeta("lumidina")
        #self.sound = SoundManager()
        #self.setup_config()
        self.scenes = {
            "start": StartScene(self.ope),
            "playerselect" : SelectScene(self.ope),
            "mainstage" : MainStageScene(self.ope),
            "gamemode" : GameModeScene(self.ope),
            "timeattack": SceneModeTimeAttack(self.ope),
            "survival" : SceneModeSurvival(self.ope),
            "gamemap" : MapScene(self.ope),
            "option": OptionScene(self.ope),
            "help" : HelpScene(self.ope),
        }
        #self.current_scene = "start"
        
        
        pyxel.run(self.update, self.draw)    
        
    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
                
        self.scenes[self.ope.current_scene].update()
                
    def draw(self):
        self.scenes[self.ope.current_scene].draw()
        

App()