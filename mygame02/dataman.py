import os
import sys
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
            "appname" : "wgrfangame02"
        }
        self.data = {}
        self.cleardata = {
            "timeattack" : {
                "forces_0" : [],
                "forces_1" : [],
                "forces_2" : [],
                "forces_3" : [],
                "forces_4" : [],
                
            },
            "survival" : {
                "forces_0" : [],
                "forces_1" : [],
                "forces_2" : [],
                "forces_3" : [],
                "forces_4" : []
            }
        }
        #---0 - local, 1 - localStorage in web browser
        self.storage_mode = 0
        if isloadjs:
            self.storage_mode = 1
        
        
        self.local_filename = "wgrfangame02.sav"
        self.local_clearfilename_timeattack = "cd_timeattack.sav"
        self.local_clearfilename_survival = "cd_survival.sav"
        self.data_key = "wgrfand"
        self.cleardata_key_timeattack = "cd_timeattack"
        self.cleardata_key_survival = "cd_survival"
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
            #---clear data
            fullpath = os.path.join(path, self.local_clearfilename_timeattack)
            if os.path.exists(fullpath):
                self.cleardata["timeattack"] = json.load(open(fullpath))
            fullpath = os.path.join(path, self.local_clearfilename_survival)
            if os.path.exists(fullpath):
                self.cleardata["survival"] = json.load(open(fullpath))
        elif self.storage_mode == DataManager.TYPE_WEB:
            rawdata = js.localStorage.getItem(self.data_key)
            if rawdata:
                self.data = json.loads(rawdata)
            #---clear data
            rawdata = js.localStorage.getItem(self.cleardata_key_timeattack)
            if rawdata:
                self.cleardata["timeattack"] = json.loads(rawdata)
            rawdata = js.localStorage.getItem(self.cleardata_key_survival)
            if rawdata:
                self.cleardata["survival"] = json.loads(rawdata)
        return ishit
    
    def save(self):
        if self.storage_mode == DataManager.TYPE_LOCAL:
            path = pyxel.user_data_dir(self.meta["vendor"], self.meta["appname"])
            fullpath = os.path.join(path, self.local_filename)
            with open(fullpath,"wt") as f:
                json.dump(self.data,f)
        elif self.storage_mode == DataManager.TYPE_WEB:
            js.localStorage.setItem(self.data_key, json.dumps(self.data))
            
    def save_result(self):
        if self.storage_mode == DataManager.TYPE_LOCAL:
            path = pyxel.user_data_dir(self.meta["vendor"], self.meta["appname"])
            fullpath = os.path.join(path, self.local_clearfilename_timeattack)
            with open(fullpath,"wt") as f:
                json.dump(self.cleardata["timeattack"],f)
            fullpath = os.path.join(path, self.local_clearfilename_survival)
            with open(fullpath,"wt") as f:
                json.dump(self.cleardata["survival"],f)
        elif self.storage_mode == DataManager.TYPE_WEB:
            js.localStorage.setItem(self.cleardata_key_timeattack, json.dumps(self.cleardata["timeattack"]))
            js.localStorage.setItem(self.cleardata_key_survival, json.dumps(self.cleardata["survival"]))
        
    def delete_alldata(self, isconfig: bool, isscore:bool):
        if self.storage_mode == DataManager.TYPE_LOCAL:
            path = pyxel.user_data_dir(self.meta["vendor"], self.meta["appname"])
            if isconfig:
                fullpath = os.path.join(path, self.local_filename)
                os.remove(fullpath)
            if isscore:
                fullpath = os.path.join(path, self.local_clearfilename_timeattack)
                os.remove(fullpath)
                fullpath = os.path.join(path, self.local_clearfilename_survival)
                os.remove(fullpath)
        elif self.storage_mode == DataManager.TYPE_WEB:
            if isconfig:
                js.localStorage.removeItem(self.data_key)
            if isscore:
                js.localStorage.removeItem(self.cleardata_key_timeattack)
                js.localStorage.removeItem(self.cleardata_key_survival)
        

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

    def get_timeattack_cleardata(self, time, forces) -> list:
        timekey = f"time_{time}"
        forceskey = f"forces_{forces}"
        return self.cleardata["timeattack"][forceskey]

    def get_survival_cleardata(self, forces) -> list:
        forceskey = f"forces_{forces}"
        return self.cleardata["survival"][forceskey]
    
    def set_timeattack_cleardata(self, time, forces, data: dict):
        timekey = f"time_{time}"
        forceskey = f"forces_{forces}"
        self.cleardata["timeattack"][forceskey].append(data)
    
    def set_survival_cleardata(self, forces, data: dict):
        forceskey = f"forces_{forces}"
        self.cleardata["survival"][forceskey].append(data)
    
    def delete_timeattack_cleardata(self, time, forces):
        timekey = f"time_{time}"
        forceskey = f"forces_{forces}"
        self.cleardata["timeattack"][timekey][forceskey].clear()
    
    def delete_survival_cleardata(self, forces):
        forceskey = f"forces_{forces}"
        self.cleardata["survival"][forceskey].clear()
    
    def get_enemy_summary(self, enemies: list, typeid, classid):
        cnt = 0
        max = 0
        for e in enemies:
            if (e["type"] == typeid) and (e["class"] == classid):
                cnt += e["cnt"]
                max += e["max"]
        return (cnt, max)