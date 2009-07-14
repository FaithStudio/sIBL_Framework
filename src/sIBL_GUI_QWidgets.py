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
***	sIBL_GUI_QWidgets.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***      	sIBL_GUI Custom Widgets.
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
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import sIBL_Common

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
cLogger = logging.getLogger( "sIBL_Overall_Logger" )

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class Variable_QPushButton( QPushButton ) :

	@sIBL_Common.sIBL_Execution_Call
	def __init__( self, cState, cColors, cButtonText, cParent = None ) :
		'''
		This Method Initializes The Class.

		@param cState: Current Button State. ( Boolean )
		@param cColors: Button Colors. ( Tuple )
		@param cButtonText: Button Texts. ( Tuple )
		'''

		cLogger.debug( "> Initializing Variable_QPushButton() Class." )
		QPushButton.__init__( self, cParent )

		# --- Setting Class Attributes. ---
		self.cState = cState
		self.cTrueText = cButtonText[0]
		self.cFalseText = cButtonText[1]

		self.trueColor = cColors[0]
		self.falseColor = cColors[1]

		# Initializing The Button
		self.setCheckable( True )
		if self.cState :
			self.setTrueState()
		else :
			self.setFalseState()

		# Variable_QPushButton Signals / Slots.
		self.connect( self, SIGNAL( "clicked()" ), self.Variable_QPushButton_OnClicked )

	@sIBL_Common.sIBL_Execution_Call
	def Variable_QPushButton_OnClicked( self ) :
		'''
		This Method Is Called When A Variable QPushButton Is Clicked.
		'''

		if self.cState == True :
			self.setFalseState()
		else :
			self.setTrueState()

	@sIBL_Common.sIBL_Execution_Call
	def setTrueState( self ) :
		'''
		This Method Sets The Variable Button True State.
		'''

		cLogger.debug( "> Setting Variable QPushButton() To 'True' State." )
		self.cState = True

		cPalette = QPalette()
		cPalette.setColor( QPalette.Button, self.trueColor )
		self.setPalette( cPalette )

		self.setChecked( True )
		self.setText( self.cTrueText )


	@sIBL_Common.sIBL_Execution_Call
	def setFalseState( self ) :
		'''
		This Method Sets The Variable QPushButton True State.
		'''

		cLogger.debug( "> Setting Variable QPushButton() To 'False' State." )

		self.cState = False

		cPalette = QPalette()
		cPalette.setColor( QPalette.Button, self.falseColor )
		self.setPalette( cPalette )

		self.setChecked( False )
		self.setText( self.cFalseText )

@sIBL_Common.sIBL_Execution_Call
def sIBL_GUI_Message( cMessageType, cTitle, cMessage ):
	'''
	This Function Provides A Fast GUI Message Box.
	'''

	cLogger.debug( "> Launching sIBL_GUI_Message()." )
	cLogger.debug( "> Message Type : '%s'.", cMessageType )
	cLogger.debug( "> Title : '%s'.", cTitle )
	cLogger.debug( "> Message : '%s'.", cMessage )

	cMessageBox = QMessageBox()
	cMessageBox.setWindowTitle( "sIBL_GUI | " + cTitle )
	cMessageBox.setText( cMessage )

	if cMessageType == "Critical" :
		cMessageBox.setIcon( QMessageBox.Critical )
		cLogger.critical( cMessage )
	elif cMessageType == "Error" :
		cMessageBox.setIcon( QMessageBox.Critical )
		cLogger.error( "'%s'.", "sIBL_GUI | " + cMessage )
	elif cMessageType == "Warning" :
		cMessageBox.setIcon( QMessageBox.Warning )
		cLogger.warning( "'%s'.", "sIBL_GUI | " + cMessage )
	elif cMessageType == "Information" :
		cMessageBox.setIcon( QMessageBox.Information )
		cLogger.info( "'%s'.", "sIBL_GUI | " + cMessage )
	cMessageBox.setWindowFlags( Qt.WindowStaysOnTopHint )
	cMessageBox.exec_()

@sIBL_Common.sIBL_Execution_Call
def sIBL_Standalone_Message( cMessageType, cCaption, cMessage ):
	'''
	This Function Provides A Standalone Message Box.
	'''

	from PyQt4 import QtGui
	QtGui.QApplication( sys.argv )
	sIBL_GUI_Message( cMessageType, cCaption, cMessage )

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
