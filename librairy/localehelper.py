#!/usr/bin/env python
# -*- coding: utf-8 -*-  
from os.path import expanduser
import locale
import os

RELATIVE_LOCALE_CONFIG_PATH = '/.config/google2ubuntu/google2ubuntu.conf'

class LocaleHelper:
    def __init__(self, defaultLocale='en_EN', languageFolder=os.path.dirname(os.path.abspath(__file__)) + '/../i18n/'):
        systemLocale = locale.getlocale()
        
        self.__systemLocale = None
        
        if systemLocale is not None and len(systemLocale) > 0:
            if systemLocale[0] is not None and len(systemLocale[0]) > 0:
                self.__systemLocale = systemLocale[0]
        
        self.__languageFolder = languageFolder
        self.__defaultLocale = defaultLocale
        self.__localeConfPath = expanduser('~') + RELATIVE_LOCALE_CONFIG_PATH
    
    def __getSystemLocale(self):
        if self.__checkIfLocalePresent(self.__systemLocale):
            return self.__systemLocale
        else:
            fallback = self.__getLocaleFallbackValue(self.__systemLocale)
            if self.__checkIfLocalePresent(fallback):
                return fallback
            else:
                return self.__defaultLocale

    def __readSingleLine(self, filePath):
        fileHandle = None
        line = None
        try:
            fileHandle = open(filePath, 'r')
            line = fileHandle.readline().strip('\n')
        except:
            pass
        finally:
            if fileHandle:
                fileHandle.close()
        return line

    def __getLocaleConfigValue(self):
        fileHandle = None
        lc = None
        try:
            fileHandle = open(self.__localeConfPath, 'r')
            for ligne in fileHandle.readlines():
                ligne = ligne.strip('\n')
                field=ligne.split('=')
                if field[0] == 'locale':
                    lc = field[1]

        except:
            pass
        finally:
            if fileHandle:
                fileHandle.close()
        if self.__checkIfLocalePresent(lc):
            return lc
        else:
            return self.__getSystemLocale()

    def __getLocaleFallbackValue(self, lang):
        if lang is not None and lang != '':
            return self.__readSingleLine(self.__languageFolder + lang + '/fallback')
        return None

    def __checkIfLocalePresent(self, lang):
        if lang is not None:
            if lang.strip() != '' and os.path.isdir(self.__languageFolder + lang + '/LC_MESSAGES') == True:
                return True
        
        return False
    
    def getFormatedLocaleString(self, localeString, longFormat=True):
        if localeString is None:
            return None
        elif localeString.strip() == '':
            return None

        localeString = localeString.replace(' ', '')

        if '_' not in localeString and longFormat == True:
            localeString = localeString + '_' + localeString.upper()
        elif '_' in localeString and longFormat == False:
            localeString = localeString.split('_')[0]
        
        return localeString
    
    def getLocale(self, longFormat=True):
        return self.getFormatedLocaleString(self.__getLocaleConfigValue(), longFormat)
