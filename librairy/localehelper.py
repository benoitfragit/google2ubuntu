#!/usr/bin/env python
# -*- coding: utf-8 -*-  
from os.path import expanduser
import locale
import os

RELATIVE_LOCALE_CONFIG_PATH = '/.config/google2ubuntu/locale.conf'

class LocaleHelper:
    def __init__(self, defaultLocale = 'en_EN', languageFolder = os.path.dirname(os.path.abspath(__file__))+'/../i18n/'):
        systemLocale = locale.getlocale()
        
        self.__systemLocale = None
        
        if systemLocale is not None and len(systemLocale) > 0:
            if systemLocale[0] is not None and len(systemLocale[0]) > 0:
                self.__systemLocale = systemLocale[0]
        
        self.__languageFolder = languageFolder
        self.__defaultLocale = defaultLocale
        self.__localeConfPath = expanduser('~')+RELATIVE_LOCALE_CONFIG_PATH
    
    def __getSystemLocale(self):
        if self.__checkIfLocalePresent(self.__systemLocale):
            return self.__systemLocale
        else:
            return self.__defaultLocale
        
    def __getLocaleConfigValue(self):
        configFileHandle = None
        localeConfig = None
        try:
            configFileHandle = open(self.__localeConfPath, 'r')
            localeConfig = configFileHandle.readline().strip('\n')
        except:
            pass
        finally:
            if configFileHandle:
                configFileHandle.close()
        
        if localeConfig is None or localeConfig == '':
            return self.__getSystemLocale()
        else:
            if self.__checkIfLocalePresent(localeConfig):
                return localeConfig
            else:
                return self.__defaultLocale
            
    def __checkIfLocalePresent(self, lang):
        return os.path.isdir(self.__languageFolder+lang) == True
    
    def getLocale(self):
        return self.__getLocaleConfigValue()
