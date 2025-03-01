from typing import NamedTuple, TypedDict

SINGLE_FONTSIZE = 8
DOUBLE_FONTSIZE = 16

IMGPLT_1 = 0
IMGPLT_2 = 1
IMGPLT_3 = 2
IMGPLT_4 = 3
IMG_CONFIG_CHECK_X = 8
IMG_CONFIG_CHECK_Y = 64
IMG_CONFIG_UNCHECK_X = 0

class GameMode:
    TYPE_TIMEATTACK = 0
    TYPE_SURVIVAL = 1
    def __init__(self):
        self.current = 0

class TimeAttackRule:
    TYPE_TIME_SHORT = 0
    TYPE_TIME_MIDDLE = 1
    TYPE_TIME_LONG = 2
    TYPE_FORCES_ALL = 0
    TYPE_FORCES_VANGUARD = 1
    TYPE_FORCES_SMALLSHIPS = 2
    TYPE_FORCES_AIRFORCE = 3
    TYPE_FORCES_HIGHFIRE = 4
    TYPE_LV1_ONLY = 0
    TYPE_LV2_ONLY = 1
    TYPE_LV3_ONLY = 2
    TYPE_LV12_ONLY = 3
    TYPE_LV1 = 4
    TYPE_LV2 = 5
    TYPE_LV3 = 6
    TIME_LIST = ["60", "120", "180"]
    FORCE_LIST = ["ALL", "DD,CL,CA", "SS,DD", "CVL,CV", "CV,BC,BB"]
    def __init__(self):
        self.current = 0

class SurvivalRule:
    TYPE_FORCES_VANGUARD = 0
    TYPE_FORCES_SMALLSHIPS = 1
    TYPE_FORCES_AIRFORCE = 2
    TYPE_FORCES_HIGHFIRE = 3
    TYPE_FORCES_ALL = 4
    FORCE_LIST = ["DD,CL,CA", "SS,DD", "CVL,CV", "CV,BC,BB","ALL"]
    def __init__(self):
        pass
class ShipKind:
    TYPE_SS = 0
    TYPE_DD = 1
    TYPE_ASDG = 2
    TYPE_CL = 3
    TYPE_CA = 4
    TYPE_CVL = 5
    TYPE_CV = 6
    TYPE_BC = 7
    TYPE_BB = 8
    LIST = ["SS", "DD", "ASDG", "CL", "CA", "CVL","CV", "BC", "BB"]
    def __init__(self):
        self.dummy = 0
    

class PlayableCharacterSelector:
    def __init__(self, title, jobtype, img_x, previewkey):
        self.title: str = title
        self.jobtype: int = jobtype
        self.image_x: int = img_x
        self.previewkey = previewkey

CSV_PLAYABLE = {
    "img_ss" : PlayableCharacterSelector("SS U47", 0, 32, "SS_preview"),
    "img_dd" : PlayableCharacterSelector("DD Ayanami",1, 48, "DD_preview"),
    "img_asdg" : PlayableCharacterSelector("ASDG Changchun",2, 64, "ASDG_preview"),
    "img_cl" : PlayableCharacterSelector("CL Atlanta",3, 80, "CL_preview"),
    "img_ca" : PlayableCharacterSelector("CA Quincy",4, 96, "CA_preview"),
    "img_cvl" : PlayableCharacterSelector("CVL Junyo",5, 112, "CVL_preview"),
    "img_cv" : PlayableCharacterSelector("CV-16 Lexington",6, 128, "CV_preview"),
    "img_bc" : PlayableCharacterSelector("BC HMS Renown",7, 144, "BC_preview")
}
class CursorImagePosition(NamedTuple):
    x: int
    y: int

CIP = TypedDict
CIP.top = CursorImagePosition(2, 80)
CIP.left = CursorImagePosition(0, 82)
CIP.right = CursorImagePosition(14, 82)
CIP.bottom = CursorImagePosition(2, 94)


IMG_CHARA_X = [
    32,  #---0: SS
    48,  #---1: DD
    64,  #---2: ASDG
    80,  #---3: CL
    96,  #---4: CA
    112, #---5: CVL
    128, #---6: CV
    144, #---7: BC
    144  #---8: BB
]
PLAYER_MOTION = {
    "dead": 0, "up": 16, "up_move": 32,
    "down": 48, "down_move": 64,
    "left_move": 80, "right_move": 96,
    "double_image" : 208 
}
MAP_SEA1 = {
    "page" : 0,
    "x" : 0,
    "y" : 0,
    "w" : 16 * 16,
    "h" : 16 * 24
}
WEAPON_IMAGES = {
    "GUN" : (0, 8),
    "TORPEDO" : (8, 8),
    "AIRCRAFT" : (16, 8),
    "AASHOOT" : (24, 0),
    "MISSILE" : (16, 0),
    "BBGUN" : (16, 16),
    "DEPTHCHARGE" : (8, 16)
}
WEAPON_IMGKEY = [
    "gun","torpedo","jet1","bbgun1","aashoot","missile","depthcharge","asa_acraft"
]
CSV_ATTACKWEAK = [
    #SS     DD     ADSG   CL     CA     CVL    CV     BC,    BB
    [False, True,  True,  True,  True,  True,  True,  True,  True], #---GUN
    [False, True,  True,  True,  True,  True,  True,  True,  True], #---TORPEDO
    [False, True,  True,  True,  True,  True,  True,  True,  True], #---AIRCRAFT
    [False, True,  True,  True,  True,  True,  True,  True,  True], #---BBGUN
    [False, True,  True,  True,  True,  True,  True,  True,  True], #---AASHOOT
    [False, True,  True,  True,  True,  True,  True,  True,  True], #---MISSILE
    [True,  False, False, False, False, False, False, False, False], #---DEPTHCHARGE
    [True,  True,  True,  True,  True,  True,  True,  True,  True], #---ANTI-SUBMARNE Attack AIRCRAFT
]

