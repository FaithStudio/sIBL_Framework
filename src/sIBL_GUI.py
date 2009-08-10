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
***	sIBL_GUI.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***      	sIBL_GUI Main Module.
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
import socket
import sys
import time
if platform.system() == "Windows" or platform.system() == "Microsoft":
	import win32com.client
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *
from PyQt4.QtOpenGL import *
from copy import deepcopy
from math import pow

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import sIBL_Collection
import sIBL_Common
import sIBL_Common_Settings
import sIBL_Exceptions
import sIBL_GUI_About
import sIBL_GUI_FTP
import sIBL_GUI_QWidgets
import sIBL_GUI_Settings
import sIBL_GUI_Updater
import sIBL_Parser
import sIBL_Recursive_Walker
import sIBL_UI

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
cLogger = logging.getLogger( "sIBL_Overall_Logger" )

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class Popup_QGraphicsItem( QGraphicsItem ) :
	'''
	This Class Is The Marker QGraphicsItem Class.
	'''

	@sIBL_Common.sIBL_Execution_Call
	def __init__( self, cSIBL_GUI, cCollectionItem_Name ) :
		'''
		This Method Initializes The Class.

		@param cSIBL_GUI: Current sIBL_GUI Window ( String )
		@param cCollectionItem_Name: Current Collection Item ( String )
		'''

		cLogger.debug( "> Initializing Popup_QGraphicsItem() Class." )

		QGraphicsItem.__init__( self )

		# --- Setting Class Attributes. ---
		self.cSIBL_GUI = cSIBL_GUI
		self.cCollectionItem_Name = cCollectionItem_Name
		self.cIBLAttributes = self.cSIBL_GUI.cGlobalCollection[self.cCollectionItem_Name]
		self.cSIBLIcon = QPixmap()
		self.cSIBLIcon.load( self.cIBLAttributes["Icon Path"] )
		self.cTextShift = 4
		self.cParagraphWidth = 200

	@sIBL_Common.sIBL_Execution_Call
	def boundingRect( self ) :
		'''
		This Method Sets The Bounding Rectangle.
		'''

		return QRectF( -self.cSIBLIcon.width() / 2 , -self.cSIBLIcon.height() / 2, self.cSIBLIcon.width() + self.cTextShift + self.cParagraphWidth, self.cSIBLIcon.height() )

	@sIBL_Common.sIBL_Execution_Call
	def paint( self, cPainter, cOptions, cWidget ) :
		'''
		This Method Paint The Popup.

		@param cPainter: QPainter ( QPainter )
		@param cOptions: QStyleOptionGraphicsItem  ( QStyleOptionGraphicsItem  )
		@param cWidget: QWidget ( QWidget )
		'''

		cPainter.drawPixmap ( -( self.cSIBLIcon.width() / 2 ), -( self.cSIBLIcon.height() / 2 ), self.cSIBLIcon )

		cPainter.setPen( QPen( Qt.black, 2, Qt.SolidLine, Qt.FlatCap, Qt.MiterJoin ) )
		cPainter.drawRect( -( self.cSIBLIcon.width() / 2 ), -( self.cSIBLIcon.height() / 2 ), self.cSIBLIcon.width(), self.cSIBLIcon.height() )

		cFont = cPainter.font()
		cFont.setBold( True )
		cFont.setPointSize( 12 )
		cPainter.setFont( cFont )
		cPainter.setPen( Qt.black )
		cTextBBox = QRectF( self.cSIBLIcon.width() / 2 + self.cTextShift, -self.cSIBLIcon.width() / 2, self.cParagraphWidth, self.cSIBLIcon.height() )
		cPainter.drawText( cTextBBox, self.cIBLAttributes["sIBL Name"] )
		cFont.setBold( False )
		cFont.setPointSize( 12 )
		cTextBBox.translate ( 0, 16 )
		cPainter.drawText( cTextBBox, self.cIBLAttributes["Location"] + " - " + self.cIBLAttributes["Author"] )
		cTextBBox.translate ( 0, 16 )
		cFont.setItalic( True )
		cPainter.drawText( cTextBBox, self.cIBLAttributes["Comment"] )

class Marker_QGraphicsItem( QGraphicsItem ) :
	'''
	This Class Is The Marker QGraphicsItem Class.
	'''

	@sIBL_Common.sIBL_Execution_Call
	def __init__( self, cSIBL_GUI, cMarker_Picture, cMarkerScale, cCollectionItem_Name ) :
		'''
		This Method Initializes The Class.
		'''

		cLogger.debug( "> Initializing Marker_QGraphicsItem() Class." )

		QGraphicsItem.__init__( self )

		# --- Setting Class Attributes. ---
		self.cSIBL_GUI = cSIBL_GUI
		self.cMarkerScale = cMarkerScale
		self.cCollectionItem_Name = cCollectionItem_Name
		self.cMarker_QPixmap = QPixmap( cMarker_Picture )
		self.setCursor( Qt.PointingHandCursor )
		self.setAcceptsHoverEvents( True )

	@sIBL_Common.sIBL_Execution_Call
	def boundingRect( self ) :
		'''
		This Method Sets The Bounding Rectangle.
		'''

		return QRectF( -( self.cMarker_QPixmap.width() ) / 2, -( self.cMarker_QPixmap.height() ) / 2, self.cMarker_QPixmap.width(), self.cMarker_QPixmap.height() )

	@sIBL_Common.sIBL_Execution_Call
	def paint( self, cPainter, cOptions, cWidget ) :
		'''
		This Method Paint The Marker.

		@param cPainter: QPainter ( QPainter )
		@param cOptions: QStyleOptionGraphicsItem  ( QStyleOptionGraphicsItem  )
		@param cWidget: QWidget ( QWidget )
		'''

		cPainter.drawPixmap ( -( self.cMarker_QPixmap.width() / 2 ), -( self.cMarker_QPixmap.height() / 2 ), self.cMarker_QPixmap )

	@sIBL_Common.sIBL_Execution_Call
	def mousePressEvent( self, cEvent ) :
		'''
		This Method Redefines mousePressEvent.

		@param cEvent: QEvent ( QEvent )
		'''

		pass

	@sIBL_Common.sIBL_Execution_Call
	def mouseDoubleClickEvent( self, cEvent ) :
		'''
		This Method Redefines mouseDoubleClickEvent.

		@param cEvent: QEvent ( QEvent )
		'''

		self.cSIBL_GUI.cEditedIBL = self.cCollectionItem_Name
		self.cSIBL_GUI.sIBL_GUI_tabWidget.setCurrentIndex( 1 )
		cLogger.info( "sIBL_GUI | Starting '%s' Import !", self.cSIBL_GUI.cEditedIBL )
		self.cSIBL_GUI.setEditedSIBLInfos()

	@sIBL_Common.sIBL_Execution_Call
	def hoverEnterEvent( self, cEvent ) :
		'''
		This Method Redefines hoverEnterEvent.

		@param cEvent: QEvent ( QEvent )
		'''

		self.cPopup = Popup_QGraphicsItem( self.cSIBL_GUI, self.cCollectionItem_Name )

		cCustomScale = 1 * ( 1 / self.cMarkerScale )
		cCustomOffset = ( 96, 96 )
		cScaleMatrix = ( self.sceneMatrix().m11(), self.sceneMatrix().m22() )
		self.cPopup.scale( cCustomScale * cScaleMatrix[0], cCustomScale * cScaleMatrix[1] )
		self.cPopup.setPos( cEvent.scenePos().x() + ( cCustomOffset[0] * cCustomScale * cScaleMatrix[0] ), cEvent.scenePos().y() + ( cCustomOffset[1] * cCustomScale * cScaleMatrix[1] ) )
		self.cPopup.setZValue( 2 )

		self.scene().addItem( self.cPopup )

		QGraphicsItem.hoverEnterEvent( self, cEvent )

	@sIBL_Common.sIBL_Execution_Call
	def hoverLeaveEvent( self, cEvent ) :
		'''
		This Method Redefines hoverLeaveEvent.

		@param cEvent: QEvent ( QEvent )
		'''

		self.scene().removeItem( self.cPopup )
		QGraphicsItem.hoverLeaveEvent( self, cEvent )

class WorldMap_QGraphicsItem( QGraphicsItem ) :
	'''
	This Class Is The World Map Picture QGraphicsItem Class.
	'''

	@sIBL_Common.sIBL_Execution_Call
	def __init__( self, cWorldMap_QPixmap ) :
		'''
		This Method Initializes The Class.
		'''

		cLogger.debug( "> Initializing WorldMap_QGraphicsItem() Class." )

		QGraphicsItem.__init__( self )

		# --- Setting Class Attributes. ---
		self.cWorldMap_QPixmap = cWorldMap_QPixmap
		self.setCursor( Qt.CrossCursor )

	@sIBL_Common.sIBL_Execution_Call
	def boundingRect( self ) :
		'''
		This Method Sets The Bounding Rectangle.
		'''

		return QRectF( -( self.cWorldMap_QPixmap.width() ) / 2, -( self.cWorldMap_QPixmap.height() ) / 2, self.cWorldMap_QPixmap.width(), self.cWorldMap_QPixmap.height() )

	@sIBL_Common.sIBL_Execution_Call
	def paint( self, cPainter, cOptions, cWidget ) :
		'''
		This Method Paint The WorldMap.

		@param cPainter: QPainter ( QPainter )
		@param cOptions: QStyleOptionGraphicsItem  ( QStyleOptionGraphicsItem  )
		@param cWidget: QWidget ( QWidget )
		'''

		cPainter.drawPixmap ( -( self.cWorldMap_QPixmap.width() / 2 ), -( self.cWorldMap_QPixmap.height() / 2 ), self.cWorldMap_QPixmap )

class WorldMap_QGraphicsView( QGraphicsView ) :
	'''
	This Class Is The GPS Map Picture QGraphicsView Class.
	'''

	@sIBL_Common.sIBL_Execution_Call
	def __init__( self, cSIBL_GUI, cWorldMapFile, cWidgetSizeX, cWidgetSizeY ) :
		'''
		This Method Initializes The Class.
		'''

		cLogger.debug( "> Initializing WorldMap_QGraphicsView() Class." )
		cLogger.info( "sIBL_GUI | Initializing World Map !" )

		QGraphicsView.__init__( self )

		# --- Setting Class Attributes. ---
		self.cSIBL_GUI = cSIBL_GUI

		self.cWorldMap_QPixmap = QPixmap()
		self.cWorldMap_QPixmap.load( cWorldMapFile )

		if self.cSIBL_GUI.OpenGLActive :
			self.setViewport( QGLWidget() )
			if self.cSIBL_GUI.GPSMapAntialiasingActive :
				self.setRenderHint( QPainter.HighQualityAntialiasing )
		else :
			if self.cSIBL_GUI.GPSMapAntialiasingActive :
				self.setRenderHint( QPainter.SmoothPixmapTransform )

		self.setHorizontalScrollBarPolicy( Qt.ScrollBarAlwaysOff )
		self.setVerticalScrollBarPolicy( Qt.ScrollBarAlwaysOff )
		self.setTransformationAnchor( QGraphicsView.AnchorUnderMouse )
		self.setDragMode( QGraphicsView.ScrollHandDrag )

		self.cScaleFactor = 1 / ( float( self.cWorldMap_QPixmap.width() ) / float( cWidgetSizeX ) )
		self.scale( self.cScaleFactor, self.cScaleFactor )

		self.cSpacer = 128

		self.cQGraphicsScene = QGraphicsScene( self )
		self.cQGraphicsScene.setItemIndexMethod( QGraphicsScene.NoIndex )
		self.cQGraphicsScene.setSceneRect( -( float( self.cWorldMap_QPixmap.width() ) + self.cSpacer ) / 2, -( float( self.cWorldMap_QPixmap.height() ) + self.cSpacer ) / 2, float( self.cWorldMap_QPixmap.width() ) + self.cSpacer, float( self.cWorldMap_QPixmap.height() ) + self.cSpacer )

		self.setScene( self.cQGraphicsScene )

		self.setBackgroundBrush( QBrush( QPixmap( ":/sIBL_GUI/Resources/Grid_Background.png" ) ) )

		self.worldMapDraw()

	@sIBL_Common.sIBL_Execution_Call
	def worldMapDraw( self ) :
		'''
		This Method Draw The WorldMap.
		'''

		self.cQGraphicsScene.clear()

		cWorldMap = WorldMap_QGraphicsItem( self.cWorldMap_QPixmap )
		self.cQGraphicsScene.addItem( cWorldMap )
		cWorldMap.setZValue( 0 )

		if len( self.cSIBL_GUI.cFilteredCollection ) != 0 :
			cCollection = self.cSIBL_GUI.cFilteredCollection
		else :
			cCollection = self.cSIBL_GUI.cGlobalCollection
		cZValue = 1
		for cKey in cCollection.keys() :
			cItemAttributes = cCollection[cKey]

			if "GPS Latitude" in cItemAttributes and "GPS Longitude" in cItemAttributes :
				cMarkerScale = 0.5
				cMarkerShift = ( 6.5, -20 )
				cInverseScaleMatrix = ( 1 / self.matrix().m11(), 1 / self.matrix().m22() )

				cMarker = Marker_QGraphicsItem( self.cSIBL_GUI, ":/sIBL_GUI/Resources/Marker_Small.png", cMarkerScale, cKey )

				cMarker.setPos( ( float( cMarkerShift[0] ) * float( cMarkerScale ) * ( cInverseScaleMatrix[0] ) ) + float( cItemAttributes["GPS Longitude"] ) * ( float( self.cWorldMap_QPixmap.width() ) / 360 ), ( float( cMarkerShift[1] ) * float( cMarkerScale ) * ( cInverseScaleMatrix[1] ) ) - float( cItemAttributes["GPS Latitude"] ) * ( float( self.cWorldMap_QPixmap.height() ) / 180 ) )
				cMarker.scale( cMarkerScale * cInverseScaleMatrix[0], cMarkerScale * cInverseScaleMatrix[1] )
				cZValue += 1
				cMarker.setZValue( cZValue )

				self.cQGraphicsScene.addItem( cMarker )

	@sIBL_Common.sIBL_Execution_Call
	def scaleView( self, scaleFactor ) :
		'''
		This Method Scale The QGraphicsView.

		@param scaleFactor: Float ( Float )
		'''

		factor = self.matrix().scale( scaleFactor, scaleFactor ).mapRect( QRectF( 0, 0, 1, 1 ) ).width()
		if factor < 0.15 or factor > 1.5 :
			return

		self.scale( scaleFactor, scaleFactor )

	@sIBL_Common.sIBL_Execution_Call
	def wheelEvent( self, cEvent ) :
		'''
		This Method Redefines wheelEvent.

		@param cEvent: QEvent ( QEvent )
		'''

		self.scaleView( pow( 1.5, -cEvent.delta() / 1500.0 ) )
		self.worldMapDraw()

	@sIBL_Common.sIBL_Execution_Call
	def keyPressEvent( self, cEvent ) :
		'''
		This Method Redefines keyPressEvent.

		@param cEvent: QEvent ( QEvent )
		'''

		cKey = cEvent.key()
		if cKey == Qt.Key_Plus:
			self.scaleView( 1.15 )
			self.worldMapDraw()
		elif cKey == Qt.Key_Minus:
			self.scaleView( 1 / 1.15 )
			self.worldMapDraw()
		else:
			QGraphicsView.keyPressEvent( self, cEvent )

class sIBL_GUI_SplashScreen( QSplashScreen ) :
	'''
	This Class Is The sIBL_GUI_SplashScreen Class.
	'''

	@sIBL_Common.sIBL_Execution_Call
	def __init__( self, cPicture, cWaitTime ) :
		'''
		This Method Initializes The Class.

		@param cPicture: Current Picture Path ( String )
		@param cWaitTime: Wait Time ( Integer )
		'''

		cLogger.debug( "> Initializing sIBL_GUI_SplashScreen() Class." )

		QSplashScreen.__init__( self, cPicture )

		self.setWindowFlags( self.windowFlags() | Qt.WindowStaysOnTopHint )

		# --- Setting Class Attributes. ---
		self.cWaitTime = cWaitTime

	@sIBL_Common.sIBL_Execution_Call
	def setMessage( self, cMessage ):
		'''
		This Method Initializes The Class.

		@param cMessage: Message To Display On The Splashscreen ( String )
		'''

		self.showMessage( cMessage )
		sIBL_Common.sIBL_Wait( self.cWaitTime )

