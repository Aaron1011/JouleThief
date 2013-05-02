from distutils.core import setup
import py2exe

setup(console=['joulethief.py'],
      options={
                "py2exe":{
                        "bundle_files":1,#1,
                        "includes":["pygame"],
                        "ascii":False,
                        "optimize":2
                }
        })