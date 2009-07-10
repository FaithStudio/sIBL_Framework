echo ----------------------------------------------------------------
echo sIBL_GUI - Windows Build
echo ----------------------------------------------------------------

rem // Windows Build.
rmdir /S /Q "Y:\sIBL\src\Releases\Windows\sIBL_GUI"
python sIBL_Framework_Exe_Setup.py py2exe
python sIBL_GUI_Exe_Setup.py py2exe

rem // Windows Release.
xcopy /e /c /i /h /k /y "Y:\sIBL\src\Help" "Y:\sIBL\src\Releases\Windows\sIBL_GUI\Help\"
xcopy /e /c /i /h /k /y "Y:\sIBL\src\Templates" "Y:\sIBL\src\Releases\Windows\sIBL_GUI\Templates"
xcopy /e /c /i /h /k /y "Y:\sIBL\src\Releases\Windows\Utilities\PyQt4" "Y:\sIBL\src\Releases\Windows\sIBL_GUI\PyQt4"
xcopy /c /y "Y:\sIBL\src\Releases\Windows\Utilities\qt.conf" "Y:\sIBL\src\Releases\Windows\sIBL_GUI\"
xcopy /c /y "Y:\sIBL\src\Resources\Earth_Map.jpg" "Y:\sIBL\src\Releases\Windows\sIBL_GUI\Resources\"

rem // Upx.
upx "Y:\sIBL\src\Releases\Windows\sIBL_GUI\sIBL_GUI.exe"
upx "Y:\sIBL\src\Releases\Windows\sIBL_GUI\sIBL_Framework.exe"
upx "Y:\sIBL\src\Releases\Windows\sIBL_GUI\w9xpopen.exe"
upx "Y:\sIBL\src\Releases\Windows\sIBL_GUI\python26.dll"
upx "Y:\sIBL\src\Releases\Windows\sIBL_GUI\pythoncom26.dll"
upx "Y:\sIBL\src\Releases\Windows\sIBL_GUI\pywintypes26.dll"
upx "Y:\sIBL\src\Releases\Windows\sIBL_GUI\QtCore4.dll"
upx "Y:\sIBL\src\Releases\Windows\sIBL_GUI\QtGui4.dll"

rem // Windows Release .DS_Store Cleanup.
python "Y:\sIBL\src\External Tools\KSL_Recursive_Remove.py" Y:\sIBL\src\Releases\Windows .DS_Store

rem // Windows XSI Release.
rmdir /S /Q "Y:\sIBL_GUI_For_XSI\Addons\sIBL_GUI_For_XSI\Application\Plugins\sIBL_GUI_Windows\"
xcopy /e /c /i /h /k /y "Y:\sIBL\src\Releases\Windows\sIBL_GUI" "Y:\sIBL_GUI_For_XSI\Addons\sIBL_GUI_For_XSI\Application\Plugins\sIBL_GUI_Windows\"
rmdir /S /Q "Y:\sIBL_GUI_For_XSI\Addons\sIBL_GUI_For_XSI\Application\Plugins\sIBL_GUI_Windows\Templates\3ds Max"
rmdir /S /Q "Y:\sIBL_GUI_For_XSI\Addons\sIBL_GUI_For_XSI\Application\Plugins\sIBL_GUI_Windows\Templates\Maya"

rem // Windows XSI Release .DS_Store Cleanup.
python "Y:\sIBL\src\External Tools\KSL_Recursive_Remove.py" Y:\sIBL_GUI_For_XSI .DS_Store
python "Y:\sIBL\src\External Tools\KSL_Recursive_Remove.py" Y:\sIBL_GUI_For_XSI Thumbs.db
