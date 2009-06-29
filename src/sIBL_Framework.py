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
***	sIBL_Framework.py
***
***	Platform :
***		Windows, Linux, Mac Os X
***
***	Description :
***      	sIBL Framework Command Line Module.
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
import optparse
import os
import sys
import time

#***********************************************************************************************
#***	Internal Imports
#***********************************************************************************************
import sIBL_Common_Settings
import sIBL_Exceptions
import sIBL_Parser

#***********************************************************************************************
#***	Global Variables
#***********************************************************************************************
cLogger = logging.getLogger( "sIBL_Overall_Logger" )

#***********************************************************************************************
#***	Module Classes And Definitions
#***********************************************************************************************
@sIBL_Common.sIBL_Execution_Call
def sIBL_About_Framework( *cArgs, **cKwArgs ):
	'''
	This Definition Prints The About Argument Stuff.
	'''

	print "sIBL_Framework - Version '%s'" % sIBL_Common_Settings.cReleaseVersion
	print "Thomas Mansencal - 2008"
	print "kelsolaar_fool@hotmail.com"

@sIBL_Common.sIBL_Execution_Call
def sIBL_GetOverrideKeys( cOverrideKeys ):
	'''
	This Definition Gets The Override cKey Command Line Argument And Conform It.

	@param cOverrideKeys: Override Keys To Process. ( String )
	@return: Processed Override Keys. ( Dictionary )
	'''

	cLogger.debug( "> Current Override Keys Argument : '%s'.", cOverrideKeys )

	cFinalOKeys = None

	try :
		cFinalOKeys = {}
		cOKeysTokens = cOverrideKeys.split( "," )
		for cToken in cOKeysTokens :
			cSubTokens = cToken.split( "=" )
			cFinalOKeys[cSubTokens[0].strip()] = cSubTokens[1].strip()
	except Exception :
		cLogger.error( "Exception In sIBL_GetOverrideKeys() Definition | '%s'", "Invalid Override Keys Formating !" )
		return None

	cLogger.debug( "> Processed Override Keys : '%s'.", cFinalOKeys )
	return cFinalOKeys

