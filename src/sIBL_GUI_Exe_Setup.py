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
***	sIBL_GUI_Exe_Setup.py
***
***	Platform :
***		Windows
***
***	Description :
***      	sIBL_GUI To Windows Executable Module.
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
from distutils.core import setup
import py2exe

#***********************************************************************************************
#***	Main Python Code
#***********************************************************************************************

setup( windows = [{"script":"sIBL_GUI.py", "icon_resources":[( 1, "./Resources/Icon_Light_32.ico" )]}], options = {"py2exe":{"dist_dir":"./Releases/Windows/sIBL_GUI", "includes":[ "sip", "PyQt4.QtCore", "PyQt4.QtGui", "PyQt4.QtNetwork", "os" ]}} )

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
