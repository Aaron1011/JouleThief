from distutils.core import setup
exec "import py2exe" #because eclipse gives this a warnining and that fucking bugs me
print "BUILDING MENUS TARGET"
setup(console=['jtmain.py', 'jtlevelselect.py', 'joulethief.py'],
      options={
                "py2exe":{
                        "bundle_files":3,#1,
                        "includes":["pygame"],
                        "ascii":False,
                        "optimize":1,#,
                        "compressed":False
                        #"skip_archive":True
                }
        }
      )
print "BUILDING ENGINE TARGET"
setup(console=['jtengine.py'], zipfile=None,
      options={
                "py2exe":{
                        "bundle_files":1,#1,
                        "includes":["pygame"],
                        "ascii":False,
                        "optimize":1,#,
                        "compressed":False,
                        "dist_dir":"distengine"
                        #"skip_archive":True
                }
        }
      )