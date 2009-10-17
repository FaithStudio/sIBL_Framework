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
***	sIBL_GUI_About.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***      	sIBL Collection Module.
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
import logging

#***********************************************************************************************
#***	internal Imports
#***********************************************************************************************
import sIBL_Common_Settings

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
cLogger = logging.getLogger( "sIBL_Overall_Logger" )

cSIBL_GUI_AboutMessage = """
	<center>
	*
	<p>
	s I B L _ G U I - %s
	</p>
	*
	<br/><br/>Thanks To All Folks At HDRLabs.com To Provide Smart IBL World !
	<br/>
	Special Thanks To : Dschaga, Tischbein3, Andy, VolXen, Gwynne, keksonja, Yuri, Rork.
	<br/>
	Another Big Thanks To Emanuele Santos For Helping Me Out On The Mac Os X Bundle.
	<br/>
	Very Special Thanks To Christian For Providing Me Some Space On His Server :]
	<p>
	This Software Uses Python, PyQT, Py2exe, Py2App, PyInstaller And NSIS.
	<br/>
	Coded With Eclipse - Pydev - Aptana - TextMate And Jedit.
	</p>
	<p>
	Light Bulb Icon Is Copyright Christian Bloch.
	</p>
	<p>
	Earth Map Is Copyright Unknown ( Author Is Unknown ).
	</p>
	<p>
	If You Are A HDRI Ressources Vendor And Are Interested In Making Your Sets SmartIBL Compliant:
	<br/>
	Please Contact Us At HDRLabs :
	<br/>
	Christian Bloch - <a href="mailto:blochi@edenfx.com"><span style=" text-decoration: underline; color:#000000;">blochi@edenfx.com</span></a>
	<br/>
	Thomas Mansencal - <a href="mailto:kelsolaar_fool@hotmail.com"><span style=" text-decoration: underline; color:#000000;">kelsolaar_fool@hotmail.com</span></a>
	</p>
	<p>
	sIBL_GUI And sIBL_Framework by Thomas Mansencal - 2008 / 2009
	<br/>
	This Software Is Released Under Terms Of GNU GPL V3 License : <a href="http://www.gnu.org/licenses/"><span style=" text-decoration: underline; color:#000000;">http://www.gnu.org/licenses/</span></a>
        <br/>
        <a href="http://my.opera.com/KelSolaar/"><span style=" text-decoration: underline; color:#000000;">http://my.opera.com/KelSolaar/</span></a>
	</p>
	*
	<p>
	<img src=":/sIBL_GUI/Resources/GPL_V3.png">
	</p>
	*
	</center>
""" % ( sIBL_Common_Settings.gReleaseVersion.replace( ".", "  .  " ) )

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
