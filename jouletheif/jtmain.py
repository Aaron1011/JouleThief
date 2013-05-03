
import pygame, datetime, gui, os



levels=['*DUMP', 'DEBUG', '*INFO', 'ERROR', '*CRIT', '*FAIL'] #log level names
fileloglevel=1
printloglevel=2
wintitle=None
call=None
execfile("config.py")
filename="jtmain.log"
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

def playButtonCallback():
    pygame.quit()
    info("Starting Main Game (Level 1)")
    dump(call.replace("%", "jtengine")+" 1")
    os.system(call.replace("%", "jtengine")+" 1")
    raise SystemExit

info("Starting JTMain")
debug("init pygame")
pygame.init()
debug("inited")
debug("pop screen")
screen=pygame.display.set_mode((650,450))
debug("popped")
debug("settitle")
pygame.display.set_caption(wintitle)
debug("set. making button")

play_button=gui.Button(100,100,50,25, "Play!", playButtonCallback)
print "BACKBACKBACK"
debug("Button Initilized")

while 1:
    for e in pygame.event.get():
        if e.type == pygame.QUIT: raise SystemExit, "QUIT"
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            raise SystemExit, "ESCAPE"
    screen.fill((0,0,0))
    play_button.update()
    play_button.draw(screen)
    pygame.display.update()