# -*- coding: utf-8 -*-  
#!/usr/bin/env python
# use  the new PyGObject binding
from gi.repository import Gtk
from gi.repository import Notify
from gi.repository import Gdk
from gi.repository import Gio
from os.path import expanduser
import os
import sys
import subprocess

class MyWindow(Gtk.ApplicationWindow):
    def __init__(self,app):
        Gtk.Window.__init__(self, title="google2ubuntu-manager",application=app)
        self.set_default_size(500, 500)  
        self.set_resizable(True)     
        self.set_border_width(0)
        self.get_focus()
        self.set_position(Gtk.WindowPosition.CENTER)
        
        # Gtk.ListStore will hold data for the TreeView
        # Only the first two columns will be displayed
        # The third one is for sorting file sizes as numbers
        store = Gtk.ListStore(str, str)
        # Get the data - see below
        self.populate_store(store)
        
        treeview = Gtk.TreeView(model=store)
        treeview.set_tooltip_text('Liste des commandes')
        treeview.set_headers_visible(False)
        treeview.set_enable_search(True)
        treeview.set_search_column(1)
        treeview.set_hexpand(True)
        treeview.set_vexpand(True)

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
        column_2.set_sort_column_id(1)
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
        scrolled_window.set_min_content_width(200)
        scrolled_window.set_min_content_height(200)
        
        # a toolbar created in the method create_toolbar (see below)
        toolbar = self.create_toolbar(store)
        # with extra horizontal space
        toolbar.set_hexpand(True)
        # show the toolbar
        toolbar.show()

        # Use a grid to add all item
        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(2);
        scrolled_window.reparent(self)
        self.grid.attach(toolbar,0,0,2,1)
        self.grid.attach(scrolled_window, 0, 1, 2, 1)    
        self.grid.attach(self.labelState,0,2,2,1)
        
        self.add(self.grid)
        self.show_all()

    def show_label(self,action):
        etat = self.labelState.get_parent()
        if action == 'show' and etat == None:
            self.grid.attach(self.labelState,0,2,2,1)
        elif action == 'hide' and etat != None:
            self.grid.remove(self.labelState)

    def command_edited(self, widget, path, text,store):
        store[path][1] = text
        self.saveTree(store)

    def key_edited(self, widget, path, text,store):
        store[path][0] = text
        self.saveTree(store)

    def on_changed(self, selection):
        # get the model and the iterator that points at the data in the model
        (model, iter) = selection.get_selected()
        if iter is not None:
            self.show_label('hide')          
         
        return True

    # a method to create the toolbar
    def create_toolbar(self,store):
        # a toolbar
        toolbar = Gtk.Toolbar()
        # which is the primary toolbar of the application
        toolbar.set_icon_size(Gtk.IconSize.LARGE_TOOLBAR)    
        toolbar.set_style(Gtk.ToolbarStyle.BOTH_HORIZ)

        # create a menu
        menu = Gtk.Menu()
        externe = Gtk.MenuItem(label="Commande externe")
        externe.connect("activate",self.add_clicked,store,'externe')
        externe.show()
        menu.append(externe)
        interne = Gtk.MenuItem(label="Commande interne")
        interne.connect("activate",self.add_clicked,store,'interne')
        interne.show()
        menu.append(interne)        
        module = Gtk.MenuItem(label="Module")
        module.connect("activate",self.add_clicked,store,'module')
        module.show()
        menu.append(module)

        # create a button for the "add" action, with a stock image
        add_button = Gtk.MenuToolButton.new_from_stock(Gtk.STOCK_ADD)
        add_button.set_label("Ajouter")
        add_button.set_menu(menu)
        image = Gtk.Image()
        image.set_from_stock(Gtk.STOCK_ADD, Gtk.IconSize.BUTTON)
        # label is shown
        add_button.set_is_important(True)
        # insert the button at position in the toolbar
        toolbar.insert(add_button, 0)
        # show the button
        add_button.connect("clicked", self.add_clicked,store,'externe')
        add_button.set_tooltip_text('Ajouter une nouvelle commande')
        add_button.show()
 
        # create a button for the "try" action
        try_button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_MEDIA_PLAY)
        try_button.set_label("Essayer")
        try_button.set_is_important(True)
        toolbar.insert(try_button,1)
        try_button.connect("clicked",self.try_command,store)
        try_button.set_tooltip_text('Tester la commande')
        try_button.show() 
         
        # create a button for the "remove" action
        remove_button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_REMOVE)
        remove_button.set_label("Supprimer")
        remove_button.set_is_important(True)
        toolbar.insert(remove_button,2)
        remove_button.connect("clicked",self.remove_clicked,store)
        remove_button.set_tooltip_text('Supprimer la commande sélectionnée')
        remove_button.show()
        
        # create a button for the "remove all" action
        all_button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_STOP)
        all_button.set_label("Nettoyer")
        all_button.set_is_important(True)
        toolbar.insert(all_button,3)
        all_button.connect("clicked",self.removeall_clicked,store)
        all_button.set_tooltip_text('Supprimer toutes les commandes')
        all_button.show() 

        # create a button for the "Help" action
        help_button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_HELP)
        help_button.set_label("Aide")
        help_button.set_is_important(True)
        toolbar.insert(help_button,4)
        help_button.connect("clicked",self.help_clicked )
        help_button.set_tooltip_text("Afficher l'aide")
        help_button.show() 

        # return the complete toolbar
        return toolbar
    
    def add_clicked(self,button,store,add_type):
        if add_type == 'externe':
            store.append(['','='])
        elif add_type == 'interne':
            store.append(['','interne/'])
        elif add_type == 'module':
            mo = moduleSelection()
            module = mo.getModule()
            if module != '-1':
                name = module.split('/')[-1]
                module=module.strip(name)
                if os.path.exists(module+'/args'):
                    path = module.split('/')[-2]
                    store.append(['<votre phrase clé>','/modules/'+path+'/'+name])
                    module_path=expanduser('~')+'/.config/google2ubuntu/modules/'
                    if not os.path.exists(module_path):
                        os.makedirs(os.path.dirname(config))
                        os.system('cp -r '+module+' '+module_path)
                else:
                    self.show_label('show')
                    self.labelState.set_text("Erreur, le fichier args n'existe pas")
            else:
                self.show_label('show')
                self.labelState.set_text("Erreur, vous n'avez choisi aucun fichier")
                
        self.selection.select_iter(store.get_iter(len(store)-1))
        

    def remove_clicked(self,button,store):
        if len(store) != 0:
            (model, iter) = self.selection.get_selected()
            if iter is not None:
                self.show_label('show')
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

    def try_command(self,button,store):
        (model, iter) = self.selection.get_selected()
        if iter is not None:
            command = model[iter][1]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output,error  = process.communicate() 
            self.show_label('show')       
            self.labelState.set_text(output+'\n'+error)
    
    def help_clicked(self,button):
        win = HelpWindow()

    def populate_store(self, store):
        config = expanduser('~') +'/.config/google2ubuntu/google2ubuntu.conf'
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
        config = expanduser('~') +'/.config/google2ubuntu/google2ubuntu.conf'            
        try:
            if not os.path.exists(os.path.dirname(config)):
                os.makedirs(os.path.dirname(config))
            
            f = open(config,"w") 
            if len(store) != 0:
                for i in range(len(store)):
                    iter = store.get_iter(i)
                    f.write(model[iter][0]+'='+model[iter][1]+'\n')
                    self.show_label('show')
                    self.labelState.set_text('Sauvegarde des commandes')                

            f.close()
        except IOError:    
            print "Unable to write the file"


