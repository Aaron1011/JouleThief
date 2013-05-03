#Title:
wintitle="Joule Thief v0.2.1"
#Set to true to enable debug logging:
_debug=True;
#Set file name to log to:
filename='jtengine.log';
#Set movement amount/keyDown event:
moveamount=3;
#Set key repeat info:
delay=25;
repeat=10;
#Set jump speed change:
jumpamount=5;
#Accel:
accelamount=0.3;
accelmax=30;
#User Settings End
#!--Do not change things below thiS--!#
if _debug:
    printloglevel=0;
    fileloglevel=0;

call="python %.py"
#call="*.exe"