class sIBL_GUI( QMainWindow, sIBL_UI.Ui_sIBL_GUI ) :
	'''
	This Class Is The Main Class For sIBL_GUI.
	'''

	#***************************************************************************************
	#***	Initialization.
	#***************************************************************************************

	@sIBL_Common.sIBL_Execution_Call
	def __init__( self ) :
		'''
		This Method Initializes The Class.
		'''

		cLogger.debug( "> Initializing sIBL_GUI() Class." )
		cSpashScreen.setMessage( "sIBL_GUI - " + sIBL_Common_Settings.cReleaseVersion + " | Setting GUI Widgets." )

		# Visual Style Choice.
		if not platform.system() == "Darwin":
			QApplication.setStyle( "Plastique" )

		QMainWindow.__init__( self )
		self.setupUi( self )

		# --- Setting Class Attributes. ---
		# Allocating Core Data Structures.
		self.cGlobalCollection = None
		self.cGlobalTemplates = None
		self.cGlobalHelpFiles = None
		self.cFilteredCollection = None
		# Allocating Various Stuff.
		self.cEditedIBL = None
		self.GPSMapAntialiasingActive = None
		self.OpenGLActive = None
		self.WorldMap_QGraphicsView = None
		self.cTextEdits_List = None
		self.cLogFileSize = None
		self.cTimer = None
		# Initializing sIBL_GUI FTP Refresh Attributes.
		self.cFTP_UI = None
		self.cFTP_Session_Active = False
		self.cTemplates_Changed = False
		self.cHelp_Changed = False
		self.cHelpFilesList = None
		# Initializing Interface Buttons Color Attributes.
		self.greenColor = QColor( 128, 192, 128 )
		self.redColor = QColor( 192, 128, 128 )

		# Replacing QFileSystemWatcher By A Custom HXC Faster File Watcher
		self.cLogFileSize = os.path.getsize( cSIBL_GUI_LogFile )
		self.cTimer = QTimer( self )
		self.cTimer.start( 20 )

		# --- sIBL_GUI Log Window Initialization. ---
		self.Log_textEdit.setReadOnly( True )
		self.Log_textEdit.setWordWrapMode( QTextOption.NoWrap )
		self.Log_textEdit.setFontFamily( "Courier" )
		self.setLogTextEdit()

		# Setting Window Title, Closing The Log Window And Ensuring Minimum Size.
		self.setWindowTitle( "sIBL_GUI - " + sIBL_Common_Settings.cReleaseVersion )
		self.sIBL_GUI_dockWidget.close()
		self.resize( 1, 1 )

		# --- sIBL_GUI Preferences Tab Initialization. ---
		cSpashScreen.setMessage( "sIBL_GUI - " + sIBL_Common_Settings.cReleaseVersion + " | Restoring Settings." )

		self.setVerboseLevelComboBox()
		self.setCollectionsPathsTableWidget()
		self.setSIBL_FrameworkPathlineEdit()
		self.setSIBLeditPathLineEdit()
		self.setTemplatesPathLineEdit()
		self.setHelpFilesPathLineEdit()
		self.setCustomTextEditorPathLineEdit()
		self.setCustomFileBrowserPathLineEdit()
		self.checkPreferencesPaths()
		self.GPSMapAntialiasingActive = self.setCheckBoxStateFromSettings( self.Activate_Antialiasing_checkBox, "Settings", "GPSMapAntialiasing" )
		self.OpenGLActive = self.setCheckBoxStateFromSettings( self.Activate_OpenGL_checkBox, "Settings", "OpenGL" )
		self.setCheckBoxStateFromSettings( self.Check_For_New_Releases_checkBox, "Settings", "OnlineUpdate" )
		self.setCheckBoxStateFromSettings( self.Ignore_Missing_Templates_checkBox, "Settings", "IgnoreMissingTemplates" )

		# --- sIBL_GUI Collection Tab Initialization. ---
		cSpashScreen.setMessage( "sIBL_GUI - " + sIBL_Common_Settings.cReleaseVersion + " | Gathering sIBL Sets." )

		# Collections Initialization.
		cSpashScreen.setMessage( "sIBL_GUI - " + sIBL_Common_Settings.cReleaseVersion + " | Initializing Thumbnails." )
		self.Collections_listWidget.setSpacing( 4 )
		self.Collections_listWidget.setIconSize( QSize( 128, 128 ) )

		self.initializeCollectionsRelationships()

		# --- sIBL_GUI GPS Map Initialization. ---
		cSpashScreen.setMessage( "sIBL_GUI - " + sIBL_Common_Settings.cReleaseVersion + " | Initializing GPS Map." )
		self.setGPSMap()

		# --- sIBL_GUI Import Tab Initialization. ---
		cSpashScreen.setMessage( "sIBL_GUI - " + sIBL_Common_Settings.cReleaseVersion + " | Gathering Templates." )

		self.cTextEdits_List = ( self.Comment_textEdit, self.Template_Comment_textEdit )
		self.initializeLineAndTextEditsPalette()

		# sIBL V2 Format Support.
		self.Shot_Date_groupBox.hide()

		# Templates Initialization.
		self.initializeTemplatesRelationships()

		# --- sIBL_GUI Help Tab Initialization. ---
		self.initializeHelpRelationships()
		self.setHelpTextBrowser()

		# --- sIBL_GUI About Tab Initialization. ---
		cSpashScreen.setMessage( "sIBL_GUI - " + sIBL_Common_Settings.cReleaseVersion + " | Setting Version Number And About Message." )
		self.setAboutMessage()

		# --- sIBL_GUI Signals / Slots. ---
		# self.connect( self.cLogWatcher, SIGNAL( "fileChanged(const QString&)" ), self.setLogTextEdit )
		self.connect( self.cTimer, SIGNAL( "timeout()" ), self.refreshLogTextEdit )

		self.connect( self.Collections_comboBox, SIGNAL( "activated(int)" ), self.Collections_comboBox_Activated )
		self.connect( self.Authors_comboBox, SIGNAL( "activated(int)" ), self.Authors_comboBox_Activated )
		self.connect( self.Locations_comboBox, SIGNAL( "activated(int)" ), self.Locations_comboBox_Activated )
		self.connect( self.Search_lineEdit, SIGNAL( "textChanged(const QString&)" ), self.Search_lineEdit_OnTextChanged )
		self.connect( self.Collections_listWidget, SIGNAL( "itemDoubleClicked(QListWidgetItem *)" ), self.sendListWidgetItemToImportTab )
		self.connect( self, SIGNAL( "WorldMap_Refresh()" ), self.WorldMap_QGraphicsView.worldMapDraw )

		self.connect( self.Software_comboBox, SIGNAL( "activated(int)" ), self.setTemplateComboBox )
		self.connect( self.Template_comboBox, SIGNAL( "activated(int)" ), self.setTemplateOptionsAndInfosWidgets )
		self.connect( self.Open_Templates_Folder_pushButton, SIGNAL( "clicked()" ), self.Open_Templates_Folder_pushButton_OnClicked )
		self.connect( self.Edit_Current_Template_pushButton, SIGNAL( "clicked()" ), self.Edit_Current_Template_pushButton_OnClicked )
		self.connect( self.Refresh_sIBL_File_pushButton, SIGNAL( "clicked()" ), self.Refresh_sIBL_File_pushButton_OnClicked )
		self.connect( self.Edit_In_sIBL_Edit_pushButton, SIGNAL( "clicked()" ), self.Edit_In_sIBL_Edit_pushButton_OnClicked )
		self.connect( self.Open_sIBL_Folder_pushButton, SIGNAL( "clicked()" ), self.Open_sIBL_Folder_pushButton_OnClicked )
		self.connect( self.Output_Loader_Script_pushButton, SIGNAL( "clicked()" ), self.Output_Loader_Script_pushButton_OnClicked )
		self.connect( self.Open_Output_Folder_pushButton, SIGNAL( "clicked()" ), self.Open_Output_Folder_pushButton_OnClicked )
		self.connect( self.Send_To_Software_pushButton, SIGNAL( "clicked()" ), self.Send_To_Software_pushButton_OnClicked )

		self.connect( self.Help_Files_comboBox, SIGNAL( "activated(int)" ), self.setHelpTextBrowser )

		self.connect( self.sIBL_Framework_Path_toolButton, SIGNAL( "clicked()" ), self.sIBL_Framework_Path_toolButton_OnClicked )
		self.connect( self.sIBL_Framework_Path_lineEdit, SIGNAL( "editingFinished()" ), self.sIBL_Framework_Path_lineEdit_OnEditFinished )
		self.connect( self.sIBLedit_Path_toolButton, SIGNAL( "clicked()" ), self.sIBLedit_Path_toolButton_OnClicked )
		self.connect( self.sIBLedit_Path_lineEdit, SIGNAL( "editingFinished()" ), self.sIBLedit_Path_lineEdit_OnEditFinished )
		self.connect( self.Templates_toolButton, SIGNAL( "clicked()" ), self.Templates_toolButton_OnClicked )
		self.connect( self.Templates_Path_lineEdit, SIGNAL( "editingFinished()" ), self.Templates_Path_lineEdit_OnEditFinished )
		self.connect( self.Help_Files_toolButton, SIGNAL( "clicked()" ), self.Help_Files_toolButton_OnClicked )
		self.connect( self.Help_Files_Path_lineEdit, SIGNAL( "editingFinished()" ), self.Help_Files_Path_lineEdit_OnEditFinished )
		self.connect( self.Collections_Paths_tableWidget, SIGNAL( "cellChanged (int,int)" ), self.Collections_Paths_tableWidget_OnCellChanged )
		self.connect( self.Refresh_Collection_pushButton, SIGNAL( "clicked()" ), self.initializeCollectionsRelationships )
		self.connect( self.Edit_Collection_pushButton, SIGNAL( "clicked()" ), self.Edit_Collection_pushButton_OnClicked )
		self.connect( self.Add_pushButton, SIGNAL( "clicked()" ), self.Add_pushButton_OnClicked )
		self.connect( self.Remove_pushButton, SIGNAL( "clicked()" ), self.Remove_pushButton_OnClicked )
		self.connect( self.Custom_Text_Editor_Path_toolButton, SIGNAL( "clicked()" ), self.Custom_Text_Editor_Path_toolButton_OnClicked )
		self.connect( self.Custom_Text_Editor_Path_lineEdit, SIGNAL( "editingFinished()" ), self.Custom_Text_Editor_Path_lineEdit_OnEditFinished )
		self.connect( self.Custom_File_Browser_Path_toolButton, SIGNAL( "clicked()" ), self.Custom_File_Browser_Path_toolButton_OnClicked )
		self.connect( self.Custom_File_Browser_Path_lineEdit, SIGNAL( "editingFinished()" ), self.Custom_File_Browser_Path_lineEdit_OnEditFinished )
		self.connect( self.Verbose_Level_comboBox, SIGNAL( "activated(int)" ), self.setVerboseLevel )
		self.connect( self.Activate_Antialiasing_checkBox, SIGNAL( "stateChanged(int)" ), self.Activate_Antialiasing_checkBox_StateChanged )
		self.connect( self.Activate_OpenGL_checkBox, SIGNAL( "stateChanged(int)" ), self.Activate_OpenGL_checkBox_StateChanged )
		self.connect( self.Toggle_Log_Window_pushButton, SIGNAL( "clicked()" ), self.Toggle_Log_Window_pushButton_OnClicked )
		self.connect( self.Check_For_New_Releases_pushButton, SIGNAL( "clicked()" ), self.Check_For_New_Releases_pushButton_OnClicked )
		self.connect( self.Check_For_New_Releases_checkBox, SIGNAL( "stateChanged(int)" ), self.Check_For_New_Releases_checkBox_StateChanged )
		self.connect( self.Ignore_Missing_Templates_checkBox, SIGNAL( "stateChanged(int)" ), self.Ignore_Missing_Templates_checkBox_StateChanged )
		self.connect( self.Get_Help_pushButton, SIGNAL( "clicked()" ), self.Get_Help_pushButton_OnClicked )
		self.connect( self.Get_Templates_pushButton, SIGNAL( "clicked()" ), self.Get_Latest_Templates_pushButton_OnClicked )

		self.connect( self.sIBL_GUI_tabWidget, SIGNAL( "currentChanged(int)" ), self.sIBL_GUI_tabWidget_OnChanged )

		# Hiding Splashscreen.
		cLogger.debug( "> Hiding SplashScreen." )
		cSpashScreen.setMessage( "sIBL_GUI - " + sIBL_Common_Settings.cReleaseVersion + " | Initialization Finished." )
		cSpashScreen.hide()

		# Wizard If Empty Collection.
		if len( self.cGlobalCollection ) == 0 :
			self.startEmptyCollectionWizard()

		# Online Updater Trigger.
		self.checkForNewReleases()

		cLogger.debug( "> Initialisation Of sIBL_GUI() Class Done." )

	#***************************************************************************************
	#***	Reimplemented Methods
	#***************************************************************************************
	@sIBL_Common.sIBL_Execution_Call
	def closeEvent( self, cEvent ) :
		'''
		This Method Is Called When sIBL_GUI Is Closed.

		@param cEvent: QEvent ( QEvent )
		'''

		cLogger.info( "sIBL_GUI | Closing Interface !" )
		cLogger.info( "-" * sIBL_Common_Settings.cVerboseSeparators )
		cLogger.info( "sIBL_GUI | Session Ended At : " + time.strftime( '%X - %x' ) )
		cLogger.info( "-" * sIBL_Common_Settings.cVerboseSeparators )

		sIBL_Common.sIBL_CloseHandler( cLogger, cConsoleHandler )
		sIBL_Common.sIBL_CloseHandler( cLogger, cFileHandler )

		self.deleteLater()
		cEvent.accept()

	#***************************************************************************************
	#***	Log File Methods
	#***************************************************************************************
	def refreshLogTextEdit( self ) :
		'''
		This Method Refresh The Log Window ( Can't Be Decorated For Recursion Issues ).
		'''

		try :
			cFileSize = os.path.getsize( cSIBL_GUI_LogFile )
			if  cFileSize != self.cLogFileSize :
				self.setLogTextEdit()
				self.cLogFileSize = cFileSize
		except :
			pass

	def setLogTextEdit( self ) :
		'''
		This Method Set The Log Window ( Can't Be Decorated For Recursion Issues ).
		'''

		try :
			cLogFile = open( cSIBL_GUI_LogFile, "r" )
			cLogFileContent = cLogFile.read()

			self.Log_textEdit.setPlainText( QString( cLogFileContent ) )
			self.Log_textEdit.moveCursor( QTextCursor.End )
			self.Log_textEdit.ensureCursorVisible()
		except :
			pass

	# def setLogTextEdit( self ) :
	#	cLogFile = sIBL_Common.sIBL_File( cSIBL_GUI_LogFile )
	#	cLogFileContent = cLogFile.getFileContent()
	#	cLogFile = open( cSIBL_GUI_LogFile, "r" )
	#	cLogFileContent = cLogFile.read()
	#	self.Log_textEdit.setPlainText( QString( cLogFileContent ) )
	#	self.Log_textEdit.moveCursor( QTextCursor.End )
	#	self.Log_textEdit.ensureCursorVisible()

	#***************************************************************************************
	#***	Collection Browser Tab Methods
	#***************************************************************************************
	@sIBL_Common.sIBL_Execution_Call
	def initializeCollectionsRelationships( self ) :
		'''
		This Method Initializes The Collections Browser Tab.
		'''

		self.cGlobalCollection = self.getGlobalCollectionExtended()

		self.cFilteredCollection = deepcopy( self.cGlobalCollection )

		cLogger.debug( "> %s" , "Clearing : Collections_comboBox, Authors_comboBox, Locations_comboBox, Collections_listWidget." )
		self.Collections_comboBox.clear()
		self.Authors_comboBox.clear()
		self.Locations_comboBox.clear()
		self.Collections_listWidget.clear()
		if self.cFilteredCollection is not None :
			cLogger.debug( "> %s" , "Setting : Collections_comboBox, Authors_comboBox, Locations_comboBox, Collections_listWidget." )
			self.setCollectionsComboBox( False )
			self.setAuthorsComboBox( False )
			self.setLocationsComboBox( False )
			self.setCollectionsListWidget()

		cLogger.debug( "> Refreshing WorldMap !" )
		self.emit( SIGNAL( "WorldMap_Refresh()" ) )

	@sIBL_Common.sIBL_Execution_Call
	def setGPSMap( self ) :
		'''
		This Method Initialize The GPS Map.
		'''

		cLogger.debug( "> Re/Initialising WorldMap !" )

		if self.WorldMap_QGraphicsView is not None :
			cLogger.debug( "> Deleting Previous GPS Map Instance : '%s'.", self.WorldMap_QGraphicsView )
			self.WorldMap_QGraphicsView.deleteLater()
			QApplication.sendPostedEvents( self, QEvent.DeferredDelete )

		cWorldMap_Texture_Path = "./Resources/Earth_Map.jpg"
		if os.path.exists( cWorldMap_Texture_Path ) :
			self.WorldMap_QGraphicsView = WorldMap_QGraphicsView( self, cWorldMap_Texture_Path, 670, 320 )
			self.GPS_Map_Page_gridLayout.addWidget( self.WorldMap_QGraphicsView )
		else :
			sIBL_GUI_QWidgets.sIBL_GUI_Message( "Critical", "Critical", cWorldMap_Texture_Path + " Not Found, Aborting Execution !" )
			sIBL_Common.sIBL_Exit( 1, cLogger, ( cConsoleHandler, cFileHandler ) )

	@sIBL_Common.sIBL_Execution_Call
	def setFilterComboBox( self, cComboBox, cFilterType, keepSelection ) :
		'''
		This Method Fills The Filtering Comboboxes

		@param cComboBox: Target Combo Box ( QComboBox )
		@param cFilterType: Current Filter Type ( String )
		@param keepSelection: Restore The Previous Current ComboBox Selection. ( Boolean )
		'''

		if keepSelection :
			cComboBoxSelectedItem = str( cComboBox.currentText() )

		cComboBox.clear()

		cCollectionsList = self.getRequestedCollectionInfosList( cFilterType )
		cCollectionsList.insert( 0, "*" )
		cLogger.debug( "> Inserting '%s' In '%ss_comboBox'.", cCollectionsList, cFilterType )
		cComboBox.insertItems( 0, QStringList( cCollectionsList ) )

		if keepSelection :
			for i in range( cComboBox.count() ) :
				if cComboBoxSelectedItem == cComboBox.itemText( i ) :
					cComboBox.setCurrentIndex( i )
					cLogger.debug( "> Selecting Index '%s' Of '%ss_comboBox'.", i, cFilterType )

	@sIBL_Common.sIBL_Execution_Call
	def setCollectionsComboBox( self, keepSelection ) :
		'''
		This Method Calls The Filling Of Collections Filtering ComboBox.

		@param keepSelection: Restore The Previous Current ComboBox Selection. ( Boolean )
		'''

		self.setFilterComboBox( self.Collections_comboBox, "Collection", keepSelection )

	@sIBL_Common.sIBL_Execution_Call
	def setAuthorsComboBox( self, keepSelection ) :
		'''
		This Method Calls The Filling Of Authors Filtering Combobox.

		@param keepSelection: Restore The Previous Current ComboBox Selection. ( Boolean )
		'''

		self.setFilterComboBox( self.Authors_comboBox, "Author", keepSelection )

	@sIBL_Common.sIBL_Execution_Call
	def setLocationsComboBox( self, keepSelection ) :
		'''
		This Method Calls The Filling Of Location Filtering ComboBox.

		@param keepSelection: Restore The Previous Current ComboBox Selection. ( Boolean )
		'''

		self.setFilterComboBox( self.Locations_comboBox, "Location", keepSelection )

	@sIBL_Common.sIBL_Execution_Call
	def getListWidgetItem( self, cItemName ) :
		'''
		This Method Returns The Current Seeked Collections ListWidget Item.

		@param cItemName: Searched Item In The Collections ListWidget. ( String )
		@return: Return The Searched Item From The Collection. ( QListWidgetItem )
		'''

		cListWidgetItem = self.Collections_listWidget.findItems( QString( cItemName ), Qt.MatchExactly )
		cLogger.debug( "> Curent QListWidget Item : '%s'.", cListWidgetItem )
		return cListWidgetItem[0]

	@sIBL_Common.sIBL_Execution_Call
	def updateFilteredCollectionItems( self ) :
		'''
		This Method Calls The Collections ListWidget Dictionary Update Once Filtered.
		'''

		cLogger.debug( "> %s" , "Starting self.cFilteredCollection Update !" )
		self.cFilteredCollection = deepcopy( self.cGlobalCollection )
		self.popFilteredItems( self.Collections_comboBox, "Collection" )
		self.popFilteredItems( self.Authors_comboBox, "Author" )
		self.popFilteredItems( self.Locations_comboBox, "Location" )

	@sIBL_Common.sIBL_Execution_Call
	def popFilteredItems( self, cComboBox, cFilterType ) :
		'''
		This Method Pops Filtered Items In The Collections ListWidget Dictionary.

		@param cComboBox: Target Combo Box ( QComboBox )
		@param cFilterType: Filter Type ( String )
		'''

		cComboBoxSelectedItem = str( cComboBox.currentText() )

		for sIBL in self.cFilteredCollection.keys() :
			cSIBLAttributes = self.cFilteredCollection[sIBL]
			if cComboBoxSelectedItem != "*" and cComboBoxSelectedItem != cSIBLAttributes[cFilterType] :
				cLogger.debug( "> Removing '%s' From 'self.cFilteredCollection'." , sIBL )
				self.cFilteredCollection.pop( sIBL )
			else:
				cLogger.debug( "> Keeping '%s' In 'self.cFilteredCollection'." , sIBL )

		cLogger.debug( "> %s", "Refreshing WorldMap !" )
		self.emit( SIGNAL( 'WorldMap_Refresh()' ) )

	@sIBL_Common.sIBL_Execution_Call
	def Collections_comboBox_Activated( self, *__None__ ) :
		'''
		This Method Triggers The Collections ListWidget Filtering.
		'''

		self.filterCollectionsListWidget( self.Collections_comboBox, "Collection" )

	@sIBL_Common.sIBL_Execution_Call
	def Authors_comboBox_Activated( self, *__None__ ) :
		'''
		This Method Triggers The Collections ListWidget Filtering.
		'''

		self.filterCollectionsListWidget( self.Authors_comboBox, "Author" )

	@sIBL_Common.sIBL_Execution_Call
	def Locations_comboBox_Activated( self, *__None__ ) :
		'''
		This Method Triggers The Collections ListWidget Filtering.
		'''

		self.filterCollectionsListWidget( self.Locations_comboBox, "Location" )

	@sIBL_Common.sIBL_Execution_Call
	def filterCollectionsListWidget( self, cComboBox, cFilterType ) :
		'''
		This Method Filters The Collections ListWidget.

		@param cComboBox: Target Combo Box ( QComboBox )
		@param cFilterType: Filter Type ( String )
		'''

		cLogger.debug( "> %s" , "Starting Collections_listWidget Filtering !" )
		self.updateFilteredCollectionItems()

		cComboBoxSelectedItem = str( cComboBox.currentText() )

		if cFilterType == "Collection":
			if cComboBoxSelectedItem == "*":
				self.setCollectionsComboBox( True )
			self.setAuthorsComboBox( True )
			self.setLocationsComboBox( True )
		elif cFilterType == "Author":
			self.setCollectionsComboBox( True )
			if cComboBoxSelectedItem == "*":
				self.setAuthorsComboBox( True )
			self.setLocationsComboBox( True )
		elif cFilterType == "Location":
			self.setCollectionsComboBox( True )
			self.setAuthorsComboBox( True )
			if cComboBoxSelectedItem == "*":
				self.setLocationsComboBox( True )

		self.setCollectionsListWidget()
		self.Collections_listWidget.sortItems( Qt.AscendingOrder )

	@sIBL_Common.sIBL_Execution_Call
	def Search_lineEdit_OnTextChanged( self, *__None__ ) :
		'''
		This Method Filters The Collections ListWidget Using The Input Search Text.
		'''

		# Reset Filters.
		self.setCollectionsComboBox( False )
		self.setAuthorsComboBox( False )
		self.setLocationsComboBox( False )

		self.cFilteredCollection = deepcopy( self.cGlobalCollection )

		for sIBL in self.cFilteredCollection.keys() :
			cSIBLPop = True
			cSIBLAttributes = self.cFilteredCollection[sIBL]
			for cSIBLAttribute in cSIBLAttributes.keys() :
				if str( self.Search_lineEdit.text() ).lower() in str( cSIBLAttributes[cSIBLAttribute] ).lower() :
					cSIBLPop = False
					break
			if cSIBLPop :
				cLogger.debug( "> Removing '%s' From 'self.cFilteredCollection'." , sIBL )
				self.cFilteredCollection.pop( sIBL )
			else:
				cLogger.debug( "> Keeping '%s' In 'self.cFilteredCollection'." , sIBL )

		self.setCollectionsListWidget()
		self.Collections_listWidget.sortItems( Qt.AscendingOrder )

		cLogger.debug( "> %s", "Refreshing WorldMap !" )
		self.emit( SIGNAL( 'WorldMap_Refresh()' ) )

	@sIBL_Common.sIBL_Execution_Call
	def setCollectionsListWidget( self ) :
		'''
		This Method Sets The Collections ListWidget.
		'''

		self.Collections_listWidget.clear()

		for sIBL in self.cFilteredCollection.keys() :
			cSIBLAttributes = self.cFilteredCollection[sIBL]
			cItem = QListWidgetItem( QString( cSIBLAttributes["sIBL Name"] ) )

			# sIBL V2 Format Support.
			if "Time" in cSIBLAttributes.keys() and "Date" in cSIBLAttributes.keys():
				cShotDateString = "Shot Date : " + self.getFormatedShotDate( cSIBLAttributes["Date"], cSIBLAttributes["Time"] )
			else :
				cShotDateString = ""

			cToolTip = QString( "<p><b>" + cSIBLAttributes["sIBL Name"] + "</b></p>" + "<p>" + "Author : " + cSIBLAttributes["Author"] + "<br>" + "Location : " + cSIBLAttributes["Location"] + "<br>" + cShotDateString + "<br>" + "Comment : " + cSIBLAttributes["Comment"] + "</p>" )

			cItem.setToolTip( cToolTip )

			if re.search( "\.[jJ][pP][gG]", cSIBLAttributes["Icon Path"] ) or re.search( "\.[jJ][pP][eE][gG]", cSIBLAttributes["Icon Path"] ) or re.search( "\.[pP][nN][gG]", cSIBLAttributes["Icon Path"] ) :
				cIcon = QIcon( QPixmap( cSIBLAttributes["Icon Path"] ) )
			elif re.search( "\.[tT][gG][aA]", cSIBLAttributes["Icon Path"] ) or re.search( "\.[tT][iI][fF]", cSIBLAttributes["Icon Path"] ) or re.search( "\.[tT][iI][fF][fF]", cSIBLAttributes["Icon Path"] ) :
				cIcon = QIcon( ":/sIBL_GUI/Resources/Thumbnails_Format_Not_Supported_Yet.png" )
			else :
				cIcon = QIcon( ":/sIBL_GUI/Resources/Thumbnails_Format_Not_Supported_Yet.png" )

			cItem.setIcon( cIcon )
			cLogger.debug( "> Adding '%s' To 'self.Collections_listWidget'.", cSIBLAttributes["sIBL Name"] )
			self.Collections_listWidget.addItem( cItem )

		self.Collections_listWidget.sortItems( Qt.AscendingOrder )

	#***************************************************************************************
	#***	Import Tab Methods.
	#***************************************************************************************
	@sIBL_Common.sIBL_Execution_Call
	def initializeLineAndTextEditsPalette( self ) :
		'''
		This Method Sets The Line Edits Background Color.
		'''

		cPalette = QPalette()
		cPalette.setColor( QPalette.Base, Qt.transparent )

		for cTextEdit in self.cTextEdits_List :
			cTextEdit.setPalette( cPalette )

	@sIBL_Common.sIBL_Execution_Call
	def initializeTemplatesRelationships( self ) :
		'''
		This Method Initializes The Import Tab.
		'''

		cLogger.debug( "> Initializing : '%s'.", "self.cGlobalTemplates" )
		self.cGlobalTemplates = self.getGlobalTemplatesExtended()
		self.setSoftwareComboBox()
		self.setTemplateComboBox()

	@sIBL_Common.sIBL_Execution_Call
	def getGlobalTemplates( self ) :
		'''
		This Method Gets The Templates List From The Templates Directory.

		@return: Templates From The Templates Directory. ( Dictionary )
		'''

		cLogger.info( "sIBL_GUI | Retrieving Templates !" )

		cTemplates = sIBL_Recursive_Walker.sIBL_Recursive_Walker( os.path.abspath( str( self.Templates_Path_lineEdit.text() ) ).replace( "\\", "/" ) + "/" )
		cTemplatesList = cTemplates.recursiveWalker( ".sIBLT" )

		cLogger.info( "sIBL_GUI | Templates List : '%s'.", cTemplatesList )

		return cTemplatesList

	@sIBL_Common.sIBL_Execution_Call
	def getGlobalTemplatesExtended( self ) :
		'''
		This Method Gathers Templates Informations And Extend The Current Template Dictionary.

		@return: Extended Templates Dictionary. ( Dictionary )
		'''

		cGlobalTemplates = self.getGlobalTemplates()
		cGlobalTemplatesExtend = None

		if cGlobalTemplates is not None :
			cGlobalTemplatesExtend = {}
			for cTemplate in cGlobalTemplates :
				cTemplateAttributes = {}
				cTemplateFile = sIBL_Parser.sIBL_Parser( cGlobalTemplates[cTemplate] )

				cTemplateAttributes["Template Name"] = cTemplate
				cTemplateAttributes["Template Software"] = sIBL_Parser.sIBL_GetExtraAttributeComponents( cTemplateFile.getAttributeValue( "Template", "Software" ), "Value" )
				cTemplateAttributes["Template Release"] = sIBL_Parser.sIBL_GetExtraAttributeComponents( cTemplateFile.getAttributeValue( "Template", "Release" ), "Value" )
				cTemplateAttributes["Template Path"] = cGlobalTemplates[cTemplate]

				cGlobalTemplatesExtend[cTemplate] = cTemplateAttributes
			cLogger.debug( "> Global Templates Extended : '%s'.", cGlobalTemplatesExtend )
			return cGlobalTemplatesExtend
		else :
			cLogger.error( "Exception In sIBL_GUI.getGlobalTemplatesExtended() Method | '%s'", "No Global Templates Extended Defined, Returning 'None' !" )
			return cGlobalTemplatesExtend

	@sIBL_Common.sIBL_Execution_Call
	def setSoftwareComboBox( self ) :
		'''
		This Method Fills The Softwares ComboBox.
		'''

		self.Software_comboBox.clear()

		cSoftwareList = self.getRequestedTemplatesInfosList( "Template Software" )
		cLogger.debug( "> Inserting '%s' In 'Software_comboBox'.", cSoftwareList )

		self.Software_comboBox.insertItems( 0, QStringList( cSoftwareList ) )

	@sIBL_Common.sIBL_Execution_Call
	def setTemplateComboBox( self, *__None__ ) :
		'''
		This Method Fills The Templates ComboBox.
		'''

		self.Template_comboBox.clear()

		cTemplateComboBoxList = []
		for cTemplate in self.cGlobalTemplates :
			cTemplateAttributes = self.cGlobalTemplates[cTemplate]
			if cTemplateAttributes["Template Software"] == self.Software_comboBox.currentText() :
				cTemplateComboBoxList.append( cTemplate )

		cLogger.debug( "> Inserting '%s' In 'Template_comboBox'.", cTemplateComboBoxList )
		self.Template_comboBox.insertItems( 0, QStringList( cTemplateComboBoxList ) )
		self.setTemplateOptionsAndInfosWidgets()

	@sIBL_Common.sIBL_Execution_Call
	def setOptionsToolBox( self, cTemplateFile, cSection, cTableWidget ) :
		'''
		This Method Defines And Sets Options TableWidgets.

		@param cTemplateFile: Current Template File. ( sIBL_File )
		@param cSection: Seeked Section. ( String )
		@param cTableWidget: Current Table Widget. ( QTableWidget )
		'''

		cTableWidget.hide()

		cFileTemplateAttributes = cTemplateFile.getSectionAttributes( cSection )
		# cTableWidget.clear()
		cTableWidget.setRowCount( len( cFileTemplateAttributes ) )
		cTableWidget.setColumnCount( 2 )
		cTableWidget.hideColumn( 0 )
		cTableWidget.horizontalHeader().setStretchLastSection( True )
		cTableWidget.setHorizontalHeaderLabels( ["Attribute", "Value"] )
		cTableWidget.horizontalHeader().hide()

		cPalette = QPalette()
		cPalette.setColor( QPalette.Base, Qt.transparent )
		cTableWidget.setPalette( cPalette )

		cVerticalHeaderLabels = []
		for row, cAttribute in enumerate( cFileTemplateAttributes.keys() ) :
			cLogger.debug( "> Current Attribute : '%s'.", cAttribute )
			cAttributeName = sIBL_Parser.sIBL_GetExtraAttributeComponents( cFileTemplateAttributes[cAttribute], "Attribute Name" )
			if cAttributeName is not None :
				cVerticalHeaderLabels.append( cAttributeName )
			else:
				# No Nice Name Provided.
				cVerticalHeaderLabels.append( self.getNiceName( cAttribute ) )

			cItem = QTableWidgetItem( QString( cAttribute ) )
			cItem.setTextAlignment( Qt.AlignCenter )
			cLogger.debug( "> Setting Item In Column '0' : '%s'.", cItem.text() )
			cTableWidget.setItem( row, 0, cItem )

			cAttributeType = sIBL_Parser.sIBL_GetExtraAttributeComponents( cFileTemplateAttributes[cAttribute], "Type" )
			if cAttributeType == "Boolean" :
				cAttributeValue = sIBL_Parser.sIBL_GetExtraAttributeComponents( cFileTemplateAttributes[cAttribute], "Value" )

				cColors = ( self.greenColor, self.redColor )
				if cAttributeValue == "1":
					cItem = sIBL_GUI_QWidgets.Variable_QPushButton( True, cColors, ( "True", "False" ) )
					cTableWidget.setCellWidget( row, 1, cItem )
					cItem.setChecked( True )
				else :
					cItem = sIBL_GUI_QWidgets.Variable_QPushButton( False, cColors, ( "True", "False" ) )
					cTableWidget.setCellWidget( row, 1, cItem )
					cItem.setChecked( False )

			elif cAttributeType == "Float" :
				cItem = QDoubleSpinBox()
				cItem.setMinimum( 0 )
				cItem.setMaximum( 65535 )
				cTableWidget.setCellWidget( row, 1, cItem )
				cItem.setValue( float ( sIBL_Parser.sIBL_GetExtraAttributeComponents( cFileTemplateAttributes[cAttribute], "Value" ) ) )
			else :
				cItem = QTableWidgetItem( QString( sIBL_Parser.sIBL_GetExtraAttributeComponents( cFileTemplateAttributes[cAttribute], "Value" ) ) )
				cItem.setTextAlignment( Qt.AlignCenter )
				cLogger.debug( "> Setting Item In Column '1' : '%s'.", cItem.text() )
				cTableWidget.setItem( row, 1, cItem )

		cTableWidget.setVerticalHeaderLabels ( cVerticalHeaderLabels )

		cTableWidget.show()

	@sIBL_Common.sIBL_Execution_Call
	def setPortWidgetsVisibility( self, cVisibilityState ) :
		'''
		This Method Hide/UnHide Remote Connections Widgets Depending The Current Remote Connection Options

		@param cVisibilityState: Current Port Widgets Visibility State. ( Boolean )
		'''

		if cVisibilityState is True:
			cLogger.debug( "> %s", "Showing Remote Connection Options !" )
			self.Remote_Connection_Options_frame.show()
		else:
			cLogger.debug( "> %s", "Hiding Remote Connection Options !" )
			self.Remote_Connection_Options_frame.hide()

	@sIBL_Common.sIBL_Execution_Call
	def resetQTableWidget( self, cTableWidget ) :
		'''
		This Method Reset The Provided Table Widget.

		@param cTableWidget: Current Table Widget ( QTableWidget )
		'''

		cLogger.debug( "> Clearing '%s' QTableWidget.", cTableWidget )
		cTableWidget.clear()
		cTableWidget.setRowCount( 0 )
		cTableWidget.setColumnCount( 0 )

	@sIBL_Common.sIBL_Execution_Call
	def setTemplateOptionsAndInfosWidgets( self, *__None__ ) :
		'''
		This Method Sets Templates Widgets And Other Stuff.
		'''

		self.resetQTableWidget( self.Common_Attributes_tableWidget )
		self.resetQTableWidget( self.Additional_Attributes_tableWidget )

		for cTemplate in self.cGlobalTemplates :
			try :
				cTemplateAttributes = self.cGlobalTemplates[cTemplate]
				if cTemplateAttributes["Template Name"] == self.Template_comboBox.currentText() :
					cTemplateFile = sIBL_Parser.sIBL_Parser( cTemplateAttributes["Template Path"] )
					cFileTemplateAttributes = cTemplateFile.getSectionAttributes( "Template" )
					cLogger.debug( "> Setting Template Infos Widgets : '%s'.", "Release_Set_label, Software_Set_groupBox, Software_Version_label, Template_Author_Set_label, Template_Email_Set_label, Loader_Script_Set_label" )
					self.Release_Set_label.setText( QString( sIBL_Parser.sIBL_GetExtraAttributeComponents( cFileTemplateAttributes["Template|Release"], "Value" ) ) )
					self.Software_Set_groupBox.setTitle( QString( sIBL_Parser.sIBL_GetExtraAttributeComponents( cFileTemplateAttributes["Template|Software"], "Value" ) ) )
					self.Software_Version_label.setText( QString( sIBL_Parser.sIBL_GetExtraAttributeComponents( cFileTemplateAttributes["Template|Version"], "Value" ) ) )
					self.Template_Author_Set_label.setText( QString( "<a href = \"mailto:" + sIBL_Parser.sIBL_GetExtraAttributeComponents( cFileTemplateAttributes["Template|EMail"], "Value" ) + "\"><span style=\" text-decoration: underline; color:#000000;\">" + sIBL_Parser.sIBL_GetExtraAttributeComponents( cFileTemplateAttributes["Template|Author"], "Value" ) + "</span></a>" ) )
					self.Loader_Script_Set_label.setText( QString( sIBL_Parser.sIBL_GetExtraAttributeComponents( cFileTemplateAttributes["Template|OutputScript"], "Value" ) ) )
					self.Template_Comment_textEdit.setText( QString( sIBL_Parser.sIBL_GetExtraAttributeComponents( cFileTemplateAttributes["Template|Comment"], "Value" ) ) )

					# Common And Additional Attributes tableWidget Set.
					cLogger.debug( "> %s", "Setting Common And Additional Attributes Options" )
					self.setOptionsToolBox( cTemplateFile, "Common Attributes", self.Common_Attributes_tableWidget )
					self.setOptionsToolBox( cTemplateFile, "Additional Attributes", self.Additional_Attributes_tableWidget )

					# Enabling/Disabling Remote Connection.
					cFileTemplateSections = cTemplateFile.getSections()
					if "Remote Connection" in cFileTemplateSections.keys() :
						self.Remote_Connection_groupBox.show()
						cRemoteConnectionAttributes = cTemplateFile.getSectionAttributes( "Remote Connection" )
						cConnectionType = sIBL_Parser.sIBL_GetExtraAttributeComponents( cRemoteConnectionAttributes["Remote Connection|ConnectionType"], "Value" )
						if cConnectionType == "Socket":
							self.Software_Port_spinBox.setValue( int( sIBL_Parser.sIBL_GetExtraAttributeComponents( cRemoteConnectionAttributes["Remote Connection|DefaultPort"], "Value" ) ) )
							self.Address_lineEdit.setText( QString( sIBL_Parser.sIBL_GetExtraAttributeComponents( cRemoteConnectionAttributes["Remote Connection|DefaultAddress"], "Value" ) ) )
							self.setPortWidgetsVisibility( True )
						else :
							self.setPortWidgetsVisibility( False )

					else:
						self.setPortWidgetsVisibility( False )
						self.Remote_Connection_groupBox.hide()
			except :
				sIBL_GUI_QWidgets.sIBL_GUI_Message( "Warning", "Warning", "'" + cTemplate + "' File Seems To Be Corrupted And Will Be Ignored !" )

	@sIBL_Common.sIBL_Execution_Call
	def setEditedSIBLInfos( self ) :
		'''
		This Method Sets sIBL Widgets Informations.
		'''

		if self.cEditedIBL is not None:
			cSIBL = self.cGlobalCollection[self.cEditedIBL]
			# Special Case Where The sIBL Has Changed Of Name During An Edit In sIBLedit.
			cLogger.debug( "> Setting sIBL Infos Widgets : '%s'.", "sIBL_Set_groupBox, Preview_label, Comment_label, sIBL_Location_Set_label, sIBL_Author_Set_label" )
			self.sIBL_Set_groupBox.setTitle( QString( cSIBL["sIBL Name"] ) )

			if re.search( "\.[jJ][pP][gG]", cSIBL["Icon Path"] ) or re.search( "\.[jJ][pP][eE][gG]", cSIBL["Icon Path"] ) or re.search( "\.[pP][nN][gG]", cSIBL["Icon Path"] ) :
				self.Preview_label.setPixmap( QPixmap( cSIBL["Icon Path"] ) )
			elif re.search( "\.[tT][gG][aA]", cSIBL["Icon Path"] ) or re.search( "\.[tT][iI][fF]", cSIBL["Icon Path"] ) or re.search( "\.[tT][iI][fF][fF]", cSIBL["Icon Path"] ) :
				self.Preview_label.setPixmap( QPixmap( ":/sIBL_GUI/Resources/Thumbnails_Format_Not_Supported_Yet.png" ) )
			else :
				cIcon = QIcon( ":/sIBL_GUI/Resources/Thumbnails_Format_Not_Supported_Yet.png" )

			self.Comment_textEdit.setText( QString( cSIBL["Comment"] ) )
			self.sIBL_Location_Set_label.setText( QString( cSIBL["Location"] ) )
			self.sIBL_Author_Set_label.setText( QString( cSIBL["Author"] ) )

			# sIBL V2 Format Support.
			if "Link" in cSIBL.keys():
				self.sIBL_Author_Set_label.setText( QString( "<a href = \"" + cSIBL["Link"] + "\"><span style=\" text-decoration: underline; color:#000000;\">" + cSIBL["Author"] + "</span></a>" ) )

			if "Date" in cSIBL.keys():
				self.Shot_Date_groupBox.show()
				self.sIBL_Date_Set_label.setText( QString( self.getFormatedShotDate( cSIBL["Date"], cSIBL["Time"] ) ) )
			else:
				self.Shot_Date_groupBox.hide()
		else:
			sIBL_GUI_QWidgets.sIBL_GUI_Message( "Error", "Error", "Current sIBL File Does'nt Exist Anymore Or It's Name Changed, Please Choose Another One !" )
			self.sIBL_GUI_tabWidget.setCurrentIndex( 0 )

	@sIBL_Common.sIBL_Execution_Call
	def getSIBLFromSIBLName( self, cName ) :
		'''
		This Method Gets The Current sIBL His Name.

		@param cName: Current sIBL Name. ( String )
		@return: Seeked SIBL. ( String )
		'''

		for sIBL in self.cGlobalCollection.keys() :
				cSIBLAttributes = self.cGlobalCollection[sIBL]
				if cSIBLAttributes["sIBL Name"] == cName :
					cLogger.debug( "> sIBL Name '%s' Owner Is : '%s'.", cName, sIBL )
					return sIBL

		cLogger.debug( "> No sIBL  Owner For : '%s'.", cName )
		return None

	@sIBL_Common.sIBL_Execution_Call
	def sendListWidgetItemToImportTab( self, *__None__ ) :
		'''
		This Method Sends Double Clicked sIBL To The Import Tab.
		'''

		self.sIBL_GUI_tabWidget.setCurrentIndex( 1 )
		cSelectedQListWidgetItems = self.Collections_listWidget.selectedItems()
		cLogger.info( "sIBL_GUI | Starting '%s' Import !", cSelectedQListWidgetItems[0].text() )
		self.cEditedIBL = self.getSIBLFromSIBLName( cSelectedQListWidgetItems[0].text() )

		self.setEditedSIBLInfos()

	@sIBL_Common.sIBL_Execution_Call
	def getSIBLPath( self ) :
		'''
		This Method Gets The Current sIBL From Widget Title.
		'''

		cSIBLAttributes = self.cGlobalCollection[self.cEditedIBL]
		cLogger.debug( "> Current Imported sIBL Path : '%s'.", cSIBLAttributes["sIBL Path"] )
		return cSIBLAttributes["sIBL Path"]

	@sIBL_Common.sIBL_Execution_Call
	def getTemplateFilePathFromComboBox( self ) :
		'''
		This Method Gets The Current Template Path From The Template ComboBox.

		@return: Current Template Absolute Path. ( String )
		'''

		for cTemplate in self.cGlobalTemplates.keys() :
			cTemplateAttributes = self.cGlobalTemplates[cTemplate]
			if cTemplateAttributes["Template Name"] == self.Template_comboBox.currentText() :
				cTemplate = cTemplateAttributes
				break
		cLogger.debug( "> Current Template Path : '%s'.", cTemplate["Template Path"] )
		return cTemplate["Template Path"]

	@sIBL_Common.sIBL_Execution_Call
	def getWidgetType( self, cWidget ) :
		'''
		This Method Returns Current Widget Type.

		@return: Current Widget Type. ( String )
		'''

		cWidgetType = cWidget.__class__.__name__
		cLogger.debug( "> '%s' Type : '%s'.", cWidget, cWidgetType )
		return cWidgetType

	@sIBL_Common.sIBL_Execution_Call
	def addKeysToOverrideString( self, cOverrideKeys, cTableWidget ) :
		'''
		This Method Builds The Override Keys String.

		@param cOverrideKeys: Build In Progress Override Keys Argument. ( String )
		@param cTableWidget: Current Table Widget. ( QTableWidget )
		@return: Argument Override Keys. ( String )
		'''

		for row in range( cTableWidget.rowCount() ) :
			cWidgetType = self.getWidgetType( cTableWidget.cellWidget( row, 1 ) )
			if cWidgetType == "Variable_QPushButton":
				cTableWidget.cellWidget( row, 1 )
				if cTableWidget.cellWidget( row, 1 ).text() == "True" :
					cKeyValue = "1"
				else:
					cKeyValue = "0"
				cOverrideKeys = cOverrideKeys + str( cTableWidget.item( row, 0 ).text() ) + " = " + cKeyValue + ", "
			elif cWidgetType == "QDoubleSpinBox":
				cOverrideKeys = cOverrideKeys + str( cTableWidget.item( row, 0 ).text() ) + " = " + str( cTableWidget.cellWidget( row, 1 ).value() ) + ", "
			else:
				cOverrideKeys = cOverrideKeys + str( cTableWidget.item( row, 0 ).text() ) + " = " + str( cTableWidget.item( row, 1 ).text() ) + ", "
		cLogger.debug( "> Override Keys : '%s'.", cOverrideKeys )
		return cOverrideKeys

	@sIBL_Common.sIBL_Execution_Call
	def setLoaderScript( self ) :
		'''
		This Method Sets The Loader Script.

		@return: Execution State ( Boolean )
		'''
		if os.path.exists( os.path.abspath( str( self.sIBL_Framework_Path_lineEdit.text() ) ) ) and  "sIBL_Framework" in self.sIBL_Framework_Path_lineEdit.text() :
			if self.cGlobalTemplates is not None :
				if self.sIBL_Set_groupBox.title() != "Preview" :
					cLogger.debug( "> %s", "Gathering Informations For sIBL_Framework Launch." )
					cSIBLPath = self.getSIBLPath()

					# Getting Template File Path From Template_comboBox.
					cTemplatePath = self.getTemplateFilePathFromComboBox()

					# Building Argument Keys For The Output Script.
					cOverrideKeys = ""

					cOverrideKeys = self.addKeysToOverrideString( cOverrideKeys, self.Common_Attributes_tableWidget )
					cOverrideKeys = self.addKeysToOverrideString( cOverrideKeys, self.Additional_Attributes_tableWidget )

					# Removing The Last ", ".
					cOverrideKeys = cOverrideKeys[0:-2]

					cSIBL_FrameworkArguments = QStringList( ["-i", cSIBLPath, "-t", cTemplatePath, "-k", cOverrideKeys, "-v", str ( int( self.Verbose_Level_comboBox.currentIndex() ) ) ] )
					cSIBL_FrameworkProcess = QProcess()
					# Forwarded Channel Seem To Not Work :|.
					cSIBL_FrameworkProcess.ProcessChannelMode( QProcess.MergedChannels )

					# Providing A Debug Line.
					cArgumentLine = ""
					for cCounter, cArgument in enumerate( cSIBL_FrameworkArguments ) :
						if cCounter % 2 == 0 :
							cArgumentLine = cArgumentLine + " " + str( cArgument )
						else :
							cArgumentLine = cArgumentLine + " " + "\"" + str( cArgument ) + "\""

					cLogger.info( "Launching sIBL_Framework With Arguments : '%s'.", cArgumentLine )
					cLogger.info( "-" * sIBL_Common_Settings.cVerboseSeparators )
					cLogger.info( "sIBL_GUI | Starting sIBL_Framework !" )
					cLogger.info( "-" * sIBL_Common_Settings.cVerboseSeparators )
					cSIBL_FrameworkProcess.start( os.path.abspath( str( self.sIBL_Framework_Path_lineEdit.text() ) ), cSIBL_FrameworkArguments )
					cSIBL_FrameworkProcess.waitForFinished( 5000 )
					cSIBL_FrameworkProcess.close()

					# Merging sIBL_Framework Verbose
					if platform.system() != "Darwin":
						cLogFilePath = os.path.join( os.path.dirname( os.path.abspath( str( self.sIBL_Framework_Path_lineEdit.text() ) ) ), sIBL_Common_Settings.cSIBL_Framework_LogFile )
					else :
						csIBL_Framework_AbsolutePath = os.path.abspath( str( self.sIBL_Framework_Path_lineEdit.text() ) )
						cPath_Tokens = csIBL_Framework_AbsolutePath.partition( ".app" )
						cLogFilePath = cPath_Tokens[0] + cPath_Tokens[1] + "/Contents/Resources/" + sIBL_Common_Settings.cSIBL_Framework_LogFile

					if os.path.exists( cLogFilePath ):
						cLogFile = sIBL_Common.sIBL_File( cLogFilePath )
						cLogFileContent = cLogFile.getFileContent( asString = True )
						cLogger.info( cLogFileContent[11:-1] )
					else :
						sIBL_GUI_QWidgets.sIBL_GUI_Message( "Error", "Error", "sIBL_Framework Log File Not Found, Loader Script Output Failed !" )
						return False

					cLogger.info( "-" * sIBL_Common_Settings.cVerboseSeparators )
					cLogger.info( "sIBL_GUI | Exiting sIBL_Framework !" )
					cLogger.info( "-" * sIBL_Common_Settings.cVerboseSeparators )

					if cSIBL_FrameworkProcess.exitCode() == 0 :
						sIBL_GUI_QWidgets.sIBL_GUI_Message( "Information", "Information", "Loader Script Output Done !" )
						return True
					else :
						sIBL_GUI_QWidgets.sIBL_GUI_Message( "Error", "Error", "Loader Script Failed !" )
						return False
				else :
					sIBL_GUI_QWidgets.sIBL_GUI_Message( "Warning", "Warning", "Please Select An sIBL File In The Collection Browser !" )
					self.sIBL_GUI_tabWidget.setCurrentIndex( 0 )
					return False
			else :
				sIBL_GUI_QWidgets.sIBL_GUI_Message( "Warning", "Warning", "Please Select A Valid Template Directory In Preferences Tab !" )
				self.sIBL_GUI_tabWidget.setCurrentIndex( 2 )
				self.Preferences_toolBox.setCurrentIndex( 0 )

				return False
		else :
			sIBL_GUI_QWidgets.sIBL_GUI_Message( "Warning", "Warning", "Please Select An Existing sIBL_Framework Executable !" )
			self.sIBL_GUI_tabWidget.setCurrentIndex( 2 )
			self.Preferences_toolBox.setCurrentIndex( 0 )
			return False

	@sIBL_Common.sIBL_Execution_Call
	def Output_Loader_Script_pushButton_OnClicked( self ) :
		'''
		This Method Triggers Loader Script Set.
		'''
		cEnvVariable = sIBL_Common.sIBL_GetTemporarySystemPath()
		if cEnvVariable is not None :
			self.setLoaderScript()
		else:
			self.setTemporaryVariableErrorMessage()

	@sIBL_Common.sIBL_Execution_Call
	def Open_Templates_Folder_pushButton_OnClicked( self ) :
		'''
		This Method Opens Templates Folder.
		'''

		if self.Templates_Path_lineEdit.text() != "":
			cPath = os.path.abspath( str( self.Templates_Path_lineEdit.text() ) )
			self.exploreProvidedFolder( "Opening Current Templates Folder With", cPath )
		else :
			sIBL_GUI_QWidgets.sIBL_GUI_Message( "Warning", "Warning", "Please Select A Valid Template Directory In Preferences Tab !" )
			self.sIBL_GUI_tabWidget.setCurrentIndex( 2 )
			self.Preferences_toolBox.setCurrentIndex( 0 )

	@sIBL_Common.sIBL_Execution_Call
	def Edit_Current_Template_pushButton_OnClicked( self ) :
		'''
		This Method Sends Current Template To Default / User Defined Text Editor.
		'''

		if self.cGlobalTemplates is not None :
			if platform.system() == "Windows" or platform.system() == "Microsoft":
				cTemplatePath = os.path.abspath( self.getTemplateFilePathFromComboBox().replace( "/" , "\\" ) + "\\" )
				if str( self.Custom_Text_Editor_Path_lineEdit.text() ) != "" :
					cLogger.info( "sIBL_GUI | Launching Custom Text Editor On : '%s'.", cTemplatePath )
					cEditCommand = "\"" + str( self.Custom_Text_Editor_Path_lineEdit.text() ) + "\"" + " \"" + cTemplatePath + "\""
				else:
					cLogger.info( "sIBL_GUI | Launching 'Notepad.exe' On : '%s'.", cTemplatePath )
					cEditCommand = "notepad.exe " + " \"" + cTemplatePath + "\""

				cLogger.debug( "> Current Edit Command : '%s'.", cEditCommand )
				cEditProcess = QProcess()
				cEditProcess.startDetached( cEditCommand )

			elif platform.system() == "Linux":
				cTemplatePath = os.path.abspath( self.getTemplateFilePathFromComboBox() )

				if str( self.Custom_Text_Editor_Path_lineEdit.text() ) != "" :
					cLogger.info( "sIBL_GUI | Launching Custom Text Editor On : '%s'.", cTemplatePath )
					cEditCommand = "\"" + str( self.Custom_Text_Editor_Path_lineEdit.text() ) + "\"" + " \"" + cTemplatePath + "\""
				else:
					cPathVariable = sIBL_Common.sIBL_EnvironmentVariables( "PATH" )
					cPaths = cPathVariable.getPath()
					cPathsTokens = cPaths["PATH"].split( ":" )

					cEditCommand = None
					cEditorFound = None

					for cTextEditor in sIBL_GUI_Settings.cLinuxTextEditorsList :
						if not cEditorFound :
							for cPath in cPathsTokens:
								if os.path.exists( os.path.join( cPath, cTextEditor ) ) :
									cLogger.info( "sIBL_GUI | Launching '%s' On : '%s'.", cTextEditor, cTemplatePath )
									cEditCommand = os.path.join( cPath, cTextEditor ) + " \"" + cTemplatePath + "\""
									cEditorFound = True
									break
						else :
							break

				if cEditCommand is not None :
					cLogger.debug( "> Current Edit Command : '%s'.", cEditCommand )
					cEditProcess = QProcess()
					cEditProcess.startDetached( cEditCommand )
				else :
					sIBL_GUI_QWidgets.sIBL_GUI_Message( "Warning", "Warning", "Please Select A Custom Text Editor In Preferences Tab !" )
					self.sIBL_GUI_tabWidget.setCurrentIndex( 2 )
					self.Preferences_toolBox.setCurrentIndex( 0 )

			elif platform.system() == "Darwin" :
				cTemplatePath = os.path.abspath( self.getTemplateFilePathFromComboBox() )
				if str( self.Custom_Text_Editor_Path_lineEdit.text() ) != "" :
					cLogger.info( "sIBL_GUI | Launching Custom Text Editor On : '%s'.", cTemplatePath )
					cEditCommand = "\"" + str( self.Custom_Text_Editor_Path_lineEdit.text() ) + "\"" + " \"" + cTemplatePath + "\""
				else:
					cLogger.info( "sIBL_GUI | Launching 'TextEdit' On : '%s'.", cTemplatePath )
					cEditCommand = "/Applications/TextEdit.app/Contents/MacOS/TextEdit " + " \"" + cTemplatePath + "\""

				cLogger.debug( "> Current Edit Command : '%s'.", cEditCommand )
				cEditProcess = QProcess()
				cEditProcess.startDetached( cEditCommand )
		else :
			sIBL_GUI_QWidgets.sIBL_GUI_Message( "Warning", "Warning", "Please Select A Valid Template Directory In Preferences Tab !" )
			self.sIBL_GUI_tabWidget.setCurrentIndex( 2 )
			self.Preferences_toolBox.setCurrentIndex( 0 )

	@sIBL_Common.sIBL_Execution_Call
	def Refresh_sIBL_File_pushButton_OnClicked( self ) :
		'''
		This Method Triggers Current Imported sIBL File Reload In The Import Tab.
		'''

		cLogger.debug( "> Current sIBL : '%s'.", self.cEditedIBL )
		self.initializeCollectionsRelationships()

		self.setEditedSIBLInfos()

	@sIBL_Common.sIBL_Execution_Call
	def Edit_In_sIBL_Edit_pushButton_OnClicked( self ) :
		'''
		This Method Sends Current sIBL To sIBLedit.
		'''

		if self.sIBL_Set_groupBox.title() != "Preview" :
			cSIBLPath = self.getSIBLPath()
			if self.sIBLedit_Path_lineEdit.text() != "" :
				cSIBLEditPath = os.path.abspath( str( self.sIBLedit_Path_lineEdit.text() ) )
				if platform.system() == "Windows" or platform.system() == "Microsoft" or platform.system() == "Linux":
						cLogger.info( "sIBL_GUI | Editing Current sIBL, Launching : '%s'.", cSIBLEditPath + " " + cSIBLPath )
						cSIBLeditProcess = QProcess()
						cSIBLeditProcess.startDetached( "\"" + cSIBLEditPath + "\"" + " " + "\"" + cSIBLPath + "\"" )
			else :
				sIBL_GUI_QWidgets.sIBL_GUI_Message( "Warning", "Warning", "Please Choose An sIBL Edit Executable !" )
				self.sIBL_GUI_tabWidget.setCurrentIndex( 2 )
				self.Preferences_toolBox.setCurrentIndex( 0 )
		else :
			sIBL_GUI_QWidgets.sIBL_GUI_Message( "Warning", "Warning", "Please Select An sIBL File In The Collection Browser !" )
			self.sIBL_GUI_tabWidget.setCurrentIndex( 0 )

	@sIBL_Common.sIBL_Execution_Call
	def Open_sIBL_Folder_pushButton_OnClicked( self ) :
		'''
		This Method Opens Current sIBL Folder.
		'''

		if self.sIBL_Set_groupBox.title() != "Preview" :
			cSIBLPath = self.getSIBLPath()
			cPath = os.path.dirname( cSIBLPath )
			self.exploreProvidedFolder( "Opening Current sIBL Folder With", cPath )
		else :
			sIBL_GUI_QWidgets.sIBL_GUI_Message( "Warning", "Warning", "Please Select An sIBL File In The Collection Browser !" )
			self.sIBL_GUI_tabWidget.setCurrentIndex( 0 )

	@sIBL_Common.sIBL_Execution_Call
	def setTemporaryVariableErrorMessage( self ) :
		'''
		This Method Defines Temporary Variable Error Messages.
		'''

		if platform.system() == "Windows" or platform.system() == "Microsoft":
			sIBL_GUI_QWidgets.sIBL_GUI_Message( "Error", "Error", "Your System Doesn't Have A 'TMP' Environment Variable Defined !" )
		elif platform.system() == "Linux" or platform.system() == "Darwin":
			sIBL_GUI_QWidgets.sIBL_GUI_Message( "Error", "Error", "Your System Doesn't Have A 'TMPDIR' Environment Variable Defined !" )

	@sIBL_Common.sIBL_Execution_Call
	def exploreProvidedFolder( self, cMessage, cFolderPath ) :
		'''
		This Method Provides Folder Browsing Capability.

		@param cMessage: Current Debug Displayed Message. ( String )
		@param cFolderPath: Folder Path To Be Browser ( String )
		'''

		if platform.system() == "Windows" or platform.system() == "Microsoft":
			cFolderPath = cFolderPath.replace( "/", "\\" )
			if str( self.Custom_File_Browser_Path_lineEdit.text() ) != "" :
				cLogger.info( "sIBL_GUI | " + cMessage + " Custom File Browser : '%s'.", cFolderPath )
				cExploreCommand = "\"" + str( self.Custom_File_Browser_Path_lineEdit.text() ) + "\"" + " \"" + cFolderPath + "\""
			else:
				cLogger.info( "sIBL_GUI | " + cMessage + " 'explorer.exe' : '%s'.", cFolderPath )
				cExploreCommand = "explorer.exe " + " \"" + cFolderPath + "\""

			cLogger.debug( "> Current Explore Command : '%s'.", cExploreCommand )
			cExplorerProcess = QProcess()
			cExplorerProcess.startDetached( cExploreCommand )

		elif platform.system() == "Linux":
			if str( self.Custom_File_Browser_Path_lineEdit.text() ) != "" :
				cBrowserCommand = str( self.Custom_File_Browser_Path_lineEdit.text() ) + " " + cFolderPath
			else:
				cPathVariable = sIBL_Common.sIBL_EnvironmentVariables( "PATH" )
				cPaths = cPathVariable.getPath()
				cPathsTokens = cPaths["PATH"].split( ":" )

				cBrowserCommand = None
				cBrowserFound = None

				for cBrowser in sIBL_GUI_Settings.cLinuxBrowsersList :
					if not cBrowserFound :
						for cPath in cPathsTokens:
							if os.path.exists( os.path.join( cPath, cBrowser ) ) :
								cLogger.info( "sIBL_GUI | " + cMessage + " '%s' : '%s'.", cBrowser, cFolderPath )
								cBrowserCommand = "\"" + os.path.join( cPath, cBrowser ) + "\"" + " " + cFolderPath
								cBrowserFound = True
								break
					else :
						break

			if cBrowserCommand is not None :
				cLogger.debug( "> Current Browser Command : '%s'.", cBrowserCommand )
				cBrowserProcess = QProcess()
				cBrowserProcess.startDetached( cBrowserCommand )
			else :
				sIBL_GUI_QWidgets.sIBL_GUI_Message( "Warning", "Warning", "Please Select A Custom Browser In Preferences Tab !" )
				self.sIBL_GUI_tabWidget.setCurrentIndex( 2 )
				self.Preferences_toolBox.setCurrentIndex( 0 )
		elif platform.system() == "Darwin" :
			if str( self.Custom_File_Browser_Path_lineEdit.text() ) != "" :
				cLogger.info( "sIBL_GUI | " + cMessage + " Custom File Browser : '%s'.", cFolderPath )
				cBrowserCommand = "\"" + str( self.Custom_File_Browser_Path_lineEdit.text() ) + "\"" + " " + cFolderPath
			else:
				cLogger.info( "sIBL_GUI | " + cMessage + " 'Finder' : '%s'.", cFolderPath )
				cBrowserCommand = "open " + " \"" + cFolderPath + "\""

			cLogger.debug( "> Current Browser Command : '%s'.", cBrowserCommand )
			cBrowserProcess = QProcess()
			cBrowserProcess.startDetached( cBrowserCommand )

	@sIBL_Common.sIBL_Execution_Call
	def Open_Output_Folder_pushButton_OnClicked( self ) :
		'''
		This Method Opens Current Loader Script Output Folder.
		'''

		cEnvVariable = sIBL_Common.sIBL_GetTemporarySystemPath()
		if cEnvVariable is not None :
			self.exploreProvidedFolder( "Opening Current Loader Script Output Folder With", cEnvVariable )
		else :
			self.setTemporaryVariableErrorMessage()

	@sIBL_Common.sIBL_Execution_Call
	def Send_To_Software_pushButton_OnClicked( self ) :
		'''
		This Method Remotes Connect To Target Software.
		'''

		cEnvVariable = sIBL_Common.sIBL_GetTemporarySystemPath()
		if cEnvVariable is not None :
			for cTemplate in self.cGlobalTemplates :
				cTemplateAttributes = self.cGlobalTemplates[cTemplate]
				if cTemplateAttributes["Template Name"] == self.Template_comboBox.currentText() :
					cTemplateFile = sIBL_Parser.sIBL_Parser( cTemplateAttributes["Template Path"] )
					cFileTemplateSections = cTemplateFile.getSections()
					if "Remote Connection" in cFileTemplateSections.keys() :
						if self.setLoaderScript() :
							cLogger.info( "sIBL_GUI | Starting Remote Connection !" )
							cTemplateAttributes = cTemplateFile.getSectionAttributes( "Template" )
							cRemoteConnectionAttributes = cTemplateFile.getSectionAttributes( "Remote Connection" )
							cConnectionType = sIBL_Parser.sIBL_GetExtraAttributeComponents( cRemoteConnectionAttributes["Remote Connection|ConnectionType"], "Value" )

							if cConnectionType == "Socket":
								try :
									cSocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
									cSocket.connect( ( str( self.Address_lineEdit.text() ), int( self.Software_Port_spinBox.value() ) ) )
									cSocketCommand = sIBL_Parser.sIBL_GetExtraAttributeComponents( cRemoteConnectionAttributes["Remote Connection|ExecutionCommand"], "Value" ).replace( "$loaderScriptPath", cEnvVariable.replace( "\\", "/" ) + "/" + sIBL_Parser.sIBL_GetExtraAttributeComponents( cTemplateAttributes["Template|OutputScript"], "Value" ) )
									cLogger.debug( "> Current Socket Command : '%s'.", cSocketCommand )
									cSocket.send( cSocketCommand )
									cDataBack = cSocket.recv( 8192 )
									cLogger.debug( "> Received Back From Application : '%s'", cDataBack )
									cSocket.close()
								except Exception, cError:
									sIBL_GUI_QWidgets.sIBL_GUI_Message( "Error", "Error", "Remote Connection Failed On Port : " + str( self.Software_Port_spinBox.value() ) )
									sIBL_Exceptions.sIBL_Exceptions_Feedback ( cError, "Remote Connection Failed On Port : " + str( self.Software_Port_spinBox.value() ), True )
									# self.sIBL_GUI_dockWidget.show()
									# raise
								break

							elif cConnectionType == "Win32" :
								if platform.system() == "Windows" or platform.system() == "Microsoft":
									try :
										cConnection = win32com.client.Dispatch( sIBL_Parser.sIBL_GetExtraAttributeComponents( cRemoteConnectionAttributes["Remote Connection|TargetApplication"], "Value" ) )
										cConnection._FlagAsMethod( "ExecuteSIBLLoaderScript" )
										cConnectionCommand = sIBL_Parser.sIBL_GetExtraAttributeComponents( cRemoteConnectionAttributes["Remote Connection|ExecutionCommand"], "Value" ).replace( "$loaderScriptPath", cEnvVariable.replace( "\\", "/" ) + "/" + sIBL_Parser.sIBL_GetExtraAttributeComponents( cTemplateAttributes["Template|OutputScript"], "Value" ) )
										cLogger.debug( "> Current Connection Command : '%s'.", cConnectionCommand )
										cConnection.ExecuteSIBLLoaderScript( cConnectionCommand )
									except:
										sIBL_GUI_QWidgets.sIBL_GUI_Message( "Error", "Error", "Remote Connection On Win32 OLE Server '" + sIBL_Parser.sIBL_GetExtraAttributeComponents( cRemoteConnectionAttributes["Remote Connection|TargetApplication"], "Value" ) + "' Failed !" )
										sIBL_Exceptions.sIBL_Exceptions_Feedback ( cError, "Remote Connection Failed On Port : " + str( self.Software_Port_spinBox.value() ), True )
										# self.sIBL_GUI_dockWidget.show()
										# raise
									break
								else:
									sIBL_GUI_QWidgets.sIBL_GUI_Message( "Warning", "Warning", "Win32 OLE Server Remote Connection Is Not Supported Under Linux !" )
					else:
						sIBL_GUI_QWidgets.sIBL_GUI_Message( "Warning", "Warning", "Target 3D Package Does'nt Support Socket Connection !" )
		else :
			self.setTemporaryVariableErrorMessage()

	#***************************************************************************************
	#***	Preferences Tab Methods.
	#***************************************************************************************
	@sIBL_Common.sIBL_Execution_Call
	def setVerboseLevel( self, *__None__ ) :
		'''
		This Method Is Called When Verbose Level ComboBox Is Triggered.
		'''

		cLogger.debug( "> Setting Verbose Level : '%s'.", self.Verbose_Level_comboBox.currentText() )
		cVerbosityLevel = int( self.Verbose_Level_comboBox.currentIndex() )
		sIBL_Common.sIBL_SetVerbosity_Level( cVerbosityLevel )
		sIBL_Set_KeyInSettings( "Settings", "VerbosityLevel", self.Verbose_Level_comboBox.currentIndex() )

	@sIBL_Common.sIBL_Execution_Call
	def setVerboseLevelComboBox( self ) :
		'''
		This Method Fills Verbose Level CombBox.
		'''

		self.Verbose_Level_comboBox.clear()
		cEnumerator = ["Critical", "Error", "Warning", "Info", "Debug"]
		cLogger.debug( "> Available Verbose Levels : '%s'.", cEnumerator )
		self.Verbose_Level_comboBox.insertItems( 0, QStringList ( cEnumerator ) )
		cVerbosityLevel = int( sIBL_Get_KeyFromSettings( "Settings", "VerbosityLevel" ) )
		self.Verbose_Level_comboBox.setCurrentIndex( cVerbosityLevel )

	@sIBL_Common.sIBL_Execution_Call
	def setCollectionsPathsTableWidget( self ) :
		'''
		This Method Fills Collections Paths Widget.
		'''

		cCollectionsPaths = self.getCollectionsPaths()

		self.Collections_Paths_tableWidget.clear()
		self.Collections_Paths_tableWidget.setSortingEnabled( False )
		self.Collections_Paths_tableWidget.setRowCount( len( cCollectionsPaths ) )
		self.Collections_Paths_tableWidget.setColumnCount( 2 )
		self.Collections_Paths_tableWidget.verticalHeader().hide()
		self.Collections_Paths_tableWidget.horizontalHeader().setStretchLastSection( True )
		self.Collections_Paths_tableWidget.setHorizontalHeaderLabels( ["Collection Name", "Path"] )

		for row, key in enumerate( cCollectionsPaths.keys() ) :
			cItem = QTableWidgetItem( QString( key ) )
			cItem.setTextAlignment( Qt.AlignCenter )
			cLogger.debug( "> Setting Item In Column '0' : '%s'.", cItem.text() )
			self.Collections_Paths_tableWidget.setItem( row, 0, cItem )

			cItem = QTableWidgetItem( QString( cCollectionsPaths[key] ) )
			cLogger.debug( "> Setting Item In Column '1' : '%s'.", cItem.text() )
			self.Collections_Paths_tableWidget.setItem( row, 1, cItem )

	@sIBL_Common.sIBL_Execution_Call
	def setSIBL_FrameworkPathlineEdit( self ) :
		'''
		This Method Fills sIBL_Framework Executable Path Widget.
		'''

		cFrameworkPath = sIBL_Get_KeyFromSettings( "Settings", "FrameworkPath" )
		cLogger.debug( "> Setting sIBL_Framework Path LineEdit : '%s'.", str( cFrameworkPath ) )
		self.sIBL_Framework_Path_lineEdit.setText( cFrameworkPath )

	@sIBL_Common.sIBL_Execution_Call
	def setSIBLeditPathLineEdit( self ) :
		'''
		This Method Fills sIBLedit Executable Path Widget.
		'''

		cSIBLeditPath = sIBL_Get_KeyFromSettings( "Settings", "sIBLeditPath" )
		cLogger.debug( "> Setting sIBLedit Path LineEdit : '%s'.", str( cSIBLeditPath ) )
		self.sIBLedit_Path_lineEdit.setText( cSIBLeditPath )

	@sIBL_Common.sIBL_Execution_Call
	def sIBL_Framework_Path_toolButton_OnClicked( self ) :
		'''
		This Method Is Called When sIBL_Framework Path ToolButton Is Clicked.
		'''

		cSIBL_FrameworkExecutable = QFileDialog.getOpenFileName( self, self.tr( "sIBL_Framework Executable :" ), QDir.currentPath() )
		cLogger.debug( "> Chosen sIBL_Framework Executable : '%s'.", cSIBL_FrameworkExecutable )
		if cSIBL_FrameworkExecutable != "":
			self.sIBL_Framework_Path_lineEdit.setText( QString( cSIBL_FrameworkExecutable ) )
			sIBL_Set_KeyInSettings( "Settings", "FrameworkPath", self.sIBL_Framework_Path_lineEdit.text() )

	@sIBL_Common.sIBL_Execution_Call
	def sIBLedit_Path_toolButton_OnClicked( self ) :
		'''
		This Method Is Called When sIBLedit Path ToolButton Is Clicked.
		'''

		cSIBLeditExecutable = QFileDialog.getOpenFileName( self, self.tr( "sIBLedit Executable :" ), QDir.currentPath() )
		cLogger.debug( "> Chosen sIBLedit Executable : '%s'.", cSIBLeditExecutable )
		if cSIBLeditExecutable != "":
			self.sIBLedit_Path_lineEdit.setText( QString( cSIBLeditExecutable ) )
			sIBL_Set_KeyInSettings( "Settings", "sIBLeditPath", self.sIBLedit_Path_lineEdit.text() )

	@sIBL_Common.sIBL_Execution_Call
	def setTemplatesPathLineEdit( self ) :
		'''
		This Method Fills Templates Path Widget.
		'''

		cTemplatesPath = sIBL_Get_KeyFromSettings( "Settings", "TemplatesPath" )
		cLogger.debug( "> Setting Templates Path LineEdit : '%s'.", str( cTemplatesPath ) )
		self.Templates_Path_lineEdit.setText( cTemplatesPath )

	@sIBL_Common.sIBL_Execution_Call
	def sIBL_Framework_Path_lineEdit_OnEditFinished( self ) :
		'''
		This Method Is Called When sIBL_Framework Path LineEdit Is Edited And Check That Entered Path Is Valid.
		'''

		if not os.path.exists( os.path.abspath( str( self.sIBL_Framework_Path_lineEdit.text() ) ) ) and str( self.sIBL_Framework_Path_lineEdit.text() ) != "":
			sIBL_GUI_QWidgets.sIBL_GUI_Message( "Error", "Error", "Invalid sIBL_Framework Executable File !" )
			# Restoring Preferences.
			cLogger.debug( "> %s", "Restoring Preferences !" )
			self.setSIBL_FrameworkPathlineEdit()
		else :
			# Saving Preferences.
			sIBL_Set_KeyInSettings( "Settings", "FrameworkPath", self.sIBL_Framework_Path_lineEdit.text() )

	@sIBL_Common.sIBL_Execution_Call
	def sIBLedit_Path_lineEdit_OnEditFinished( self ) :
		'''
		This Method Is Called When sIBLedit Path LineEdit Is Edited And Check That Entered Path Is Valid.
		'''

		if not os.path.exists( os.path.abspath( str( self.sIBLedit_Path_lineEdit.text() ) ) ) and str( self.sIBLedit_Path_lineEdit.text() ) != "":
			sIBL_GUI_QWidgets.sIBL_GUI_Message( "Error", "Error", "Invalid sIBLedit Executable File !" )
			# Restoring Preferences.
			cLogger.debug( "> %s", "Restoring Preferences !" )
			self.setSIBLeditPathLineEdit()
		else :
			# Saving Preferences.
			cLogger.debug( "> %s", "Saving Preferences !" )
			sIBL_Set_KeyInSettings( "Settings", "sIBLeditPath", self.sIBLedit_Path_lineEdit.text() )

	@sIBL_Common.sIBL_Execution_Call
	def Templates_toolButton_OnClicked( self ) :
		'''
		This Method Is Called When Templates Path ToolButton Is Clicked.
		'''

		cDirectory = QFileDialog.getExistingDirectory( self, self.tr( "Templates Directory :" ), QDir.currentPath() )
		cLogger.debug( "> Chosen Templates Folder : '%s'.", cDirectory )
		if cDirectory != "":
			self.Templates_Path_lineEdit.setText( QString( cDirectory ) )
			self.initializeTemplatesRelationships()
			sIBL_Set_KeyInSettings( "Settings", "TemplatesPath", self.Templates_Path_lineEdit.text() )

	@sIBL_Common.sIBL_Execution_Call
	def Templates_Path_lineEdit_OnEditFinished( self ) :
		'''
		This Method Is Called When Templates Path LineEdit Is Edited And Check That Entered Path Is Valid.
		'''

		if not os.path.exists( os.path.abspath( str( self.Templates_Path_lineEdit.text() ) ) ) and str( self.Templates_Path_lineEdit.text() ) != "":
			sIBL_GUI_QWidgets.sIBL_GUI_Message( "Error", "Error", "Invalid Templates Directory !" )
			# Restoring Preferences.
			cLogger.debug( "> %s", "Restoring Preferences !" )
			self.setTemplatesPathLineEdit()
		else :
			self.initializeTemplatesRelationships()
			# Saving Preferences.
			sIBL_Set_KeyInSettings( "Settings", "TemplatesPath", self.Templates_Path_lineEdit.text() )

	@sIBL_Common.sIBL_Execution_Call
	def setHelpFilesPathLineEdit( self ) :
		'''
		This Method Fills Help Files Path Widget.
		'''

		cHelpFilesPath = sIBL_Get_KeyFromSettings( "Settings", "HelpFilesPath" )
		cLogger.debug( "> Setting Help Files LineEdit : '%s'.", str( cHelpFilesPath ) )
		self.Help_Files_Path_lineEdit.setText( cHelpFilesPath )

	@sIBL_Common.sIBL_Execution_Call
	def Help_Files_toolButton_OnClicked( self ) :
		'''
		This Method Is Called When Help Files Path ToolButton Is Clicked.
		'''

		cDirectory = QFileDialog.getExistingDirectory( self, self.tr( "Help Files Directory :" ), QDir.currentPath() )
		cLogger.debug( "> Chosen Help Files Folder : '%s'.", cDirectory )
		if cDirectory != "":
			self.Help_Files_Path_lineEdit.setText( QString( cDirectory ) )
			self.initializeHelpRelationships()
			sIBL_Set_KeyInSettings( "Settings", "HelpFilesPath", self.Help_Files_Path_lineEdit.text() )

	@sIBL_Common.sIBL_Execution_Call
	def Help_Files_Path_lineEdit_OnEditFinished( self ) :
		'''
		This Method Is Called When Help Files Path LineEdit Is Edited And Check That Entered Path Is Valid.
		'''

		if not os.path.exists( os.path.abspath( str( self.Help_Files_Path_lineEdit.text() ) ) ) and str( self.Help_Files_Path_lineEdit.text() ) != "":
			sIBL_GUI_QWidgets.sIBL_GUI_Message( "Error", "Error", "Invalid Help Files Path !" )
			# Restoring Preferences.
			cLogger.debug( "> %s", "Restoring Preferences !" )
			self.setHelpFilesPathLineEdit()
		else :
			# Saving Preferences.
			self.initializeHelpRelationships()
			sIBL_Set_KeyInSettings( "Settings", "HelpFilesPath", self.Help_Files_Path_lineEdit.text() )

	@sIBL_Common.sIBL_Execution_Call
	def Activate_OpenGL_checkBox_StateChanged( self, *__None__ ) :
		'''
		This Method Saves The Current OpenGL State.
		'''

		if self.Activate_OpenGL_checkBox.isChecked() :
			sIBL_Set_KeyInSettings( "Settings", "OpenGL", 1 )
			self.OpenGLActive = True
		else :
			sIBL_Set_KeyInSettings( "Settings", "OpenGL", 0 )
			self.OpenGLActive = False

		self.setGPSMap()

	@sIBL_Common.sIBL_Execution_Call
	def Activate_Antialiasing_checkBox_StateChanged( self, *__None__ ) :
		'''
		This Method Saves The GPS Map Antialising State.
		'''

		if self.Activate_Antialiasing_checkBox.isChecked() :
			sIBL_Set_KeyInSettings( "Settings", "GPSMapAntialiasing", 1 )
			self.GPSMapAntialiasingActive = True
		else :
			sIBL_Set_KeyInSettings( "Settings", "GPSMapAntialiasing", 0 )
			self.GPSMapAntialiasingActive = False

		self.setGPSMap()

	@sIBL_Common.sIBL_Execution_Call
	def Toggle_Log_Window_pushButton_OnClicked( self ) :
		'''
		This Method Is Called When Toggle Log Window Button Is Clicked.
		'''

		if self.sIBL_GUI_dockWidget.isHidden() :
			cLogger.debug( "> %s", "Showing Log Window !" )
			self.sIBL_GUI_dockWidget.show()
		else :
			cLogger.debug( "> %s", "Hiding Log Window !" )
			self.sIBL_GUI_dockWidget.close()

	@sIBL_Common.sIBL_Execution_Call
	def isPathUniqueInCollectionsPaths( self, cItem ) :
		'''
		This Method Check If An Item Is Not Unique In The Collections Paths TableWidget.

		@param cItem: Item Uniqueness To Be Checked ( String )
		@return: Item Uniqueness ( Boolean )
		'''

		cCollectionsPaths = self.getCollectionsPaths()
		for key in  cCollectionsPaths.keys() :
			if cItem == cCollectionsPaths[key] :
				cLogger.debug( "> %s Is Already In Collection Paths !", cItem )
				return False
		cLogger.debug( "> %s Is Not In Collection Paths !", cItem )
		return True

	@sIBL_Common.sIBL_Execution_Call
	def isNameUniqueInCollectionsNames( self, cItem ) :
		'''
		This Method Check If An Item Is Not Unique In The Collections Names TableWidget.

		@param cItem: Item Uniqueness To Be Checked ( String )
		@return: Item Uniqueness ( Boolean )
		'''

		cCollectionsPaths = self.getCollectionsPaths()
		for key in  cCollectionsPaths.keys() :
			if cItem == key :
				cLogger.debug( "> %s Is Already In Collection Names !", cItem )
				return False
		cLogger.debug( "> %s Is Not In Collection Names !", cItem )
		return True

	@sIBL_Common.sIBL_Execution_Call
	def isItemNotUniqueInTableWidget( self, cItem, cTableWidget , cColumn ) :
		'''
		This Method Check If An Item Is Not Unique In The Current TableWidget.

		@param cItem: Item Uniqueness To Be Checked ( String )
		@param cTableWidget: Current Table Widget ( QTableWidget )
		@param cColumn: Column To Check ( Int )
		@return: Item Uniqueness ( Boolean )
		'''

		for row in range( 0, cTableWidget.rowCount() ) :
			if cItem == str( cTableWidget.item( row, cColumn ).text() ) :
				cLogger.debug( "> %s Is Already In Column '%s' Of '%s'!", cItem, cColumn, cTableWidget )
				return True
		cLogger.debug( "> %s Is Not In Column '%s' Of '%s'!", cItem, cColumn, cTableWidget )
		return False

	@sIBL_Common.sIBL_Execution_Call
	def Collections_Paths_tableWidget_OnCellChanged( self, *__None__ ) :
		'''
		This Method Is Called When Collections Paths TableWidget Is Edited.
		'''

		cSelectedItemsIndexes = self.Collections_Paths_tableWidget.selectedIndexes()

		if len( cSelectedItemsIndexes ) != 0 :
			cIndex = ( int( cSelectedItemsIndexes[0].row() ), int( cSelectedItemsIndexes[0].column() ) )

			if cIndex[1] == 1 :
				cDirectoryPath = str( self.Collections_Paths_tableWidget.item( cIndex[0], 1 ).text() )
				if os.path.exists( cDirectoryPath ) and cDirectoryPath.endswith( "/" ) :
					isPathUniqueInCollection = self.isPathUniqueInCollectionsPaths( cDirectoryPath )

					if isPathUniqueInCollection :
						self.initializeCollectionsRelationships()
						cLogger.debug( "> %s", "Saving Preferences !" )
						self.setCollectionsPaths()
					else :
						sIBL_GUI_QWidgets.sIBL_GUI_Message( "Error", "Error", "Chosen Directory Already Exists In Global Collection !" )
						# Restoring Paths From Stored Preferences.
						cLogger.debug( "> %s", "Restoring Preferences !" )
						self.setCollectionsPathsTableWidget()
				else :
					sIBL_GUI_QWidgets.sIBL_GUI_Message( "Error", "Error", "Chosen Collection Path Is Not Valid !" )
					# Restoring Paths From Stored Preferences.
					cLogger.debug( "> %s", "Restoring Preferences !" )
					self.setCollectionsPathsTableWidget()
			else :
				isNameUniqueInCollection = self.isNameUniqueInCollectionsNames( self.Collections_Paths_tableWidget.item( cIndex[0], 0 ).text() )

				if isNameUniqueInCollection :
					self.initializeCollectionsRelationships()
					cLogger.debug( "> %s", "Saving Preferences !" )
					self.setCollectionsPaths()
				else :
					sIBL_GUI_QWidgets.sIBL_GUI_Message( "Error", "Error", "Chosen Collection Name Already Exists In Global Collection !" )
					# Restoring Paths From Stored Preferences.
					cLogger.debug( "> %s", "Restoring Preferences !" )
					self.setCollectionsPathsTableWidget()

	@sIBL_Common.sIBL_Execution_Call
	def getNewCollection( self ) :
		'''
		This Method Add A New Collection.
		'''

		cDialogMessage = "Enter Your New Collection Name !"
		nCollectionName = QInputDialog.getText( self, self.tr( "sIBL_GUI | Get New Collection" ), cDialogMessage )
		if nCollectionName[1] is not False :
			isNameInCollection = self.isItemNotUniqueInTableWidget( nCollectionName[0], self.Collections_Paths_tableWidget , 0 )
			if isNameInCollection is False :
				cDirectory = QFileDialog.getExistingDirectory( self, self.tr( "New Collection Directory :" ), QDir.currentPath() )
				if cDirectory != "" :
					if not str( cDirectory ).endswith( "/" ) :
						cDirectory = cDirectory + "/"
					isDirectoryInCollection = self.isItemNotUniqueInTableWidget( cDirectory, self.Collections_Paths_tableWidget , 1 )
					if isDirectoryInCollection is False :
						# Clearing Selection To Avoid Problems With Collections_Paths_tableWidget_OnCellChanged() Method.
						self.Collections_Paths_tableWidget.clearSelection()

						self.Collections_Paths_tableWidget.setRowCount( self.Collections_Paths_tableWidget.rowCount() + 1 )
						cItem = QTableWidgetItem( QString( nCollectionName[0] ) )
						cItem.setTextAlignment( Qt.AlignCenter )
						cLogger.debug( "> Setting Item In Column '0' : '%s'.", cItem.text() )
						self.Collections_Paths_tableWidget.setItem( self.Collections_Paths_tableWidget.rowCount() - 1, 0, cItem )
						cItem = QTableWidgetItem( QString( cDirectory ) )
						cLogger.debug( "> Setting Item In Column '1' : '%s'.", cItem.text() )
						self.Collections_Paths_tableWidget.setItem( self.Collections_Paths_tableWidget.rowCount() - 1, 1, cItem )
						self.initializeCollectionsRelationships()
						cLogger.debug( "> %s", "Saving Preferences !" )
						self.setCollectionsPaths()
					else :
						sIBL_GUI_QWidgets.sIBL_GUI_Message( "Error", "Error", "Chosen Directory Already Exists In Global Collection !" )
			else :
				sIBL_GUI_QWidgets.sIBL_GUI_Message( "Error", "Error", "Chosen Collection Name Already Exists In Global Collection !" )

	@sIBL_Common.sIBL_Execution_Call
	def Edit_Collection_pushButton_OnClicked( self ) :
		'''
		This Method Is Called When Edit Button Is Clicked.
		'''

		cSelectedItems = self.Collections_Paths_tableWidget.selectedItems()
		if len( cSelectedItems ) > 1 :
			sIBL_GUI_QWidgets.sIBL_GUI_Message( "Warning", "Warning", "Multiple Items Selected ! Only The First One Will Be Edited !" )
		if len( cSelectedItems ) != 0 :
			cDirectory = QFileDialog.getExistingDirectory( self, self.tr( "Edit Collection Directory :" ), QDir.currentPath() )
			if cDirectory != "" :
				if not str( cDirectory ).endswith( "/" ) :
					cDirectory = cDirectory + "/"
				isDirectoryInCollection = self.isItemNotUniqueInTableWidget( cDirectory, self.Collections_Paths_tableWidget , 1 )
				if isDirectoryInCollection is False :
					# Clearing Selection To Avoid Problems With Collections_Paths_tableWidget_OnCellChanged() Method.
					self.Collections_Paths_tableWidget.clearSelection()

					cItem = QTableWidgetItem( QString( cDirectory ) )
					cLogger.debug( "> Setting Item In Column '1' : '%s'.", cItem.text() )
					self.Collections_Paths_tableWidget.setItem( cSelectedItems[0].row(), 1, cItem )
					self.initializeCollectionsRelationships()
					cLogger.debug( "> %s", "Saving Preferences !" )
					self.setCollectionsPaths()
				else :
					sIBL_GUI_QWidgets.sIBL_GUI_Message( "Error", "Error", "Chosen Directory Already Exists In Global Collection !" )

	@sIBL_Common.sIBL_Execution_Call
	def Add_pushButton_OnClicked( self ) :
		'''
		This Method Is Called When Add Button Is Clicked.
		'''

		self.getNewCollection()

	@sIBL_Common.sIBL_Execution_Call
	def Remove_pushButton_OnClicked( self ) :
		'''
		This Method Is Called When Remove Button Is Clicked.
		'''

		cSelectedItems = self.Collections_Paths_tableWidget.selectedItems()
		if len( cSelectedItems ) != 0 :
			cRemoveList = cSelectedItems
			for cItem in cSelectedItems :
				for cItemCompared in cSelectedItems :
					if cItem.row() == cItemCompared.row() and cItem != cItemCompared :
						cRemoveList.remove( cItemCompared )
			for item in cRemoveList :
				cLogger.debug( "> Removing Row : '%s'.", item.row() )
				self.Collections_Paths_tableWidget.removeRow( item.row() )
			self.initializeCollectionsRelationships()
			cLogger.debug( "> %s", "Saving Preferences !" )
			self.setCollectionsPaths()

	@sIBL_Common.sIBL_Execution_Call
	def startEmptyCollectionWizard( self ) :
		'''
		This Method Is The Empty Collection Wizard.
		'''

		cMessage = "Your Collection Is Empty, Do You Want To Add Items To It ?"
		cReply = QMessageBox.question( self, self.tr( "sIBL_GUI | Question" ), cMessage, QMessageBox.Yes, QMessageBox.Cancel )
		if cReply == QMessageBox.Yes:
			cLogger.info( "sIBL_GUI | Starting New Collection Wizard !" )
			self.getNewCollection()
		else:
			cLogger.info( "sIBL_GUI | New Collection Wizard Canceled !" )

	@sIBL_Common.sIBL_Execution_Call
	def setCustomTextEditorPathLineEdit( self ) :
		'''
		This Method Fills Custom Text Editor Path Widget.
		'''

		cCustomTextEditor = sIBL_Get_KeyFromSettings( "Others", "CustomTextEditor" )
		cLogger.debug( "> Setting Custom Text Editor Path LineEdit : '%s'.", str( cCustomTextEditor ) )
		self.Custom_Text_Editor_Path_lineEdit.setText( cCustomTextEditor )

	@sIBL_Common.sIBL_Execution_Call
	def setCustomFileBrowserPathLineEdit( self ) :
		'''
		This Method Fills Custom File Browser Path Widget.
		'''

		cCustomFileBrowser = sIBL_Get_KeyFromSettings( "Others", "CustomFileBrowser" )
		cLogger.debug( "> Setting Custom Text Editor Path LineEdit : '%s'.", str( cCustomFileBrowser ) )
		self.Custom_File_Browser_Path_lineEdit.setText( cCustomFileBrowser )

	@sIBL_Common.sIBL_Execution_Call
	def Custom_Text_Editor_Path_lineEdit_OnEditFinished( self ) :
		'''
		This Method Is Called When Custom Text Editor Path LineEdit Is Edited And Check That Entered Path Is Valid.
		'''

		if not os.path.exists( os.path.abspath( str( self.Custom_Text_Editor_Path_lineEdit.text() ) ) ) and str( self.Custom_Text_Editor_Path_lineEdit.text() ) != "":
			sIBL_GUI_QWidgets.sIBL_GUI_Message( "Error", "Error", "Invalid Custom Text Editor Executable File !" )
			# Restoring Preferences.
			cLogger.debug( "> %s", "Restoring Preferences !" )
			self.setCustomTextEditorPathLineEdit()
		else :
			# Saving Preferences.
			sIBL_Set_KeyInSettings( "Others", "CustomTextEditor", self.Custom_Text_Editor_Path_lineEdit.text() )

	@sIBL_Common.sIBL_Execution_Call
	def Custom_File_Browser_Path_lineEdit_OnEditFinished( self ) :
		'''
		This Method Is Called When Custom File Browser Path LineEdit Is Edited And Check That Entered Path Is Valid.
		'''

		if not os.path.exists( os.path.abspath( str( self.Custom_File_Browser_Path_lineEdit.text() ) ) ) and str( self.Custom_File_Browser_Path_lineEdit.text() ) != "":
			sIBL_GUI_QWidgets.sIBL_GUI_Message( "Error", "Error", "Invalid Custom File Browser Executable File !" )
			# Restoring Preferences.
			cLogger.debug( "> %s", "Restoring Preferences !" )
			self.setCustomFileBrowserPathLineEdit()
		else :
			# Saving Preferences.
			sIBL_Set_KeyInSettings( "Others", "CustomFileBrowser", self.Custom_File_Browser_Path_lineEdit.text() )

	@sIBL_Common.sIBL_Execution_Call
	def Custom_Text_Editor_Path_toolButton_OnClicked( self ) :
		'''
		This Method Is Called When Custom Text Editor ToolButton Is Clicked.
		'''

		cCustomTextEditorExecutable = QFileDialog.getOpenFileName( self, self.tr( "Custom Text Editor Executable :" ), QDir.currentPath() )
		cLogger.debug( "> Chosen Custom Text Editor Executable : '%s'.", cCustomTextEditorExecutable )
		if cCustomTextEditorExecutable != "":
			self.Custom_Text_Editor_Path_lineEdit.setText( QString( cCustomTextEditorExecutable ) )
			sIBL_Set_KeyInSettings( "Others", "CustomTextEditor", self.Custom_Text_Editor_Path_lineEdit.text() )

	@sIBL_Common.sIBL_Execution_Call
	def Custom_File_Browser_Path_toolButton_OnClicked( self ) :
		'''
		This Method Is Called When Custom Text Editor ToolButton Is Clicked.
		'''

		cFileBrowserExecutable = QFileDialog.getOpenFileName( self, self.tr( "Custom File Browser Executable :" ), QDir.currentPath() )
		cLogger.debug( "> Chosen Custom File Browser Executable : '%s'.", cFileBrowserExecutable )
		if cFileBrowserExecutable != "":
			self.Custom_File_Browser_Path_lineEdit.setText( QString( cFileBrowserExecutable ) )
			sIBL_Set_KeyInSettings( "Others", "CustomFileBrowser", self.Custom_File_Browser_Path_lineEdit.text() )

	@sIBL_Common.sIBL_Execution_Call
	def setSIBL_GUI_FTPWindow( self, cWindowTitle , cRemoteDirectory, cLocalDirectory, cIgnoreList = None ) :
		'''
		This Method Starts The sIBL_GUI FTP Window.

		@param cWindowTitle: FTP Window Title ( String )
		@param cRemoteDirectory: Remote Directory To Transfer From( String )
		@param cLocalDirectory: Local Directory To Transfer To ( String )
		@param cIgnoreList: Current Ignore List ( List )
		'''

		if not self.cFTP_Session_Active :
			self.cFTP_UI = sIBL_GUI_FTP.sIBL_GUI_FTP( self, sIBL_GUI_Settings.cFTP_Host, sIBL_GUI_Settings.cFTP_Port, sIBL_GUI_Settings.cFTP_Login, sIBL_GUI_Settings.cFTP_Password, cRemoteDirectory , cLocalDirectory, cIgnoreList )
			self.cFTP_UI.setWindowTitle( cWindowTitle )
			self.cFTP_UI.show()
		else :
			sIBL_GUI_QWidgets.sIBL_GUI_Message( "Warning", "Warning", "FTP Session Already Active !" )

	@sIBL_Common.sIBL_Execution_Call
	def Get_Help_pushButton_OnClicked( self ) :
		'''
		This Method Triggers The Help Download.
		'''
		self.getLatestHelp()

	@sIBL_Common.sIBL_Execution_Call
	def getLatestHelp( self ):
		'''
		This Method Triggers sIBL_GUI FTP For Help Download.
		'''

		if hasattr( sys, "frozen" ) :
			cLocalTemplatesPath = os.path.abspath( str( self.Help_Files_Path_lineEdit.text() ) )
		else :
			cLocalTemplatesPath = "./FTP/Help/"

		self.setSIBL_GUI_FTPWindow( "sIBL_GUI FTP - Online Help Download ", sIBL_GUI_Settings.cOnlineRepository + "Help/" , cLocalTemplatesPath )
		self.cHelp_Changed = True

	@sIBL_Common.sIBL_Execution_Call
	def Get_Latest_Templates_pushButton_OnClicked( self ) :
		'''
		This Method Triggers The Templates Download.
		'''

		self.getLatestTemplates()

	@sIBL_Common.sIBL_Execution_Call
	def getLatestTemplates( self, cIgnoreList = None ) :
		'''
		This Method Triggers sIBL_GUI FTP For Templates Download.

		@param cIgnoreList: Current Ignore List. ( List )
		'''

		if hasattr( sys, "frozen" ) :
			cLocalTemplatesPath = os.path.abspath( str( self.Templates_Path_lineEdit.text() ) )
		else :
			cLocalTemplatesPath = "./FTP/Templates/"

		self.setSIBL_GUI_FTPWindow( "sIBL_GUI FTP - Online Templates Download", sIBL_GUI_Settings.cOnlineRepository + "Templates/" , cLocalTemplatesPath, cIgnoreList )
		self.cTemplates_Changed = True

	@sIBL_Common.sIBL_Execution_Call
	def setCheckBoxStateFromSettings( self, cCheckbox, cSection, cKey ) :
		'''
		This Method Restore The Provided CheckBox State From Settings.

		@param cCheckbox: Current CheckBox To Set. ( QCheckBox )
		@param cSection: Current Section To Retrieve Key From. ( String )
		@param cKey: Current Key To Retrieve. ( String )
		@return: Current Key Value. ( String )
		'''

		cStoredState = sIBL_Get_KeyFromSettings( cSection, cKey )
		if cStoredState == "1":
			cLogger.debug( "> Setting %s State : 'True'", cKey )
			cCheckbox.setChecked( True )
			return True
		else :
			cLogger.debug( "> Setting %s State : 'False'", cKey )
			cCheckbox.setChecked( False )
			return False

	@sIBL_Common.sIBL_Execution_Call
	def Check_For_New_Releases_checkBox_StateChanged( self, *__None__ ) :
		'''
		This Method Saves The Current Online Update State.
		'''

		if self.Check_For_New_Releases_checkBox.isChecked() :
			sIBL_Set_KeyInSettings( "Settings", "OnlineUpdate", 1 )
		else :
			sIBL_Set_KeyInSettings( "Settings", "OnlineUpdate", 0 )

	@sIBL_Common.sIBL_Execution_Call
	def Ignore_Missing_Templates_checkBox_StateChanged( self, *__None__ ) :
		'''
		This Method Saves The Current Missing Templates State.
		'''

		if self.Ignore_Missing_Templates_checkBox.isChecked() :
			sIBL_Set_KeyInSettings( "Settings", "IgnoreMissingTemplates", 1 )
		else :
			sIBL_Set_KeyInSettings( "Settings", "IgnoreMissingTemplates", 0 )

	@sIBL_Common.sIBL_Execution_Call
	def Check_For_New_Releases_pushButton_OnClicked( self ) :
		'''
		This Method Launch sIBL_GUI Updater.
		'''

		cLogger.debug( "> Launching Online Updater UnMuted." )
		self.setCursor( Qt.WaitCursor )
		self.setOnlineUpdater( True )

	@sIBL_Common.sIBL_Execution_Call
	def checkForNewReleases( self ) :
		if self.Check_For_New_Releases_checkBox.isChecked() :
			cLogger.info( "sIBL_GUI | Online Update Is Currently Enabled !" )
			self.setOnlineUpdater()
		else:
			cLogger.info( "sIBL_GUI | Online Update Is Currently Disabled !" )

	@sIBL_Common.sIBL_Execution_Call
	def setOnlineUpdater( self, showInfoMessage = None ) :
		'''
		This Method Triggers sIBL_GUI Updater.

		@param cInfoMessage: Information Message Display ( Boolean )
		'''

		cUpdate = sIBL_GUI_Updater.sIBL_Online_Update( self, showInfoMessage )
		cUpdate.startWorkerThread()

	@sIBL_Common.sIBL_Execution_Call
	def checkPreferencesPaths( self ) :
		'''
		This Method Checks If Preferences Paths Are Valid.
		'''

		cPathsValid = True
		if self.sIBL_Framework_Path_lineEdit.text() != "" :
			if not os.path.exists( os.path.abspath( str( self.sIBL_Framework_Path_lineEdit.text() ) ) ) :
				sIBL_GUI_QWidgets.sIBL_GUI_Message( "Error", "Error", "Stored sIBL_Framework Path Is Invalid, Resetting Path !" )
				cPathsValid = False
				self.sIBL_Framework_Path_lineEdit.setText( QString( "" ) )
				sIBL_Set_KeyInSettings( "Settings", "FrameworkPath", "" )

		if self.sIBLedit_Path_lineEdit.text() != "" :
			if not os.path.exists( os.path.abspath( str( self.sIBLedit_Path_lineEdit.text() ) ) ) :
				sIBL_GUI_QWidgets.sIBL_GUI_Message( "Error", "Error", "Stored sIBLedit Path Is Invalid, Reseting Path !" )
				cPathsValid = False
				self.sIBLedit_Path_lineEdit.setText( QString( "" ) )
				sIBL_Set_KeyInSettings( "Settings", "sIBLeditPath", "" )

		if self.Help_Files_Path_lineEdit.text() != "" :
			if not os.path.exists( os.path.abspath( str( self.Help_Files_Path_lineEdit.text() ) ) ) :
				sIBL_GUI_QWidgets.sIBL_GUI_Message( "Error", "Error", "Stored Help Files Path Is Invalid, Reseting Path !" )
				cPathsValid = False
				self.Help_Files_Path_lineEdit.setText( QString( "" ) )
				sIBL_Set_KeyInSettings( "Settings", "HelpFilesPath", "" )

		if self.Templates_Path_lineEdit.text() != "" :
			if not os.path.exists( os.path.abspath( str( self.Templates_Path_lineEdit.text() ) ) ) :
				sIBL_GUI_QWidgets.sIBL_GUI_Message( "Error", "Error", "Stored Templates Path Is Invalid, Reseting Path !" )
				cPathsValid = False
				self.Templates_Path_lineEdit.setText( QString( "" ) )
				sIBL_Set_KeyInSettings( "Settings", "TemplatesPath", "" )

		if self.Custom_Text_Editor_Path_lineEdit.text() != "" :
			if not os.path.exists( os.path.abspath( str( self.Custom_Text_Editor_Path_lineEdit.text() ) ) ) :
				sIBL_GUI_QWidgets.sIBL_GUI_Message( "Error", "Error", "Stored Custom Text Editor Path Is Invalid, Reseting Path !" )
				cPathsValid = False
				self.Custom_Text_Editor_Path_lineEdit.setText( QString( "" ) )
				sIBL_Set_KeyInSettings( "Others", "CustomTextEditor", "" )

		if self.Custom_File_Browser_Path_lineEdit.text() != "" :
			if not os.path.exists( os.path.abspath( str( self.Custom_File_Browser_Path_lineEdit.text() ) ) ) :
				sIBL_GUI_QWidgets.sIBL_GUI_Message( "Error", "Error", "Stored Custom File Browser Path Is Invalid, Reseting Path !" )
				cPathsValid = False
				self.Custom_File_Browser_Path_lineEdit.setText( QString( "" ) )
				sIBL_Set_KeyInSettings( "Others", "CustomFileBrowser", "" )

		for row in range( 0, self.Collections_Paths_tableWidget.rowCount() ) :
			cRowPath = str( self.Collections_Paths_tableWidget.item( row, 1 ).text() )
			if cRowPath != "" :
				if not os.path.exists( os.path.abspath( cRowPath ) ) :
					sIBL_GUI_QWidgets.sIBL_GUI_Message( "Error", "Error", "Stored " + str( self.Collections_Paths_tableWidget.item( row, 0 ).text() ) + " Collection Path Is Invalid, Reseting Path !" )
					cPathsValid = False
					self.Collections_Paths_tableWidget.item( row, 1 ).setText( QString( "" ) )
					self.setCollectionsPaths()

		if cPathsValid :
			cLogger.debug( "> %s", "Preferences Paths Are Valid !" )

	#***************************************************************************************
	#***	Help Tab Methods.
	#***************************************************************************************
	@sIBL_Common.sIBL_Execution_Call
	def initializeHelpRelationships( self ) :
		'''
		This Method Initializes The Help Tab.
		'''

		cLogger.debug( "> Initializing : '%s'.", "self.cGlobalHelpFiles" )
		self.cGlobalHelpFiles = self.getHelpFiles()
		cLogger.debug( "> Clearing : '%s'.", "Help_Files_comboBox" )
		self.Help_Files_comboBox.clear()
		if self.cGlobalHelpFiles is not None :
			self.setHelpFilesComboBox()

	@sIBL_Common.sIBL_Execution_Call
	def setHelpFilesComboBox( self ) :
		'''
		This Method Fills The Softwares ComboBox.
		'''

		self.Help_Files_comboBox.clear()

		cHelpFiles_Keys = self.cGlobalHelpFiles.keys()

		cSIBL_GUI_Manual_Exists = False
		cManualBaseName = ""
		for cItem in cHelpFiles_Keys :
			if cItem in sIBL_GUI_Settings.cSIBL_GUI_ManualFile :
				cSIBL_GUI_Manual_Exists = True
				cManualBaseName = cItem
				cLogger.debug( "> Inserting '%s' In 'Help_Files_comboBox'.", sIBL_GUI_Settings.cSIBL_GUI_ManualFile )
				self.Help_Files_comboBox.insertItem( 0, QString( cItem ) )
				self.Help_Files_comboBox.insertSeparator( 1 )

		if cSIBL_GUI_Manual_Exists :
			cHelpFiles_Keys.remove( cManualBaseName )
			cInsertPosition = 2
		else :
			cInsertPosition = 0

		cLogger.debug( "> Inserting '%s' In 'Help_Files_comboBox'.", cHelpFiles_Keys )
		self.Help_Files_comboBox.insertItems( cInsertPosition, QStringList( cHelpFiles_Keys ) )
		self.setHelpTextBrowser()

	@sIBL_Common.sIBL_Execution_Call
	def getHelpFiles( self ) :
		'''
		This Method Gets The Help Files.

		@return: Helps Files. ( Dictionary )
		'''

		cLogger.info( "sIBL_GUI | Retrieving Help Files !" )

		cHelpFiles = sIBL_Recursive_Walker.sIBL_Recursive_Walker( os.path.abspath( str( self.Help_Files_Path_lineEdit.text() ) ).replace( "\\", "/" ) + "/" )
		self.cHelpFilesList = cHelpFiles.recursiveWalker( ".htm" )

		cLogger.info( "sIBL_GUI | Help Files List : '%s'.", self.cHelpFilesList )

		return self.cHelpFilesList

	@sIBL_Common.sIBL_Execution_Call
	def setHelpTextBrowser( self, *__None__ ) :
		'''
		This Method Sets The Help TextBrowser.
		'''

		if self.cHelpFilesList is not {} or self.cHelpFilesList is not None :
			cManualPath = os.path.abspath( self.cHelpFilesList[str( self.Help_Files_comboBox.currentText() )] )
			cLogger.debug( "> Loading Help Manual : '%s'.", cManualPath )
			if ( platform.system() == "Windows" or platform.system() == "Microsoft" ) and cManualPath.startswith( "\\\\" ):
				cManualFileUrl = QUrl( QString( "file:\\" + cManualPath[2:] ) )
			else:
				cManualFileUrl = QUrl.fromLocalFile( QString( cManualPath ) )
			self.Help_webView.load( cManualFileUrl )

	#***************************************************************************************
	#***	About Tab Methods.
	#***************************************************************************************
	@sIBL_Common.sIBL_Execution_Call
	def setAboutMessage( self ):
		'''
		This Method Sets The About Message.
		'''

		cLogger.debug( "> Setting About Tab Message !" )
		self.About_label.setText( sIBL_GUI_About.cSIBL_GUI_AboutMessage )

	#***************************************************************************************
	#***	Utilities Methods.
	#***************************************************************************************
	@sIBL_Common.sIBL_Execution_Call
	def getCollectionsPaths( self ) :
		'''
		This Method Gets Collections Paths From The Preferences File.

		@return: Collections Paths List. ( Dictionary )
		'''

		cCollectionsPaths = {}
		if "Collections" in cSettings.childGroups() :
			cSettings.beginGroup( "Collections" )
			for cCollection in cSettings.childKeys() :
				cCollectionsPaths[ str( cCollection ) ] = str( cSettings.value( cCollection ).toString() )
			cSettings.endGroup()
		cLogger.debug( "> Current Stored Paths : '%s'.", cCollectionsPaths )
		return cCollectionsPaths

	@sIBL_Common.sIBL_Execution_Call
	def setCollectionsPaths( self ) :
		'''
		This Method Store Collections Paths In Settings File.
		'''

		cCollections = self.getCollections()
		for cCollection in cCollections :
			cLogger.debug( "> Saving '%s' In Collections Section With Value : '%s' In Settings File.", cCollection, cCollections[cCollection] )
			sIBL_Set_KeyInSettings( "Collections", cCollection, cCollections[cCollection] )

		# Removing Unused Collections From Settings
		cSettings.beginGroup( "Collections" )
		for cCollection in cSettings.childKeys() :
			if not cCollection in cCollections.keys() :
				cLogger.debug( "> Removing '%s' From Settings File.", cCollection )
				cSettings.remove( cCollection )
		cSettings.endGroup()

	@sIBL_Common.sIBL_Execution_Call
	def getCollections( self ) :
		'''
		This Method Gets Collections List From The Collections Paths TableWidget.

		@return: Collections List. ( Dictionary )
		'''

		cCollections = {}
		for row in range( 0, self.Collections_Paths_tableWidget.rowCount() ) :
			cCollections[str( self.Collections_Paths_tableWidget.item( row, 0 ).text() )] = str( self.Collections_Paths_tableWidget.item( row, 1 ).text() )
		cLogger.info( "sIBL_GUI | Retrieving Collections !" )
		cLogger.info( "sIBL_GUI | {'Collections' : 'Paths'} : '%s'.", cCollections )
		return cCollections

	@sIBL_Common.sIBL_Execution_Call
	def getGlobalCollection( self ) :
		'''
		This Method Gets Collections Content From The Collections Dictionary.

		@return: Global Collections Content. ( Dictionary )
		'''

		cCollections = self.getCollections()
		cGlobalCollection = {}
		for key in cCollections.keys() :
			cCollection = sIBL_Collection.sIBL_Collection( cCollections[key] )
			cGlobalCollection[key] = cCollection.getCollectionContent()
		cLogger.debug( "> Current Global Collection : '%s'.", cGlobalCollection )
		return cGlobalCollection

	@sIBL_Common.sIBL_Execution_Call
	def getGlobalCollectionExtended( self ) :
		'''
		This Method Extends Current Collections Informations From The Global Collections.

		@return: Extended Collections Content. ( Dictionary )
		'''

		cGlobalCollection = self.getGlobalCollection()

		cCombinedGlobalCollection = {}

		for collection in cGlobalCollection.keys() :
			cCollection = cGlobalCollection[collection]
			if cCollection is not None:
				for sIBL in cCollection.keys() :
					try:
						cExtendedSIBL = {}
						cExtendedSIBL["sIBL Path"] = cCollection[sIBL]

						cSIBLFile = sIBL_Parser.sIBL_Parser( cCollection[sIBL] )
						cSIBLFileHeaderAttributes = cSIBLFile.getSectionAttributes( "Header" )
						cExtendedSIBL["Collection"] = collection
						cExtendedSIBL["Icon Path"] = os.path.join( os.path.dirname( cCollection[sIBL] ), cSIBLFileHeaderAttributes["Header|ICOfile"] )
						cExtendedSIBL["sIBL Name"] = cSIBLFileHeaderAttributes["Header|Name"]
						cExtendedSIBL["Author"] = cSIBLFileHeaderAttributes["Header|Author"]
						cExtendedSIBL["Location"] = cSIBLFileHeaderAttributes["Header|Location"]
						cExtendedSIBL["Comment"] = cSIBLFileHeaderAttributes["Header|Comment"]

						# sIBL V2 Format Support.
						if "Header|GEOlat" in cSIBLFileHeaderAttributes and "Header|GEOlong" in cSIBLFileHeaderAttributes :
							cExtendedSIBL["GPS Latitude"] = cSIBLFileHeaderAttributes["Header|GEOlat"]
							cExtendedSIBL["GPS Longitude"] = cSIBLFileHeaderAttributes["Header|GEOlong"]
						if "Header|Link" in cSIBLFileHeaderAttributes :
							cExtendedSIBL["Link"] = cSIBLFileHeaderAttributes["Header|Link"]
						if "Header|Date" in cSIBLFileHeaderAttributes :
							cExtendedSIBL["Date"] = cSIBLFileHeaderAttributes["Header|Date"]
						if "Header|Time" in cSIBLFileHeaderAttributes :
							cExtendedSIBL["Time"] = cSIBLFileHeaderAttributes["Header|Time"]

						cCombinedGlobalCollection[sIBL] = cExtendedSIBL
					except :
						sIBL_GUI_QWidgets.sIBL_GUI_Message( "Warning", "Warning", "'" + cCollection[sIBL] + "' File Seems To Be Corrupted And Will Be Ignored !" )
			else:
				sIBL_GUI_QWidgets.sIBL_GUI_Message( "Warning", "Warning", "'" + collection + "'" + " Collection Returned No Sets !" )
		cLogger.debug( "> Current Extended Collection : '%s'.", cCombinedGlobalCollection )

		return cCombinedGlobalCollection

	@sIBL_Common.sIBL_Execution_Call
	def getRequestedCollectionInfosList( self, cInfo ) :
		'''
		This Method Gets Specific Filtered Collection Informations List.

		@param cInfo: Current Requested Info Type. ( String )
		@return: Informations List. ( List )
		'''

		cList = []
		for sIBL in self.cFilteredCollection.keys() :
			cSIBLAttributes = self.cFilteredCollection[sIBL]
			for attribute in cSIBLAttributes:
				if attribute is cInfo and cSIBLAttributes[attribute] not in cList:
					cList.append( cSIBLAttributes[attribute] )
		cLogger.debug( "> %s(s) : '%s'.", cInfo, cList )
		return cList

	@sIBL_Common.sIBL_Execution_Call
	def getRequestedTemplatesInfosList( self, cInfo ) :
		'''
		This Method Gets Specific Templates Informations List.

		@param cInfo: Current Requested Info Type. ( String )
		@return: Informations List. ( List )
		'''

		cList = []
		for cTemplate in self.cGlobalTemplates.keys() :
			cTemplateAttributes = self.cGlobalTemplates[cTemplate]
			for attribute in cTemplateAttributes:
				if attribute == cInfo and cTemplateAttributes[attribute] not in cList:
					cList.append( cTemplateAttributes[attribute] )
		cLogger.debug( "> %s(s) : '%s'.", cInfo, cList )
		return cList

	@sIBL_Common.sIBL_Execution_Call
	def sIBL_GUI_tabWidget_OnChanged( self, *__None__ ) :
		'''
		This Method Triggers Some Random Actions When A Tab Is Changed.
		'''

		if self.cTemplates_Changed :
			self.initializeTemplatesRelationships()
			self.cTemplates_Changed = False

		if self.cHelp_Changed :
			self.initializeHelpRelationships()
			self.cHelp_Changed = False

	@sIBL_Common.sIBL_Execution_Call
	def getFormatedShotDate( self, cDate, cTime ):
		'''
		This Method Returns A Formatted Shot Date.

		@param cDate: sIBL Set Date Key Value ( String )
		@param cTime: sIBL Set Time Key Value ( String )
		@return: Current Shot Date ( String )
		'''

		cShotTime = cTime.split( ":" )
		cShotTime = cShotTime[0] + "H" + cShotTime[1]
		cShotDate = cDate.replace( ":", "/" )[2:] + " - " + cShotTime

		return cShotDate

	@sIBL_Common.sIBL_Execution_Call
	def getNiceName( self, cString ) :
		'''
		This Method Converts A String To Nice String : currentLogText -> Current Log Text.

		@param cString: Current String To Be Nicified. ( String )
		@return: Nicified String. ( String )
		'''

		cNiceName = ""
		for cChar in range( len( cString ) ) :
			if cChar == 0:
				cNiceName += cString[ cChar ].upper()
			else :
				if cString[ cChar ].upper() == cString[ cChar ] :
					cNiceName += " " + cString[ cChar ]
				else:
					cNiceName += cString[ cChar ]
		cLogger.debug( "> '%s' To '%s'.", cString, cNiceName )
		return cNiceName

