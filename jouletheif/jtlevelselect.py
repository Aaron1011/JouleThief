
import pygame, datetime, gui, os



levels=['*DUMP', 'DEBUG', '*INFO', 'ERROR', '*CRIT', '*FAIL'] #log level names
fileloglevel=1
printloglevel=2
wintitle=None
call=None
execfile("config.py")
filename="jtlevelselect.log"
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
currlvlloc=0
ll2=[]
def leftButtonCallback():
    global currlvlloc, ll2
    debug("left clicked")
    if currlvlloc!=0:
        debug("Moving to "+str(currlvlloc-1))
        currlvlloc -= 1
def rightButtonCallback():
    global currlvlloc, ll2
    debug("right clicked")
    if currlvlloc<len(ll2)-1:
        debug("Moving to "+str(currlvlloc+1))
        currlvlloc += 1
def selectButtonCallback():
    global currlvlloc, ll2
    debug("selected level "+ll2[currlvlloc])
    pygame.quit()
    info("Starting Main Game Engine")
    dump(call.replace("%", "jtengine")+" "+ll2[currlvlloc])
    os.system(call.replace("%", "jtengine")+" "+ll2[currlvlloc])
    raise SystemExit

info("Starting JTLevelSelect")
debug("init pygame")
pygame.init()
debug("inited")
debug("pop screen")
screen=pygame.display.set_mode((650,450))
debug("popped")
debug("settitle")
pygame.display.set_caption(wintitle)
debug("set. making button")

info("Loading Level List")
lvllist=os.listdir("lvl/")
debug("list: "+str(lvllist))
debug("Filtering list")
ll2=[]
for i in lvllist:
    if i.endswith(".py"):
        ll2.append(i.replace("lvl", "").replace(".py", ""))
debug("list2:"+str(ll2))

l_button=gui.MButton(100,100, "<-", leftButtonCallback)
r_button=gui.MButton(200,100, "->", rightButtonCallback)
debug("Button Initilized")

while 1:
    s_button=gui.Button(125, 100, ll2[currlvlloc], selectButtonCallback)
    for e in pygame.event.get():
        if e.type == pygame.QUIT: raise SystemExit, "QUIT"
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            raise SystemExit, "ESCAPE"
    screen.fill((0,0,0))
    l_button.update()
    r_button.update()
    s_button.update()
    l_button.draw(screen)
    r_button.draw(screen)
    s_button.draw(screen)
    pygame.display.update()