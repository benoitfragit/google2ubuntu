Project specification
=====================

Commands' storage
-----------------

By default, google2ubuntu comes with several commands stored in a default xml file:

/usr/share/google2ubuntu/config/<your_language>/default.xml

For the moment, there is a default file for French and English users, if your language is not currently supported the default voice will be English.

At the first, launch, a module folder is created in: ~/.config/google2ubuntu

The first time you add, modify or rmove a command, your commands' configuration will be also stored in this folder: ~/.config/google2ubuntu/google2ubuntu.xml


Commands' description
---------------------

A command is a pair of `key` and `action`. Each `key` referes to an `action`. Many `key` can leads to the same `action`.
To define a command, you do not need to make explicitaly all the word you will tell, I mean, if I want to create the command:

* key: open my documents
* action: xdg-open ~/Documents

The word `my` is not usefull so, I will put:


* key: open documents
* action: xdg-open ~/Documents

Don't care about capital letter, because the program automatically put the text in lowercase.


I've implemented different types of command:

* **external commands**
* **internal commands**
* **modules**

External commands
^^^^^^^^^^^^^^^^^
External commands are basically commands that you can run in your terminal:

`exo-open --launch MailReader`

If you want to add an external command, just click on the "Add" button. Then find the newline and replace "your key" by the key you want to associate to the command and replace "your command" by the action.

Internal commands
^^^^^^^^^^^^^^^^^
Internal commands are commands that I've implemented in google2ubuntu, for the moment there is 3 internal commands:

* time # show the time
* power # show and say the state of the battery
* clipboard # read the text selected by the cursor

If you want to add an internal command, open the little menu near the "Add" button and select "internal". Then replace "your key" by the "key" you will pronounce to call this command and replace "word" by one of those 3 actions 

Modules
^^^^^^^
In order to extand google2ubuntu very easily I've implemented a system of menu that let developers adds their own scripts in google2ubuntu. Besides, all modules will receive the text tha you pronouce in parameter

Module's description
""""""""""""""""""""
A module is composed of 2 files, an executable file and a config file named "args" placed both in the same folder.
The args file contains 2 fields:

* **linker** a vord that let us distinguish the call to the module and the parameter we have to send to this module. For example, if I want to configure the module google, I can choose the linker "google " because when I make a research I say: "google who is barack obama" So, the google module will be call with `who is barack obama` in parameter.
* **spacebyplus** If spacebyplus=1 then space are replace py +.

How to add a module
"""""""""""""""""""
If you want to add a script, but this script doesn't have an args file don't worry, the gui will help you to create one and will place the module in :

"~/.config/google2ubuntu/modules"

You can add a module by opening the menu near to the "Add" button then selecting the executable files of the module. 
Yu can also simply drag&drop this executable on the treeview and the module will be automatically added. When you add a new module you don't have to modify the `action` field in the newline. You just have to modify the `key` field in the gui.

Already available
""""""""""""""""""
google2ubuntu already comes with 6 modules:

* `plugin google <https://github.com/benoitfragit/google2ubuntu/tree/master/modules/google>`_ This plugin allows you to make search on Google and open the web browser on the search page you ask for.
* `plugin wikipedia <https://github.com/benoitfragit/google2ubuntu/tree/master/modules/wikipedia>`_ This plugin allows you to make search on Wikipedia
* `plugin youtube <https://github.com/benoitfragit/google2ubuntu/tree/master/modules/youtube>`_ This plugin allows you to make search on YouTube
* `plugin way <https://github.com/benoitfragit/google2ubuntu/tree/master/modules/way>`_ This plugin allows you to find a way between to place on Google map. You have to pronounce your place like this: "way between Pars and Marseille". So your locations need to be between the word "between" and "and"
* `plugin weather <https://github.com/benoitfragit/google2ubuntu/tree/master/modules/weather>`_ This plugin allows you to ask Google to show you the weather for a city
* `plugin meaning <https://github.com/benoitfragit/google2ubuntu/tree/master/modules/meaning>`_ This plugin allows you to ask to the meaning of a word, for exemple if I ask: "meaning barack obama". The plugin will tell me that he is the actual president of the US

Note for the user
"""""""""""""""""
Perhaps, you will have to modify the linker field of those module by modifying the corresponding args file in :

"~/.config/google2ubuntu/modules/<name>/args"