@sIBL_Common.sIBL_Execution_Call
def sIBL_Framework( sIBLFile, cTemplateFile, cOutputFile, cOverrideKeys ):
	'''
	This Definition Outputs The Loader Script File By Processing The sIBL File And The Template File.

	@param sIBLFile: Current sIBL File Path. ( String )
	@param cTemplateFile: Current Template File Path. ( String )
	@param cOutputFile: Current Loader Script Output Path. ( String )
	@param cOverrideKeys: Current Provided Override Keys. ( String )
	@return: Error State Of The Output And Output File Path. ( Boolean, String )
	'''

	sIBLPath = os.path.abspath( os.path.dirname( sIBLFile ) ).replace( "\\", "/" ) + "/"
	cLogger.debug( "> Current sIBLPath : '%s'.", sIBLPath )

	# Get sIBL File Concatened Sections Attributes.
	cLogger.debug( "> ------ Parsing '%s' File ------", "sIBL" )
	cSIBLFile = sIBL_Parser.sIBL_Parser( sIBLFile )

	if cSIBLFile is  None :
		return False, None
	cSIBLFileSections = cSIBLFile.getSections()

	# If .IBL File Seem Corrupted Or Invalid.
	if cSIBLFileSections is None :
		return False, None

	cSIBLSectionsAttributes = {}
	cDynamicLights = []
	for cSection in cSIBLFileSections.keys():
		cLogger.debug( "> Current sIBL File Section : '%s'.", cSection )
		if not "Light" in cSection :
			cSIBLSectionsAttributes.update( cSIBLFile.getSectionAttributes( cSection ) )
		else :
			# Dynamic Lights Attributes
			cLightAttributes = cSIBLFile.getSectionAttributes( cSection, True )
			cDynamicLights.append( cSection )
			cDynamicLights.append( cLightAttributes["LIGHTname"] )
			cLightColorTokens = cLightAttributes["LIGHTcolor"].split( "," )
			for cColor in cLightColorTokens:
				cDynamicLights.append( cColor )
			cDynamicLights.append( cLightAttributes["LIGHTmulti"] )
			cDynamicLights.append( cLightAttributes["LIGHTu"] )
			cDynamicLights.append( cLightAttributes["LIGHTv"] )

			cLogger.debug( "> Dynamic Lights : '%s'.", cDynamicLights )

	# Preparing The Dynamic Lights String
	cDynamicLightsString = ""
	for cComponent in cDynamicLights :
		cDynamicLightsString = cDynamicLightsString + cComponent + "|"

	# Adding The Dynamic Lights String
	if cDynamicLightsString == "" :
		cDynamicLightsString = "-1"
	else :
		cDynamicLightsString = cDynamicLightsString[:-1]

	print cDynamicLightsString
	cSIBLSectionsAttributes[sIBL_Parser.sIBL_CompoundNamespace( "Lights", "DynamicLights" )] = cDynamicLightsString

	# Get Template File Sections.
	cLogger.debug( "> ------ Parsing '%s' File ------", "Template" )
	cTemplateFile = sIBL_Parser.sIBL_Parser( cTemplateFile )

	if cTemplateFile is None :
		return False, None
	cTemplateFileSections = cTemplateFile.getSections()

	# If Template File Seem Corrupted Or Invalid.
	if cTemplateFileSections is None :
		return False, None

	# Get Template File Concatened Sections Attributes And Values.
	cTemplateSectionsAttributesStore = {}

	for cKey in cTemplateFileSections.keys():
		if cKey != "Script" :
			cLogger.debug( "> Current Template File Processed Section : '%s'.", cKey )
			if cKey == "sIBL File Attributes" :
				cTemplateSectionsAttributesStore.update( cTemplateFile.getSectionAttributes( cKey, True ) )
			else :
				cTemplateSectionsAttributesStore.update( cTemplateFile.getSectionAttributes( cKey ) )

	# Get A Copy Of Template File Concatened Sections Attributes In Order To Update It.
	cTemplateSectionsAttributes = cTemplateSectionsAttributesStore.copy()

	# Update Template File Attributes With sIBL File Ones.
	for cKey in cTemplateSectionsAttributes:
		if cKey in cSIBLSectionsAttributes :
			# Updating Path To The File.
			if "file" in cKey:
				cTemplateSectionsAttributes[cKey] = sIBLPath + cSIBLSectionsAttributes[cKey]
			else :
				cTemplateSectionsAttributes[cKey] = cSIBLSectionsAttributes[cKey]
		else :
			# Need An Number Here More Than A String Here, Or Typed Variables Script Will Need To Write Cast Functions.
			cTemplateSectionsAttributes[cKey] = "-1"
			# cTemplateSectionsAttributes[cKey] = "\"Not Available\""

	# Get Default Values, Types And Update Template Attributes With Default Values.
	cTemplateSectionsAttributesValues = {}
	cTemplateSectionsAttributesTypes = {}
	for cKey in cTemplateSectionsAttributesStore:
		if "|" in cTemplateSectionsAttributesStore[cKey] :
			cTemplateSectionsAttributesValues[cKey] = sIBL_Parser.sIBL_GetExtraAttributeComponents( cTemplateSectionsAttributesStore[cKey], "Value" )
			cTemplateSectionsAttributesTypes[cKey] = sIBL_Parser.sIBL_GetExtraAttributeComponents( cTemplateSectionsAttributesStore[cKey], "Type" )
			cTemplateSectionsAttributesStore[cKey] = sIBL_Parser.sIBL_GetExtraAttributeComponents( cTemplateSectionsAttributesStore[cKey], "Attribute Link Name" )

	cTemplateSectionsAttributes.update( cTemplateSectionsAttributesValues )

	# Manually Updating Template Attributes With Override Keys (Manual In Order To Not Transmit Erroneus Keys).
	if cOverrideKeys is not None :
		for cKey in cOverrideKeys :
			if cKey in cTemplateSectionsAttributes :
				cTemplateSectionsAttributes[cKey] = cOverrideKeys[cKey]
			else :
				try:
					raise sIBL_Exceptions.Invalid_Key_Error( "Invalid cKey Provided ! : '%s'" % cKey )
				except sIBL_Exceptions.Invalid_Key_Error, cError:
					sIBL_Exceptions.sIBL_Exceptions_Feedback ( cError, "Exception In sIBL_Framework Main() Definition | '%s'" % cError.cValue )
					return False, None

	# Processing The Final Script.
	cLogger.debug( "> ------ Processing '%s' ------", "Output Loader Script" )
	cScriptContent = cTemplateFileSections["Script"]

	if cTemplateSectionsAttributes["Template|OutputScript"] is not None :
		scriptOutputName = cTemplateSectionsAttributes["Template|OutputScript"]
	else :
		cOutputName = "Undefined_sIBL_Framework_Output_Script"
		cLogger.warning( "> Output Script Name Not Found In Template File, Current Output Loader Script Name : '%s'.", cOutputName )
		scriptOutputName = cOutputName

	for i in range( 0, len( cScriptContent ) ):
		cScriptContent[i] = cScriptContent[i] + "\n"
		if "@" in cScriptContent[i]:
			for cKey in cTemplateSectionsAttributes:
				if cTemplateSectionsAttributesStore[cKey] in cScriptContent[i]:
					cLogger.debug( "> Output Loader Script 'cKey = Value' : '%s' = '%s'.", cKey, str( cTemplateSectionsAttributes[cKey] ) )
					nLine = cScriptContent[i].replace( cTemplateSectionsAttributesStore[cKey], str( cTemplateSectionsAttributes[cKey] ) )
					cScriptContent[i] = nLine

	if cOutputFile is None :
		cEnvVariable = sIBL_Common.sIBL_GetTemporarySystemPath()
		if cEnvVariable is not None :
			cScriptFilePath = cEnvVariable.replace( "\\", "/" ) + scriptOutputName
		else :
			cLogger.error( "> Can't Output Loader Script : '%s'.", "No 'TMP' Or 'TMPDIR' Environment Variables Found on the Current System !" )
			return False, None
	else :
		cScriptFilePath = cOutputFile.replace( "\\", "/" )

	cScriptFile = sIBL_Common.sIBL_File( cScriptFilePath )
	cScriptFile.setFileContent( cScriptContent )

	return True , cScriptFilePath

