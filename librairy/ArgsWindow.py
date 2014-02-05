#!/usr/bin/env python
# -*- coding: utf-8 -*-  
from gi.repository import Gtk
from gi.repository import Notify
from gi.repository import Gdk
from gi.repository import Gio
from os.path import expanduser
import os, sys, subprocess, gettext

gettext.install('google2ubuntu',os.path.dirname(os.path.abspath(__file__))+'/i18n/')

# gère l'apparition de la fenêtre d'assistance de création de module
class ArgsWindow():
    """
    @author: Benoit Franquet
    
    @description: This class is calling when the user want to add a new
    module, if this module hasn't got an configuration file then this class
    create a winddow to help the user configurating his new module
    
    @param: module
        the folder containing module's files
    
    @param: name
        the name of the module
    
    @param: store
        the Gtk.Listore en which we will add the new module
    """
    def __init__(self,module,name,store):
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
        button = Gtk.Button()
        button.set_label(_("Go"))
        button.set_tooltip_text(_("Go"))
        image = Gtk.Image()
        image.set_from_stock(Gtk.STOCK_APPLY, Gtk.IconSize.BUTTON)
        button.set_image(image)
        button.connect("clicked",self.do_clicked,module,name,store)
        
        grid.attach(label1,0,0,4,1)
        grid.attach(self.entry1,0,1,4,1)
        grid.attach(self.checkbutton,0,2,4,1) 
        grid.attach(button,3,3,1,1)                
        self.w.add(grid)
        self.w.show_all()
    
    def do_clicked(self,button,module,name,store):
        """
            @function: callback function activated when the user click on the
            button Go
            
            @param: button
                the button that has to be clicked
            
            @param: module
                the module's folder
            
            @param: name
                the module's name
            
            @param: store
                the Gtk.Listore in which a new line will be added
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
