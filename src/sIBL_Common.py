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
***	sIBL_Common.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***      	sIBL Common Classes And Definitions Module.
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
import os
import platform
import sys
import time

#***********************************************************************************************
#***	Global Definitions
#***********************************************************************************************
def sIBL_SetVerbosity_Level( cLevel ):
	'''
	This Definition Provides Overall Verbosity Levels Through An Integer.

	@param cLevel: Verbosity Level ( Integer )
	'''

	if cLevel == 0:
		cLogger.setLevel( logging.CRITICAL )
	elif cLevel == 1:
		cLogger.setLevel( logging.ERROR )
	elif cLevel == 2:
		cLogger.setLevel( logging.WARNING )
	elif cLevel == 3:
		cLogger.setLevel( logging.INFO )
	elif cLevel == 4:
		cLogger.setLevel( logging.DEBUG )

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
cVerbosityLevel = 4

cLogger = logging.getLogger( "sIBL_Overall_Logger" )

cFormatter = logging.Formatter( "%(levelname)-8s : %(message)s" )
sIBL_SetVerbosity_Level( cVerbosityLevel )

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
def sIBL_Execution_Call( cObject ):
	'''
	This Definition Is Used As A Decorator For Function Tracing.

	@param cObject: Python Object ( Object )
	@return: Python Function. ( Function )
	'''

	def sIBL_Function_Call( *cArgs, **cKwArgs ):
		'''
		This Decorator Is Used For Function Logging.

		@return: Python Object. ( Python )
		'''

		cDebugLine = str( cObject.__name__ + " " + "Function" )
		if cArgs :
			if "class" in str( type( cArgs[0] ) ):
				cDebugLine = str( cArgs[0].__class__.__name__ + "." + cObject.__name__ + " " + "Method" )

		if len( cLogger.__dict__["handlers"] ) is not 0 :
			cLogger.debug( "--->>> '%s' <<<---", cDebugLine )

		rValue = cObject( *cArgs, **cKwArgs )

		if len( cLogger.__dict__["handlers"] ) is not 0 :
			cLogger.debug( "---<<< '%s' >>>---", cDebugLine )

		return rValue

	return sIBL_Function_Call

def sIBL_CloseHandler( cLogger, cHandler ):
	'''
	This Method Shuts Down The Provided Handler.

	@param cLogger: Current Logger. ( Object )
	@param cHandler: Current Handler. ( Object )
	'''

	try:
		if len( cLogger.__dict__["handlers"] ) is not 0 :
			cLogger.debug( "> Stopping Handler : '%s'.", cHandler )
		if cHandler is not None :
			cHandler.flush()
			cHandler.close()
			cLogger.removeHandler( cHandler )
	except :
		pass

@sIBL_Execution_Call
def sIBL_Exit( cExitCode, cLogger, cHandlers ):
	'''
	This Method Shuts Down The Logging And Exit The Current Process.

	@param cExitCode: Current Exit Code. ( Int )
	'''

	cLogger.info( "sIBL_Common | Exiting Current Process !" )

	cLogger.debug( "> Stopping Logging Handlers And Logger, Then Exiting." )
	for cHandler in cHandlers :
		sIBL_CloseHandler( cLogger, cHandler )

	sys.exit( cExitCode )

class sIBL_EnvironmentVariables( object ):
	'''
	This Class Provides Methods To Manipulate Environment Variables.
	'''

	@sIBL_Execution_Call
	def __init__( self, cVariable ):
		'''
		This Method Initializes The Class.

		@param cVariable: Current Variable To Be Manipulated. ( String )
		'''
		cLogger.debug( "> %s", "Initializing sIBL_EnvironmentVariables() Class." )

		# --- Setting Class Attributes. ---
		self.cVariable = cVariable
		cLogger.debug( "> self.cVariable : '%s'.", self.cVariable )

	@sIBL_Execution_Call
	def getPath( self ):
		'''
		This Method Gets The Chosen Environment Variable Path As A String.

		@return: Either The Searched Variable Or "os.environ". ( Dictionary )
		'''

		cLogger.debug( "> Current Environment Variable : '%s'.", self.cVariable )
		cLogger.debug( "> Available System Environment Variables : '%s'.", os.environ.keys() )

		for param in os.environ.keys():
			if( self.cVariable == param ):
				cEnvironmentVariable = {}
				cEnvironmentVariable[param] = os.environ[param]
				return cEnvironmentVariable
				break
		return os.environ

