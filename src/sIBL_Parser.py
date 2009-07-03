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
***	sIBL_Parser.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***      	sIBL Input And Output Module.
***
***	Others :
***
************************************************************************************************
'''

#***********************************************************************************************
#***	Python Begin
#***********************************************************************************************

#***********************************************************************************************
#***	Externals Imports
#***********************************************************************************************
import logging
import re

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
class sIBL_Parser( sIBL_Common.sIBL_File ):
	'''
	This Class Provide Methods To Reads .IBL / Templates Files And Return Associated Dictionnary.
	'''

	@sIBL_Common.sIBL_Execution_Call
	def __init__( self, filePath ):
		'''
		This Method Initializes The Class.

		@param filePath: Current File Path. ( String )
		'''

		cLogger.debug( "> %s", "Initializing sIBL_Parser() Class." )
		cLogger.debug( "> self.filePath : '%s'.", filePath )

		# --- Setting Class Attributes. ---
		self.filePath = filePath

		self.cFileContent = self.getFileContent()
		self.cFileSections = None

	@sIBL_Common.sIBL_Execution_Call
	def getSections( self, cSectionsOnly = None ):
		'''
		This Method Gets The File Content And Process It To Extract The Sections As A Dictionnary.

		@return: Current File Sections. ( Dictionary Or None )
		'''

		cLogger.debug( "> Reading Sections From : '%s'.", self.filePath )
		try :
			if re.search( "^\[Header\]|^\[Template\]|^\[sIBL_GUI\]", self.cFileContent[0] ) :
				self.cFileSections = {}
				cSectionAttributes = []
				for cLine in self.cFileContent:
					if re.search( "^\[.*\]", cLine ):
						cSectionKey = re.search( "(?<=^\[)(.*)(?=\])", cLine )
						cSectionKey = cSectionKey.group( 0 )
						cSectionAttributes = []
					else:
						if re.search( "^\n", cLine ) or re.search( "^\r\n", cLine ) :
							cSectionAttributes.append( "" )
						else :
							cSectionAttributes.append( cLine.rstrip() )

					if cSectionsOnly :
						self.cFileSections[cSectionKey] = ""
					else :
						self.cFileSections[cSectionKey] = cSectionAttributes
			else:
				try:
					raise sIBL_Exceptions.File_Content_Error( "Provided File '%s' Seems Incompatible With sIBL_Parser !" % self.filePath )
				except sIBL_Exceptions.File_Content_Error, cError:
					sIBL_Exceptions.sIBL_Exceptions_Feedback ( cError, "Exception In sIBL_Parser.getSections() Method | '%s'" % cError.cValue )
					return self.cFileSections
		except Exception, cError:
			sIBL_Exceptions.sIBL_Exceptions_Feedback ( cError, "Exception In sIBL_Parser.getSections() Method | '%s'" % cError.cValue, True )
		finally :
			if self.cFileSections is not None:
				cLogger.debug( "> Current File Sections : '%s'.", self.cFileSections.keys() )
			return self.cFileSections

	@sIBL_Common.sIBL_Execution_Call
	def getSectionAttributes( self, cSection, cNamespaceStrip = None ):
		'''
		This Method Gets The File Sections And Process Them To Extract The Sections Attributes As A Dictionnary.

		@param cSection: Provided Section To Retrieve Attributes From. ( String )
		@return: Current Section Attributes. ( Dictionary Or None )
		'''

		if self.cFileSections is None :
			self.cFileSections = self.getSections()

		attributesList = None
		try :
			attributesList = {}
			for cAttribute in self.cFileSections[cSection]:
				if cAttribute.startswith( "--" ):
					attributesList["nComment"] = cAttribute.strip( "--" )
				# sIBL V2 Format Support.
				elif cAttribute.startswith( ";" ):
					attributesList["nComment"] = cAttribute.strip( ";" )
				else:
					cAttributeTokens = cAttribute.split( "=" )
					if cNamespaceStrip :
						attributesList[cAttributeTokens[0].strip()] = cAttributeTokens[1].strip().strip( "\"" )
					else :
						attributesList[cSection + "|" + cAttributeTokens[0].strip()] = cAttributeTokens[1].strip().strip( "\"" )

		except Exception, cError:
			sIBL_Exceptions.sIBL_Exceptions_Feedback ( cError, "Exception In sIBL_Parser.getSectionAttributes() Method | '%s'" % cError.cValue, True )
		finally :
			cLogger.debug( "> Current Section Attributes : '%s'.", attributesList.keys() )
			return attributesList

	@sIBL_Common.sIBL_Execution_Call
	def getAttributeValue( self, cSection, cAttribute ):
		'''
		This Method Returns The Seeked Attribute Value.

		@param cSection: Section Containing The Seeked Attribute. ( String )
		@param cAttribute: Attribute To Retrieve The Value. ( String )
		@return: Current Attribute Value. ( String )
		'''

		cAttribute = sIBL_CompoundNamespace( cSection, cAttribute )
		cSectionAttributes = self.getSectionAttributes( cSection )
		if cAttribute in cSectionAttributes.keys():
			return cSectionAttributes[cAttribute]
		else :
			return None

@sIBL_Common.sIBL_Execution_Call
def sIBL_CompoundNamespace( cSection, cAttribute ):
	'''
	This Method Returns The Compounded Attribute And Compounded Namespace.

	@param cSection: Section ( String )
	@param cAttribute: Attribute. ( String )
	@return: Current Compounded Attribute. ( String )
	'''

	return str( cSection + "|" + cAttribute )

@sIBL_Common.sIBL_Execution_Call
def sIBL_StripNamespace( cAttribute ):
	'''
	This Method Returns The Compounded Attribute And Compounded Namespace.

	@param cSection: Section ( String )
	@param cAttribute: Attribute. ( String )
	@return: Current Compounded Attribute. ( String )
	'''

	cAttributeTokens = cAttribute.split( "|" )
	return cAttributeTokens[len( cAttributeTokens ) - 1]

@sIBL_Common.sIBL_Execution_Call
def sIBL_GetExtraAttributeComponents( cAttributeValue, cKey ):
	'''
	This Definition Gets Extra Section Attributes Components As A Dictionnary.

	@return: Current Attribute Components. ( Dictionary Or None )
	'''
	if cAttributeValue is not None :
		cLogger.debug( "> Current Attribute Values : '%s'.", cAttributeValue )
		cLogger.debug( "> Current Seeked Key : '%s'.", cKey )

		allTokens = None
		if "|" in cAttributeValue :
			cAttributeTokens = cAttributeValue.split( "|" )
			allTokens = {}
			allTokens["Attribute Link Name"] = cAttributeTokens[0].strip()
			allTokens["Value"] = cAttributeTokens[1].strip()
			allTokens["Type"] = cAttributeTokens[2].strip()
			if len( cAttributeTokens ) == 4:
				allTokens["Attribute Name"] = cAttributeTokens[3].strip()
			else:
				allTokens["Attribute Name"] = None
			cLogger.debug( "> Current Key Value : '%s'.", allTokens[cKey] )
			return allTokens[cKey]
		else :
			try:
				raise sIBL_Exceptions.Invalid_Attribute_Error( "Provided Attribute Is Not And Extra Attribute" )
			except sIBL_Exceptions.File_Content_Error, cError:
				sIBL_Exceptions.sIBL_Exceptions_Feedback ( cError, "Exception In sIBL_Parser.sIBL_GetExtraAttributeComponents() Method | '%s'" % cError.cValue )
				return allTokens

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
