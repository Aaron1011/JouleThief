import datetime #for logging
import pygame
import time
import sys
levels=['*DUMP', 'DEBUG', '*INFO', 'ERROR', '*CRIT', '*FAIL'] #log level names
fileloglevel=1
printloglevel=2
filename=None
moveamount=None
wintitle=None
jumpamount=None
accelamount=None
accelmax=None
delay=None
repeat=None
print "PRELOG... Loading configuration"
execfile("config.py") #execute config.pcfg in the current namespace (set defaults, then modify them in the config)
def _log_format(message, level):
    global levels
    return str(datetime.datetime.now())+"\t["+levels[level]+"]: "+message
def log(message, level):
    global fileloglevel, printloglevel, filename
    f=open(filename, 'a')
    if level>=printloglevel: print _log_format(message, level)
    if level>=fileloglevel: f.write(_log_format(message, level)+"\n")
    f.close()
def dump(message): log(message, 0) #log message at XXXX? level
def debug(message): log(message, 1)
def info(message): log(message, 2)
def error(message): log(message, 3)
def crit(message): log(message, 4)
def fail(message): log(message, 5)
debug("==========================SESS_BR8K=============================")
info("Loading")
debug("Logging Initilized")
debug("Importing Pygame")

def load_image(name, colorkey=None):
    fullname = name#os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', fullname
        raise SystemExit, message
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()
class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.image,self.rect=load_image("image/char.png")
        self.image=self.image.convert_alpha()
        self.setXY(x,y)
    def update(self, up, down, left, right, platforms):
        if up:
            # only jump if on the ground
            if self.onGround: self.yvel -= jumpamount
        if down:
            pass
        if left:
            self.xvel = -moveamount
        if right:
            self.xvel = moveamount
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += accelamount
            # max falling speed
            if self.yvel > accelmax: self.yvel = accelmax
        if not(left or right):
            self.xvel = 0
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        self.collide(self.xvel, 0, platforms)
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        self.collide(0, self.yvel, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if p.rect.colliderect(self):#pygame.sprite.collide_rect(self, p):
                
                if xvel > 0: self.rect.right = p.rect.left
                if xvel < 0: self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0: 
                    self.rect.top = p.rect.bottom
                    self.yvel=0
                p.onPlayerCollide(self)

    def setXY(self, x, y):
        self.rect=pygame.Rect(x,y,16,16)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
class Platform(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image, _ = load_image("image/ocolor_tile.png")
        self.rect = pygame.Rect(x, y, 16, 16)

    def update(self):
        pass

    def onPlayerCollide(self, player):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)
class WinPlatform(Platform):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image, _ = load_image("image/battery_full.png")
        self.rect = pygame.Rect(x, y, 16, 16)
    def onPlayerCollide(self, player):
        print "YOU FUCKING WIN"
class SpikePlatform(Platform):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image, _ = load_image("image/bot1.png")
        self.rect = pygame.Rect(x, y, 16, 16)
    def onPlayerCollide(self, player):
        print "Death"
        raw_input("YOU FCKED UP NOW YOUR DEAD (PRESS ENTER)")
        sys.exit(1)
class TeleporterPlatform(Platform):
    def __init__(self, x, y, linkx, linky):
        Entity.__init__(self)
        self.image, _ = load_image("image/battery_empty.png")
        self.rect = pygame.Rect(x, y, 16, 16)
        self.linkx=linkx
        self.linky=linky
    def onPlayerCollide(self, player):
        player.setXY(self.linkx, self.linky)
        debug("Teleporting "+str(player)+" to "+str(self.linkx)+" X "+str(self.linky))
class NonsolidRect(pygame.rect.Rect):
    def colliderect(self, *args, **kwargs):return False
    def collidelist(self, *args, **kwargs):return False
    def collidelistall(self, *args, **kwargs):return False
    def collidedict(self, *args, **kwargs):return False
    def collidedictall(self, *args, **kwargs):return False
    def contains(self, *args, **kwargs):return False
    def collidepoint(self, *args, **kwargs):return False
    def collide_rect(self, *args, **kwargs):return False
class DecorationPlatform(Platform):
    def __init__(self, x, y, path):
        Entity.__init__(self)
        self.image, _ = load_image(path)
        self.rect = NonsolidRect(x,y,16,16)
class ExecuteCodePlatform(Platform):
    def __init__(self, x, y, command, path):
        Entity.__init__(self)
        self.image, _ = load_image(path)
        self.rect = pygame.Rect(x, y, 16, 16)
        self.cmd=command
    def onPlayerCollide(self, player):
        exec self.cmd
def load_level(name):
    debug("Loading Level")
    _lvl_map=None
    _lvl_level=None
    #exec "from level import lvl"+str(name)+"_map as _lvl_map"
    #exec "from level import lvl"+str(name)+"_level as _lvl_level"
    lvl=None
    debug("Excecuting: "+"import lvl"+str(name)+" as lvl")
    sys.path.append("./lvl")
    exec "import lvl"+str(name)+" as lvl"
    _lvl_map, _lvl_level = lvl._lvl_map, lvl._lvl_level
    assert _lvl_map !=None
    assert _lvl_level !=None
    debug("Passed assertions")
    loaded=[]
    l=0
    for line in _lvl_level:
        c=0
        #print "l:"+str(line)
        for char in line:
            #print "c:"+str(char)
            #print str(line.index(char))
            #print str(_lvl_level.index(line))
            #print _lvl_map[char].replace("%1%", str(line.index(char)*16)).replace("%2%", str(_lvl_level.index(line)*16))
            if char!=" ":loaded.append(eval(_lvl_map[char].replace("%1%", str(c*16)).replace("%2%", str(l*16))))
            c+=1
        l+=1
    return loaded, lvl.setx, lvl.sety

debug("Init Pygame")
ltag=raw_input("Level tag: ")
pygame.init()
debug("Opening Window")
pygame.display.set_caption(wintitle)
screen=pygame.display.set_mode((650,450))
info("Starting!")
run=True
debug("Creating Player")
player=Player(2*16,2*16)
debug("Setting Repeat")
pygame.key.set_repeat(delay, repeat)
up=down=left=right=False
level, px, py=load_level(ltag)
player.setXY(px, py)
timer=pygame.time.Clock()
up=down=left=right=False
while run:
    timer.tick(50)
    for e in pygame.event.get():
        if e.type == pygame.QUIT: raise SystemExit, "QUIT"
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            raise SystemExit, "ESCAPE"
        if e.type == pygame.KEYDOWN and e.key == pygame.K_UP:
            up = True
        if e.type == pygame.KEYDOWN and e.key == pygame.K_DOWN:
            down = True
        if e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT:
            left = True
        if e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT:
            right = True

        if e.type == pygame.KEYUP and e.key == pygame.K_UP:
            up = False
        if e.type == pygame.KEYUP and e.key == pygame.K_DOWN:
            down = False
        if e.type == pygame.KEYUP and e.key == pygame.K_LEFT:
            left = False
        if e.type == pygame.KEYUP and e.key == pygame.K_RIGHT:
            right = False
    player.update(up, down, left, right, level)
    screen.fill((0,0,0))
    for i in level:i.draw(screen)
    player.draw(screen)
    pygame.display.flip()
    time.sleep(0.015)
info("Closing")