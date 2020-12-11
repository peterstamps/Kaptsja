Introduction
============
The configuration file  KaptsjaConfiguration.py is located in /Kaptsja/scripts/ directory.
Before changing this file make a backup!
You may adapt the configuration settings. Be aware that this is normal Python code! 

Note: there are many settings to control the output, urls, directories, file names and so on.
Before changing a setting reead the comments in the configuration file to understand its usage and defaults, the maximum and minimum value, 

In the /Kaptsja/scripts/ directory you will find: 
 * KaptsjaGenerator.py         --> This module generates the Kaptsja Image and the HTML file with JavaScript (see below)
 * KaptsjaConfiguration.py     --> The configuration settings used by files listed below.
 * KaptsjaSite.py              --> The Kaptsja web site startup module (requires installation of bottle package).
 * KaptsjaEncDec.py            --> A AES Encryption / Decryption module, can be used for may purposes 
 * KaptsjaHTMLpages.py         --> This generator creates the static HTML pages for the Success Page, Failure Page and Home Page
                                  

KaptsjaConfiguration.py module is imported by following modules: 
 * KaptsjaGenerator.py 
 * KaptsjaSite.py 
 * KaptsjaHTMLpages.py
 * KaptsjaPictureIco.py

**KaptsjaGenerator.py**: processing overview (input and output)
----------------------------------------------------------------
All examples are based on default settings in KaptsjaConfiguration.py.

 * The generator imports the configuration file and checks first the settings. Configuration errors are logged and the module exits. When possible useful default value will be set when not provided.
 * The generator expects always 1 input picture from the /Kaptsja/media/ directory as defined in the configuration file. 
 * When the randomlist setting is set to True, the input pictures will be randomly taken from the directory as defined for setting randomlist_dir in the configuration. During startup the directory is read once. Newly added pictures become active after restart of the KaptsjaSite.py. During run time of this modue no pictures should be deleted as that will/might cause an error.
 * Too large input pictures are automatically (once) resized when needed. The original picture will be overwritten, so keep a copy of the originals.
 * A Copyright text and its color can be specified and the position can be set to right or left upper corner.
 * Too small input pictures may cause issues like too less space to position all circles with character without an overlap. Consult the error log when indicated on the web page. Analyse the error and follow the generated recommendation for better picture sizes nad to avoid such errors in the future.
 *  A string of UPPERCASE letters and digits must be provided when running the KaptsjaGenerator module from a command prompt. When nothing is provided (as for example from a web page) such string will be generated randomly. Unicode charcaters are supported, so Chinese characters will be displayed as well when defined in the configuration file.
 *   For each (generated or provided) character one (1) circle will be created in the picture at a random location, but always outside the calculated text zone at the bottom where the instruction text for the user is placed.
 *   The diameter of a circle and its colors are random created. 
 *   The transparency percentage for a circle can be changed in the configuration file.
 *   Each character is randomly distorted/morphed (configurable morphing) to make it difficult for automatic recognition. 
 *   A human is usually better in "connecting the missing parts" to determine the intended character.
 *   A "crowded" input picture might require a decrease of the transparency percentage. 
 *   The user can always renew a generated picture to obtain a Kaptsja picture with a better visibility/readability of the characters.
 *   A user is asked to sort the characters in a given order as shown in the text zone (instruction text). 
 *   The sorting order is randomly determined and the instructions for the user are adapted accordingly.
 *   The instructions in the text zone are somewhat distorted by overlapping lines.
 *   The line color and width, text color, background color and transparency of the text zone and text alignment (left or centered) can be defined
 *   The user needs to click on each circle only once. 
 *   A number of clicks is counted and shown. It tells the user how many circles have been clicked.
 *   When the number of clicks equals the number of displayed characters (circles) the Submit button is enabled.
 *   When a user makes a clicking mistake a Retry is possible before clicking the Submit button. 
 *   The Retry button resets the counter to zero clicks and will disable the Submit button.
 *   A user can retry till the number of retries as defined in the configuration file has been reached (default 2 Retries).
 *   A user has "One plus the number of defined retries" possibities to execute this exercise (default 3 possibilities). 
 *   If the number of retries is exceeded the user gets a message "too many retries".
 *   In such case a reload / refresh of the Kaptsja page is required to generate a new picture. 
 *   Going back to the Kaptsja page in the browser to retry the Kaptsja again is not possible. A refresh of the full page is mandatory.
 *   When the user Submits the page, the click result will be checked and either a Success Page or a Failure page will be displayed. This routing behavior can easily be overruled in the configuration file, so a user can for example be routed to the next page on the site when the Kaptsja check returns a Success code.

