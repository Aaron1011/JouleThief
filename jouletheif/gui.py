
import pygame

def noCallBack():
    print "No Callback Set!"

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, text, callback=noCallBack, textsize=20, tcolor=(0,255,0), ocolor=(0,0,255)):
        #self.rect=pygame.rect.Rect(x,y,xsize,ysize)
        #print "making font"
        textf=pygame.font.Font("freesansbold.ttf", textsize)#load font, use to make image, use pygame.draw to add rect
        #print "made"
        #print "making image"
        s=textf.size(text)
        self.image=pygame.surface.Surface((s[0]+5, s[1]+5))
        #print "drawing text"
        #print "surface..."
        surf=textf.render(text, False, tcolor)
        #print "sim size..."
        
        #print "gen rect..."
        r=pygame.rect.Rect(0,0,s[0],s[1])
        #print "blitting"
        self.image.blit(surf,r)
        #print "drawing rect"
        pygame.draw.rect(self.image, ocolor, pygame.rect.Rect(0,0,s[0], s[1]), 3)
        #print "genning rect"
        self.rect=pygame.rect.Rect(x,y,s[0],s[1])
        #print "rect set. setting callback"
        self.callback=callback
        #print "dont. setting calledback"
        self.calledback=False
        #print "done"
    def update(self):
        if self.rect.contains(pygame.rect.Rect(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1], 1, 1)) and pygame.mouse.get_pressed()[0] and not self.calledback:
            self.callback.__call__()
            self.calledback=True
    def draw(self, screen):
        screen.blit(self.image, self.rect)
class MButton(Button):
    cup=0
    def update(self):
        self.cup += 1
        if self.cup==200:
            self.calledback=False
            self.cup=0
        Button.update(self)