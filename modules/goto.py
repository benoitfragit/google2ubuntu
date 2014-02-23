#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys,os, re

if len(sys.argv) >= 2:
    web = sys.argv[1]
    web = web.replace(' ','+')
    web = web.lower()
    
    url = 'www.'+web
    os.system('xdg-open '+url+' &')
