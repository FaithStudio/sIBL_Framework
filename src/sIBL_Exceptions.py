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
***	sIBL_Exceptions.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***      	sIBL Exceptions Module.
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
import sIBL_Common

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
cLogger = logging.getLogger( "sIBL_Overall_Logger" )

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
@sIBL_Common.sIBL_Execution_Call
def sIBL_Exceptions_Feedback( cError, cMessage = None, cVerboseState = None ):
	'''
	This Definition Provides Exceptions / Exceptions Handler Feedback.
	'''

	if cMessage :
		cLogger.error( "!> '%s'.", cMessage )

	if cVerboseState :
		cLogger.error( "!> Exception Raised : '%s'.", cError )
		cLogger.error( "!> Exception Description : '%s'.", cError.__doc__ )

	cLogger.debug( "> Exception Class : '%s'.", cError.__class__ )

class Command_Line_Error( Exception ):
	'''
	This Class Is Used For Command Line Error.
	'''
	@sIBL_Common.sIBL_Execution_Call
	def __init__( self, cValue ) :
		'''
		This Method Initializes The Class.

		@param cValue: Error Value Or Message ( String )
		'''

		self.cValue = cValue

	def __str__( self ) :
		return repr( self.cValue )


class File_Content_Error( Exception ):
	'''
	This Class Is Used For Errors In The File Content.
	'''

	@sIBL_Common.sIBL_Execution_Call
	def __init__( self, cValue ) :
		'''
		This Method Initializes The Class.

		@param cValue: Error Value Or Message ( String )
		'''

		self.cValue = cValue

	def __str__( self ) :
		return repr( self.cValue )


class File_Exist_Error( Exception ):
	'''
	This Class Is Used For Non Existing File.
	'''

	@sIBL_Common.sIBL_Execution_Call
	def __init__( self, cValue ) :
		'''
		This Method Initializes The Class.

		@param cValue: Error Value Or Message ( String )
		'''

		self.cValue = cValue

	def __str__( self ) :
		return repr( self.cValue )

class File_Corrupted_Error( Exception ):
	'''
	This Class Is Used For Corrupted File.
	'''

	@sIBL_Common.sIBL_Execution_Call
	def __init__( self, cValue ) :
		'''
		This Method Initializes The Class.

		@param cValue: Error Value Or Message ( String )
		'''

		self.cValue = cValue

	def __str__( self ) :
		return repr( self.cValue )


class File_Locked_Error( Exception ):
	'''
	This Class Is Used For Locked File.
	'''

	@sIBL_Common.sIBL_Execution_Call
	def __init__( self, cValue ) :
		'''
		This Method Initializes The Class.

		@param cValue: Error Value Or Message ( String )
		'''

		self.cValue = cValue

	def __str__( self ) :
		return repr( self.cValue )


class Directory_Exist_Error( Exception ):
	'''
	This Class Is Used For Non Existing Directory.
	'''

	@sIBL_Common.sIBL_Execution_Call
	def __init__( self, cValue ) :
		'''
		This Method Initializes The Class.

		@param cValue: Error Value Or Message ( String )
		'''

		self.cValue = cValue

	def __str__( self ) :
		return repr( self.cValue )

class Invalid_Attribute_Error( Exception ):
	'''
	This Class Is Used For Invalid Attribute.
	'''

	@sIBL_Common.sIBL_Execution_Call
	def __init__( self, cValue ) :
		'''
		This Method Initializes The Class.

		@param cValue: Error Value Or Message ( String )
		'''

		self.cValue = cValue

	def __str__( self ) :
		return repr( self.cValue )

class Invalid_Key_Error( Exception ):
	'''
	This Class Is Used For Invalid Key Error.
	'''

	@sIBL_Common.sIBL_Execution_Call
	def __init__( self, cValue ) :
		'''
		This Method Initializes The Class.

		@param cValue: Error Value Or Message ( String )
		'''

		self.cValue = cValue

	def __str__( self ) :
		return repr( self.cValue )

class Remote_Connection_Error( Exception ):
	'''
	This Class Is Used For Remote Connection Error.
	'''

	@sIBL_Common.sIBL_Execution_Call
	def __init__( self, cValue ) :
		'''
		This Method Initializes The Class.

		@param cValue: Error Value Or Message ( String )
		'''

		self.cValue = cValue

	def __str__( self ) :
		return repr( self.cValue )

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
