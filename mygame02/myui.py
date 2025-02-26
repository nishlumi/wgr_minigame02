from mycls import Vector2, Bounds, pos
from appconst import IMGPLT_1, IMG_CONFIG_CHECK_X, IMG_CONFIG_CHECK_Y, IMG_CONFIG_UNCHECK_X
import pyxel
import re

class TextWrapper:
    def __init__(self, char_width=8, char_height=8):
        self.char_width = char_width
        self.char_height = char_height
        
    def is_japanese_char(self, char):
        return '\u4e00' <= char <= '\u9fff' or \
               '\u3040' <= char <= '\u309f' or \
               '\u30a0' <= char <= '\u30ff' or \
               char in 'ー～－＠'

    def calc_text_width(self, text):
        total_width = 0
        for char in text:
            if self.is_japanese_char(char):
                total_width += self.char_width
            else:
                total_width += self.char_width // 2
        return total_width

    def split_text(self, text):
        # 英単語、日本語文字、句読点などを分割
        pattern = r'([ぁ-んァ-ン一-龥ーｰ～－、。！？]|[a-zA-Z0-9]+|[\/,.!?@<>\-]|\s+)'
        return [x for x in re.findall(pattern, text) if x]

    def wrap_text(self, text, max_width):
        words = self.split_text(text)
        lines = []
        current_line = []
        current_width = 0

        for word in words:
            word_width = self.calc_text_width(word)

            # 現在の行に単語を追加できる場合
            if current_width + word_width <= max_width:
                current_line.append(word)
                current_width += word_width
            else:
                # 英単語の場合
                if re.match(r'^[a-zA-Z0-9]+$', word):
                    # 現在の行が空でない場合、確定して次の行へ
                    if current_line:
                        lines.append(''.join(current_line))
                        current_line = []
                        current_width = 0
                    
                    # 単語自体が最大幅を超える場合のみ分割
                    if word_width > max_width:
                        chars = list(word)
                        temp_line = []
                        temp_width = 0
                        
                        for char in chars:
                            char_width = self.calc_text_width(char)
                            if temp_width + char_width <= max_width:
                                temp_line.append(char)
                                temp_width += char_width
                            else:
                                if temp_line:  # 行が空でない場合のみ追加
                                    lines.append(''.join(temp_line))
                                temp_line = [char]
                                temp_width = char_width
                        
                        if temp_line:
                            current_line = temp_line
                            current_width = temp_width
                    else:
                        current_line = [word]
                        current_width = word_width
                # 日本語文字や句読点の場合
                else:
                    if current_line:
                        lines.append(''.join(current_line))
                    current_line = [word]
                    current_width = word_width

        # 最後の行を追加
        if current_line:
            lines.append(''.join(current_line))

        return lines

class GameUI:
    TYPE_TEXT = 0
    TYPE_IMAGE = 1
    TYPE_CHECKBOX = 2
    TYPE_RECT = 3
    TYPE_BUTTON = 4
    TYPE_DIALOG = 5
    def __init__(self, uitype: int, xywh: Bounds):
        self.name = ""
        self.bounds: Bounds = xywh  #Bounds(0, 0, 0, 0)
        self.endx: int = 0
        self.endy: int = 0
        self.set_size(self.bounds.w, self.bounds.h)
        self.type = uitype
        self.roundui = {
            "up": None,
            "left": None,
            "right": None,
            "bottom": None
        }
        self.referlist: dict = {}
        self.selectable = False
    
    def get_object(self, name):
        if name in self.referlist:
            return self.referlist[name]
        return None
    
    def set_round(self, upui = None, leftui = None, rightui = None, bottomui = None):
        if type(upui) == str:
            self.roundui["up"] = self.get_object(upui)
        else:
            self.roundui["up"] = upui
        if type(leftui) == str:
            self.roundui["left"] = self.get_object(leftui)
        else:
            self.roundui["left"] = leftui
        if type(rightui) == str:
            self.roundui["right"] = self.get_object(rightui)
        else:
            self.roundui["right"] = rightui
        if type(bottomui) == str:
            self.roundui["bottom"] = self.get_object(bottomui)
        else: 
            self.roundui["bottom"] = bottomui
        
    def set_pos(self, x, y):
        self.bounds.x = x
        self.bounds.y = y
    
    def set_size(self, w, h):
        self.bounds.w = w
        self.bounds.h = h
        self.endx = self.bounds.x + self.bounds.w
        self.endy = self.bounds.y + self.bounds.h
    
    def check_touch_area(self, x, y):
        ishit = False
        ishit = (self.bounds.x <= x <= self.endx) and (self.bounds.y <= y <= self.endy)
        if not self.selectable:
            ishit = False
        
        return ishit
        
    def update(self):
        pass

    def draw(self):
        pass
    
