#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re, os, sys, gettext

gettext.install('way',os.path.dirname(os.path.abspath(__file__))+'/i18n/')

if len(sys.argv) >= 2:
    s = sys.argv[1]
    
    # this words will be translate
    l1 = _('between')
    l2 = _('and')
    print l1, l2    
    
    cities = re.findall(l1+r' ?([^\'">]+) '+l2+r' ?([^\'">]+)',s)
    print cities
    if len(cities[0]) >= 2: 
        os.system('exo-open '+'"https://maps.google.fr/maps?saddr='+cities[0][0]+'&daddr='+cities[0][1]+' &"')
