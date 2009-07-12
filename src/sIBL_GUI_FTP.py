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
***	sIBL_GUI_FTP.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***      	sIBL_GUI FTP.
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
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import sIBL_Common
import sIBL_FTP
import sIBL_UI_FTP

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
cLogger = logging.getLogger( "sIBL_Overall_Logger" )

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class sIBL_GUI_FTP( QWidget, sIBL_UI_FTP.Ui_sIBL_GUI_FTP_Form ):
	'''
	This Class Is sIBL_GUI_FTP Class.
	'''

	@sIBL_Common.sIBL_Execution_Call
	def __init__( self, cSIBL_GUI_Instance, cHost, cPort, cLogin, cPassword, cRemoteDirectory, cLocalDirectory, cIgnoreList = None, cParent = None ):
		'''
		This Method Initializes The Class.

		@param cHost: FTP Host. ( String )
		@param cPort: FTP Connection Port. ( Int )
		@param cLogin: Connection Login. ( String )
		@param cPassword: Connection Password. ( String )
		@param cRemoteDirectory: Starting Remote Directory For Transfers. ( String )
		@param cLocalDirectory: Starting Local Directory For Transfers. ( String )
		@param cIgnoreList: Current Ignore List. ( List )
		@param cParent: Current Parent. ( QObject )
		'''

		cLogger.debug( "> Initializing sIBL_GUI_FTP() Class." )
		cLogger.info( "sIBL_GUI_FTP | Initializing sIBL_GUI FTP !" )

		QWidget.__init__( self )
		self.setupUi( self )

		# Setting Up The UI.
		self.Cancel_pushButton.setText( "Close" )
		self.Download_progressBar.hide()
		self.Download_progressBar.setValue( 0 )

		# --- Setting Class Attributes. ---
		self.cParent = cParent
		self.cSIBL_GUI_Instance = cSIBL_GUI_Instance
		self.cHost = cHost
		self.cPort = cPort
		self.cLogin = cLogin
		self.cPassword = cPassword
		self.cIgnoreList = cIgnoreList
		self.cCommands = { "Downloads":[( cRemoteDirectory, cLocalDirectory, "Directories" )]}

		self.cFTP_Thread = None

		self.cTimer = QTimer( self )

		# sIBL_GUI_FTP Signals / Slots.
		self.connect( self.cTimer, SIGNAL( "timeout()" ), self.updateFtpProgress )

		self.connect( self.Start_Download_pushButton, SIGNAL( "clicked()" ), self.Start_Download_pushButton_OnClicked )
		self.connect( self.Cancel_pushButton, SIGNAL( "clicked()" ), self.Cancel_pushButton_OnClicked )


	@sIBL_Common.sIBL_Execution_Call
	def closeEvent( self, cEvent ):
		'''
		This Method Is Called When sIBL_GUI_FTP Is Closed.

		@param cEvent: QEvent ( QEvent )
		'''
		cLogger.debug( "> Closing sIBL_GUI_FTP Widget." )
		if self.cFTP_Thread is not None :
			self.stopWorkerThread()

		self.deleteLater()
		cEvent.accept()

	@sIBL_Common.sIBL_Execution_Call
	def workerThreadStarted( self ):
		'''
		This Method Is Called When FTP Worker Starts.
		'''

		cLogger.debug( "> FTP Worker Thread Started !" )

		self.cTimer.start( 125 )

		self.cSIBL_GUI_Instance.cFTP_Session_Active = True

		# Setting Up The UI.
		self.Current_File_label.setText( "" )
		self.Cancel_pushButton.setText( "Cancel" )
		self.Download_progressBar.hide()
		self.Download_progressBar.setValue( 0 )

	@sIBL_Common.sIBL_Execution_Call
	def workerThreadFinished( self ):
		'''
		This Method Is Called When FTP Worker Finished.
		'''

		cLogger.debug( "> FTP Worker Thread Finished !" )

		self.cTimer.stop()

		self.cSIBL_GUI_Instance.cFTP_Session_Active = False

		# Setting Up The UI.
		self.Current_File_label.setText( self.cFTP_Thread.cFTP.cProgressMessage[len( self.cFTP_Thread.cFTP.cProgressMessage ) - 1] )
		self.Cancel_pushButton.setText( "Close" )
		self.Download_progressBar.hide()
		self.Download_progressBar.setValue( 0 )

	@sIBL_Common.sIBL_Execution_Call
	def startWorkerThread( self ):
		'''
		This Method Starts The FTP Worker Thread.
		'''

		cLogger.debug( "> Starting FTP Worker Thread !" )

		# Initializing The FTP Worker Thread
		self.cFTP_Thread = sIBL_FTP_Worker( self.cHost, self.cPort, self.cLogin, self.cPassword, self.cCommands, self.cIgnoreList, self )

		self.connect( self.cFTP_Thread, SIGNAL( "started()" ), self.workerThreadStarted )
		self.connect( self.cFTP_Thread, SIGNAL( "finished()" ), self.workerThreadFinished )

		self.cFTP_Thread.start()

	@sIBL_Common.sIBL_Execution_Call
	def stopWorkerThread( self ):
		'''
		This Method Starts The FTP Worker Thread.
		'''

		cLogger.debug( "> Stopping FTP Worker Thread !" )

		self.cFTP_Thread.cFTP.closeConnectionState = True

		self.cFTP_Thread.exit()
		self.cFTP_Thread.wait()

	@sIBL_Common.sIBL_Execution_Call
	def Start_Download_pushButton_OnClicked( self ):
		'''
		This Method Triggers The FTP Worker Starting Method.
		'''

		cLogger.info( "sIBL_GUI_FTP | Initializing Online Repository Files Download !" )

		self.startWorkerThread()

	@sIBL_Common.sIBL_Execution_Call
	def Cancel_pushButton_OnClicked( self ):
		'''
		This Method Stops The Download And Triggers The Connection Close.
		'''

		cLogger.info( "sIBL_GUI_FTP | Stopping sIBL_GUI FTP !" )

		if self.cFTP_Thread is not None :
			self.stopWorkerThread()

		if str( self.Cancel_pushButton.text() ) == "Close" :
			self.close()

	@sIBL_Common.sIBL_Execution_Call
	def updateFtpProgress( self ):
		'''
		This Method Refreshes The GUI Progress Message.
		'''

		self.Current_File_label.setText( QString( self.cFTP_Thread.cFTP.cProgressMessage[len( self.cFTP_Thread.cFTP.cProgressMessage ) - 1] ) )

		if self.cFTP_Thread.cFTP.cDownloadProgress is not None :
			self.Download_progressBar.show()
			self.Download_progressBar.setRange( 0, len( self.cFTP_Thread.cFTP.cWalkerFilesList ) )
			self.Download_progressBar.setValue( self.cFTP_Thread.cFTP.cDownloadProgress )
		else :
			self.Download_progressBar.hide()

