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
***	sIBL_GUI_Updater.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***      	sIBL_GUI Updater.
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
import re
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *
from copy import deepcopy

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import sIBL_Common
import sIBL_Common_Settings
import sIBL_Exceptions
import sIBL_GUI_FTP
import sIBL_GUI_QWidgets
import sIBL_GUI_Settings
import sIBL_Parser
import sIBL_UI_Updater

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
cLogger = logging.getLogger( "sIBL_Overall_Logger" )

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class sIBL_GUI_Updater( QWidget, sIBL_UI_Updater.Ui_sIBL_GUI_Updater_Form ):
	'''
	This Class Is sIBL_GUI_Updater Class.
	'''

	@sIBL_Common.sIBL_Execution_Call
	def __init__( self, cSIBL_GUI, cReleasesInfos, cLocalReleasesFile, cParent = None ):
		'''
		This Method Initializes The Class.

		@param cReleasesInfos: Releases Informations. ( Dictionary )
		@param cLocalReleasesFile: Change Log Local Path. ( String )
		@param cParent: Current Parent. ( QObject )
		'''

		cLogger.debug( "> Initializing sIBL_GUI_Updater() Class." )
		cLogger.info( "sIBL_GUI_Updater | Initializing sIBL_GUI Updater !" )

		QWidget.__init__( self )
		self.setupUi( self )

		# --- Setting Class Attributes. ---
		self.cSIBL_GUI = cSIBL_GUI
		self.cParent = cParent
		self.cLocalReleasesFile = cLocalReleasesFile
		self.cReleasesInfos = cReleasesInfos
		self.greenColor = QColor( 128, 192, 128 )
		self.redColor = QColor( 192, 128, 128 )

		# Setting Up The UI.
		self.sIBL_GUI_groupBox.hide()
		self.Open_Repository_pushButton.hide()
		self.Templates_groupBox.hide()
		self.setSIBL_GUI_ReleaseInfos()
		self.setTemplates_ReleaseInfos()

		# sIBL_GUI Signals / Slots.
		self.connect( self.Open_Repository_pushButton, SIGNAL( "clicked()" ), self.Open_Repository_pushButton_OnClicked )
		self.connect( self.Get_Latest_Templates_pushButton, SIGNAL( "clicked()" ), self.Get_Latest_Templates_pushButton_OnClicked )
		self.connect( self.Close_pushButton, SIGNAL( "clicked()" ), self.Close_pushButton_OnClicked )

	@sIBL_Common.sIBL_Execution_Call
	def setSIBL_GUI_ReleaseInfos( self ):
		'''
		This Method Sets sIBL_GUI Updater Related Informations.
		'''

		if sIBL_Common_Settings.cReleaseVersion != self.cReleasesInfos["sIBL_GUI"][0] :
			# Setting Up The UI.
			self.sIBL_GUI_groupBox.show()
			self.Open_Repository_pushButton.show()

			self.Your_Version_label.setText( QString( sIBL_Common_Settings.cReleaseVersion.replace( ".", " . " ) ) )
			self.Latest_Version_label.setText( QString( self.cReleasesInfos["sIBL_GUI"][0].replace( ".", " . " ) ) )

			cLogger.debug( "> Loading Change Log : '%s'.", self.cLocalReleasesFile )
			cLocalReleasesFileUrl = QUrl.fromEncoded( QByteArray( sIBL_GUI_Settings.cChangeLog ) )
			self.Change_Log_webView.load( cLocalReleasesFileUrl )

	def setTemplates_ReleaseInfos( self ):
		'''
		This Method Sets Templates Updater Related Informations.
		'''

		cTemplatesInfos = deepcopy( self.cReleasesInfos )
		if "sIBL_GUI" in cTemplatesInfos.keys() :
			del( cTemplatesInfos["sIBL_GUI"] )

		for cTemplate in cTemplatesInfos.keys():
			if cTemplatesInfos[cTemplate][0] == cTemplatesInfos[cTemplate][1] :
				del( cTemplatesInfos[cTemplate] )

		if len( cTemplatesInfos ) > 0 :
			self.Templates_groupBox.show()
			self.Get_Latest_Templates_pushButton.show()

		self.Templates_tableWidget.clear()
		self.Templates_tableWidget.setEditTriggers( QAbstractItemView.NoEditTriggers )
		self.Templates_tableWidget.setSortingEnabled( False )
		self.Templates_tableWidget.setRowCount( len( cTemplatesInfos ) )
		self.Templates_tableWidget.setColumnCount( 5 )
		self.Templates_tableWidget.horizontalHeader().setStretchLastSection( True )
		self.Templates_tableWidget.setHorizontalHeaderLabels( ["Local Version", "Get It!", "Repository Version", "Release Type", "Comment"] )

		cColors = ( self.greenColor, self.redColor )
		cVerticalHeaderLabels = []
		for row, cKey in enumerate( cTemplatesInfos.keys() ) :
			if cKey != "sIBL_GUI" :
				cVerticalHeaderLabels.append( cKey )
				
				cItem = sIBL_GUI_QWidgets.Variable_QPushButton( True, cColors, ( "Yes", "No" ) )
				cLogger.debug( "> Setting Item In Column '1' : ' % s'.", cItem.text() )
				self.Templates_tableWidget.setCellWidget( row, 0, cItem )

				cItem = QTableWidgetItem( QString( cTemplatesInfos[cKey][0] ) )
				cItem.setTextAlignment( Qt.AlignCenter )
				cLogger.debug( "> Setting Item In Column '0' : ' % s'.", cItem )
				self.Templates_tableWidget.setItem( row, 1, cItem )

				cItem = QTableWidgetItem( QString( cTemplatesInfos[cKey][1] ) )
				cItem.setTextAlignment( Qt.AlignCenter )
				cLogger.debug( "> Setting Item In Column '2' : ' % s'.", cItem.text() )
				self.Templates_tableWidget.setItem( row, 2, cItem )

				cItem = QTableWidgetItem( QString( cTemplatesInfos[cKey][2] ) )
				cItem.setTextAlignment( Qt.AlignCenter )
				cLogger.debug( "> Setting Item In Column '3' : ' % s'.", cItem.text() )
				self.Templates_tableWidget.setItem( row, 3, cItem )

				cItem = QTableWidgetItem( QString( cTemplatesInfos[cKey][3] ) )
				cLogger.debug( "> Setting Item In Column '4' : ' % s'.", cItem.text() )
				self.Templates_tableWidget.setItem( row, 4, cItem )

		self.Templates_tableWidget.setVerticalHeaderLabels ( cVerticalHeaderLabels )
		self.Templates_tableWidget.resizeColumnsToContents()

	@sIBL_Common.sIBL_Execution_Call
	def Get_Latest_Templates_pushButton_OnClicked( self ):
		'''
		This Method Launch The Templates Download.
		'''
		
		cTemplatesList = deepcopy( self.cSIBL_GUI.cGlobalTemplates.keys() )		

		cDownloadList = []

		for row in range( self.Templates_tableWidget.rowCount() ) :
			cRemoteTemplate = str( self.Templates_tableWidget.verticalHeaderItem( row ).text() )
			if cRemoteTemplate not in cTemplatesList:
				cTemplatesList.append( cRemoteTemplate )
			if self.Templates_tableWidget.cellWidget( row, 0 ).text() == "Yes":
				cDownloadList.append( cRemoteTemplate )
		
		if len( cDownloadList ) != 0:
			cIgnoreList = deepcopy( cTemplatesList )
	
			for cTemplate in cTemplatesList :
				if cTemplate in cDownloadList:
					cIgnoreList.remove( cTemplate )
	
			cLogger.debug( "> Current Ignore List : '%s'.", cIgnoreList )
			self.cSIBL_GUI.getLatestTemplates( cIgnoreList )
		else:
			sIBL_GUI_QWidgets.sIBL_GUI_Message( "Warning", "Updater", "No Templates Selected For Download !" )

	@sIBL_Common.sIBL_Execution_Call
	def Open_Repository_pushButton_OnClicked( self ):
		'''
		This Method Open The Repository URL.
		'''

		if self.cReleasesInfos["sIBL_GUI"][1] == "Nightly" :
			cBranch = "Nightly/"
		else :
			cBranch = "Stable/"

		if platform.system() == "Windows" or platform.system() == "Microsoft":
			cReleaseURL = sIBL_GUI_Settings.cReleasesURL + cBranch + "Windows"
		elif platform.system() == "Linux":
			cReleaseURL = sIBL_GUI_Settings.cReleasesURL + cBranch + "Linux"
		elif platform.system() == "Darwin":
			cReleaseURL = sIBL_GUI_Settings.cReleasesURL + cBranch + "MacOsX"

		cLogger.debug( "> Opening URL : '%s'.", cReleaseURL )
		QDesktopServices.openUrl( QUrl( QString( cReleaseURL ) ) )

	@sIBL_Common.sIBL_Execution_Call
	def Close_pushButton_OnClicked( self ):
		'''
		This Method Closes sIBL_GUI_Updater.
		'''

		cLogger.info( "sIBL_GUI_Updater | Closing sIBL_GUI Updater !" )

		self.cParent.deleteLocalReleaseFile()
		self.close()

