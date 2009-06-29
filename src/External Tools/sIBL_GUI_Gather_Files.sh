#/bin/bash
echo ----------------------------------------------------------------
echo sIBL_GUI - Files Gathering
echo ----------------------------------------------------------------

export COPYFILE_DISABLE=true

#! Setting Release Environment Variable.
eval $( python ./External\ Tools/KSL_Set_Current_Release.py )
if [ "$1" != "" ]
then
export sIBL_GUI_Release=$sIBL_GUI_Release-Nightly
fi

echo ----------------------------------------------------------------
echo sIBL_GUI Release : $sIBL_GUI_Release
echo ----------------------------------------------------------------

#! Gathering Folder Cleanup.
rm -rf ./Releases/Gathering/*

#! Windows Gathering.
cp ./Installers/NSIS/sIBL_GUI_Setup.exe ./Releases/Gathering/sIBL_GUI_Setup-$sIBL_GUI_Release.exe

#! XSI Gathering.
cp -rf ./../../sIBL_GUI_For_XSI/Addons/sIBL_GUI_For_XSI.xsiaddon ./Releases/Gathering/
cd ./Releases/Gathering/
tar -czvf ./sIBL_GUI_For_XSI.xsiaddon-$sIBL_GUI_Release.tar.gz sIBL_GUI_For_XSI.xsiaddon
rm -f sIBL_GUI_For_XSI.xsiaddon
cd ../../

#! Linux Gathering.
cp ./Releases/Linux/sIBL_GUI.tar.gz ./Releases/Gathering/sIBL_GUI-$sIBL_GUI_Release.tar.gz

#! MacOsX Gathering.
cp ./Releases/MacOsX/sIBL_Framework.dmg ./Releases/Gathering/sIBL_Framework-$sIBL_GUI_Release.dmg
cp ./Releases/MacOsX/sIBL_GUI.dmg ./Releases/Gathering/sIBL_GUI-$sIBL_GUI_Release.dmg

#! Source Code Gathering.
rm -rf ./Releases/sIBL_GUI_Source/*
cp ./COPYING ./Releases/sIBL_GUI_Source/
cp ./*.py ./Releases/sIBL_GUI_Source/
cp ./*.qrc ./Releases/sIBL_GUI_Source/
cp -rf ./UI ./Releases/sIBL_GUI_Source/
cp -rf ./Templates ./Releases/sIBL_GUI_Source/
cp -rf ./Help ./Releases/sIBL_GUI_Source/
cp -rf ./Installers ./Releases/sIBL_GUI_Source/
rm -rf ./Releases/sIBL_GUI_Source/Installers/*.exe
cp -rf ./Resources ./Releases/sIBL_GUI_Source/
rm -rf ./Releases/sIBL_GUI_Source/Resources/Builders
rm -rf ./Releases/sIBL_GUI_Source/Resources/*.psd
#! Source Cleanup.
python ./External\ Tools/KSL_Recursive_Remove.py ./Releases/sIBL_GUI_Source .DS_Store
#! Source Code Archiving.
cd ./Releases/
tar -czvf ./Gathering/sIBL_GUI_Source-$sIBL_GUI_Release.tar.gz sIBL_GUI_Source/
cd ..

#! Templates Gathering.
cp -rf ./Templates ./Releases/Gathering/

#! Manual - Help File Gathering.
cp -rf ./Help ./Releases/Gathering/

#! sIBL_GUI Change Log Gathering.
mkdir ./Releases/Gathering/sIBL_GUI\ Change\ Log
cp -rf ./../Change\ Log/Change\ Log.htm ./Releases/Gathering/sIBL_GUI\ Change\ Log

#! XSI Addon Change Log Gathering.
mkdir ./Releases/Gathering/sIBL_XSI\ Addon\ Change\ Log
cp -rf ./../../sIBL_GUI_For_XSI/Change\ Log/Change\ Log.htm ./Releases/Gathering/sIBL_XSI\ Addon\ Change\ Log

#! Releases File Gathering.
cp ./Releases/sIBL_GUI_Releases.rc ./Releases/Gathering/

#! Gathering Folder Cleanup.
python ./External\ Tools/KSL_Recursive_Remove.py ./Releases/Gathering .DS_Store

export COPYFILE_DISABLE=false