#***************************************************************************************
#***	Overall Utilities Methods.
#***************************************************************************************
@sIBL_Common.sIBL_Execution_Call
def sIBL_Set_DefaultSettingsFile( cFileName ) :
	'''
	This Method Defines The Default Settings File Content.

	@return: Current Default Settings. ( List )
	'''

	cLogger.debug( "> %s" , "Initializing Default Settings !" )

	cSettings = QSettings( cFileName, QSettings.IniFormat )

	cSettings.beginGroup( "Settings" )
	if platform.system() == "Windows" or platform.system() == "Microsoft":
		cSettings.setValue( "FrameworkPath", QVariant( "sIBL_Framework.exe" ) )
	elif platform.system() == "Linux":
		cSettings.setValue( "FrameworkPath", QVariant( "sIBL_Framework" ) )
	elif platform.system() == "Darwin":
		cSettings.setValue( "FrameworkPath", QVariant( "../../../sIBL_Framework.app/Contents/MacOS/sIBL_Framework" ) )
	cSettings.setValue( "sIBLeditPath", QVariant( "" ) )
	cSettings.setValue( "TemplatesPath", QVariant( "Templates/" ) )
	cSettings.setValue( "HelpFilesPath", QVariant( "Help/" ) )
	cSettings.setValue( "VerbosityLevel", QVariant( "3" ) )
	cSettings.setValue( "OnlineUpdate", QVariant( "1" ) )
	cSettings.setValue( "IgnoreMissingTemplates", QVariant( "0" ) )
	cSettings.setValue( "OpenGL", QVariant( "0" ) )
	cSettings.setValue( "GPSMapAntialiasing", QVariant( "1" ) )
	cSettings.endGroup()
	cSettings.beginGroup( "Collections" )
	cSettings.endGroup()
	cSettings.beginGroup( "Others" )
	cSettings.setValue( "CustomTextEditor", QVariant( "" ) )
	cSettings.setValue( "CustomFileBrowser", QVariant( "" ) )
	cSettings.endGroup()

