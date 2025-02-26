import os
import csv

class BankImageElement:
    def __init__(self, page = 0, x = 0, y = 0, w = 8, h = 8):
        self.page = page
        self.x = x
        self.y = y
        self.w = w
        self.h = h

class ImageBankManager:
    def __init__(self):
        self.images = {}
        
        #self.bnkcsv_filename = "assets/data/imgbnk.csv"
        for c in CSV_IMAGES:
            self.images[c] = BankImageElement(CSV_IMAGES[c][0], CSV_IMAGES[c][1], CSV_IMAGES[c][2], CSV_IMAGES[c][3], CSV_IMAGES[c][4])
        #self.load()
    
    def load(self):
        if os.path.exists(self.bnkcsv_filename):
            print("exist=",self.bnkcsv_filename)
            with open(self.bnkcsv_filename) as f:
                reader = csv.reader(f,delimiter="\t")
                for row in reader:
                    self.images[row[0]] = BankImageElement(row[1], row[2], row[3], row[4], row[5])
        else:
            print("csv file not found:", self.bnkcsv_filename)
            
    def get(self, name) -> BankImageElement:
        if name in self.images:
            return self.images[name]
        else:
            return None


CSV_IMAGES = {
    "nocollision" : (0, 8, 0, 8, 8),
    "missile"     : (0, 16, 0, 8, 8),
    "aashoot"     : (0, 24, 0, 8, 8),
    "SS_down"     : (0, 32, 0, 16, 16),
    "DD_down"     : (0, 48, 0, 16, 16),
    "ASDG_down"   : (0, 64, 0, 16, 16),
    "CL_down"     : (0, 80, 0, 16, 16),
    "CA_down"     : (0, 96, 0, 16, 16),
    "CVL_down"    : (0, 112, 0, 16, 16),
    "CV_down"     : (0, 128, 0, 16, 16),
    "BC_down"     : (0, 144, 0, 16, 16),
    "eDD1_a"      : (0, 160, 0, 8, 8),
    "eDD2_a"      : (0, 168, 0, 8, 8),
    "eCL_a"       : (0, 176, 0, 16, 16),
    "eCA_a"       : (0, 192, 0, 16, 16),
    "eCVL_a"      : (0, 208, 0, 16, 16),
    "eCV_a"       : (0, 224, 0, 32, 16),
    #
    "gun"         : (0, 0, 8, 8, 8),
    "torpedo"     : (0, 8, 8, 8, 8),
    "jet1"        : (0, 16, 8, 8, 8),
    "jet2"        : (0, 24, 8, 8, 8),
    "eDD1_b"      : (0, 160, 8, 8, 8),
    "eDD2_b"      : (0, 168, 8, 8, 8),
    #
    "ship"         : (0, 0, 16, 8, 8),
    "depthcharge"  : (0, 8, 16, 8, 8),
    "bbgun1"       : (0, 16, 16, 8, 16),
    "bbgun2"       : (0, 24, 16, 8, 16),
    "SS_back1"     : (0, 32, 16, 16, 16),
    "DD_back1"     : (0, 48, 16, 16, 16),
    "ASDG_back1"   : (0, 64, 16, 16, 16),
    "CL_back1"     : (0, 80, 16, 16, 16),
    "CA_back1"     : (0, 96, 16, 16, 16),
    "CVL_back1"    : (0, 112, 16, 16, 16),
    "CV_back1"     : (0, 128, 16, 16, 16),
    "BC_back1"     : (0, 144, 16, 16, 16),
    "eCL_b"       : (0, 176, 16, 16, 16),
    "eCA_b"       : (0, 192, 16, 16, 16),
    "eCVL_b"      : (0, 208, 16, 16, 16),
    "eCV_b"       : (0, 224, 16, 32, 16),
    #
    "asa_acraft"  : (0, 0, 24, 8, 8),
    #
    "mapsea1"      : (0, 0, 32, 8, 8),
    "mapwave"      : (0, 8, 32, 8, 8),
    "blast1"       : (0, 16, 32, 8, 8),
    "blast2"       : (0, 24, 32, 8, 8),
    "SS_back2"     : (0, 32, 32, 16, 16),
    "DD_back2"     : (0, 48, 32, 16, 16),
    "ASDG_back2"   : (0, 64, 32, 16, 16),
    "CL_back2"     : (0, 80, 32, 16, 16),
    "CA_back2"     : (0, 96, 32, 16, 16),
    "CVL_back2"    : (0, 112, 32, 16, 16),
    "CV_back2"     : (0, 128, 32, 16, 16),
    "BC_back2"     : (0, 144, 32, 16, 16),
    "eDDE_a"      : (0, 160, 32, 16, 16),
    "eSS_a"        : (0, 176, 32, 16, 16),
    "eBC_a"        : (0, 208, 32, 16, 32),
    "eBB_a"        : (0, 224, 32, 16, 32),
    #
    "maprock"     : (0, 0, 40, 8, 8),
    "maphashi"    : (0, 8, 40, 8, 8),
    "blast3"      : (0, 16, 40, 16, 8),
    #
    "mapwave2"    : (0, 0, 48, 8, 8),
    "mapwave3"    : (0, 8, 48, 8, 8),
    "blast4"      : (0, 16, 48, 16, 16),
    "SS_front1"     : (0, 32, 48, 16, 16),
    "DD_front1"     : (0, 48, 48, 16, 16),
    "ASDG_front1"   : (0, 64, 48, 16, 16),
    "CL_front1"     : (0, 80, 48, 16, 16),
    "CA_front1"     : (0, 96, 48, 16, 16),
    "CVL_front1"    : (0, 112, 48, 16, 16),
    "CV_front1"     : (0, 128, 48, 16, 16),
    "BC_front1"     : (0, 144, 48, 16, 16),
    "eDDE_b"      : (0, 160, 48, 16, 16),
    "eSS_b"        : (0, 176, 48, 16, 16),
    #
    #
    "checkoff"      : (0, 0, 64, 8, 8),
    "checkon"      : (0, 8, 64, 8, 8),
    "damecon"       : (0, 16, 64, 8, 8),
    "juice"       : (0, 24, 64, 8, 8),
    "SS_front2"     : (0, 32, 64, 16, 16),
    "DD_front2"     : (0, 48, 64, 16, 16),
    "ASDG_front2"   : (0, 64, 64, 16, 16),
    "CL_front2"     : (0, 80, 64, 16, 16),
    "CA_front2"     : (0, 96, 64, 16, 16),
    "CVL_front2"    : (0, 112, 64, 16, 16),
    "CV_front2"     : (0, 128, 64, 16, 16),
    "BC_front2"     : (0, 144, 64, 16, 16),
    "eBC_b"        : (0, 208, 64, 16, 32),
    "eBB_b"        : (0, 224, 64, 16, 32),
    #
    "larrow"      : (0, 0, 72, 8, 8),
    "rarrow"      : (0, 8, 72, 8, 8),
    "curry1"       : (0, 16, 72, 16, 8),
    #
    "cursor"      : (0, 0, 80, 16, 16),
    "curry2"      : (0, 16, 80, 16, 8),
    "SS_left"     : (0, 32, 80, 16, 16),
    "DD_left"     : (0, 48, 80, 16, 16),
    "ASDG_left"   : (0, 64, 80, 16, 16),
    "CL_left"     : (0, 80, 80, 16, 16),
    "CA_left"     : (0, 96, 80, 16, 16),
    "CVL_left"    : (0, 112, 80, 16, 16),
    "CV_left"     : (0, 128, 80, 16, 16),
    "BC_left"     : (0, 144, 80, 16, 16),
    #
    "rader2"       : (0, 16, 88, 16, 16),
    #
    "effect1"      : (0, 0, 96, 16, 16),
    "SS_right"     : (0, 32, 96, 16, 16),
    "DD_right"     : (0, 48, 96, 16, 16),
    "ASDG_right"   : (0, 64, 96, 16, 16),
    "CL_right"     : (0, 80, 96, 16, 16),
    "CA_right"     : (0, 96, 96, 16, 16),
    "CVL_right"    : (0, 112, 96, 16, 16),
    "CV_right"     : (0, 128, 96, 16, 16),
    "BC_right"     : (0, 144, 96, 16, 16),
    #
    "shield"       : (0,16,104,8,8),
    "rader1"       : (0,24,104,8,8),
    #
    "ginger_fishcakes"     : (0, 16, 112, 16, 16),
    "SS_mid_back1"     : (0, 32, 112, 16, 16),
    "DD_mid_back1"     : (0, 48, 112, 16, 16),
    "ASDG_mid_back1"   : (0, 64, 112, 16, 16),
    "CL_mid_back1"     : (0, 80, 112, 16, 16),
    "CA_mid_back1"     : (0, 96, 112, 16, 16),
    "CVL_mid_back1"    : (0, 112, 112, 16, 16),
    "CV_mid_back1"     : (0, 128, 112, 16, 16),
    "BC_mid_back1"     : (0, 144, 112, 16, 16),
    #
    "victory_c"        : (0, 0, 128, 32, 32),
    "SS_mid_back2"     : (0, 32, 128, 16, 16),
    "DD_mid_back2"     : (0, 48, 128, 16, 16),
    "ASDG_mid_back2"   : (0, 64, 128, 16, 16),
    "CL_mid_back2"     : (0, 80, 128, 16, 16),
    "CA_mid_back2"     : (0, 96, 128, 16, 16),
    "CVL_mid_back2"    : (0, 112, 128, 16, 16),
    "CV_mid_back2"     : (0, 128, 128, 16, 16),
    "BC_mid_back2"     : (0, 144, 128, 16, 16),
    #
    "SS_mid_front1"     : (0, 32, 144, 16, 16),
    "DD_mid_front1"     : (0, 48, 144, 16, 16),
    "ASDG_mid_front1"   : (0, 64, 144, 16, 16),
    "CL_mid_front1"     : (0, 80, 144, 16, 16),
    "CA_mid_front1"     : (0, 96, 144, 16, 16),
    "CVL_mid_front1"    : (0, 112, 144, 16, 16),
    "CV_mid_front1"     : (0, 128, 144, 16, 16),
    "BC_mid_front1"     : (0, 144, 144, 16, 16),
    #
    "victory_b"         : (0, 0, 160, 32, 32),
    "SS_mid_front2"     : (0, 32, 160, 16, 16),
    "DD_mid_front2"     : (0, 48, 160, 16, 16),
    "ASDG_mid_front2"   : (0, 64, 160, 16, 16),
    "CL_mid_front2"     : (0, 80, 160, 16, 16),
    "CA_mid_front2"     : (0, 96, 160, 16, 16),
    "CVL_mid_front2"    : (0, 112, 160, 16, 16),
    "CV_mid_front2"     : (0, 128, 160, 16, 16),
    "BC_mid_front2"     : (0, 144, 160, 16, 16),
    #
    "SS_mid_left"     : (0, 32, 176, 16, 16),
    "DD_mid_left"     : (0, 48, 176, 16, 16),
    "ASDG_mid_left"   : (0, 64, 176, 16, 16),
    "CL_mid_left"     : (0, 80, 176, 16, 16),
    "CA_mid_left"     : (0, 96, 176, 16, 16),
    "CVL_mid_left"    : (0, 112, 176, 16, 16),
    "CV_mid_left"     : (0, 128, 176, 16, 16),
    "BC_mid_left"     : (0, 144, 176, 16, 16),
    #
    "victory_a"        : (0, 0, 192, 32, 32),
    "SS_mid_right"     : (0, 32, 192, 16, 16),
    "DD_mid_right"     : (0, 48, 192, 16, 16),
    "ASDG_mid_right"   : (0, 64, 192, 16, 16),
    "CL_mid_right"     : (0, 80, 192, 16, 16),
    "CA_mid_right"     : (0, 96, 192, 16, 16),
    "CVL_mid_right"    : (0, 112, 192, 16, 16),
    "CV_mid_right"     : (0, 128, 192, 16, 16),
    "BC_mid_right"     : (0, 144, 192, 16, 16),
    #
    "SS_preview"     : (0, 32, 208, 16, 32),
    "DD_preview"     : (0, 48, 208, 16, 32),
    "ASDG_preview"   : (0, 64, 208, 16, 32),
    "CL_preview"     : (0, 80, 208, 16, 32),
    "CA_preview"     : (0, 96, 208, 16, 32),
    "CVL_preview"    : (0, 112, 208, 16, 32),
    "CV_preview"     : (0, 128, 208, 16, 32),
    "BC_preview"     : (0, 144, 208, 16, 32),
    #
    "victory_s"        : (0, 0, 224, 32, 32),
    
}

IBNK = ImageBankManager()
