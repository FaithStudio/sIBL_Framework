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
#***********************************************************s************************************
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
***	sIBL_Recursive_Walker.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***      	sIBL Recursive Walker Module
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

#***********************************************************************************************
#***	internal Imports
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
class sIBL_Recursive_Walker( object ):
	'''
	This Class Provides Methods For sIBL Templates Tasks.
	'''

	@sIBL_Common.sIBL_Execution_Call
	def __init__( self, rDirectoryPath ):
		'''
		This Method Initializes The Class.

		@param rDirectoryPath: Root Directory Path To Recurse. ( String )
		'''

		cLogger.debug( "> %s", "Initializing sIBL_Walker() Class." )
		self.rDirectoryPath = rDirectoryPath
		cLogger.debug( "> self.rDirectoryPath : '%s'.", self.rDirectoryPath )

	@sIBL_Common.sIBL_Execution_Call
	def recursiveWalker( self, cFilter = None ):
		'''
		This Method Gets Root Directory Files List As A Dictionnary.

		@return: Files List. ( Dictionary Or None )
		'''
		if cFilter :
			cLogger.debug( "> Current Filter : '%s'.", cFilter )

		cRootDirectory = self.rDirectoryPath
		cFiles = None
		if os.path.exists( cRootDirectory ):
			cFiles = {}
			for root, dirs, files in os.walk( cRootDirectory, topdown = False ):
				for item in files:
					cLogger.debug( "> Current File : '%s' In '%s'.", item, cRootDirectory )
					cItemPath = os.path.join( root, item ).replace( "\\", "/" )
					if os.path.isfile( cItemPath ):
						if cFilter :
							if not cFilter in cItemPath :
								continue
						cFileTokens = os.path.splitext( item )
						if cFileTokens[0] in cFiles:
							cPathTags = cItemPath.replace( cRootDirectory, "" ).replace( "/", "_" ).replace( item, "" )
							cItemName = cPathTags + cFileTokens[0]
							cLogger.debug( "> Adding '%s' With Path : '%s' To File List.", cItemName, cItemPath )
							cFiles[cItemName] = cItemPath
						else:
							cLogger.debug( "> Adding '%s' With Path : '%s' To File List.", cFileTokens[0], cItemPath )
							cFiles[cFileTokens[0]] = cItemPath
		else :
			try:
				raise sIBL_Exceptions.Directory_Exist_Error( "'%s' Is Not A Valid Directory !" % ( cRootDirectory ) )
			except sIBL_Exceptions.Directory_Exist_Error, cError:
				sIBL_Exceptions.sIBL_Exceptions_Feedback ( cError, "Exception In sIBL_Recursive_Walker.recursiveWalker() Method | '%s'" % cError.cValue )
				return cFiles

		return cFiles

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
