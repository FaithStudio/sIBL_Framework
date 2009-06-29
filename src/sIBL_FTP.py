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
***	sIBL_FTP.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***      	sIBL_FTP.
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
import ftplib
import logging
import os
import platform
import sIBL_Common
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import sIBL_Common
import sIBL_Exceptions

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
cLogger = logging.getLogger( "sIBL_Overall_Logger" )

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class sIBL_FTP( object ):
	'''
	This Class Is sIBL_FTP Class.
	'''

	@sIBL_Common.sIBL_Execution_Call
	def __init__( self ) :
		'''
		This Method Initializes The Class.
		'''

		cLogger.debug( "> Initializing sIBL_FTP() Class." )

		# Setting Class Attributes.
		self.cFTP = ftplib.FTP()

		self.cWalkerFilesList = []
		self.cDownloadProgress = None
		self.cProgressMessage = []

		self.closeConnectionState = False

	@sIBL_Common.sIBL_Execution_Call
	def setProgressMessage( self, cProgressMessage, cWaitTime = None ) :
		'''
		This Method Sets The Progress Message.

		@param cProgressMessage: Progress Message. ( String )
		'''

		cLogger.debug( "> Setting Progress Message : '%s'.", cProgressMessage )
		cLogger.info( "sIBL_FTP | '%s'", cProgressMessage )
		self.cProgressMessage.append( cProgressMessage )
		if cWaitTime :
			sIBL_Common.sIBL_Wait( cWaitTime )

	@sIBL_Common.sIBL_Execution_Call
	def closeConnection( self ) :
		'''
		This Method Close The FTP Connection.
		'''

		self.setProgressMessage( "Connection Closed !", cWaitTime = 0.75 )
		self.cFTP.close()

	@sIBL_Common.sIBL_Execution_Call
	def setConnection( self, cHost, cPort ) :
		'''
		This Method Initialize The FTP Connection.

		@param cHost: FTP Host. ( String )
		@param cPort: FTP Connection Port. ( Int )
		@return: Connection State ( Boolean )
		'''

		self.setProgressMessage( "Connecting To '%s'" % cHost, cWaitTime = 0.75 )

		try :
			self.cFTP.connect( cHost, cPort )
		except Exception, cError:
			sIBL_Exceptions.sIBL_Exceptions_Feedback ( cError, "Exception In sIBL_FTP.setConnection() Method | '%s' Connection Failed !" % cHost, True )
			self.setProgressMessage( "Connection On '%s' Failed !" % cHost )
			return False

		return True

	@sIBL_Common.sIBL_Execution_Call
	def setLogin( self, cLogin, cPassword ) :
		'''
		This Method Log The User To FTP.

		@param cLogin: Connection Login. ( String )
		@param cPassword: Connection Password. ( String )
		@return: Login State ( Boolean )
		'''

		cLogger.debug( " > Login : '%s'.", cLogin )
		cLogger.debug( " > Password : '%s'.", cPassword )

		self.setProgressMessage( "Login On FTP !", cWaitTime = 0.75 )

		try :
			self.cFTP.login( cLogin, cPassword )
		except Exception, cError:
			sIBL_Exceptions.sIBL_Exceptions_Feedback ( cError, "Exception In sIBL_FTP.setConnection() Method | Login Failed !", True )
			self.setProgressMessage( "Login Failed !" )
			return False

		return True

	@sIBL_Common.sIBL_Execution_Call
	def recursiveWalker( self, cWorkingDirectory ) :
		'''
		This Method Is A Recursive FTP Walker.

		@param cWorkingDirectory: Current FTP Directory To Process. ( String )
		'''

		if not self.closeConnectionState :

			self.cFTP.cwd( cWorkingDirectory )

			cLogger.debug( " > Current Working Directory  : '%s'.", cWorkingDirectory )

			cDirectories, cFiles = self.getListing()

			cSubDirectories = []
			for cDirectory in cDirectories.keys() :
				cSubDirectories.append( os.path.join( cWorkingDirectory, cDirectory ) )

			for cFile in cFiles.keys() :
				self.cWalkerFilesList.append( os.path.join( cWorkingDirectory, cFile ) )

			for cSubDirectory in cSubDirectories:
				cLogger.debug( " > Entering : '%s'.", cSubDirectory )
				self.recursiveWalker( cSubDirectory )
		else :
			self.cFTP.close()

	@sIBL_Common.sIBL_Execution_Call
	def getListing( self ) :
		'''
		This Method Returns Directories And Files Of The Current FTP Directory.

		@return cDirectories, cFiles: Directories And Files Dictionaries Of The Current FTP Directory. ( Dictionaries )
		'''

		cDirectories, cFiles = {}, {}
		cListing = []
		self.cFTP.retrlines( 'LIST', cListing.append )
		cLogger.debug( " > Current Server Listing : '%s'.", cListing )
		for cLine in cListing:
			cTokens = cLine.split( None, 8 )

			if len( cTokens ) < 6:
				continue

			cItemName = cTokens[8].strip()

			if cItemName in ( '.', '..' ):
				continue

			cSymlink = None
			i = cItemName.find( " -> " )
			if i >= 0:
				cSymlink = cItemName[i + 4:]
				cItemName = cItemName[:i]

			cSize = int( cTokens[4] )

			cDate = ( cTokens[5], cTokens[6], cTokens[7] )

			cMode = cTokens[0]

			if cMode[0] == 'd':
				cDirectories[ cItemName ] = ( cSize, cMode, cDate, cSymlink )
			else:
				cFiles[ cItemName ] = ( cSize, cMode, cDate, cSymlink )

		cLogger.debug( " > Current Directories : '%s'.", cDirectories.keys() )
		cLogger.debug( " > Current Files : '%s'.", cFiles.keys() )

		return cDirectories, cFiles

	@sIBL_Common.sIBL_Execution_Call
	def setLocalDirectory( self, cLocalDirectory ) :
		'''
		This Method Create A Local Directory.

		@param cLocalDirectory: Local Directory To Create. ( String )
		@return: Success Of The Creation ( Boolean )
		'''

		if not os.path.exists( cLocalDirectory ):
			try:
				cLogger.debug( " > Creating Directory Tree : '%s'.", cLocalDirectory )
				os.makedirs( cLocalDirectory )
				return True
			except Exception, cError:
				sIBL_Exceptions.sIBL_Exceptions_Feedback ( cError, "Exception In sIBL_FTP.setLocalDirectory() Method | '%s' Creation Failed !" % cLocalDirectory )
				return False
		else:
			cLogger.debug( " > '%s' Directory Tree Already Exist, Skipping Creation !", cLocalDirectory )
			return True

	@sIBL_Common.sIBL_Execution_Call
	def setLocalFile( self, cRemoteFile, cLocalFilePath ) :
		'''
		This Method Download A Remote File.

		@param cRemoteFile: Remote File To Download. ( String )
		@param cLocalFilePath: Local Target File. ( String )
		'''

		try:
			cLogger.debug( " > Starting Remote File Download From '%s' To '%s' Local File. ", cRemoteFile, cLocalFilePath )
			cLocalFile = open( cLocalFilePath, "wb" )
			self.cFTP.retrbinary( 'RETR ' + cRemoteFile, cLocalFile.write )
			cLocalFile.close()

			return True

		except Exception, cError:
			sIBL_Exceptions.sIBL_Exceptions_Feedback ( cError, "Exception In sIBL_FTP.setLocalFile() Method | '%s' Creation Failed !" % cLocalFilePath, True )
			return False

	@sIBL_Common.sIBL_Execution_Call
	def getRemoteTree( self, cRemoteDirectory, cLocalDirectory ) :
		'''
		This Method Download A Remote Tree.

		@param cRemoteDirectory: Remote Tree Download. ( String )
		@param cLocalDirectory: Local Target Directory. ( String )
		'''

		if self.setLocalDirectory( cLocalDirectory ) and not self.closeConnectionState :

			cLogger.debug( " > Starting Remote Tree Download From '%s' To '%s' Local Directory.", cRemoteDirectory, cLocalDirectory )

			self.cFTP.cwd( cRemoteDirectory )
			self.cWalkerFilesList = []
			self.cDownloadProgress = None

			self.setProgressMessage( "Gathering Files List !" )

			self.recursiveWalker( cRemoteDirectory )

			self.setProgressMessage( "Gathering Done !", cWaitTime = 1.0 )
			self.setProgressMessage( "Starting Download !", cWaitTime = 1.0 )

			cStoredLocalDirectories = []

			self.cDownloadProgress = 0
			for cFile in self.cWalkerFilesList :
				if not self.closeConnectionState :
					self.setProgressMessage( "Downloading : '%s'" % os.path.basename( cFile ) )

					cRemoteFileDirectory = os.path.dirname( cFile )
					cOutputDirectory = cRemoteFileDirectory.replace( cRemoteDirectory, "" )
					if cOutputDirectory.startswith( " / " ) or cOutputDirectory.startswith( "\\" ) :
						cOutputDirectory = cOutputDirectory[1:]
					if platform.system() == "Windows":
						cOutputDirectory = cOutputDirectory.replace( " / ", "\\" )
					elif platform.system() == "Linux" or platform.system() == "Darwin":
						cOutputDirectory = cOutputDirectory.replace( "\\", " / " )

					if not cOutputDirectory in cStoredLocalDirectories :
						cStoredLocalDirectories.append( cOutputDirectory )
						self.setLocalDirectory( os.path.join( os.path.abspath( cLocalDirectory ), cOutputDirectory ) )

					cLocalFilePath = os.path.join( os.path.abspath( cLocalDirectory ), cOutputDirectory, os.path.basename( cFile ) )
					self.setLocalFile( cFile, cLocalFilePath )
					self.cDownloadProgress += 1
				else:
					return False

			self.setProgressMessage( "Downloading Done !", cWaitTime = 1.0 )
			self.cDownloadProgress = None

			return True
		else:
			return False

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