class sIBL_FTP_Worker( QThread ):
	'''
	This Class Is sIBL_FTP_Worker Class.
	'''

	@sIBL_Common.sIBL_Execution_Call
	def __init__( self, cHost, cPort, cLogin, cPassword, cCommands, cIgnoreList, cParent = None ):
		'''
		This Method Initializes The Class.

		@param cHost: FTP Host. ( String )
		@param cPort: FTP Connection Port. ( Int )
		@param cLogin: Connection Login. ( String )
		@param cPassword: Connection Password. ( String )
		@param cCommands: Download Commands. ( Dictionary )
		@param cIgnoreList: Current Ignore List. ( List )
		@param cParent: Current Parent. ( QObject )
		'''

		cLogger.debug( "> Initializing sIBL_FTP_Worker() Class." )

		QThread.__init__( self, cParent )

		# --- Setting Class Attributes. ---
		self.cHost = cHost
		self.cPort = cPort
		self.cLogin = cLogin
		self.cPassword = cPassword
		self.cCommands = cCommands
		self.cIgnoreList = cIgnoreList
		self.cParent = cParent
		self.cFTP = sIBL_FTP.sIBL_FTP()

	@sIBL_Common.sIBL_Execution_Call
	def run( self ):
		'''
		This Method Starts The Thread.
		'''

		cLogger.debug( "> Current FTP Worker Thread Started." )
		if self.cFTP.setConnection( self.cHost, self.cPort ):
			if self.cFTP.setLogin( self.cLogin, self.cPassword ):
				if "Downloads" in self.cCommands.keys():
					for cDownloads in self.cCommands["Downloads"]:
						if cDownloads[2] is "Directories" :
							cLogger.debug( "> Launching FTP Worker Directories Download Command." )
							self.cFTP.getRemoteTree( cDownloads[0], cDownloads[1], self.cIgnoreList )
						if cDownloads[2] is "Files":
							cLogger.debug( "> Launching FTP Worker Files Command." )
							self.cFTP.setLocalFile( cDownloads[0], cDownloads[1] )

				self.cFTP.closeConnection()

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
