import os, shutil, zipfile, glob
folder = 'dist'
for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception, e:
        print e
#shutil.rmtree("dist")
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
shutil.rmtree('build')
shutil.rmtree('dist/tcl')
shutil.copy("C:\Python27\lib\site-packages\pygame\SDL_ttf.dll", "dist/SDL.dll")
shutil.copy("C:\Python27\lib\site-packages\pygame\libogg-0.dll", "dist/libogg-0.dll")
if raw_input("Do Zip? [Y]").upper()=="Y":
    print "Zipping..."
    os.system("del buildto/build.zip")
    myzip=zipfile.ZipFile('buildto/build.zip', 'w')
    for i in glob.glob("dist/*.*"):
        myzip.write(i)
    for i in glob.glob("dist/lvl/*.*"):
        myzip.write(i)
    for i in glob.glob("dist/image/*.*"):
        myzip.write(i)
    myzip.close()