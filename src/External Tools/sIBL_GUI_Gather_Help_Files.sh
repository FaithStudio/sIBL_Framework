#/bin/bash
echo ----------------------------------------------------------------
echo sIBL_GUI - Help Gathering
echo ----------------------------------------------------------------

#! Gathering Folder Cleanup.
rm -rf ./Releases/Gathering/Help/*

#! Templates Gathering.
cp -rf ./Help ./Releases/Gathering/

#! Gathering Folder Cleanup.
python ./External\ Tools/KSL_Recursive_Remove.py ./Releases/Gathering/Help/ .DS_Store
python ./External\ Tools/KSL_Recursive_Remove.py ./Releases/Gathering/Help/ Thumbs.db