CSV_ENEMY_APPEAR_RATE = {
    "appear_interval" : (40, 30, 15),
    #"appear_ddlv2"    : (20, 15, 10),
    #"appear_ddlv3"    : (15, 10, 15),
    "appear_ss"       : ( 5,  7, 10),
    "appear_cl"       : (20, 20, 25),
    "appear_ca"       : (15, 17,  8),
    "appear_cvl"      : (10, 12, 15),
    "appear_cv"       : ( 5,  7,  7),
    "appear_bc"       : ( 5,  5,  7),
    "appear_bb"       : ( 2,  3,  8)
}
CSV_TIMEATTACK_TIME = (60, 120, 180)
CSV_TIMEATTACK_APPEAR_RATE = {
    #            all       vanguard  smallship  airforces highfire
    "SS"       : (( 1, 5), ( 0, 0),  ( 1,25),   ( 0, 0),  ( 0, 0) ),
    "CL"       : (( 6,25), ( 1,30),  (26,35),   ( 1,10),  ( 1,10) ),
    "CA"       : ((26,40), (31,55),  (36,40),   (11,15),  (11,20) ),
    "CVL"      : ((41,50), (56,57),  (41,41),   (16,50),  (21,25) ),
    "CV"       : ((51,55), (58,58),  (42,42),   (51,75),  (26,50) ),
    "BC"       : ((56,60), (59,59),  (43,43),   (76,76),  (51,80) ),
    "BB"       : ((61,62), (60,60),  (44,44),   (77,77),  (81,96) ),
    "DD"       : ((63,100),(61,100), (45,100),  (78,100), (97,100) ),
}

CSV_TIMEATTACK_APPEAR_LV = (
    ((1, 100),(0, 0),(0, 0)),    #---lv 1 only
    ((0, 0),(1, 100),(0, 0)),    #---lv 2 only
    ((0, 0),(0, 0),(1, 100)),    #---lv 3 only
    ((1, 70),(71, 100),(0,0)),   #---lv.1,2 only
    ((1, 70),(71, 90),(91,100)), #---lots of lv.1 (lv1, lv2, lv3)
    ((1, 50),(51, 90),(91,100)), #---lots of lv.2 (lv1, lv2, lv3)
    ((1, 30),(31, 60),(61,100)), #---lots of lv.3 (lv1, lv2, lv3)
)

CSV_RANK_IMAGE = [
    (0, 128, 32, 32),     #---C
    (0, 160, 32, 32),     #---B
    (0, 192, 32, 32),     #---A
    (0, 224, 32, 32),     #---S
]

CSV_MAP_EVENT_IMG = {
    "E1" : ((2, 0, 16, 8, 8),(2, 0, 32, 8, 8)),
    "E2" : ((2, 8, 16, 8, 8),(2, 8, 32, 8, 8)),
    "E3" : ((2, 0, 24, 8, 8),(2, 0, 40, 8, 8)),
    "D"  : ((2, 8, 24, 8, 8),(2, 8, 40, 8, 8)),
}
CSV_BMAP1 = [
    ["S",   "S",    "S",    "S",    "S",    "S",    "E3",   "E3",   "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S"],
    ["S",   "S",    "S",    "S",    "S",    "S",    "E1",   "E2",   "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S"],
    ["S",   "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S"],
    ["E3",  "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S"],
    ["E3",  "E3",   "S",    "S",    "S",    "S",    "S",    "S",    "E3",   "S",    "S",    "S",    "S",    "S",    "S",    "S"],
    ["S",   "S",    "S",    "S",    "S",    "S",    "S",    "S",    "E2",   "E2",   "S",    "S",    "S",    "S",    "S",    "S"],
    ["S",   "S",    "S",    "S",    "S",    "S",    "S",    "S",    "E1",   "S",    "S",    "S",    "S",    "S",    "S",    "S"],
    ["S",   "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S"],
    ["S",   "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S"],
    ["S",   "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "E3",   "S",    "S",    "S"],
    ["S",   "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "E1",   "E1",   "E2",   "S",    "S"],
    ["S",   "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S"],
    ["S",   "S",    "E1",   "S",    "S",    "S",    "S",    "E1",   "E2",   "S",    "S",    "S",    "S",    "S",    "S",    "S"],
    ["S",   "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S"],
    ["S",   "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S"],
    ["S",   "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S",    "S"],
]