#!/usr/bin/env python
# -*- coding: utf-8 -*-  
from gi.repository import Gtk
from gi.repository import Notify
from gi.repository import Gdk
from gi.repository import Gio
from os.path import expanduser
import os, sys, subprocess, gettext

# gère l'apparition de la fenêtre d'assistance de création de module
class ArgsWindow():
    """
    @description: Display a window to help the user create a config for a
    module
    
    @param module
        module's folder
    
    @param name
        module's name
    
    @param store
        a Gtk.Listore in which we will append a new line for this module
    """
    def __init__(self,module,name,store,exist=False):
        self.w = Gtk.Window()
        self.w.set_title(_("Module setup"))
        self.w.set_resizable(False)     
        self.w.get_focus()
        self.w.set_position(Gtk.WindowPosition.CENTER)      
        self.w.set_default_size(300,300)  
        self.w.set_border_width(5)
        
        grid = Gtk.Grid()
        label1 = Gtk.Label(_("Linking word"))
        label1.set_justify(Gtk.Justification.LEFT) 
        label1.set_halign(Gtk.Align.START) 
        self.entry1 = Gtk.Entry()
        self.entry1.set_tooltip_text(_("Word to separate call and parameter"))
        self.checkbutton = Gtk.CheckButton()
        self.checkbutton.set_label(_("Replace space by plus"))
        self.checkbutton.set_tooltip_text(_("Replace space by plus"))
        self.checkbutton.set_active(False)
        button = Gtk.Button()
        button.set_label(_("Go"))
        button.set_tooltip_text(_("Go"))
        image = Gtk.Image()
        image.set_from_stock(Gtk.STOCK_APPLY, Gtk.IconSize.BUTTON)
        button.set_image(image)
        
        print module, name
        if exist is False:
            button.connect("clicked",self.do_clicked,module,name,store)
        else:
            # currently modifying
            # if selection is not None then the user want to modify an existing module
            path = name.split('.')[0]
            # args file for the module should exist
            argsfile = expanduser('~')+'/.config/google2ubuntu/modules/'+path+'/args'

            if os.path.exists(argsfile):
                f = open(argsfile,"r")
                linker = (f.readline().strip('\n')).split('=')[-1]
                spacebyplus = (f.readline().strip('\n')).split('=')[-1]
                f.close()
                self.entry1.set_text(linker)
                if spacebyplus == '1':
                    self.checkbutton.set_active(True)
                button.connect("clicked",self.do_modify,argsfile)
                
        grid.attach(label1,0,0,4,1)
        grid.attach(self.entry1,0,1,4,1)
        grid.attach(self.checkbutton,0,2,4,1) 
        grid.attach(button,3,3,1,1)                
        self.w.add(grid)
        self.w.show_all()
        
    def do_clicked(self,button,module,name,store):
        """
        @description: callback function called when the user want to finish
        the configuration of the module. If everything is ok then the config
        file is written at the right place
        """
        linker = self.entry1.get_text()
        if self.checkbutton.get_active():
            spacebyplus='1' 
        else:
            spacebyplus='0'
        
        if linker is not '':
            try:
                folder = name.split('.')[0]
                module_path=expanduser('~')+'/.config/google2ubuntu/modules/'+folder

                if not os.path.exists(module_path):
                    os.makedirs(module_path)    
                                
                f = open(module_path+'/args',"w")
                f.write('linker='+linker+'\n')
                f.write('spacebyplus='+spacebyplus+'\n')
                f.close()
                
                os.system('cp '+module+name+' '+module_path)
                store.append(['<phrase clé>',folder+'/'+name,'modules'])    
            except IOError:
                "Unable to open the file"
        
        self.w.destroy()
    
    def do_modify(self,button,argsfile):
        f = open(argsfile,"w")
        f.write('linker='+self.entry1.get_text()+'\n')
        if self.checkbutton.get_active():
            f.write('spacebyplus=1\n')
        else:
            f.write('spacebyplus=0\n')
            
        f.close()
        self.w.destroy()
