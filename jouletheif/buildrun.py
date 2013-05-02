import os, shutil
os.system("python builddep.py py2exe")
try:
    shutil.copytree("lvl/", "dist/lvl/")
except Exception: print "Levels already copied!"
try:
    shutil.copy("config.py", "dist/config.py")
except Exception: print "Config already copied!"
try:
    shutil.copytree("image/", "dist/image/")
except Exception: print "Images already copied!"
shutil.rmtree('dist')