class sIBL_Online_Update( QObject ):
	'''
	This Class Is sIBL_Online_Update Class.
	'''

	@sIBL_Common.sIBL_Execution_Call
	def __init__( self, cSIBL_GUI, showInfoMessage, cParent = None ):
		'''
		This Method Initializes The Class.
		'''
		QObject.__init__( self, cParent )

		cLogger.debug( "> Initializing sIBL_Online_Update() Class." )

		# --- Setting Class Attributes. ---
		cLogger.debug( "> Change Log URL : '%s'.", sIBL_GUI_Settings.cReleasesFile )
		self.cReleasesFilePath = sIBL_GUI_Settings.cReleasesFile

		self.cLocalReleasesFile = None
		self.cReleases = None

		self.cFTP_Thread = None
		self.cSIBL_GUI = cSIBL_GUI
		self.showInfoMessage = showInfoMessage

	@sIBL_Common.sIBL_Execution_Call
	def startWorkerThread( self ):
		'''
		This Method Starts The FTP Worker Thread.
		'''

		cLogger.debug( "> Starting FTP Worker Thread !" )

		self.getLocalReleaseFile()

		# Initializing The FTP Worker Thread
		if self.cLocalReleasesFile is not None :
			self.cFTP_Thread = sIBL_GUI_FTP.sIBL_FTP_Worker( sIBL_GUI_Settings.cFTP_Host, sIBL_GUI_Settings.cFTP_Port, sIBL_GUI_Settings.cFTP_Login, sIBL_GUI_Settings.cFTP_Password, { "Downloads" : [ ( self.cReleasesFilePath, self.cLocalReleasesFile, "Files" )]}, self )

			self.connect( self.cFTP_Thread, SIGNAL( "finished()" ), self.workerThreadFinished )

			self.cFTP_Thread.start()

	@sIBL_Common.sIBL_Execution_Call
	def workerThreadFinished( self ):
		'''
		This Method Is Called When FTP Worker Finished.
		'''

		cLogger.debug( "> FTP Worker Thread Finished !" )

		self.getLatestVersions()
		self.startUpdater()

	@sIBL_Common.sIBL_Execution_Call
	def getLatestVersions( self ):
		'''
		This Method Gets The Last Online Release Version Number By Downloading The Change Log File And Parse It.
		'''

		if os.path.exists( self.cLocalReleasesFile ):
			self.cReleases = sIBL_Parser.sIBL_Parser( self.cLocalReleasesFile )
		else :
			cLogger.error( "'%s'.", "sIBL_GUI | " + "Failed To Access Local Change Log !" )

	@sIBL_Common.sIBL_Execution_Call
	def getLocalReleaseFile( self ):
		'''
		This Method Gets A Local Download Path For The Change Log.

		@return: Change Log Local Path. ( String )
		'''
		self.cLocalReleasesFile = os.path.join( sIBL_Common.sIBL_GetTemporarySystemPath(), os.path.basename( self.cReleasesFilePath ) )

		cLogger.debug( "> Current Change Log Local Path : '%s'.", self.cLocalReleasesFile )

		return self.cLocalReleasesFile

	@sIBL_Common.sIBL_Execution_Call
	def deleteLocalReleaseFile( self ):
		'''
		This Method Delete The Local Change Log.
		'''

		try:
			cLogger.debug( "> Deleting Local Change Log : '%s'.", self.cLocalReleasesFile )

			os.remove( self.cLocalReleasesFile )

		except Exception, cError:
			sIBL_Exceptions.sIBL_Exceptions_Feedback ( cError, "Exception In sIBL_Online_Update.deleteLocalReleaseFile() Method | '%s' Deleting Failed" % self.cLocalReleasesFile, True )

	@sIBL_Common.sIBL_Execution_Call
	def startUpdater( self ):
		'''
		This Method Gets A Local Download Path For The Change Log.
		'''

		if self.cReleases is not None :
			cUpdaterStartState = False

			cReleasesInfos = {}

			cReleasesInfos["sIBL_GUI"] = ( self.cReleases.getAttributeValue( "sIBL_GUI", "Release" ), self.cReleases.getAttributeValue( "sIBL_GUI", "Type" ) )

			if sIBL_Common_Settings.cReleaseVersion != self.cReleases.getAttributeValue( "sIBL_GUI", "Release" ) :
				cUpdaterStartState = True

			cReleasesSections = self.cReleases.getSections()
			cLocalVersionExists = False
			cTemplateSkippingState = False
			for cKey in cReleasesSections.keys() :
				if cKey not in self.cSIBL_GUI.cGlobalTemplates :
					if cKey != "sIBL_GUI" :
						cLocalVersionExists = False
						cUpdaterStartState = True
				else :
					cLocalVersionExists = True
					cLocalTemplate = self.cSIBL_GUI.cGlobalTemplates[cKey]
					if self.cReleases.getAttributeValue( cKey, "Release" ) != cLocalTemplate["Template Release"] :
						cUpdaterStartState = True

				if cLocalVersionExists :
					cLocalVersion = cLocalTemplate["Template Release"]
				else :
					cLocalVersion = "No Local Version"

				if cLocalVersion == "No Local Version" and self.cSIBL_GUI.Ignore_Missing_Templates_checkBox.isChecked() :
					cTemplateSkippingState = True
				else :
					cTemplateSkippingState = False

				if cKey != "sIBL_GUI" and not cTemplateSkippingState :
					cReleasesInfos[cKey] = ( cLocalVersion, self.cReleases.getAttributeValue( cKey, "Release" ), self.cReleases.getAttributeValue( cKey, "Type" ), self.cReleases.getAttributeValue( cKey, "Comment" ) )

			if cUpdaterStartState :
				cLogger.debug( "> Starting Online Updater." )
				self.cSIBL_GUI.setCursor( Qt.ArrowCursor )
				self.cUI = sIBL_GUI_Updater( self.cSIBL_GUI, cReleasesInfos, self.cLocalReleasesFile, self )
				self.cUI.show()
			else :
				self.deleteLocalReleaseFile()

				# Reseting sIBL_GUI Cursor.
				self.cSIBL_GUI.setCursor( Qt.ArrowCursor )

				if self.showInfoMessage :
					sIBL_GUI_QWidgets.sIBL_GUI_Message( "Information", "Updater", "Your sIBL_GUI Release Is Up To Date !" )
				else :
					cLogger.info( "sIBL_GUI | Your sIBL_GUI Release Is Up To Date !" )
		else :
			cLogger.error( "sIBL_GUI | Current Latest Version Is Not Available !" )

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
