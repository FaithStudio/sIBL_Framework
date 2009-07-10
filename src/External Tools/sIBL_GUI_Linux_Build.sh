#/usr/bin/bash

echo ----------------------------------------------------------------
echo sIBL_GUI - Linux Build
echo ----------------------------------------------------------------

#! Linux Build.
rm -rf /media/psf/Developement/sIBL/src/Releases/linux/dist/
rm -rf /media/psf/Developement/sIBL/src/Releases/linux/build
rm -rf /media/psf/Developement/sIBL/src/Releases/linux/Source
mkdir /media/psf/Developement/sIBL/src/Releases/linux/Source
cp /media/psf/Developement/sIBL/src/*.py /media/psf/Developement/sIBL/src/Releases/linux/Source
python /home/kelsolaar/Developement/pyinstaller/Makespec.py -F /media/psf/Developement/sIBL/src/Releases/linux/Source/sIBL_Framework.py -o /media/psf/Developement/sIBL/src/Releases/linux/
python /home/kelsolaar/Developement/pyinstaller/Build.py /media/psf/Developement/sIBL/src/Releases/linux/sIBL_Framework.spec
python /home/kelsolaar/Developement/pyinstaller/Makespec.py -F /media/psf/Developement/sIBL/src/Releases/linux/Source/sIBL_GUI.py -o /media/psf/Developement/sIBL/src/Releases/linux/
python /home/kelsolaar/Developement/pyinstaller/Build.py /media/psf/Developement/sIBL/src/Releases/linux/sIBL_GUI.spec

#! Linux Standalone.
rm -rf /media/psf/Developement/sIBL/src/Releases/Linux/sIBL_GUI/
mkdir /media/psf/Developement/sIBL/src/Releases/Linux/sIBL_GUI/
cp -rf /media/psf/Developement/sIBL/src/Releases/Linux/dist/* /media/psf/Developement/sIBL/src/Releases/Linux/sIBL_GUI/
cp -rf /media/psf/Developement/sIBL/src/Templates /media/psf/Developement/sIBL/src/Releases/Linux/sIBL_GUI/
cp -rf /media/psf/Developement/sIBL/src/Help /media/psf/Developement/sIBL/src/Releases/Linux/sIBL_GUI/
cp -rf /media/psf/Developement/sIBL/src/COPYING /media/psf/Developement/sIBL/src/Releases/Linux/sIBL_GUI/
rm -rf /media/psf/Developement/sIBL/src/Releases/Linux/sIBL_GUI/Templates/3ds\ Max
mkdir /media/psf/Developement/sIBL/src/Releases/Linux/sIBL_GUI/Resources
cp /media/psf/Developement/sIBL/src/Resources/Earth_Map.png /media/psf/Developement/sIBL/src/Releases/Linux/sIBL_GUI/Resources/
cd /media/psf/Developement/sIBL/src/Releases/Linux/

#! sIBL_GUI Linux Release Cleanup.
python /media/psf/Developement/sIBL/src/External\ Tools/KSL_Recursive_Remove.py ./ .DS_Store
python /media/psf/Developement/sIBL/src/External\ Tools/KSL_Recursive_Remove.py ./ Thumbs.db

#! sIBL_GUI Linux Archiving.
tar -czvf sIBL_GUI.tar.gz sIBL_GUI/

#! XSI Addon.
rm -rf /media/psf/Developement/sIBL_GUI_For_XSI/Addons/sIBL_GUI_For_XSI/Application/Plugins/sIBL_GUI_Linux/*
cp -rf /media/psf/Developement/sIBL/src/Releases/Linux/sIBL_GUI/* /media/psf/Developement/sIBL_GUI_For_XSI/Addons/sIBL_GUI_For_XSI/Application/Plugins/sIBL_GUI_Linux/
cp -f /media/psf/Developement/sIBL/src/sIBL_GUI_Generate_Launcher.py /media/psf/Developement/sIBL_GUI_For_XSI/Addons/sIBL_GUI_For_XSI/Application/Plugins/sIBL_GUI_Linux/
rm -rf /media/psf/Developement/sIBL_GUI_For_XSI/Addons/sIBL_GUI_For_XSI/Application/Plugins/sIBL_GUI_Linux/Templates/Maya/
