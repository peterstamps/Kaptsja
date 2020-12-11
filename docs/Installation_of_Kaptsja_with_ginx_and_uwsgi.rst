*Installation of Kaptsja on Ubuntu with Nginx and uwsgi*
========================================================
Next instructions are valid for Ubuntu (tested on 20.04)
Important steps to start with!

 * Copy Kaptsja into /var/www/Kaptsja.

 * Change the ownership of the Kaptsja directory with its sub-directories: 
 
    **sudo chown -R www-data:www-data /var/www/Kaptsja**

    When PermissionErrors like below occur during start of uwsgi, the command above hasn't been executed (poperly). 
    PermissionError: [Errno 13] Permission denied: '/var/www/Kaptsja/log/Kaptsja.log'

 * Create this directory AND it sub directories if it doesn't exist: 
 
    *  **sudo mkdir /run/uwsgi/app/bottle/socket**
    *  **sudo mkdir /run/uwsgi**
    *  **sudo mkdir /run/uwsgi/app/**
    *  **sudo mkdir /run/uwsgi/app/bottle**
    *  **sudo chown -R www-data:www-data /run/uwsgi**

    When bind() error occurs when runing uwsgi with this message: No such file or directory [core/socket.c line 230] appears, the commands above haven't been executed (or repeate them).
    Probably  you switched to another wsgi executable and the Bottle directory had been removed .
    uwsgi is default started with the option vacuum = true and tries to remove all of the generated files and sockets. 
    
    See also below the section: ** uwsgi: bind(): No such file or directory [core/socket.c line 230]**


When using a virtual Python environment extra attention must be paid to the location of the executable binary files.
(virtual Python environment as documented here https://docs.python.org/3/tutorial/venv.html).

Multiple versions of Python (or Nginx/uwsgi) may be installed and the right paths to the executables must be used.
For example when installing packages with pip or running uwsgi it can easily go wrong here.

First check if you are in a virtual environment setup. This command could help.
Multiple Python versions might be installed on the Linux distribution. 
Therefore always verify which pip you are using. 

Run pip -V (uppercase) and check path.
When pip is not found install pip with: **sudo apt install python3-pip**.

Replace <USER>
At the Linux prompt run:~$ **pip -V**. Below it has been executed in a Python virtual environment.

    pip 20.2.4 from /home/<USER>/.pyenv/versions/3.7.4/lib/python3.7/site-packages/pip (python 3.7)

**Installation of required packages**
=====================================
When in doubt use the full path to pip3 like /usr/bin/pip3, else simply use: pip install <package>.

 * sudo pip3 install bottle  
 * sudo pip3 install uwsgi 
 * sudo pip3 install uwsgi-plugin-python3 
 * sudo pip3 install pycryptodome ( 1 )
 * Optional: sudo pip3 install gevent   

 ( 1 ) Alternatively pycrypto can be used combined with Python 3.7.4.  

Using pycrypto with Python 3.8 generates this error:  AttributeError: module 'time' has no attribute 'clock' 
See readme2.rst to solve this error


*"Native" installation of Nginx*
================================
**sudo apt install nginx**
    
How to configure nginx?
-----------------------
Note: default installation locations have been used here.

 * Create file Kaptsja.conf with the listed content below in /etc/nginx/sites-available directory.
 * Change in Kaptsja.conf <name_of_the_server> e.g.  Kaptsja.com  or localhost. 
 * Keep other Nginx directives unless you want to change them for example the listen port or location /captsite.

 * Create a soft link in /etc/nginx/sites-enabled directory to the Kaptsja.conf file in /etc/nginx/sites-available directory.
   
 How to create the soft link? 
 * cd  /etc/nginx/sites-enabled
 * sudo ln -s /etc/nginx/sites-available/Kaptsja.conf  Kaptsja.conf

Content of /etc/nginx/sites-available/Kaptsja.conf 
--------------------------------------------------

::

    server {
    listen 9000;
    server_name <name_of_the_server>;
    # development, else commented    root /var/www/Kaptsja;

    location /captsite {
        try_files $uri @uwsgi;
    }

    location @uwsgi {
        include uwsgi_params;
        uwsgi_pass _bottle;
    }
    }
    upstream _bottle {
    # this path must be exactly the same as used in Kaptsja.ini file for uwsgi!
    server unix:/run/uwsgi/app/bottle/socket;
    }


**Installation of uwsgi with Python3 plugin**
=============================================
 * sudo apt install uwsgi
 * sudo apt install uwsgi-plugin-python3
 * Optional: sudo apt install uwsgi-logger-file 

How to configure uwsgi?
----------------------- 
Note: default installation locations have been used here.

* Create file Kaptsja.ini with the listed content below in /etc/uwsgi/apps-available directory.
* Keep the uwsgi settings unless you want to change them.
* Note: plugin must contain: python3 <-- Do specify python3 here.
* Locate in /usr/lib/uwsgi/plugins this module *python3_plugin.so* (python38_plugin.so is there when Python 3.8 was installed)
* Create a soft link in /etc/uwsgi/apps-enabled directory to the Kaptsja.ini file in /etc/uwsgi/apps-available directory. 

  How to create the soft link?
   * cd  /etc/uwsgi/apps-enabled
   * sudo ln -s /etc/uwsgi/apps-available/Kaptsja.ini  Kaptsja.ini

Content of /etc/uwsgi/apps-available/Kaptsja.ini 
------------------------------------------------
**EXAMPLE 1**
 
::

    [uwsgi]
    socket = /run/uwsgi/app/bottle/socket
    chdir = /var/www/Kaptsja
    master = true
    plugins-dir = /usr/lib/uwsgi/plugins
    plugins = /usr/lib/uwsgi/plugins/python3_plugin.so
    plugin = python3
    file = /var/www/Kaptsja/scripts/KaptsjaSite.py
    vacuum = false
    chown-socket = www-data
    chmod-socket = 660
    uid = www-data
    gid = www-data
    log-date = true


**EXAMPLE 2**

::

    [uwsgi]
    socket = /run/uwsgi/app/bottle/socket
    chdir = /var/www/Kaptsja
    master = true
    binary-path = /home/<USER>/.pyenv/shims/uwsgi
    plugins-dir = /usr/lib/uwsgi/plugins
    plugins = /usr/lib/uwsgi/plugins/python3_plugin.so
    plugin = python3,ping
    virtualenv = /home/<USER>/.pyenv
    file = /var/www/Kaptsja/scripts/KaptsjaSite.py
    pythonpath = /var/www/Kaptsja/scripts
    module = KaptsjaSite
    # user identifier of uWSGI Unix socket
    vacuum = false
    chown-socket = www-data
    # set mode of created UNIX socket
    chmod-socket = 660
    # place timestamps into log
    log-date = true
    # user identifier of uWSGI processes
    uid = www-data
    # group identifier of uWSGI processes
    gid = www-data

**Explanation, some extra settings are provided and can be useful**

 - socket:    keep it as defined /run/uwsgi/app/bottle/socket 
 - chdir:    put here the directory in which Kaptsja has been placed
 - master:         keep value true
 - binary-path: the uWSGI executable to use. Remove if you didn’t install the (optional) uwsgi package in your virtual environment.
        In this example replace <user>:  binary-path = /home/<user>/.pyenv/shims/uwsgi 
 - plugins-dir: the full path to the directory where the uwsgi plugins are found
 - plugins:     (the full path to) the file of the uwsgi plugin(s) like: /usr/lib/uwsgi/plugins/python3_plugin.so
 - plugin:      Same as plugins, only here the plugin name is defined: python3. More plugins are specified with comma: python,ping
 - virtualenv:  The virtual environment for your application. Example: virtualenv = /home/<user>/.pyenv
 - file:        The name of the file that houses your application, and the object that speaks the WSGI interface, separated by colons. 
                This depends on your web framework. Bottle program must contain: app = application = Bottle()
                Example: file = /var/www/Kaptsja/scripts/KaptsjaSite.py
 - module:      The name of the module that houses your application (see file). 
                The module(s) must be found on the Python path; use pythonpath parameter when needed. 
                Example: module = KaptsjaSite. Use file if not sure.
 - pythonpath:  This path will be Added to the pythonpath of the used environment.
                Example: pythonpath = /var/www/Kaptsja/scripts                
 - vacuum:      Defaults to true. vacuum = false means that uwsgi will not try to  remove all of the generated file/sockets.
                The /run/uwsgi/app/bottle/socket and its directory bottle will not be deleted else you need to recreate and set ownership to www-data for user and group on the (sub-directory /run/uwsgi/app/bottle when you had switched to another uwsgi binary command. 
 - chown-socket:   Keep: www-data. The user (owner) identifier of uWSGI Unix socket
 - chmod-socket:   Keep 660. Set mode of created UNIX socket
 - log-date:       Keep true. Places timestamps into log
 - uid:            Keep: www-data. The user identifier of uWSGI processes
 - gid:            Keep: www-data. The group identifier of uWSGI processes


*Before starting nginx and uwsgi*
=================================
The following checks might be needed:
 - Check KaptsjaConfiguration.py for these settings:
   
   * sitehost and siteport must be specified to your needs/situation
   * siteserver MUST be set to: siteserver = "python_server"  (between quotes)
   * sitedebug = False
   * site_reloader = False 
 
    
**The new startup for the Kaptsja site is now:**
    
**1. Start of uwsgi**
    
 In a default setup the startup command would be:
 * sudo service uwsgi start   options: {start|stop|status|restart|reload|force-reload}
 or
 * sudo /usr/bin/uwsgi --ini /etc/uwsgi/apps-enabled/Kaptsja.ini (optional with --plugin-list to show which are used)
        
 When in working with a Virtual Python environment the command would be (replace <user>!):
    
 * sudo /home/<user>/.pyenv/shims/uwsgi --ini /etc/uwsgi/apps-enabled/Kaptsja.ini
        
 When the uwsgi Emperor is installed the startup would be (replace <user>!):
    
 * default installation: sudo /usr/bin/uwsgi --ini /etc/uwsgi-emperor/emperor.ini
        
 * virtual environment:  sudo /home/<user>/.pyenv/shims/uwsgi --ini  /etc/uwsgi-emperor/emperor.ini

**2. Start of nginx**

 * In a default setup the startup command would be:
   * sudo service nginx start   options: {start|stop|status|restart|reload|force-reload}
   or
   * sudo /usr/sbin/nginx -c /etc/nginx/sites-enabled/Kaptsja.conf
 * When in working with a Virtual Python environment the command would be (replace <user>!):
        sudo /home/<user>/.pyenv/shims/nginx -c /etc/nginx/sites-enabled/Kaptsja.conf

 3. Open browser and enter url: http://<name_of_the_server>:9000/capsite
       
   * When changes are made in the Nginx file then this url and port must probably be adapted as well.
       

*Common Errors*
---------------

**No module named 'python_server'**

After changing the siteserver setting a start up with Python might give an error like shown below.
E.g. this can easily happen when virtual environment and non virtual settings are mixed by accident.

Example:    
sudo /home/<user>/.pyenv/shims/python3.7 /var/www/Kaptsja/scripts/KaptsjaSite.py

::   
  Traceback (most recent call last):
  File "/home/<user>/.pyenv/versions/3.7.4/lib/python3.7/site-packages/bottle.py", line 3124, in run
  server = load(server)
  File "/home/<user>/.pyenv/versions/3.7.4/lib/python3.7/site-packages/bottle.py", line 3044, in load
  if module not in sys.modules: __import__(module)
  ModuleNotFoundError: No module named 'python_server'    

Check if the uwsgi module **python3_plugin.so** can be located from this (virtual) environment. Probably not!

Run **sudo /usr/bin/uwsgi --ini /etc/uwsgi/apps-enabled/Kaptsja.ini --plugin-list** to show which plugins are used.


**[Errno 2] No such file or directory**

When KaptsjaSite.py is started from the wrong directory the following error will be displayed. Correct the path.
Example, when run from <user>'s home directory: 

    sudo /usr/bin/python3.8 /var/www/Kaptsja/scripts/KaptsjaSite.py
    
::
    Start this program from Kaptsja home directory. It was started in /home/<user>.
    [Errno 2] No such file or directory: '/home/<user>/log/Kaptsja.log'
    
**uwsgi: bind(): No such file or directory [core/socket.c line 230]**

 This error appears when:
 *  /run/uwsgi directory and/or its sub-dorectories do not exist anymore. uwsgi might have removed them, see below.

**Listing Example part 1**

::

    Thu Dec 10 11:42:07 2020 - thunder lock: disabled (you can enable it with --thunder-lock)
    Thu Dec 10 11:42:07 2020 - bind(): No such file or directory [core/socket.c line 230]
    
To solve the issue. run following sequence of commands:
 *  sudo mkdir /run/uwsgi/app/bottle/socket
 *  sudo mkdir /run/uwsgi
 *  sudo mkdir /run/uwsgi/app/
 *  sudo mkdir /run/uwsgi/app/bottle
 *  sudo chown -R www-data:www-data /run/uwsgi
 *  sudo /usr/bin/uwsgi   --ini /etc/uwsgi/apps-enabled/Kaptsja.ini

**Listing Example part 1**

::

    [uWSGI] getting INI configuration from /etc/uwsgi/apps-enabled/Kaptsja.ini
    Thu Dec 10 11:46:30 2020 - *** Starting uWSGI 2.0.18-debian (64bit) on [Thu Dec 10 11:46:30 2020] ***
    Thu Dec 10 11:46:30 2020 - compiled with version: 10.0.1 20200405 (experimental) [master revision 0be9efad938:fcb98e4978a:705510a708d3642c9c962beb663c476167e4e8a4] on 11 April 2020 11:15:55
    Thu Dec 10 11:46:30 2020 - os: Linux-4.19.128-microsoft-standard #1 SMP Tue Jun 23 12:58:10 UTC 2020
    Thu Dec 10 11:46:30 2020 - nodename: <SERVER_NAME>
    Thu Dec 10 11:46:30 2020 - machine: x86_64
    Thu Dec 10 11:46:30 2020 - clock source: unix
    Thu Dec 10 11:46:30 2020 - pcre jit disabled
    Thu Dec 10 11:46:30 2020 - detected number of CPU cores: 8
    Thu Dec 10 11:46:30 2020 - current working directory: /home/<USER>/demo
    Thu Dec 10 11:46:30 2020 - detected binary path: /usr/bin/uwsgi-core
    Thu Dec 10 11:46:30 2020 - chdir() to /var/www/Kaptsja
    Thu Dec 10 11:46:30 2020 - your processes number limit is 37954
    Thu Dec 10 11:46:30 2020 - your memory page size is 4096 bytes
    Thu Dec 10 11:46:30 2020 - detected max file descriptor number: 1024
    Thu Dec 10 11:46:30 2020 - lock engine: pthread robust mutexes
    Thu Dec 10 11:46:30 2020 - thunder lock: disabled (you can enable it with --thunder-lock)
    Thu Dec 10 11:46:30 2020 - uwsgi socket 0 bound to UNIX address /run/uwsgi/app/bottle/socket fd 3
    Thu Dec 10 11:46:30 2020 - setgid() to 33
    Thu Dec 10 11:46:30 2020 - setuid() to 33
    Thu Dec 10 11:46:30 2020 - Python version: 3.8.5 (default, Jul 28 2020, 12:59:40)  [GCC 9.3.0]
    Thu Dec 10 11:46:31 2020 - *** Python threads support is disabled. You can enable it with --enable-threads ***
    Thu Dec 10 11:46:31 2020 - Python main interpreter initialized at 0x562a9c2903c0
    Thu Dec 10 11:46:31 2020 - your server socket listen backlog is limited to 100 connections
    Thu Dec 10 11:46:31 2020 - your mercy for graceful operations on workers is 60 seconds
    Thu Dec 10 11:46:31 2020 - mapped 145840 bytes (142 KB) for 1 cores
    Thu Dec 10 11:46:31 2020 - *** Operational MODE: single process ***
    Thu Dec 10 11:46:31 2020 - WSGI app 0 (mountpoint='') ready in 0 seconds on interpreter 0x562a9c2903c0 pid: 3430 (default app)
    Thu Dec 10 11:46:31 2020 - *** uWSGI is running in multiple interpreter mode ***
    Thu Dec 10 11:46:31 2020 - spawned uWSGI master process (pid: 3430)
    Thu Dec 10 11:46:31 2020 - spawned uWSGI worker 1 (pid: 3438, cores: 1)
    
