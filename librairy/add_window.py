#!/usr/bin/env python
# -*- coding: utf-8 -*-  
from gi.repository import Gtk
from gi.repository import Notify
from gi.repository import Gdk
from gi.repository import Gio
from os.path import expanduser
from ArgsWindow import ArgsWindow
from moduleSelection import moduleSelection
from HelpWindow import HelpWindow
from localehelper import LocaleHelper
import os
import sys
import subprocess
import gettext
import locale
import xml.etree.ElementTree as ET

TARGET_TYPE_URI_LIST = 80
dnd_list = [Gtk.TargetEntry.new('text/uri-list', 0, TARGET_TYPE_URI_LIST )]

class add_window():
    """
    @description: This class allow the user to manage all his commands thanks
    to a treeview. The grid generated will be added to the window
    """
    def __init__(self):
        # Gtk.ListStore will hold data for the TreeView
        # Only the first two columns will be displayed
        # The third one is for sorting file sizes as numbers
        store = Gtk.ListStore(str, str, str)
        # Get the data - see below
        self.populate_store(store)

        # use a filter in order to filtering the data
        self.tree_filter = store.filter_new()

        # create the treeview
        treeview = Gtk.TreeView.new_with_model(self.tree_filter)
        treeview.set_tooltip_text(_('list of commands'))
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
        column_1 = Gtk.TreeViewColumn(_('Keys'), renderer_1, text=0)
        column_1.set_min_width(200)
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
        column_2 = Gtk.TreeViewColumn(_('Commands'), renderer_2, text=1)
        # Mak the Treeview column sortable by the third ListStore column
        # which contains the actual file sizes
        column_2.set_sort_column_id(1)
        treeview.append_column(column_2)
        
        # the label we use to show the selection
        self.labelState = Gtk.Label()
        self.labelState.set_text(_("Ready"))
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
        scrolled_window.connect('drag_data_received', self.on_drag_data_received,store)
        scrolled_window.drag_dest_set( Gtk.DestDefaults.MOTION | Gtk.DestDefaults.HIGHLIGHT | Gtk.DestDefaults.DROP, dnd_list, Gdk.DragAction.COPY)
                
        # a toolbar created in the method create_toolbar (see below)
        toolbar = self.create_toolbar(store)
        toolbar.set_hexpand(True)
        toolbar.show()

        # define the visible func toolbar should be create
        self.tree_filter.set_visible_func(self.match_func)

        # Use a grid to add all item
        self.grid = Gtk.Grid()
        self.grid.set_row_spacing(2);
        self.grid.attach(toolbar,0,0,1,1)
        self.grid.attach(scrolled_window, 0, 1, 1, 1)    
        self.grid.attach(self.labelState,0,2,1,1)        

    def get_grid(self):
        """
        @description: get the grid
        
        @return a Gtk.Grid
        """
        return self.grid

    def on_drag_data_received(self,widget, context, x, y, Selection, target_type, timestamp,store):
        """
        @description: The treeview allows dnd so, if the user select a file then the process to 
        add a module start and finally a new line is added to the treeview. If the user select a 
        folder then a new line is added to the treeview with a command to open this folder
        
        @param: widget
            the widget that support dnd
        
        @param: Selection
            the item selected
        
        @param: store
            the listStore to append the new entry
        """
        if target_type == TARGET_TYPE_URI_LIST:
            uri= Selection.get_uris()[0]
            uri = uri.strip('\r\n\x00')
            uris= uri.split('://')
            if len(uris) >= 1 :
                path = uris[1]
                print 'path', path
                if os.path.isfile(path):
                    self.addModule(store,path)
                elif os.path.isdir(path):
                    store.append([_('key sentence'),'xdg-open '+path,_('external')])

    def show_label(self,action):
        """
        @description: Show or hide the bottom label
        
        @param: action
            a string 'show' or 'hide'
        """
        etat = self.labelState.get_parent()
        if action == 'show' and etat == None:
            self.grid.attach(self.labelState,0,2,2,1)
        elif action == 'hide' and etat != None:
            self.grid.remove(self.labelState)

    def command_edited(self, widget, path, text,store):
        """
        @description: callback function called when the user edited the command
        field of the treeview, we need to modify the liststore
        
        @param: widget
            a Gtk.Widget
        
        @param: path
            the way to find the modifiyed item
        
        @param: text
            the new text
        
        @param: store
            the listStore to modify
        """
        iters = self.tree_filter.get_iter(path)
        path = self.tree_filter.convert_iter_to_child_iter(iters)
        store[path][1] = text
        self.saveTree(store)

    def key_edited(self, widget, path, text,store):
        """
        @description: same thing that the previous function
        """
        iters = self.tree_filter.get_iter(path)
        path = self.tree_filter.convert_iter_to_child_iter(iters)        
        store[path][0] = text
        self.saveTree(store)

    def on_changed(self, selection):
        """
        @description: hide the bottom label when the selection change
        
        @param: selection
            the selection from the treeview
            
        @return: a boolean 
        """
        # get the model and the iterator that points at the data in the model
        (model, iter) = selection.get_selected()
        if iter is not None:
            self.show_label('hide')          
         
        return True

    # a method to create the toolbar
    def create_toolbar(self,store):
        """
        @description: create the toolbar of the main window
        
        @param: store
            the listStore to connect to some buttons
            
        @return: a Gtk.toolbar
        """
        # a toolbar
        toolbar = Gtk.Toolbar()
        # which is the primary toolbar of the application
        toolbar.set_icon_size(Gtk.IconSize.LARGE_TOOLBAR)    
        toolbar.set_style(Gtk.ToolbarStyle.BOTH_HORIZ)
        toolbar.set_show_arrow(True) 

        # create a menu
        menu = Gtk.Menu()
        externe = Gtk.MenuItem(label=_("External commands"))
        externe.connect("activate",self.add_clicked,store,'externe')
        externe.show()
        menu.append(externe)
        interne = Gtk.MenuItem(label=_("Internal commands"))
        interne.connect("activate",self.add_clicked,store,'interne')
        interne.show()
        menu.append(interne)        
        module = Gtk.MenuItem(label=_("Module"))
        module.connect("activate",self.add_clicked,store,'module')
        module.show()
        menu.append(module)

        # create a button for the "add" action, with a stock image
        add_button = Gtk.MenuToolButton.new_from_stock(Gtk.STOCK_ADD)
        add_button.set_label(_("Add"))
        add_button.set_menu(menu)
        image = Gtk.Image()
        image.set_from_stock(Gtk.STOCK_ADD, Gtk.IconSize.BUTTON)
        # label is shown
        add_button.set_is_important(True)
        # insert the button at position in the toolbar
        toolbar.insert(add_button, 0)
        # show the button
        add_button.connect("clicked", self.add_clicked,store,'externe')
        add_button.set_tooltip_text(_('Add a new command'))
        add_button.show()
        
        # create a menu to store remove action
        delete_menu = Gtk.Menu()
        one_item = Gtk.MenuItem(label=_("Remove"))
        one_item.connect("activate",self.remove_clicked,store)
        one_item.set_tooltip_text(_('Remove this command'))
        one_item.show()
        delete_menu.append(one_item)
        all_item = Gtk.MenuItem(label=_("Clean up"))
        all_item.connect("activate",self.removeall_clicked,store)
        all_item.set_tooltip_text(_('Remove all commands'))
        all_item.show()
        delete_menu.append(all_item)   

        remove_button = Gtk.MenuToolButton.new_from_stock(Gtk.STOCK_REMOVE)
        remove_button.set_label(_("Remove"))
        remove_button.set_menu(delete_menu)
        image = Gtk.Image()
        image.set_from_stock(Gtk.STOCK_REMOVE, Gtk.IconSize.BUTTON)
        # label is shown
        remove_button.set_is_important(True)
        # insert the button at position in the toolbar
        toolbar.insert(remove_button, 1)
        # show the button
        remove_button.connect("clicked", self.remove_clicked,store)
        remove_button.set_tooltip_text(_('Remove this command'))
        remove_button.show()

         # create a button for the "try" action
        try_button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_MEDIA_PLAY)
        try_button.set_label(_("Try"))
        try_button.set_is_important(True)
        toolbar.insert(try_button,2)
        try_button.connect("clicked",self.try_command,store)
        try_button.set_tooltip_text(_('Try this command'))
        try_button.show() 
        
        # create a button to edit a module
        module_button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_EDIT)
        module_button.set_label(_('Module setup'))
        module_button.set_is_important(True)
        toolbar.insert(module_button,3)
        module_button.connect("clicked",self.edit_clicked,store)
        module_button.set_tooltip_text(_('Module setup'))
        module_button.show()
        
        # create a button for the "Help" action
        help_button = Gtk.ToolButton.new_from_stock(Gtk.STOCK_HELP)
        help_button.set_label(_("Help"))
        help_button.set_is_important(True)
        toolbar.insert(help_button,4)
        help_button.connect("clicked",self.help_clicked )
        help_button.set_tooltip_text(_("Display help message"))
        help_button.show() 
        
        # create a combobox to store user choice
        self.combo = self.get_combobox()
        toolcombo = Gtk.ToolItem()
        toolcombo.add(self.combo)
        toolcombo.show()
        toolbar.insert(toolcombo,5)        
        
        # add a separator
        separator = Gtk.ToolItem()
        separator.set_expand(True)
        toolbar.insert(separator,6)
        
        # create a little menu button to override locale language
        current_locale = locale.getdefaultlocale()[0]
        
        locale_config=expanduser('~')+'/.config/google2ubuntu/locale.conf'
        if os.path.exists(locale_config):
            f = open(locale_config,"r")
            tmp = f.readline().strip('\n')
            f.close()
            if tmp is not None and tmp is not '':
                current_locale = tmp
            
        locale_path = os.path.dirname(os.path.abspath(__file__)).strip('librairy')
        locale_path += 'i18n'
        locale_menu = Gtk.Menu()
        
        for language in os.listdir(locale_path):
            if os.path.isdir(locale_path+'/'+language):
                item = Gtk.MenuItem(label=language)
                item.connect("activate",self.change_locale,locale_path,language)
                item.show()
                locale_menu.append(item)
        
        self.locale_button = Gtk.MenuToolButton.new(None,current_locale)
        self.locale_button.set_is_important(True)
        self.locale_button.set_menu(locale_menu)
        self.locale_button.show()
        toolbar.insert(self.locale_button,7)
        
        # return the complete toolbar
        return toolbar

    # change the locale set
    def change_locale(self,button,locale_path,language):
        """
        @description: set the local desired by the user among supported
        locale
        
        @param: button
            the button that has to be clicked
        
        @param: locale_path
            the folder containing locales
        
        @param: language
            desired locale
        """
        self.locale_button.set_label(language)
        try:
            locale_config=expanduser('~')+'/.config/google2ubuntu/locale.conf'
            f = open(locale_config,"w")
            f.write(language+'\n')
            f.close()
        except Exception:
            print "error, while opening locale.conf file"

    # return a combobox to add to the toolbar
    def get_combobox(self):
        """
        @description: get the combobox of the toolbar
        
        @return: a Gtk.Combobox
        """
        # the data in the model, of type string
        listmodel = Gtk.ListStore(str)
        # append the data in the model
        listmodel.append([_('All')])
        listmodel.append([_('External')])
        listmodel.append([_('Internal')])
        listmodel.append([_('Modules')])
                        
        # a combobox to see the data stored in the model
        combobox = Gtk.ComboBox(model=listmodel)
        combobox.set_tooltip_text(_("What type of command to add")+'?')

        # a cellrenderer to render the text
        cell = Gtk.CellRendererText()

        # pack the cell into the beginning of the combobox, allocating
        # no more space than needed
        combobox.pack_start(cell, False)
        # associate a property ("text") of the cellrenderer (cell) to a column (column 0)
        # in the model used by the combobox
        combobox.add_attribute(cell, "text", 0)

        # the first row is the active one by default at the beginning
        combobox.set_active(0)

        # connect the signal emitted when a row is selected to the callback function
        combobox.connect("changed", self.on_combochanged)
        return combobox
    
    # callback function attach to the combobox   
    def on_combochanged(self,combo):
        """
        @description: the combobox is used to filter the treeview and switch
        between different commands types
        """
        self.tree_filter.refilter()

    # filter function
    def match_func(self, model, iterr, data=None):
        """
        @description: we get the combobox selection and filter the treeview
        data thanks to this selection.
        
        @return: a boolean
        """
        query = self.combo.get_active()
        value = model.get_value(iterr, 1)
        field = model.get_value(iterr, 2)
        
        if query == 0:
            return True
        elif query == 1 and _('modules') not in field and _('internal') not in field:
            return True
        elif query == 2 and _('internal') in field:
            return True
        elif query == 3 and _('modules') in field:
            return True
        else:
            return False
    
    def edit_clicked(self,button,store):
        # get the selected line, if it is module then we can open the window
        (model, iters) = self.selection.get_selected()
        if len(store) != 0:
            if iters is not None:
                iter = self.tree_filter.convert_iter_to_child_iter(iters)
                if store[iter][2] == _('modules'):
                    w=ArgsWindow("",((store[iter][1]).split('/'))[-1],store,True)
                    
    def add_clicked(self,button,store,add_type):
        """
        @description: callback function called when the user want to add
        command
        
        @param: button
            the button that has to be clicked
        
        @param: store
            the listStore that will contain a new entry
        
        @param: add_type
            the type of the new command to add
        """
        if add_type == 'externe':
            store.append([_('key sentence'),_('your command'),_('external')])
        elif add_type == 'interne':
            store.append([_('key sentence'),_('word'),_('internal')])
        elif add_type == 'module':
            mo = moduleSelection()
            module = mo.getModule()
            if module != '-1':
                self.addModule(store,module)
            else:
                self.show_label('show')
                self.labelState.set_text(_("Error, you must choose a file"))


    def addModule(self,store,module):
        """
        @description: function that adds a module
        
        @param: store
            the listStore that will receive a new entry
        
        @param: module
            the path of the executable file of the module
        """
        # ex: recup de weather.sh
        name = module.split('/')[-1]
        # ex: ~/.config/google2ubuntu/weather
        module=module.strip(name)
        print module+"args"
        # ex: recherche du fichier args
        if os.path.exists(module+'args'):
            # ex: récupération de weather
            path = module.split('/')[-2]
            store.append([_('key sentence'),path+'/'+name,'modules'])
            # si le dossier de modules n'existe pas
            module_path=expanduser('~')+'/.config/google2ubuntu/modules/'
            if not os.path.exists(module_path):
                os.makedirs(os.path.dirname(module_path))
                # on copie le dossier du module    
            os.system('cp -r '+module+' '+module_path)
        else:
            self.show_label('show')
            self.labelState.set_text(_("Error, args file missing"))
            win = ArgsWindow(module,name,store)        
    
    def remove_clicked(self,button,store):
        """
        @description: callback function called wnen the user want to remove 
        a line of the treeview
        
        @param: button
            the button that will be clicked
        
        @param: store
            the listStore that is going to be modify
        """
        if len(store) != 0:
            (model, iters) = self.selection.get_selected()
            if iters is not None:
                iter = self.tree_filter.convert_iter_to_child_iter(iters)
                if iter is not None:
                    self.show_label('show')
                    self.labelState.set_text(_('Remove')+': '+store[iter][0]+' '+store[iter][1]) 
                    store.remove(iter)
                    self.saveTree(store)
                else:
                    print "Select a title to remove"
        else:
            print "Empty list"

    def removeall_clicked(self,button,store):
        """
        @description: Same as the past function but remove all lines of the 
        treeview
        """
        # if there is still an entry in the model
        old = expanduser('~') +'/.config/google2ubuntu/google2ubuntu.xml'
        new = expanduser('~') +'/.config/google2ubuntu/.google2ubuntu.bak'
        if os.path.exists(old):
            os.rename(old,new)

        if len(store) != 0:
            # remove all the entries in the model
            self.labelState.set_text(_('Remove all commands'))               
            for i in range(len(store)):   
                iter = store.get_iter(0)
                store.remove(iter)
            
            self.saveTree(store)   
        print "Empty list"        

    def try_command(self,button,store):
        """
        @description: try a command (bash)
        
        @param: button
            the button that has to be clicked
        
        @param: store
            the listStore
        """
        (model, iter) = self.selection.get_selected()
        if iter is not None:
            command = model[iter][1]
            Type = model[iter][2]
            if _('internal') != Type and _('modules') != Type:
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                output,error = process.communicate() 
                self.show_label('show')       
                self.labelState.set_text(output+'\n'+error)
    
    def help_clicked(self,button):
        """
        @description: show the help window
        
        @param: button
            the button that has to be clicked
        """
        win = HelpWindow()

    def populate_store(self, store):    
        """
        @description: load the treeview from the google2ubuntu.xml file or
        from the default.xml file
        
        @param: store
            the listStore that will be modify
        """    
        # user ocnfig file
        config = expanduser('~') +'/.config/google2ubuntu/google2ubuntu.xml'
        
        # default config file for the selected language
        path = os.path.dirname(os.path.abspath(__file__)).strip('librairy')    
        localeHelper = LocaleHelper('en_EN')
        lang = localeHelper.getLocale()
        # this line can be remove if we change config/en_EN to config/en
        #lang = lang+'_'+lang.upper()
        
        default = path +'config/'+lang+'/default.xml'        

        try:
            if os.path.isfile(config):
                # here the program refuses to load the xml file
                tree = ET.parse(config)
            else:
                if os.path.exists(expanduser('~') +'/.config/google2ubuntu') == False:
                    os.makedirs(expanduser('~') +'/.config/google2ubuntu')
                    os.system('cp -r /usr/share/google2ubuntu/modules '+expanduser('~') +'/.config/google2ubuntu')    
                
                tree = ET.parse(default)
            
            root = tree.getroot()
            for entry in root.findall('entry'):
                Type=entry.get('name')
                Key=entry.find('key').text
                Command=entry.find('command').text
                store.append([Key, Command, Type])  
        except Exception as e:
            print 'Error while reading config file'
            print type(e)
            print e.args
            print e

    def saveTree(self,store):
        """
        @description: save the treeview in the google2ubuntu.xml file
        
        @param: store
            the listStore attach to the treeview
        """
        # if there is still an entry in the model
        model = self.tree_filter.get_model()
        config = expanduser('~') +'/.config/google2ubuntu/google2ubuntu.xml'     
        try:
            if not os.path.exists(os.path.dirname(config)):
                os.makedirs(os.path.dirname(config))            
            
            root = ET.Element("data")
            if len(store) != 0:
                for i in range(len(store)):
                    iter = store.get_iter(i)
                    if model[iter][0] != '' and model[iter][1] != '':
                        for s in model[iter][0].split('|'):
                            s = s.lower()
                            s = s.replace('*',' ')
                            Type = ET.SubElement(root, "entry")
                            Type.set("name",unicode(model[iter][2],"utf-8"))
                            Key = ET.SubElement(Type, "key")
                            Key.text = unicode(s,"utf-8")
                            Command = ET.SubElement(Type, "command")
                            Command.text = unicode(model[iter][1],"utf-8")
                
            tree = ET.ElementTree(root).write(config,encoding="utf-8",xml_declaration=True)

            self.show_label('show')
            self.labelState.set_text(_('Save commands'))   
        except IOError:
            print "Unable to write the file"    
