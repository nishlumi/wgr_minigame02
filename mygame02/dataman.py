import os
import glob
import json
import pyxel
isloadjs = False
try:
    import js
    isloadjs =  True
except Exception as e:
    print(e)
    isloadjs = False
    

class DataManager:
    TYPE_LOCAL = 0
    TYPE_WEB = 1
    def __init__(self):
        self.meta = {
            "vendor" : "lumis_lumidina",
            "appname" : "wgrfangame01"
        }
        self.data = {}
        #---0 - local, 1 - localStorage in web browser
        self.storage_mode = 0
        if isloadjs:
            self.storage_mode = 1
        
        
        self.local_filename = "wgrfangame01.sav"
        self.data_key = "wgrfand"
        #---enemy data
        self.enemydata_filename = "assets/data/enemy_*.json"
        self.enemy_data = {}
        #---game mode: time attack
        self.timeattackdata_filename = "assets/data/timeattackrate.json"
        self.timeattack_data = {}
        #---game mode: survival
        self.survivaldata_filename = "assets/data/survivalrate.json"
        self.survival_data = {}
        
    def load(self):
        ishit = False
        if self.storage_mode == DataManager.TYPE_LOCAL:
            path = pyxel.user_data_dir(self.meta["vendor"], self.meta["appname"])
            fullpath = os.path.join(path, self.local_filename)
            if os.path.exists(fullpath):
                self.data = json.load(open(fullpath))
                ishit = True
        elif self.storage_mode == DataManager.TYPE_WEB:
            rawdata = js.localStorage.getItem(self.data_key)
            if rawdata:
                self.data = json.loads(rawdata)
                ishit = True
        return ishit
    
    def save(self):
        if self.storage_mode == DataManager.TYPE_LOCAL:
            path = pyxel.user_data_dir(self.meta["vendor"], self.meta["appname"])
            fullpath = os.path.join(path, self.local_filename)
            with open(fullpath,"wt") as f:
                json.dump(self.data,f)
        elif self.storage_mode == DataManager.TYPE_WEB:
            js.localStorage.setItem(self.data_key, json.dumps(self.data))
            
    def load_timeattack_data(self):
        if os.path.exists(self.timeattackdata_filename):
            self.timeattack_data = json.load(open(self.timeattackdata_filename))
        else:
            print("error: time attack data file not found...")
            
    def load_survival_data(self):
        if os.path.exists(self.survivaldata_filename):
            self.survival_data = json.load(open(self.survivaldata_filename))
        else:
            print("error: survival data file not found...")
            
    def load_enemy_data(self):
        glst = glob.glob(self.enemydata_filename)
        for gl in glst:
            if os.path.exists(gl):
                js = json.load(open(gl))
                if ("type" in js) and ("eachclass" in js):
                    self.enemy_data[js["type"]] = js
            else:
                print("error: enemy data file not found...")
    
    def get_enemydata(self, jobtype, jobclass, lv) -> dict:
        """get data by jobtype,jobclass,lv 
        return ['eachclass']['normal'][0]
        """
        ret = None
        #for name in self.enemy_data[jobtype]["eachclass"]:
        ec = self.enemy_data[jobtype]["eachclass"]
        
        jobd = []
        if jobclass == 0: #---normal
            jobd = ec["normal"]
        elif jobclass == 1: #---enhanced
            jobd = ec["enhanced"]
        elif jobclass == 2: #---super
            jobd = ec["super"]
        elif jobclass == 3: #---boss
            jobd = ec["boss"]
        
        ishit = False
        for lvdata in jobd:
            if lvdata["lv"] == lv:
                ret = lvdata
                ishit = True
                break
        
        return ret