class GUIImage(GameUI):
    def __init__(self, x: int , y: int, image_page, image_rect: Bounds, col_key: int = 0, rotate=0, scale=1.0):
        super().__init__(GameUI.TYPE_IMAGE, Bounds(x, y, image_rect.w, image_rect.h))
        self.img_page = image_page
        self.img_bnd: Bounds = image_rect
        self.tracol = col_key
        self.rotate = rotate
        self.scale = scale
    
    def update(self):
        return super().update()

    def draw(self):
        pyxel.dither(1)
        pyxel.blt(self.bounds.x, self.bounds.y, self.img_page, self.img_bnd.x, self.img_bnd.y, self.img_bnd.w, self.img_bnd.h, self.tracol, self.rotate, self.scale)
        return super().draw()
        
        
class GUIText(GameUI):
    def __init__(self, text: str, x: int , y: int, font = None, color1 = pyxel.COLOR_BLACK, color2 = pyxel.COLOR_BLACK, shifted_x: int = 0, shifted_y: int = 0):
        super().__init__(GameUI.TYPE_TEXT, Bounds(x, y, 0, 0))
        self.wrapper = TextWrapper(8, 8)
        self.is_wrap = True
        self.realtexts = []
        self.set_text(text)
        self.color1 = color1
        self.color2 = color2
        self.shifted = Vector2(shifted_x, shifted_y)
        self.font = font

    def set_text(self, text):
        self.realtexts.clear()
        self.text = text
        self.bounds.w = len(text) * 8
        self.bounds.h = 8
        self.endx = self.bounds.x + self.bounds.w
        self.endy = self.bounds.y + self.bounds.h
        #---calculate wrappered text
        if self.is_wrap:
            self.recalc_wrap()
        else:
            self.realtexts.append(self.text)
    
    def recalc_wrap(self):
        self.realtexts = self.wrapper.wrap_text(self.text, self.bounds.w)
        
    def update(self):
        return super().update()
    
    def draw(self):
        pyxel.dither(1)
        for i, line in enumerate(self.realtexts):
            if (self.shifted.x != 0 or self.shifted.y != 0):
                pyxel.text(self.bounds.x+self.shifted.x, self.bounds.y+self.shifted.y + i * self.wrapper.char_height, line, self.color2, self.font)
            pyxel.text(self.bounds.x, self.bounds.y + i * self.wrapper.char_height, line, self.color1, self.font)
            
        return super().draw()

class GUICheckbox(GameUI):
    def __init__(self, text, x, y, chked: bool = False, font=None, color1=pyxel.COLOR_BLACK, color2=pyxel.COLOR_BLACK, shifted_x = 0, shifted_y = 0):
        super().__init__(GameUI.TYPE_CHECKBOX, Bounds(x, y, 8, 8))
        self.type = GameUI.TYPE_CHECKBOX
        #self.check_bounds = Bounds(x, y, 8, 8)
        self.checked = chked
        self.text = GUIText(text, x+12, y, font, color1, color2, shifted_x, shifted_y)
        self.selectable = True

    def check_touch_area(self, x, y):
        ishit = super().check_touch_area(x, y)
        #---check checkbox
        
        ishit = (
            self.bounds.x <= x <= (self.bounds.x+self.bounds.w)
            ) and (
            self.bounds.y <= y <= (self.bounds.y+self.bounds.h)
        )
        if not self.selectable:
            ishit = False
        
        #if ishit:
        #    print(self.name,self.check_bounds.x,self.check_bounds.w,self.bounds.w)
        #---check text
        #if ishit:
        #    return ishit
        
        #ishit = super().check_touch_area(x, y)
        
        return ishit
    
    def update(self):
        
        self.text.update()
        return super().update()
    
    def draw(self):
        pyxel.dither(1)
        if self.checked:
            pyxel.blt(self.bounds.x, self.bounds.y, IMGPLT_1, IMG_CONFIG_CHECK_X, IMG_CONFIG_CHECK_Y, self.bounds.w, self.bounds.h, pyxel.COLOR_BLACK)
        else:
            pyxel.blt(self.bounds.x, self.bounds.y, IMGPLT_1, IMG_CONFIG_UNCHECK_X, IMG_CONFIG_CHECK_Y, self.bounds.w, self.bounds.h, pyxel.COLOR_BLACK)
        self.text.draw()
        
        return super().draw()

class GUIRect(GameUI):
    def __init__(self, x, y, w, h, color, filled = True, transparency = 1.0, transparent_interval = 0):
        super().__init__(GameUI.TYPE_RECT, Bounds(x, y, w, h))
        self.color = color
        self.filled = filled
        self.transparency = transparency
        self.transparent_interval = transparent_interval
        self.cur_interval = self.transparency
        if self.transparent_interval > 0:
            self.interval_calcflag = (1.0 - self.transparency) / self.transparent_interval
        else:
            self.interval_calcflag = 0.0
    
    def update(self):
        if self.transparent_interval > 0:
            if self.cur_interval == self.transparency:
                self.interval_calcflag = (1.0 - self.transparency) / self.transparent_interval
            elif self.cur_interval > 1.0:
                self.interval_calcflag = -((1.0 - self.transparency) / self.transparent_interval)
        
        self.cur_interval += self.interval_calcflag
        return super().update()
    
    def draw(self):
        
        pyxel.dither(self.cur_interval)
        pyxel.rect(self.bounds.x, self.bounds.y, self.bounds.w, self.bounds.h, self.color)
        
        return super().draw()