@sIBL_Common.sIBL_Execution_Call
def sIBL_GetCommandLineParameters( argv ):
	'''
	This Definition Process Command Line Arguments.

	@param argv: Command Line Parameters. ( String )
	@return: Settings, Arguments ( Parser Instance )
	'''

	if argv is None:
		argv = sys.argv[1:]

	parser = optparse.OptionParser( formatter = optparse.IndentedHelpFormatter ( indent_increment = 2, max_help_position = 8, width = 128, short_first = 1 ), add_help_option = None )

	parser.add_option( "-h", "--help", action = "help", help = "'Show This Help Message And Exit'" )
	parser.add_option( "-a", "--about", action = "store_true", default = False, dest = "cAboutValue", help = "'Print About sIBL_Framework'" )
	parser.add_option( "-i", "--input", action = "store", dest = "sIBLFile", help = "'.IBL Input File'" )
	parser.add_option( "-t", "--template", action = "store", dest = "cTemplateFile", help = "'Template Input File'" )
	parser.add_option( "-k", "--keys", action = "store", dest = "oKeys", help = "'Custom Override Keys, Format : \"A = ValueA, B = ValueB\"'" )
	parser.add_option( "-o", "--output", action = "store", dest = "cOutputFile", help = "'Output Loader Script File'" )
	parser.add_option( "-v", "--verbose", action = "store", type = "int", dest = "cVerbosityLevel", help = "'sIBL Verbosity Level :  0 = No Verbose | 1 = Error | 2 = Error, Info | 3 = Error, Info, Debug'" )

	settings, args = parser.parse_args( argv )

	if args:
		parser.error( 'This Program Takes No Command-Line Arguments; ''"%s" Ignored.' % ( args, ) )

	return settings, args