@sIBL_Execution_Call
def sIBL_GetTemporarySystemPath():
	'''
	This Definition Returns A "TMP" Directory Path On Windows And "TMPDIR" Directory Path On Linux.

	@return: Current Platform Temporary Directory Path ( String )
	'''

	if platform.system() == "Windows" or platform.system() == "Microsoft":
		cEnvVariable = sIBL_EnvironmentVariables( "TMP" )
		cVariablesList = cEnvVariable.getPath()
		if "TMP" in cVariablesList.keys():
			return cVariablesList["TMP"].replace( "/", "\\" ) + "/"
	elif platform.system() == "Linux" or platform.system() == "Darwin":
		cEnvVariable = sIBL_EnvironmentVariables( "TMPDIR" )
		cVariablesList = cEnvVariable.getPath()
		if "TMPDIR" in cVariablesList.keys():
			if cVariablesList["TMPDIR"].endswith( "/" ):
				return cVariablesList["TMPDIR"]
			else :
				return cVariablesList["TMPDIR"] + "/"
	return None

@sIBL_Execution_Call
def sIBL_Wait( cWaitTime ):
	'''
	This Definition Is A Wait Timer.

	@param cWaitTime: Current Sleep Time In Seconds ( Integer )
	'''

	cLogger.debug( "> Waiting '%s' Seconds !", cWaitTime )

	time.sleep( cWaitTime )

@sIBL_Execution_Call
def sIBL_Path_Join( cStringA, cStringB, cJoinCharacter ):
	'''
	This Definition Joins Two Strings Together.

	@param cStringA: String A ( String )
	@param cStringB: String B ( String )
	@param cJoinCharacter: Join Character ( String )
	@return: Joined String. ( String )
	'''

	cLogger.debug( "> Joining '%s' And '%s' With '%s'.", cStringA, cStringB, cJoinCharacter )

	if cStringA.endswith( cJoinCharacter ):
		if cStringB.startswith( cJoinCharacter ):
			return cStringA + cStringB[1:]
		else :
			return cStringA + cStringB
	else :
		if cStringB.startswith( cJoinCharacter ):
			return cStringA + cStringB
		else :
			return cStringA + cJoinCharacter + cStringB

class sIBL_File( object ):
	'''
	This Class Provides Methods To Read / Write Files.
	'''

	@sIBL_Execution_Call
	def __init__( self, filePath ):
		'''
		This Method Initializes The Class.

		@param filePath: Current File Path. ( String )
		'''

		cLogger.debug( "> Initializing sIBL_File() Class." )

		# --- Setting Class Attributes. ---
		self.filePath = filePath
		cLogger.debug( "> self.filePath : '%s'.", self.filePath )

	@sIBL_Execution_Call
	def getFileContent( self, asString = None ):
		'''
		This Method Reads Provided File And Return The Content As A List Or A String.

		@param asString ( Optional ): Returned Object Will Be A String. ( String )
		@return: Current Read File Content. ( List / String )
		'''

		cLogger.debug( "> Current File Path : '%s'.", self.filePath )
		cLogger.debug( "> Reading Current File Content." )
		cFile = None
		cFileContent = None
		try :
			cFilePath = self.filePath
			cFile = open( cFilePath, "r" )
			if not asString :
				cFileContent = cFile.readlines()
			else :
				cFileContent = cFile.read()
		except IOError, cError:
			cLogger.error( "Exception In sIBL_File.getFileContent() Method | '%s'", cError )

		finally:
			if cFile:
				cFile.close()
				return cFileContent

	@sIBL_Execution_Call
	def setFileContent( self, cFileContent ):
		'''
		This Method Writes Content To Provided File.

		@param cFileContent: Content To Be Wrote In Current File ( List )
		'''

		cLogger.debug( "> Current File Path : '%s'.", self.filePath )

		cFile = open( self.filePath, "w" )
		for line in cFileContent:
			cFile.write( line )

		cFile.close()

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
