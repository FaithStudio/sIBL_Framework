#!/usr/bin/env python
# -*- coding: utf-8 -*-

#***********************************************************************************************
#
# Copyright (C) 2008 / 2009 - Thomas Mansencal - kelsolaar_fool@hotmail.com
#
#***********************************************************************************************
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#***********************************************************************************************
#
# The Following Code Is Protected By GNU GPL V3 Licence.
#
#***********************************************************************************************
#
# If You Are A HDRI Ressources Vendor And Are Interested In Making Your Sets SmartIBL Compliant:
# Please Contact Us At HDRLabs :
# Christian Bloch - blochi@edenfx.com
# Thomas Mansencal - kelsolaar_fool@hotmail.com
#
#***********************************************************************************************

'''
************************************************************************************************
***	sIBL_GUI_Generate_Launcher.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***      	sIBL_GUI Launcher Generation Module.
***
***	Others :
***
************************************************************************************************
'''

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***	External Imports
#***********************************************************************************************
import os

#***********************************************************************************************
#***	Main Code Start
#***********************************************************************************************
cFileContent = []

cWorkingDirectory = os.path.abspath( os.getcwd() )
cFileContent.append( "cd " + cWorkingDirectory + "\n" )
cFileContent.append( "./sIBL_GUI" )

cLauncherFile = open( cWorkingDirectory + "/sIBL_GUI_Launcher", "w" )
for line in cFileContent:
	cLauncherFile.write( line )
cLauncherFile.close()

# Setting Executable Attributes On The Files.
os.system( "chmod +x " + cWorkingDirectory + "/sIBL_GUI" )
os.system( "chmod +x " + cWorkingDirectory + "/sIBL_Framework" )
os.system( "chmod +x " + cWorkingDirectory + "/sIBL_GUI_Launcher" )

#***********************************************************************************************
#***	Python End
#***********************************************************************************************