**Generation of Kaptsja pages for the different models (dynamic generation versus pre-generated Kaptsja pages):**

 *   If setting max_captcha_sets = 0 then the dynamic Kaptsja generation will occur automatically
 * 	 When in dynamic mode of operandi the setting time_keep_captcha_set defines how long the generated Kaptsja pages will "survive" in work_dir after being served.
 *   This allows proper time to transport to in the browser of the user (brwoser might load with some delay )
 *   When max_captcha_sets has a value greater than 0, the modus of operandi will change to pre-generation of Kaptsja pages.
 *   The specified number of sets will be generated when you Run from Kaptsja home directory ./scripts/KaptsjaGenerator.py.
 *   When the work_dir is not empty a message will be displayed and existing files must first be deleted manually.
 *   Generating Kaptsja pages will take moment. Wait till "Finished" appears in the command window.
 
**KaptsjaGenerator.py**: Input - Output overview
------------------------------------------------ 
The following input / output (files) will be used or created.

``Input``: The background Kaptsja picture is located in /Kaptsja/media/ directory. It is defined in the configuration file.
               You can use an own picture (jpeg, png and other types as well) as background for the Kaptsja circles with characters.

               **Pictures with a width > 588 pixels will automatically be resized to fit in the modal window of 600px and the provided picture will be overwritten (at the same location).**

``Input/Output``: Kaptsja_secret_key.txt in /Kaptsja/key/ directory  --> when this file does not exist or is deleted a new one will be generated automatically

``Output``: KaptsjaPicture_xxx.png in /Kaptsja/work/ directory  --> the generated Kaptsja image with circles and  somewhat morphed characters and Text is added to the background Kaptsja picture.

``Output``: KaptsjaPage_xxx.html in /Kaptsja/html/ directory   --> the generated HTML page includes Javascript and generated href references (links). Based on the original defaults in the configuration file the following mapping is used: 

        - href: /captsite/work/KaptsjaPicture_xxx.png?random=1605640339.2643156 --> file: /Kaptsja/work/KaptsjaPicture_xxx.png
          ?random=....... is added to always force a reload of the picture. Some web browsers did not refresh despite special header settings in the response document like: "Cache-Control" : "no-cache" or "Cache-Control" : "must-revalidate, max-age=1, no-store"
        - href: /captsite/css/bootstrap.min-3.3.7.css --> file: /Kaptsja/css/bootstrap.min-3.3.7.css
        - href: /captsite/js/bootstrap.min-3.3.7.js   --> file: /Kaptsja/js/bootstrap.min-3.3.7.js
        - href: /captsite/js/jquery.min-3.5.1.js      --> file: /Kaptsja/js/jquery.min-3.5.1.js
            
