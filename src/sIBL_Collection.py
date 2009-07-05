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
***	sIBL_Collection.py
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
import os
import logging

#***********************************************************************************************
#***	internal Imports
#***********************************************************************************************
import sIBL_Exceptions
import sIBL_Common

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
cLogger = logging.getLogger( "sIBL_Overall_Logger" )

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
class sIBL_Collection( object ):
	'''
	This Class Provides Methods For sIBL Collection Tasks.
	'''

	@sIBL_Common.sIBL_Execution_Call
	def __init__( self, rDirectoryPath ) :
		'''
		This Method Initializes The Class.

		@param rDirectoryPath: Collection Directory ( String )
		'''

		cLogger.debug( "> %s", "Initializing sIBL_Collection() Class." )

		# --- Setting Class Attributes. ---
		self.rDirectoryPath = rDirectoryPath
		cLogger.debug( "> self.rDirectoryPath : '%s'.", self.rDirectoryPath )

	@sIBL_Common.sIBL_Execution_Call
	def getCollectionContent( self ) :
		'''
		This Method Gets sIBL Collection Content As A Dictionary.

		@return: Collection Content ( Dictionary Or None )
		'''

		cRootDirectory = self.rDirectoryPath
		cCollection = None
		if os.path.exists( cRootDirectory ):
			cCollection = {}
			cDirectoryContent = os.listdir( cRootDirectory )
			for item in cDirectoryContent :
				itemPath = cRootDirectory + item
				if os.path.isdir( itemPath ):
					cLogger.debug( "> Current Directory : '%s' In '%s'.", itemPath, cRootDirectory )
				else :
					cLogger.debug( "> Current File : '%s' In '%s'.", itemPath, cRootDirectory )
				if os.path.isdir( itemPath ):
					cSubDirectoryContent = os.listdir( itemPath )
					isValidSIBL = False
					cSIBLFile = ""
					for subItem in cSubDirectoryContent :
						subItemPath = itemPath + "/" + subItem
						if os.path.isdir( subItemPath ):
							cLogger.debug( "> Current Directory : '%s' In '%s'.", subItemPath, itemPath )
						else:
							cLogger.debug( "> Current File : '%s' In '%s'.", subItemPath, itemPath )
						if ".ibl" in subItem :
							if os.path.getsize( subItemPath ) > 64 :
								isValidSIBL = True
								cSIBLFile = subItemPath
								break
							else :
								try:
									raise sIBL_Exceptions.File_Corrupted_Error( "'%s' Seem To Be Corrupted !" % ( subItemPath ) )
								except sIBL_Exceptions.File_Corrupted_Error, cError:
									sIBL_Exceptions.sIBL_Exceptions_Feedback ( cError, "Exception In sIBL_Collection.getCollectionContent() Method | '%s'" % cError.cValue )
					if isValidSIBL :
						cCollection[item] = cSIBLFile
					else :
						try:
							raise sIBL_Exceptions.File_Exist_Error( "'%s' Doesn't Contain Any Valid .ibl file !" % ( itemPath ) )
						except sIBL_Exceptions.File_Exist_Error, cError:
							sIBL_Exceptions.sIBL_Exceptions_Feedback ( cError, "Exception In sIBL_Collection.getCollectionContent() Method | '%s'" % cError.cValue )
		else :
			try:
				raise sIBL_Exceptions.Directory_Exist_Error( "'%s' Is Not A Valid Directory !" % ( cRootDirectory ) )
			except sIBL_Exceptions.Directory_Exist_Error, cError:
				sIBL_Exceptions.sIBL_Exceptions_Feedback ( cError, "Exception In sIBL_Collection.getCollectionContent() Method | '%s'" % cError.cValue )
				return cCollection

		return cCollection

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
