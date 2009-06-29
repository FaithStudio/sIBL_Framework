#/usr/bin/bash

echo ----------------------------------------------------------------
echo sIBL_GUI - Mac Os X - sIBL_Framework Build
echo ----------------------------------------------------------------

#! sIBL_Framework Build.
rm -rf ./build
rm -rf ./dist/sIBL_Framework.app
rm -rf ./dist/sIBL_Framework.dmg
/Library/Frameworks/Python.framework/Versions/2.6/bin/./python sIBL_Framework_App_Setup.py py2app --strip
cp -f ./COPYING ./dist/sIBL_Framework.app/

#! sIBL_Framework Debug Remove.
rm -rf `find ./dist/sIBL_Framework.app/ -name *_debug`

#! sIBL_Framework Cleanup.
python ./External\ Tools/KSL_Recursive_Remove.py ./dist/sIBL_Framework.app/ .DS_Store