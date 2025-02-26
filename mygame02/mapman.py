import pyxel
from mycls import Vector2, Bounds, GameObject
from appconst import CSV_MAP_EVENT_IMG

class MapEvent(GameObject):
    def __init__(self, app, x, y):
        super().__init__(app, x, y)
        self.tilepos = Vector2(x, y)
        self.motioninx: int = 0
        self.motionlst: list[Bounds] = []
        self.motionspeed = 30
        
        self.target_enemy = -1
        self.target_firstlv = -1
    
    def change_image(self, lst: tuple):
        self.motionlst.clear()
        for t in lst:
            self.img_page = t[0]
            self.motionlst.append(Bounds(t[1],t[2],t[3],t[4]))
        
    def update(self):
        if len(self.motionlst) > 0:
            self.img_bnd.x = self.motionlst[self.motioninx].x
            self.img_bnd.y = self.motionlst[self.motioninx].y
            self.img_bnd.w = self.motionlst[self.motioninx].w
            self.img_bnd.h = self.motionlst[self.motioninx].h
        
        if pyxel.frame_count % self.motionspeed == 0:
            self.motioninx += 1
            if self.motioninx >= len(self.motionlst):
                self.motioninx = 0
        
        return super().update()

    def draw(self):
        pyxel.blt(self.tilepos.x*8, self.tilepos.y*8, self.img_page, self.img_bnd.x, self.img_bnd.y, self.img_bnd.w, self.img_bnd.h, pyxel.COLOR_BLACK)
        
        return super().draw()

class GameMap(GameObject):
    def __init__(self, app, x, y):
        super().__init__(app, x, y)
        self.tilesize = Vector2(8, 8)
        self.mapsize = Vector2(16, 16)
        self.events: list[MapEvent] = []
        
    def change_map(self, page, imgx, imgy, w, h):
        self.img_page = page
        self.img_bnd.x = imgx
        self.img_bnd.y = imgy
        self.img_bnd.w = w
        self.img_bnd.h = h
    
    def load_map_event(self, map: list[list]):
        self.events.clear()
        for ln in enumerate(map):
            for cl in enumerate(ln[1]):
                cell = cl[1]
                ev = MapEvent(self, cl[0], ln[0])
                if cell in CSV_MAP_EVENT_IMG:
                    ev.change_image(CSV_MAP_EVENT_IMG[cell])
                    self.events.append(ev)
                
                
        
    def update(self):
        
        for ev in self.events:
            ev.update()
        
        return super().update()
    
    def draw(self):
        pyxel.bltm(self.x, self.y, self.img_page, self.img_bnd.x, self.img_bnd.y, self.mapsize.x*self.tilesize.x, self.mapsize.y*self.tilesize.y, pyxel.COLOR_BLACK)
        
        for ev in self.events:
            ev.draw()
            
        return super().draw()