@sIBL_Common.sIBL_Execution_Call
def sIBL_Set_KeyInSettings( cSection, cKey, cValue ) :
	'''
	This Method Store Provided Key In Settings File.

	@param cSection: Current Section To Save The Key Into. ( String )
	@param cKey: Current Key To Save. ( String )
	@param cValue: Current Key Value To Save. ( Object )
	'''

	cLogger.debug( "> Saving '%s' In '%s' Section With Value : '%s' In Settings File.", cKey, cSection, cValue )
	cSettings.beginGroup( cSection )
	cSettings.setValue( cKey , QVariant( cValue ) )
	cSettings.endGroup()

@sIBL_Common.sIBL_Execution_Call
def sIBL_Get_KeyFromSettings( cSection, cKey ) :
	'''
	This Method Get Key Value From Settings File.

	@param cSection: Current Section To Retrieve Key From. ( String )
	@param cKey: Current Key To Retrieve. ( String )
	@return: Current Key Value. ( String )
	'''

	cLogger.debug( "> Retrieving '%s' In '%s' Section.", cKey, cSection )
	cSettings.beginGroup( cSection )
	cKeyValue = cSettings.value( cKey ).toString()
	cLogger.debug( "> Key Value : '%s'.", cKeyValue )
	cSettings.endGroup()

	# Facts : At Some Point, During The Refactoring Beetween 1.0.0 And 1.3.0,
	# After Changing Many Many Things, It Appears That QJPEG4 Wasn't Working
	# Anymore, It Was Really Strange, When Starting A Fresh Installed sIBL_GUI
	# Everything Was Ok, But When Starting It Back, No More JPEG Files :(
	# After Spending A Bunch Of Time Messing Up The Code, I Finally Narrowed
	# Down The Problem To This Function, And Especially The Return.
	# Casting The Return Value To A String Seems To Do The Trick, There Is Some
	# Voodoo Magic I Don't Understand :)

	return str( cKeyValue )

