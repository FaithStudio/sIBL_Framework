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

'''
************************************************************************************************
***	sIBL_GUI_Exe_Setup.py
***
***	Platform :
***		Windows
***
***	Description :
***      	KSL Set Current Version.
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
import sys
import os
import platform

#***********************************************************************************************
#***	Main Python Code
#***********************************************************************************************
def KSL_Set_Current_Release( cFilePath, cAttribute, cVariable, cWindowsBat ) :

	cFile = open( cFilePath, "r" )
	cFileContent = cFile.readlines()
	for cLine in cFileContent :
		if cAttribute in cLine :
			cLineTokens = cLine.split( "=" )
			cVersion = cLineTokens[1].strip().strip( "\"" )
			if platform.system() == "Windows":
				cFile = open( cWindowsBat, "w" )
				cFile.write( "set '%s'='%s'\n" % ( cVariable, cVersion ) )
				cFile.close()
			elif platform.system() == "Linux" or platform.system() == "Darwin":
				print( "export '%s'='%s'\n" % ( cVariable, cVersion ) )
			break

KSL_Set_Current_Release( "./sIBL_Common_Settings.py", "gReleaseVersion", "sIBL_GUI_Release", "./sIBL_Set_Release_Environment_Variable.bat" )

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
