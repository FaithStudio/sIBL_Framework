#/bin/bash
echo ----------------------------------------------------------------
echo sIBL_GUI - Templates Gathering
echo ----------------------------------------------------------------

#! Gathering Folder Cleanup.
rm -rf ./Releases/Gathering/Templates/*

#! Templates Gathering.
cp -rf ./Templates ./Releases/Gathering/

#! Releases File Gathering.
cp ./Releases/sIBL_GUI_Releases.rc ./Releases/Gathering/

#! Gathering Folder Cleanup.
python ./External\ Tools/KSL_Recursive_Remove.py ./Releases/Gathering/Templates/ .DS_Store
python ./External\ Tools/KSL_Recursive_Remove.py ./Releases/Gathering/Templates/ Thumbs.db