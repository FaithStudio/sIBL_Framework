"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['sIBL_Framework.py']
DATA_FILES = []
OPTIONS = {'argv_emulation': True, 'iconfile': './Resources/Icon_Light_512.icns'}

setup( 
    app = APP,
    data_files = DATA_FILES,
    options = {'py2app': OPTIONS},
    setup_requires = ['py2app'],
 )