``Output``: Kaptsja.log in /Kaptsja/log/ directory --> you can change in KaptsjaGenerator.py the level of logging. 
  
  Search for this line: 
   logging.basicConfig(filename=log_file, level=logging.ERROR

  When needed change level:  level=logging.INFO or level=logging.DEBUG.

**KaptsjaSite.py** performs following processing
-------------------------------------------------
The Bottle server is used. 

``Imports``
    KaptsjaSite.py imports *KaptsjaGenerator.py* and *KaptsjaConfiguration.py* and *KaptsjaHTMLpages.py* to call various functions like:
     - create_KaptsjaHome_html_file
     - create_KaptsjaFailure_html_file
     - create_captcha
     - get_captcha
     - verify_kcaptcha
     
     It uses the urls settings from the configuration file for routing. See @app.route(....) in the module.

     It uses the file settings from the configuration file for file locations.

     It picks the sitehost, siteport and more settings to configure the HTTP server (like site server = "wsgiref" , "gevent" or "python_server")
     
    
    Function verify_captcha returns code True or 0 when the Kaptsja is solved with success and redirects to the static HTML page KaptsjaSuccesPage.html.

    Function verify_captcha returns code False or 1 when the Kaptsja is NOT solved with success and redirect to the static HTML page KaptsjaFailurePage.html 
 
    When Function verify_captcha returns code > 1 then an HTML section is displayed "<p>An error has occured. Check the log file.</p>". In such case look into the log file CapthCha.log in /Kaptsja/log/ directory.
    
    When in KaptsjaConfiguration.py setting is *site_reloader = True*, all messages will be double printed during start of the Bottle server.
    To prevent a lot of restarts during development/test, the auto reloader will load the newest version of the code, when a change happened in the used code. 
    The main process of the reloader will not start a server, but spawn a new child process. Note: The effect is that all code is executed at least twice! The code looks similar like this:

::

   from bottle import run
   run(reloader=True)

    
``Logging`` 
    Kaptsja.log in /Kaptsja/log/ directory --> you can change in KaptsjaSite.py the level of logging. 
  
    Search for this line:

    logging.basicConfig(filename=log_file, level=logging.ERROR)
   
    When needed change log level:  level=logging.INFO or level=logging.DEBUG.
        
Following examples are based on default settings.

The Bottle HTTP Server listens on ip "localhost" and port 8080 as defined in configuration file.

Look for settings: sitehost and port.
The URL http://localhost:8080/ redirects to Home page with URL http://localhost:8080/captsite/  
 
    
The **Home page** shows:
------------------------
  TABS:| Home | 1. Kaptsja Page  | 2. Kaptsja Modal Page  | 3. Kaptsja inside page element <div> ... </div> |
	To select the activated Kaptsja model click on tab 3.
	Only one model can be active at a time. To activate another model,
	change setting 'active_captcha_model' in configuration file KaptsjaConfiguration.py.

    
*Small scale production*
------------------------
    The Bottle server should be able to handle small volumes.
    When not in development mode change in KaptsjaConfiguration.py the following settings:    
    sitedebug = False
    site_reloader = False

*Notes to Caching issues*
-------------------------
During development of the Kaptsja software tough caching issues appeared and it caused a lof of time and effort to find proper resolutions.
Following measurements, tricks and settings are applied. The author does not guarantee that all possible caching problems have been solved, but up till now it looks okay.

* Extra Headers are added to the HTTP response documents.
	
   * response.set_header("Cache-Control", "no-cache, no-store, must-revalidate, max-age=0, s-maxage=0, proxy-revalidate") 
	
   * response.set_header("Pragma", "no-cache")
	
   * response.set_header("Expires", "Sat, 12 Oct 1991 05:00:00 GMT")
	
   * response.set_header("Vary", "*")
	
* To generated pictures, javascripts and css files a random unique string is added to the URL to trigger browser to retrieve the latest version
	
* In Javascript code: URL + ?random=" + formatted_stamp

* In Python code    : URL + ?random={force_reload}  where force_reload is set to time.time() (time from epoch) 

* In Python code    : as ultimate possibility (not activated, but you can search for "os.utime" in KaptsjaGenerator.py )

     # update the time stamps of the pre-generated files,
 
     # before serving it as it will help to force reloads, 

     # however when browser caching time of 1 second is not yet exceeded then user must refresh page again by clicking new picture

     # Therefore a short dealy of 1.5 seconds is programmed	search for "setTimeout" in KaptsjaGenerator.py
  
     # Try to use this "dirty trick" when there are still caching issues you cannot solve
            #os.utime(os.path.normpath(served_captcha_file))  


*Using another Web server*
--------------------------
To inform clients that the resource they’re requesting now resides at a different location, you can use the URL rewrite function in Apache and Nginx to map to the site referenced as "/captsite/".

The whole Kaptsja directory can be put under /var/www or other locations. A stock installation of Apache or Nginx on Ubuntu Linux will place their root directory at /var/www/.  

So you could for example use /var/www/Kaptsja. 

Add this directory to your PYTHONPATH environment variable when necessary. 

*Example Installation of Kaptsja with Nginx and uwsgi.rst*
----------------------------------------------------------
In file **Installation of Kaptsja with Nginx and uwsgi.rst** in /Kaptsja/docs an example configuration with installation instructions is provided. See ./docs/Installation_of_Kaptsja_with _ginx_and_uwsgi.rst

*How to avoid Bottle displaying a ResourceWarning message*
-----------------------------------------------------------
When running the Bottle HTTP server (version bottle==0.12.18) in a command window and using CTRL-C to stop it the following error or similar is displayed:
  ResourceWarning: unclosed <socket.socket fd=4, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('127.0.0.1', 8080)>  
  server.run(app)
  ResourceWarning: Enable tracemalloc to get the object allocation traceback
  
To avoid this message locate file bottle.py in the Python packages directories. Use following commands when needed:

*  Global site-packages ("dist-packages") directories are listed in sys.path when you run: **python -m site**. ...
*  The per user site-packages directory is where Python installs your local packages: **python -m site --user-site**.
 
Adapt the code as shown below. Around line 2787.  - (minus sign) means comment or delete this line; + (plus sign) means add this line.
:: 

    --- /usr/local/bin/bottle.py	2021-07-05 15:03:00.323108321 +0000
    +++ /usr/local/bin/bottle.py	2021-07-05 15:03:23.722962103 +0000

    @@ -2787,7 +2787,11 @@
                         address_family = socket.AF_INET6
     
             srv = make_server(self.host, self.port, app, server_cls, handler_cls)
    -        srv.serve_forever()
    +        try:
    +            srv.serve_forever()
    +        except KeyboardInterrupt:
    +            srv.shutdown() # Stops the serve_forever loop.
    +            srv.server_close() # Called to clean-up the server.
    +            raise

     
     class CherryPyServer(ServerAdapter):


**KaptsjaEncDec.py** performs following processing.
---------------------------------------------------
This module is a AES Encryption / Decryption module and encrypts/decrypts the values needed to verify the Captcha puzzle (see also KaptsjaGenerator.py paragraphs).
  
All Encryption and Decryption Steps are in detailed explained with examples in this module.
It has been tested with Chinese and West-Europe Characters.
Also Text Files can be encrypted/decrypted.
Test files created by this module when started from a command line are:

 * Z__input.txt
     
   Contains a sentence written as text by KaptsjaEncDec.py like: A long NEW FILE sentence with some extra Chinese words. 

 * Z__input_enc.txt

   Contains the Encrypted Version of the input

 *  Z__input_dec.txt

   Contains the Decrypted Version of the Encrypted input 

**KaptsjaHTMLpages.py** performs following processing.
--------------------------------------------------------------------------------

This generator creates the static HTML pages for the Modal HTML, Success Page, Failure Page and Home Page DIV Page using the Configuration Settings.
When KaptsjaSite.py is started all pages will be (re-)generated before the Bottle Server starts.
If a Configuration setting has been changed w.r.t to URLs, picture sizes, number of retries, clicks etcetera, then re-run this module from the home directory (Default Kaptsja  "./") or re-start KaptsjaSite.py.

Enter command: *python ./scripts/KaptsjaHTMLpages.py* and read the shown results. 
Or  *python ./scripts/KaptsjaSite.py* and read the shown results. 


**KaptsjaPictureIco.py** performs following processing.
--------------------------------------------------------------------------------

Modeul KaptsjaPictureIco.py (re-)creates the Kaptsja_bg.jpg and Kaptsja.ico and puts them in media_dir.
In a command window run from the Kaptsja home directory this command: python ./scripts/KaptsjaPictureIco.py.
That's it!

 