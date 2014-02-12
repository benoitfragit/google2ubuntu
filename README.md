google2ubuntu
=============

#Presentation

The aim of this project is to let you use the Google speech recognition API to control your linux computer. The project is developed in Python.

google2ubuntu is a tool that I started 2 years ago. Unfortunatly, I was not able to do what I wanted because of a lack of time. So the project consists in 2 principal Python scripts:

* google2ubuntu.py
* google2ubuntu-manager.py

The first one lets you send commands to Google and then execute some actions. The second one lets you manage all the commands. 

I've done huge efforts to make the program easy to install and easy to use. Besides, the program can be internationalize, for the moment, it is already available in French, English, Deutch, Spanish and Italian.

# Special thanks
Before I begin, I want to thank some of you that help me.

##Contributors
Devs | Translators | Bug reports
-----| ----- | -----
[tectas](https://github.com/tectas)|[tectas](https://github.com/tectas)|[bmeznarsic](https://github.com/bmeznarsic) 
[mte90](https://github.com/mte90)|[mte90](https://github.com/mte90)|[Andrew from Webupd8](https://github.com/hotice)
[levan7](https://github.com/Levan7)|[lincus](https://github.com/lincus)|[mte90](https://github.com/mte90)
[ladios](https://github.com/ladios)|[ladios](https://github.com/ladios)|[mads5408](https://github.com/mads5408)


##Publication

* [WebUpd8](http://www.webupd8.org/2014/02/linux-speech-recognition-using-google.html#more)
* [La vache libre](http://la-vache-libre.org/google2ubuntu-le-projet-de-reconnaissance-vocale-pour-gnulinux-a-un-nouveau-developpeur/)



#Installation
## Dependancies

For the moment, dependancies are:

* bash
* python
* python-gi
* libnotify-dev
* sox
* xdotool
* libsox-fmt-mp3
* acpi
* python-simplejson

If you are installing google2ubuntu from source not from deb or from ppa, type this:
```
   sudo apt-get install bash python python-gi python-simplejson libsox-fmt-mp3 sox libnotify-dev acpi xdotool
```

##Find the package
google2ubuntu is available on Github on the [release](https://github.com/benoitfragit/google2ubuntu/releases) page and in my [ppa](https://launchpad.net/~benoitfra/+archive/google2ubuntu). To install google2ubuntu 

```
sudo add-apt-repository ppa:benoitfra/google2ubuntu
sudo apt-get update
sudo apt-get install google2ubuntu
```

##First launch
Once you have installed google2ubuntu, you can attribute a shortcut to those 2 Python scripts:

```
/usr/share/google2ubuntu/google2ubuntu.py
/usr/share/google2ubuntu/google2ubuntu-manager.py
```

Moreover, if you search in the application's menu you will find two launchers, one for each of those programs.

After that, you can launch google2ubuntu-manager.py in order to manage all commands.
![google2ubuntu-manager](http://pix.toile-libre.org/upload/original/1391806249.png)
<a href='http://pix.toile-libre.org/?img=1391805854.png'><img src='http://pix.toile-libre.org/upload/thumb/1391805854.png' /></a> <a href='http://pix.toile-libre.org/?img=1391805991.png'><img src='http://pix.toile-libre.org/upload/thumb/1391805991.png' /></a> <a href='http://pix.toile-libre.org/?img=1391806086.png'><img src='http://pix.toile-libre.org/upload/thumb/1391806086.png' /></a> <a href='http://pix.toile-libre.org/?img=1391806166.png'><img src='http://pix.toile-libre.org/upload/thumb/1391806166.png' /></a> 


As you can see, google2ubuntu comes with several default commands. I will explain you how to manage and add commands.

#Manage commands
##Commands' storage
By default, google2ubuntu comes with several commands stored in a default xml file:
```
/usr/share/google2ubuntu/config/<your_language>/default.xml
```
For the moment, there is a default file for French, English, Spanish, Deutch and Italian users, if your language is not currently supported the default voice will be English.

At the first, launch, a module folder is created in:
```
~/.config/google2ubuntu
```
The first time you add, modify or remove a command, your commands' configuration will be also stored in this folder in the file:
```
~/.config/google2ubuntu/google2ubuntu.xml
```


##Commands' description
A command is a pair of `key` and `action`. Each `key` referes to an `action`. Many `key` can leads to the same `action`.
To define a command, you do not need to make explicitaly all the word you will tell, I mean, if I want to create the command:
```
key: open my documents
action: xdg-open ~/Documents
```
The word `my` is not usefull so, I will put:
```
key: open documents
action: xdg-open ~/Documents
```
Don't care about capital letter, because the program automatically put the text in lowercase.


I've implemented different types of command:

* **external commands**
* **internal commands**
* **modules**

###External commands

External commands are basically commands that you can run in your terminal:
```
exo-open --launch MailReader
```
If you want to add an external command, just click on the "Add" button. Then find the newline and replace "your key" by the key you want to associate to the command and replace "your command" by the action.

###Internal commands
####What are they ?
Internal commands are commands that I've implemented in google2ubuntu, for the moment there is 3 internal commands:

| Name | Function | 
| --- | --- |
| time   |  Tell the current time |
| power | Tell the battery state |
| clipboard | Read the text selected by the cursor |
| dictation mode | Enter in dictation mode |
| exit dictation mode | Exit dictation mode | 

If you want to add an internal command, open the little menu near the "Add" button and select "internal". Then replace "your key" by the "key" you will pronounce to call this command and replace "word" by one of those 5 actions' name. 

####Some words about dictation mode

The dictation mode let you type all word you pronouce. If you want to enter in the dictation mode use the dictation mode internal function. If you want to exit this mode just use the associated function. Dictation is not continue so you have to launch google2ubuntu for each sentence you want to type

###Modules
In order to extand google2ubuntu very easily I've implemented a system of menu that let developers adds their own scripts in google2ubuntu. Besides, all modules will receive the text tha you pronouce in parameter

####Module's description
A module is composed of 2 files, an executable file and a config file named "args" placed both in the same folder.
The args file contains 2 fields:

* linker
a vord that let us distinguish the call to the module and the parameter we have to send to this module. For example, if I want to configure the module google, I can choose the linker "google " because when I make a research I say:
```
google who is barack obama
```
So, the google module will be call with `who is barack obama` in parameter.
* spacebyplus
If spacebyplus=1 then space are replace py +.

####How to add a module
If you want to add a script, but this script doesn't have an args file don't worry, the gui will help you to create one and will place the module in :
```
~/.config/google2ubuntu/modules
```

You can add a module by opening the menu near to the "Add" button then selecting the executable files of the module. 
Yu can also simply drag&drop this executable on the treeview and the module will be automatically added. When you add a new module you don't have to modify the `action` field in the newline. You just have to modify the `key` field in the gui.


####Already available
google2ubuntu already comes with 6 modules:

* **google**
This plugin allows you to make search on Google and open the web browser on the search page you ask for.
* **wikipedia**
This plugin allows you to make search on Wikipedia
* **youtube**
This plugin allows you to make search on YouTube
* **way**
This plugin allows you to find a way between to place on Google map. You have to pronounce your place like this:
```
way between Pars and Marseille
```
So your locations need to be between the word "between" and "and"
* **weather**
This plugin allows you to ask Google to show you the weather for a city
* **meaning**
This plugin allows you to ask to the meaning of a word, for exemple if I ask:
```
meaning barack obama
```
The plugin will tell me that he is the actual president of the US

####Note for the user
Perhaps, you will have to modify the linker field of those module by modifying the corresponding args file in :
```
~/.config/google2ubuntu/modules/<name>/args
```
#Go Linux automation
Once you have personalized and take care about the commands already included in google2ubuntu, you can launch the recognition by launching `google2ubuntu.py`

A little sound is played and a notification tell you to speak. Then the notification show the result and the action associated to the text you have pronounced is played.

#How-to contribute
##Design some modules
If you want you can write a module that will be integrated in the Github page, the user will have to download it and will be able to use it
##Translate the app
###Translate the google2ubuntu core
If you want to translate this app, you need first to download the [project](https://github.com/benoitfragit/google2ubuntu/archive/master.zip) then unzip it and open a terminal and place yourself in the folder newly created. Then, be sure that all string that you want to translate are like that:
```
_('text to translate')
```
Then be sure, that there is this at the begenning of the file you want to translate (only needed for google2ubuntu.py, gogl2ubuntu-manager.py)
```
import gettext

gettext.install('google2ubuntu',os.path.dirname(os.path.abspath(__file__))+'/i18n/')
```

So, if you want to add a new language, you should type:

```
mkdir -p i18n/<new_language/LC_MESSAGES
xgettext --language=Python --keyword=_ --output=./i18n/google2ubuntu.pot ./*.py librairy/*.py
msginit --input=./i18n/google2ubuntu.pot --output=./i18n/<new_language>/LC_MESSAGES/google2ubuntu.po
```
The 2 first line are optional and are usefull only there is no .pot file in the i18n/ folder.

Then, open the `.po` file and translate all the line, then compoile the `.po` :
```
msgfmt ./i18n/<new_language>/LC_MESSAGES/google2ubuntu.po --output-file ./i18n/<new_language>/LC_MESSAGES/google2ubuntu.mo
```


###Update the translation
To update an existing translation, you have to do several actions:
```
xgettext --language=Python --keyword=_ --output=./i18n/google2ubuntu.pot ./*.py librairy/*.py
msgmerge --update --no-fuzzy-matching --backup=off ./i18n/<current_language>/LC_MESSAGES/google2ubuntu.po ./i18n/google2ubuntu.pot
```

Then translate new line and compile the `.po`:
```
msgfmt ./i18n/<current_language>/LC_MESSAGES/google2ubuntu.po --output-file ./i18n/<current_language>/LC_MESSAGES/google2ubuntu.mo
```
## Share ideas
You can share ideas and contact me on the google+ comunauty:
[google2ubuntu](https://plus.google.com/u/0/communities/103854623082229435165)

## Demonstration
<a href="http://www.youtube.com/watch?feature=player_embedded&v=vkuX4tqaLFU
" target="_blank"><img src="http://img.youtube.com/vi/vkuX4tqaLFU/0.jpg" 
alt="google2ubuntu" width="480" height="360" border="5" /></a>

## Documentation page
I've wrote a documentation page with Sphinx
[Documentation](http://benoitfragit.github.io/google2ubuntu/)

#Update

## Improvements

| State | Addons    
|---|---
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | adding a menu to change language 
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | adding a class to manage locale easily
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | adding a dictation mode
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | adding the possibility to reconfigure a module from google2ubuntu-manager
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | drag & drop a folder automaticcaly add a line in the treeview with a command to open it
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | adding a man page
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | adding spanish translation
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | adding deutch translation
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | adding italian translation
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | correct dependancies
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | adding Sox not recording in 16kHz bug fixe
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | correct module setup button bug
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | correct pyGobject constructor issue
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | regroupe both remove all and delete in one button
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | delete button bug fixe when no item selected
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | localHelper not cut locale name
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | beginning to work on the HelpWindow
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | changing i18n locale's folder name
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | correct a bug due to module execution
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | adding pt_BR support
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | adding pt_PT support
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | adding traditional chinese translation
| ![done](http://www.pronosoft.com/fr/bookmakers/img/logo_ok.png) | correct the wikipedia module
| ![todo](http://www.yabo-concept.ch/admin/themes/YaboConcept/images/icons/system/false.gif) | update the documentation
| ![todo](http://www.yabo-concept.ch/admin/themes/YaboConcept/images/icons/system/false.gif) | improve translation 
| ![todo](http://www.yabo-concept.ch/admin/themes/YaboConcept/images/icons/system/false.gif) | bug fixe 
| ![todo](http://www.yabo-concept.ch/admin/themes/YaboConcept/images/icons/system/false.gif) | adding russian translation
