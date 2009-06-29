#/usr/bin/bash

echo ----------------------------------------------------------------
echo sIBL_GUI - Mac Os X - Overall Build
echo ----------------------------------------------------------------

#! sIBL_Framework Build.
rm -rf ./build
rm -rf ./dist/sIBL_Framework.app
rm -rf ./dist/sIBL_Framework.dmg
/Library/Frameworks/Python.framework/Versions/2.6/bin/./python sIBL_Framework_App_Setup.py py2app --no-strip
cp -f ./COPYING ./dist/sIBL_Framework.app/

#! sIBL_Framework Debug Remove.
rm -rf `find ./dist/sIBL_Framework.app/ -name *_debug`

#! sIBL_Framework Cleanup.
python ./External\ Tools/KSL_Recursive_Remove.py ./dist/sIBL_Framework.app/ .DS_Store

#! sIBL_Framework DMG.
hdiutil create "./dist/sIBL_Framework.dmg" -volname "sIBL_Framework" -fs HFS+ -srcfolder "./dist/sIBL_Framework.app"
cp -f ./dist/sIBL_Framework.dmg ./Releases/MacOsX/

#! sIBL_GUI Build.
rm -rf ./build
rm -rf ./dist/sIBL_GUI.app
rm -rf ./dist/sIBL_GUI.dmg
/Library/Frameworks/Python.framework/Versions/2.6/bin/./python sIBL_GUI_App_Setup.py py2app --includes "sip" --no-strip
mkdir ./dist/sIBL_GUI.app/Contents/Resources/Resources
cp -f ./COPYING ./dist/sIBL_GUI.app/
cp -f ./Releases/MacOsX/Utilities/__boot__.py ./dist/sIBL_GUI.app/Contents/Resources/
cp -f ./Releases/MacOsX/Utilities/qt.conf ./dist/sIBL_GUI.app/Contents/Resources/
cp -rf ./Releases/MacOsX/Utilities/imageformats ./dist/sIBL_GUI.app/Contents/MacOs
cp -rf ./Templates ./dist/sIBL_GUI.app/Contents/Resources
cp -rf ./Help ./dist/sIBL_GUI.app/Contents/Resources
cp -rf ./Resources/Earth_Map.png ./dist/sIBL_GUI.app/Contents/Resources/Resources
rm -rf ./dist/sIBL_GUI.app/Contents/Resources/Templates/3ds\ Max
rm -rf ./dist/sIBL_GUI.app/Contents/Resources/Templates/XSI

#! sIBL_GUI Debug Remove.
rm -rf `find ./dist/sIBL_GUI.app/ -name *_debug`

#! sIBL_GUI Cleanup.
python ./External\ Tools/KSL_Recursive_Remove.py ./dist/sIBL_GUI.app/ .DS_Store

#! sIBL_GUI DMG.
hdiutil create ./dist/sIBL_GUI.dmg -volname "sIBL_GUI" -fs HFS+ -srcfolder "./dist/sIBL_GUI.app"
cp -f ./dist/sIBL_GUI.dmg ./Releases/MacOsX/