class HelpWindow():
    # constructor for a window (the parent window)
    def __init__(self):
        #a  Gtk.AboutDialog
        self.aboutdialog = Gtk.AboutDialog()

        # lists of authors and documenters (will be used later)
        authors = ["Franquet Benoit"]
        documenters = ["Franquet Benoit"]

        # we fill in the aboutdialog
        self.aboutdialog.set_program_name("Aide Google2Ubuntu")
        self.aboutdialog.set_copyright("Copyright \xc2\xa9 2014 Franquet Benoit")
        self.aboutdialog.set_authors(authors)
        self.aboutdialog.set_documenters(documenters)
        self.aboutdialog.set_website("https://github.com/benoitfragit/google2ubuntu")
        self.aboutdialog.set_website_label("http://forum.ubuntu-fr.org/viewtopic.php?id=804211&p=1")

        # we do not want to show the title, which by default would be "About AboutDialog Example"
        # we have to reset the title of the messagedialog window after setting the program name
        self.aboutdialog.set_title("")

        # to close the aboutdialog when "close" is clicked we connect the
        # "response" signal to on_close
        self.aboutdialog.connect("response", self.on_close)
        # show the aboutdialog
        self.aboutdialog.show()
        
    # destroy the aboutdialog
    def on_close(self, action, parameter):
        action.destroy()

class moduleSelection():
    def __init__(self):
        w=Gtk.Window()
        dialog = Gtk.FileChooserDialog("Choisissez un fichier", w,Gtk.FileChooserAction.OPEN,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,Gtk.STOCK_OPEN, Gtk.ResponseType.OK))        
        dialog.set_default_size(800, 400)

        response = dialog.run()
        self.module = '-1'
        if response == Gtk.ResponseType.OK:
            self.module=dialog.get_filename()
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")

        dialog.destroy()
    
    def getModule(self):
        return self.module


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