#***********************************************************************************************
#***	Launcher
#***********************************************************************************************
if __name__ == "__main__":

	# Starting The Console Handler.
	cConsoleHandler = logging.StreamHandler( sys.stdout )
	cConsoleHandler.setFormatter( sIBL_Common.cFormatter )
	cLogger.addHandler( cConsoleHandler )

	# Getting An Absolute LogFile Path.
	cSIBL_GUI_LogFile = os.path.join( os.path.abspath( os.getcwd() ), sIBL_GUI_Settings.cSIBL_GUI_LogFile )

	try :
		if os.path.exists( cSIBL_GUI_LogFile ) :
			os.remove( cSIBL_GUI_LogFile )
	except :
		sIBL_GUI_QWidgets.sIBL_Standalone_Message( "Error", "Error", "'%s' File Is Currently Locked By Another Process, Unpredictable Logging Behavior !" % cSIBL_GUI_LogFile )
	finally:
		# Retrieving sIBL_GUI Verbose Level From Settings File.
		cLogger.debug( "> %s", "Initializing sIBL_GUI !" )
		cLogger.debug( "> %s", "Retrieving Stored Verbose Level." )

		cSettingsFile = os.path.join( os.path.abspath( os.getcwd() ), sIBL_GUI_Settings.cSIBL_GUI_SettingsFile )
		if not os.path.exists( cSettingsFile ) :
			sIBL_Set_DefaultSettingsFile( cSettingsFile )
			cSettings = QSettings( cSettingsFile, QSettings.IniFormat )
		else :
			cSettings = QSettings( cSettingsFile, QSettings.IniFormat )
			cVerbosityLevel = int( sIBL_Get_KeyFromSettings( "Settings", "VerbosityLevel" ) )
			cLogger.debug( "> Setting Logger Verbosity Level To : '%s'.", cVerbosityLevel )
			sIBL_Common.sIBL_SetVerbosity_Level( cVerbosityLevel )

		if hasattr( sys, "frozen" ) :
			cConsoleHandler.flush()
			cConsoleHandler.close()
			cLogger.removeHandler( cConsoleHandler )

		try :
			cFileHandler = logging.FileHandler( cSIBL_GUI_LogFile )
			cFileHandler.setFormatter( sIBL_Common.cFormatter )
			cLogger.addHandler( cFileHandler )

		except Exception, cError:
			sIBL_Exceptions.sIBL_Exceptions_Feedback ( cError, "Exception In sIBL_GUI Module | '%s'" % "Failed Accessing The Log File !", True )
			sIBL_GUI_QWidgets.sIBL_Standalone_Message( "Critical", "Critical", "Exception In sIBL_GUI Module | '%s'" % "Failed Accessing The Log File !" )
			sIBL_Common.sIBL_Exit( 1, cLogger, ( cConsoleHandler ) )

		cLogger.info( "-" * sIBL_Common_Settings.cVerboseSeparators )
		cLogger.info( "sIBL_GUI | Copyright ( C ) 2009 Thomas Mansencal - kelsolaar_fool@hotmail.com" )
		cLogger.info( "sIBL_GUI | This Software Is Released Under Terms Of GNU GPL V3 License." )
		cLogger.info( "sIBL_GUI | http: // www.gnu.org / licenses / " )
		cLogger.info( "sIBL_GUI | Version : " + sIBL_Common_Settings.cReleaseVersion )
		cLogger.info( "sIBL_GUI | Session Started At : " + time.strftime( '%X - %x' ) )
		cLogger.info( "-" * sIBL_Common_Settings.cVerboseSeparators )
		cLogger.info( "sIBL_GUI | Starting Interface !" )

		cApplication = QApplication( sys.argv )

		# Initializing SplashScreen.
		cLogger.debug( "> Initializing SplashScreen." )

		cSplashScreenPicture = QPixmap( ":/sIBL_GUI/Resources/sIBL_GUI_SpashScreen.png" )
		cSpashScreen = sIBL_GUI_SplashScreen( cSplashScreenPicture, 0.25 )
		cSpashScreen.setMessage( "sIBL_GUI - " + sIBL_Common_Settings.cReleaseVersion + " | Initializing Interface." )
		cSpashScreen.show()

		cUI = sIBL_GUI()
		cUI.show()

		sys.exit( cApplication.exec_() )

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