#***********************************************************************************************
#***	Main Definition
#***********************************************************************************************
@sIBL_Common.sIBL_Execution_Call
def sIBL_Framework_Executable( argv = None ):
	'''
	This Definition Is sIBL_Framework Main() Definition.

	@param argv: Command Line Arguments ( None )
	'''

	settings, args = sIBL_GetCommandLineParameters( argv )

	if settings.cVerbosityLevel is not None :
		sIBL_Common.sIBL_SetVerbosity_Level( settings.cVerbosityLevel )

	if settings.cAboutValue is False :
		if settings.sIBLFile is None :
			try:
				raise sIBL_Exceptions.Command_Line_Error( "An Input .sIBL File Is Required !" )
			except sIBL_Exceptions.Command_Line_Error, cError:
				sIBL_Exceptions.sIBL_Exceptions_Feedback ( cError, "Exception In sIBL_Framework Main() Definition | '%s'" % cError.cValue )
				return 1

		if not os.path.isfile( settings.sIBLFile ):
			try:
				raise sIBL_Exceptions.File_Exist_Error( "Input .IBL File Does Not Exist !" )
			except sIBL_Exceptions.File_Exist_Error, cError:
				sIBL_Exceptions.sIBL_Exceptions_Feedback ( cError, "Exception In sIBL_Framework Main() Definition | '%s'" % cError.cValue )
				return 1

		if settings.cTemplateFile is None :
			try:
				raise sIBL_Exceptions.Command_Line_Error( "An Input Template File Is Required !" )
			except sIBL_Exceptions.Command_Line_Error, cError:
				sIBL_Exceptions.sIBL_Exceptions_Feedback ( cError, "Exception In sIBL_Framework Main() Definition | '%s'" % cError.cValue )
				return 1

		if not os.path.isfile( settings.cTemplateFile ):
			try:
				raise sIBL_Exceptions.File_Exist_Error( "Input Template File Does Not Exist !" )
			except sIBL_Exceptions.File_Exist_Error, cError:
				sIBL_Exceptions.sIBL_Exceptions_Feedback ( cError, "Exception In sIBL_Framework Main() Definition | '%s'" % cError.cValue )
				return 1

		if settings.oKeys is not None :
			oKeys = sIBL_GetOverrideKeys( settings.oKeys )
			if oKeys is None :
				return 1
		else :
			cLogger.warning( "> No Override Keys Provided, Using \"'%s'\" Template Default Values !", os.path.basename( settings.cTemplateFile ) )
			oKeys = None

		cFrameworkExitStatus, cScriptFilePath = sIBL_Framework( settings.sIBLFile, settings.cTemplateFile, settings.cOutputFile, oKeys )

		if cFrameworkExitStatus :
			cLogger.info( "'%s' Output Done !", cScriptFilePath )
			sIBL_Common.sIBL_Exit( 0, cLogger, ( cConsoleHandler, cFileHandler ) )
		else :
			cLogger.error( "Exception In sIBL_Framework Main() Definition | Output Failed !" )
			sIBL_Common.sIBL_Exit( 1, cLogger, ( cConsoleHandler, cFileHandler ) )
	else :
		sIBL_About_Framework()

#***********************************************************************************************
#***	Launcher
#***********************************************************************************************
if __name__ == '__main__':

	# Starting The Console Handler.
	cConsoleHandler = logging.StreamHandler( sys.stdout )
	cConsoleHandler.setFormatter( sIBL_Common.cFormatter )
	cLogger.addHandler( cConsoleHandler )

	# Getting An Absolute LogFile Path.
	cSIBL_Framework_LogFile = os.path.join( os.path.abspath( os.getcwd() ), sIBL_Common_Settings.cSIBL_Framework_LogFile )
	cLogger.critical( cSIBL_Framework_LogFile )
	try :
		if os.path.exists( cSIBL_Framework_LogFile ):
			os.remove( cSIBL_Framework_LogFile )
	except Exception, cError:
		sIBL_Exceptions.sIBL_Exceptions_Feedback ( cError, None, True )
	finally :
		try :
			cFileHandler = logging.FileHandler( cSIBL_Framework_LogFile )
			cFileHandler.setFormatter( sIBL_Common.cFormatter )
			cLogger.addHandler( cFileHandler )
		except Exception, cError:
			sIBL_Exceptions.sIBL_Exceptions_Feedback ( cError, "Exception In sIBL_Framework Module | '%s'" % "Failed Accessing The Log File !", True )

		cLogger.info( "-" * sIBL_Common_Settings.cVerboseSeparators )
		cLogger.info( "sIBL_Framework | Copyright (C) 2009 Thomas Mansencal - kelsolaar_fool@hotmail.com" )
		cLogger.info( "sIBL_Framework | This Software Is Released Under Terms Of GNU GPL V3 License." )
		cLogger.info( "sIBL_Framework | http://www.gnu.org/licenses/" )
		cLogger.info( "sIBL_Framework | Version : " + sIBL_Common_Settings.cReleaseVersion )
		cLogger.info( "sIBL_Framework | Session Started At : " + time.strftime( '%X - %x' ) )
		cLogger.info( "-" * sIBL_Common_Settings.cVerboseSeparators )
		cLogger.info( "sIBL_Framework | " + "Starting Processing !" )

		sys.exit( sIBL_Framework_Executable() )

#***********************************************************************************************
#***	Python End
#***********************************************************************************************
