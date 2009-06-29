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
***      	KSL Recursion Delete.
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

#***********************************************************************************************
#***	Main Python Code
#***********************************************************************************************
def KSL_Recursive_Remove( cRootDirectory, cMatchingString ):

	if os.path.exists( cRootDirectory ):
		for root, dirs, files in os.walk( cRootDirectory ):
			for cItem in files:
				cItemPath = os.path.join( root, cItem ).replace( "\\", "/" )
				if cMatchingString in str( cItem )  :
					KSL_Remove( cItemPath )

def KSL_Remove( cItem ):
	print( "KSL_Recursive_Delete | Removing : '%s'" % cItem )
	try :
		os.remove( cItem )
	except:
		print( "KSL_Recursive_Delete | '%s' Remove Failed !" % cItem )

if __name__ == '__main__':
	KSL_Recursive_Remove( sys.argv[1], sys.argv[2] )

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
