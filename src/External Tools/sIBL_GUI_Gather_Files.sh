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

export sIBL_GUI_Release=-$sIBL_GUI_Release

#! Gathering Folder Cleanup.
rm -rf ./Releases/Gathering/*

#! Windows Gathering.
cp ./Installers/NSIS/sIBL_GUI_Setup.exe ./Releases/Gathering/sIBL_GUI$sIBL_GUI_Release.exe

#! XSI Gathering.
cp -rf ./../../sIBL_GUI_For_XSI/Addons/sIBL_GUI_For_XSI.xsiaddon ./Releases/Gathering/
cd ./Releases/Gathering/
tar -czvf ./sIBL_GUI_For_XSI.xsiaddon$sIBL_GUI_Release.tar.gz sIBL_GUI_For_XSI.xsiaddon
rm -f sIBL_GUI_For_XSI.xsiaddon
cd ../../

#! Linux Gathering.
cp ./Releases/Linux/sIBL_GUI.tar.gz ./Releases/Gathering/sIBL_GUI$sIBL_GUI_Release.tar.gz

#! MacOsX Gathering.
cp ./Releases/MacOsX/sIBL_GUI.dmg ./Releases/Gathering/sIBL_GUI$sIBL_GUI_Release.dmg

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

#! XSI Server Change Log Gathering.
mkdir ./Releases/Gathering/sIBL_GUI_XSI_Server\ Change\ Log
cp -rf ./../../sIBL_GUI_XSI_Server/Change\ Log/Change\ Log.htm ./Releases/Gathering/sIBL_GUI_XSI_Server\ Change\ Log

#! Maya Helper Script Change Log Gathering.
mkdir ./Releases/Gathering/sIBL_GUI_For_Maya\ Change\ Log
cp -rf ./../../sIBL_GUI_For_Maya/Change\ Log/Change\ Log.htm ./Releases/Gathering/sIBL_GUI_For_Maya\ Change\ Log

#! 3dsMax Startup Script Change Log Gathering.
mkdir ./Releases/Gathering/sIBL_GUI_For_3dsMax\ Change\ Log
cp -rf ./../../sIBL_GUI_For_3dsMax/Change\ Log/Change\ Log.htm ./Releases/Gathering/sIBL_GUI_For_3dsMax\ Change\ Log

#! Releases File Gathering.
cp ./Releases/sIBL_GUI_Releases.rc ./Releases/Gathering/

#! Gathering Folder Cleanup.
python ./External\ Tools/KSL_Recursive_Remove.py ./Releases/Gathering .DS_Store
python ./External\ Tools/KSL_Recursive_Remove.py ./Releases/Gathering Thumbs.db

export COPYFILE_DISABLE=false