class GUIButton(GameUI):
    def __init__(self, label, x, y, w, h, font: pyxel.Font = None):
        super().__init__(GameUI.TYPE_BUTTON, Bounds(x, y, w, h))
        self.set_text(label)
        self.pressed = False
        self.bgcolor = pyxel.COLOR_WHITE
        self.fontcolor = pyxel.COLOR_BLACK
        self.font = font
    
    def set_text(self, text):
        self.label = text
        self.labellen = len(text)
        self.bounds.w = (self.labellen+1) * 4
        self.labelposx = self.bounds.x + ((self.bounds.w - self.labellen * 4) / 2) 
    
    def update(self):
        if (
            (self.bounds.x <= pyxel.mouse_x <= (self.bounds.x + self.bounds.w))
            and
            (self.bounds.y <= pyxel.mouse_y <= (self.bounds.y + self.bounds.h))
        ):
            self.pressed = pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
        
        return super().update()
    
    def draw(self):
        pyxel.rect(self.bounds.x, self.bounds.y, self.bounds.w, self.bounds.h, self.bgcolor)
        #if self.label != "":
        pyxel.text(self.labelposx, self.bounds.y, self.label, self.fontcolor, self.font)
        
        return super().draw()
    
class GUIDialog(GameUI):
    BTN_OK = 0
    BTN_YESNO = 1
    BTN_YESNOCANCEL = 2
    def __init__(self, x, y, w, h, btns = BTN_OK):
        super().__init__(GameUI.TYPE_DIALOG, Bounds(x, y, w, h))
        
        self.contents = []
        self.buttons = []
        if btns == self.BTN_OK:
            button = GUIButton("OK", 0, h - 8, 0, 8)
            button.bounds.x = self.bounds.w - self.button.bounds.w - 4
            button.bounds.y = self.bounds.y + self.bounds.h - 8
            button.set_text("OK")
            #print(self.button.bounds.x, self.button.bounds.y, self.button.labelposx)
            self.buttons.append(button)
        elif btns == self.BTN_YESNO:
            button = GUIButton("NO", 0, h - 8, 0, 8)
            button.bounds.x = self.bounds.w - button.bounds.w - 4
            button.bounds.y = self.bounds.y + self.bounds.h - 8
            button.set_text("NO")
            button1 = GUIButton("Yes", 0, h - 8, 0, 8)
            button1.bounds.x = self.bounds.w - button.bounds.w - 4 - button1.bounds.w - 4
            button1.bounds.y = self.bounds.y + self.bounds.h - 8
            button1.set_text("Yes")
            self.buttons.append(button1)
            self.buttons.append(button)
        self.drawtime = 15
        self.curdraw = 0
        self.is_statdraw = False
        self.is_drawend = False
    
    def add_contents(self, element: GameUI):
        element.bounds.x += self.bounds.x
        element.bounds.y += self.bounds.y
        if element.type == GameUI.TYPE_TEXT:
            element.bounds.w = self.bounds.w
            element.recalc_wrap()
        self.contents.append(element)
    
    def open(self):
        self.is_statdraw = True
    
    def is_open(self):
        return self.is_drawend
    
    def close(self):
        self.is_statdraw = False
        self.is_drawend = False
        self.curdraw = 0
        for button in self.buttons:
            button.pressed = False
        
    def update(self):
        if self.is_statdraw:
            if self.is_drawend:
                for u in self.contents:
                    u.update()
                
                for button in self.buttons:
                    button.update()
            else:
                if self.curdraw <= self.drawtime:
                    self.curdraw += 1
                else:
                    self.is_drawend = True
                    self.curdraw = 0
                    
        
        return super().update()
    
    def draw(self):
        if self.is_drawend:
            pyxel.dither(0.1)
            pyxel.rect(0, 0, pyxel.width, pyxel.height, pyxel.COLOR_BLACK)
            pyxel.dither(1.0)
            pyxel.rect(self.bounds.x, self.bounds.y, self.bounds.w, self.bounds.h, pyxel.COLOR_BLACK)
            for u in self.contents:
                u.draw()
            for button in self.buttons:
                button.draw()
        else:
            pyxel.rect(self.bounds.x, self.bounds.y, pos(self.curdraw), self.bounds.h, pyxel.COLOR_BLACK)
        
        return super().draw()

class GUIPauseButton(GUIButton):
    def __init__(self, x, y, w, h, font = None):
        super().__init__("P", x, y, w, h, font)
        
    def update(self):
        return super().update()
    
    def draw(self):
        return super().draw()