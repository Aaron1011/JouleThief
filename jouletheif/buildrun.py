import os, shutil, zipfile, glob
folder = 'dist'
print "Cleaning"
for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception, e:
        print e
folder="distengine"
for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
    except Exception, e:
        print e
#shutil.rmtree("dist")
print "Building"
os.system("python builddep.py py2exe")
print "Copying levels"
try:
    shutil.copytree("lvl/", "dist/lvl/")
except Exception: print "Levels already copied!"
print "Copying config"
try:
    shutil.copy("config.py", "dist/config.py")
except Exception: print "Config already copied!"
print "Copying images"
try:
    shutil.copytree("image/", "dist/image/")
except Exception: print "Images already copied!"
print "Cleaning build"
shutil.rmtree('build')
print "Removing TCL"
shutil.rmtree('dist/tcl')
print "Copying DLLs (and fonts)"
needed=os.listdir("buildreq")
for i in needed: shutil.copy("buildreq/"+i, "dist/")
#print "Copying fonts"
#shutil.copytree("fonts/", "dist/fonts/")
print "Editing config..."
f=open("dist/config.py",'a')
f.write('call="%"')
f.close()
print "Copying engine into dist dir"
shutil.copy("distengine/joulethief.exe", "dist/jouletheif.exe")
if raw_input("Do Zip? [Y]").upper()=="Y":
    print "Zipping..."
    os.system("del buildto/build.zip")
    myzip=zipfile.ZipFile('buildto/build.zip', 'w')
    print "Zipping EXEs"
    for i in glob.glob("dist/*.*"):
        myzip.write(i)
    print "Zipping Levels"
    for i in glob.glob("dist/lvl/*.*"):
        myzip.write(i)
    print "Zipping Images"
    for i in glob.glob("dist/image/*.*"):
        myzip.write(i)
    print "Zipping Extras"
    myzip.write("alpha_readme.txt")
    myzip.write("credits.txt")
    print "Writing Zip"
    myzip.close()
raw_input("Done! (Press raw enter)")