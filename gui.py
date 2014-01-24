# -*- coding: utf-8 -*-  
#!/usr/bin/env python
# use  the new PyGObject binding
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Gio
import os
import sys

class MyWindow(Gtk.ApplicationWindow):
    def __init__(self,app):
        Gtk.Window.__init__(self, title="Gestionnaire de commandes Google2Ubuntu",application=app)
        self.set_default_size(200, 100)  
        self.set_resizable(False)     
        self.set_border_width(10)
        
        # Gtk.ListStore will hold data for the TreeView
        # Only the first two columns will be displayed
        # The third one is for sorting file sizes as numbers
        store = Gtk.ListStore(str, str)
        # Get the data - see below
        self.populate_store(store)
        
        treeview = Gtk.TreeView(model=store)
        treeview.set_tooltip_text('Liste des commandes')

        # The first TreeView column displays the data from
        # the first ListStore column (text=0), which contains
        # file names
        renderer_1 = Gtk.CellRendererText()        
        renderer_1.set_property("editable", True)
        renderer_1.connect("edited", self.key_edited,store)
        column_1 = Gtk.TreeViewColumn('Clés', renderer_1, text=0)
        # Calling set_sort_column_id makes the treeViewColumn sortable
        # by clicking on its header. The column is sorted by
        # the ListStore column index passed to it 
        # (in this case 0 - the first ListStore column) 
        column_1.set_sort_column_id(0)        
        treeview.append_column(column_1)
        
        # xalign=1 right-aligns the file sizes in the second column
        renderer_2 = Gtk.CellRendererText(xalign=1)
        renderer_2.set_property("editable", True)
        renderer_2.connect("edited", self.command_edited,store)
        # text=1 pulls the data from the second ListStore column
        # which contains filesizes in bytes formatted as strings
        # with thousand separators
        column_2 = Gtk.TreeViewColumn('Commandes', renderer_2, text=1)
        # Mak the Treeview column sortable by the third ListStore column
        # which contains the actual file sizes
        column_2.set_sort_column_id(2)
        treeview.append_column(column_2)
        
        # the label we use to show the selection
        self.labelState = Gtk.Label()
        self.labelState.set_text("Ready")
        self.labelState.set_justify(Gtk.Justification.LEFT) 
        self.labelState.set_halign(Gtk.Align.START) 

        # when a row of the treeview is selected, it emits a signal
        self.selection = treeview.get_selection()
        self.selection.connect("changed", self.on_changed)
        
        # Use ScrolledWindow to make the TreeView scrollable
        # Otherwise the TreeView would expand to show all items
        # Only allow vertical scrollbar
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.add(treeview)
        scrolled_window.set_min_content_height(200)
        
        # a toolbar created in the method create_toolbar (see below)
        toolbar = self.create_toolbar(store)
        # with extra horizontal space
        toolbar.set_hexpand(True)
        # show the toolbar
        toolbar.show()

        # Use a grid to add all item
        grid = Gtk.Grid()
        grid.set_row_spacing(5);
        scrolled_window.reparent(grid)
        grid.attach(toolbar,0,0,2,1)
        grid.attach(scrolled_window, 0, 1, 2, 1)    
        grid.attach(self.labelState,0,2,2,1)
        
        self.add(grid)
        self.show_all()

    def command_edited(self, widget, path, text,store):
        store[path][1] = text
        self.saveTree(store)

    def key_edited(self, widget, path, text,store):
        store[path][0] = text
        self.saveTree(store)
        self.saveTree(store)

    def on_changed(self, selection):
        # get the model and the iterator that points at the data in the model
        (model, iter) = selection.get_selected()
        if iter is not None:
            self.labelState.set_text('')                  
         
        return True

    # a method to create the toolbar
    def create_toolbar(self,store):
        # a toolbar
        toolbar = Gtk.Toolbar()
        # which is the primary toolbar of the application
        toolbar.get_style_context().add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR);

        # create a button for the "add" action, with a stock image
        add_button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_ADD)
        # label is shown
        add_button.set_is_important(True)
        # insert the button at position in the toolbar
        toolbar.insert(add_button, 0)
        # show the button
        add_button.connect("clicked", self.add_clicked,store)
        add_button.set_tooltip_text('Ajouter une nouvelle commande')
        add_button.show()
 
        # create a button for the "remove" action
        remove_button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_REMOVE)
        remove_button.set_is_important(True)
        toolbar.insert(remove_button,1)
        remove_button.connect("clicked",self.remove_clicked,store)
        remove_button.set_tooltip_text('Supprimer la commande sélectionnée')
        remove_button.show()
        
        # create a button for the "remove all" action
        all_button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_STOP)
        all_button.set_is_important(True)
        toolbar.insert(all_button,2)
        all_button.connect("clicked",self.removeall_clicked,store)
        all_button.set_tooltip_text('Supprimer toutes les commandes')
        all_button.show() 
        
        # return the complete toolbar
        return toolbar
    
    def add_clicked(self,button,store):
            store.append(['',''])

    def remove_clicked(self,button,store):
        if len(store) != 0:
            (model, iter) = self.selection.get_selected()
            if iter is not None:
                self.labelState.set_text('Suppression: '+model[iter][0]+' '+model[iter][1]) 
                store.remove(iter)
                self.saveTree(store)
            else:
                print "Select a title to remove"
        else:
            print "Empty list"

    def removeall_clicked(self,button,store):
        # if there is still an entry in the model
        old = os.path.dirname(os.path.abspath(__file__)) +'/google2ubuntu.conf'
        new = os.path.dirname(os.path.abspath(__file__)) +'/.google2ubuntu.bak'
        os.rename(old,new)

        if len(store) != 0:
            # remove all the entries in the model
            self.labelState.set_text('Suppression de toutes les commandes')                
            for i in range(len(store)):   
                iter = store.get_iter(0)
                store.remove(iter)
            
            self.saveTree(store)   
        print "Empty list"        

    def populate_store(self, store):
        config = os.path.dirname(os.path.abspath(__file__)) +'/google2ubuntu.conf'
        try:
            f = open(config,"r")
            for line in f:
                if len(line.split('=')) == 2:
                    line = line.rstrip('\n\r') 
                    store.append([line.split('=')[0], line.split('=')[1]])       
                    
            f.close()
        except IOError:
            print "Le fichier de config n'existe pas"

    def saveTree(self,store):
        # if there is still an entry in the model
        (model, aa) = self.selection.get_selected()
        config = os.path.dirname(os.path.abspath(__file__)) +'/google2ubuntu.conf'            
        try:
            f = open(config,"w")        
            if len(store) != 0:
                for i in range(len(store)):
                    iter = store.get_iter(i)
                    f.write(model[iter][0]+'='+model[iter][1]+'\n')
                    self.labelState.set_text('Sauvegarde des commandes')                

            f.close()
        except IOError:    
            print "Unable to write the file"

class MyApplication(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        win = MyWindow(self)
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)
            

app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)
