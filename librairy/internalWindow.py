#!/usr/bin/env python
# -*- coding: utf-8 -*-  
from gi.repository import Gtk
from gi.repository import Notify
from gi.repository import Gdk
from gi.repository import Gio
from os.path import expanduser
import os, sys, subprocess, gettext, locale
import xml.etree.ElementTree as ET

class internalWindow():
    def __init__(self,store,iter=None):        
        self.grid = Gtk.Grid()
        self.grid.set_border_width(5)
        self.grid.set_row_spacing(5)
        self.grid.set_vexpand(True)
        self.grid.set_hexpand(True)
        self.grid.set_column_spacing(2)
        self.grid.set_column_homogeneous(False)
        self.grid.set_row_homogeneous(False)
        
        label1 = Gtk.Label(_('key sentence'))
        label1.set_justify(Gtk.Justification.LEFT) 
        label1.set_halign(Gtk.Align.START) 
        label1.set_hexpand(True)
        label2 = Gtk.Label(_('your command'))
        label2.set_justify(Gtk.Justification.LEFT) 
        label2.set_halign(Gtk.Align.START)
        ll = Gtk.Label()
        ll.set_vexpand(True)
        self.entry1 = Gtk.Entry()
        if iter is not None:
            self.entry1.set_text(store[iter][0])
            
        self.combo = self.__get_combobox(store,iter)
        button = Gtk.Button.new_from_stock(Gtk.STOCK_OK)
        button.connect("clicked",self.button_clicked,store,iter)
        button_cancel = Gtk.Button.new_from_stock(Gtk.STOCK_CANCEL)
        button_cancel.connect("clicked",self.do_destroy)
        
        
        self.grid.attach(label1,0,0,11,1)
        self.grid.attach(self.entry1,11,0,4,1)
        self.grid.attach(label2,0,1,11,1)
        self.grid.attach(self.combo,11,1,4,1)
        self.grid.attach(ll,0,2,15,1)
        self.grid.attach(button_cancel,13,3,1,1)
        self.grid.attach(button,14,3,1,1)
        self.grid.show_all()
    
    def do_destroy(self,button):
        self.grid.destroy()    
    
    def get_grid(self):
        return self.grid
    
    def button_clicked(self,button,store,iter):
        if iter is None:
            if self.entry1.get_text() is not '':
                store.append([self.entry1.get_text(),str(self.dic[self.combo.get_active()]),_('internal'),' ',' '])
                self.saveTree(store)
        else:
            store[iter][0] = str(self.entry1.get_text())
            store[iter][1] = str(self.dic[self.combo.get_active()])
            self.saveTree(store)
        
        self.grid.destroy()
        
    # return a combobox to add to the toolbar
    def __get_combobox(self,store,iter):
        """
        @description: get the combobox of the toolbar
        
        @return: a Gtk.Combobox
        """
        # the data in the model, of type string
        listmodel = Gtk.ListStore(str)
        # append the data in the model
        self.dic = {}
        self.dic[0] = _('time')
        listmodel.append([_('time')])
        self.dic[1] = _('power')
        listmodel.append([_('power')])
        self.dic[2] = _('clipboard')
        listmodel.append([_('clipboard')])
        self.dic[3] = _('dictation mode')
        listmodel.append([_('dictation mode')])
        self.dic[4] = _('exit dictation mode')
        listmodel.append([_('exit dictation mode')])
        
        selected = 0
        if iter is not None:
            for i in range(len(self.dic)):
                if self.dic[i] == store[iter][1]:
                    selected = i
                    
        # a combobox to see the data stored in the model
        combobox = Gtk.ComboBox(model=listmodel)
        combobox.set_tooltip_text(_("Which internal command to choose")+'?')

        # a cellrenderer to render the text
        cell = Gtk.CellRendererText()

        # pack the cell into the beginning of the combobox, allocating
        # no more space than needed
        combobox.pack_start(cell, False)
        # associate a property ("text") of the cellrenderer (cell) to a column (column 0)
        # in the model used by the combobox
        combobox.add_attribute(cell, "text", 0)

        # the first row is the active one by default at the beginning
        combobox.set_active(selected)

        return combobox

    def saveTree(self,store):
        """
        @description: save the treeview in the google2ubuntu.xml file
        
        @param: store
            the listStore attach to the treeview
        """
        # if there is still an entry in the model
        config = expanduser('~') +'/.config/google2ubuntu/google2ubuntu.xml'     
        try:
            if not os.path.exists(os.path.dirname(config)):
                os.makedirs(os.path.dirname(config))            
            
            root = ET.Element("data")
            if len(store) != 0:
                for i in range(len(store)):
                    iter = store.get_iter(i)
                    if store[iter][0] != '' and store[iter][1] != '':
                        for s in store[iter][0].split('|'):
                            s = s.lower()
                            s = s.replace('*',' ')
                            Type = ET.SubElement(root, "entry")
                            Type.set("name",unicode(store[iter][2],"utf-8"))
                            Key = ET.SubElement(Type, "key")
                            Key.text = unicode(s,"utf-8")
                            Command = ET.SubElement(Type, "command")
                            Command.text = unicode(store[iter][1],"utf-8")
                            Linker = ET.SubElement(Type, "linker") 
                            Spacebyplus = ET.SubElement(Type, "spacebyplus")
                            if store[iter][3] is not None and store[iter][4] is not None:
                                Linker.text = unicode(store[iter][3],"utf-8")
                                Spacebyplus.text = unicode(store[iter][4],"utf-8")
                
            tree = ET.ElementTree(root).write(config,encoding="utf-8",xml_declaration=True)

        except IOError:
            print "Unable to write the file"    
