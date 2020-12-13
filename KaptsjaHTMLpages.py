###################################################################################################
#  KaptsjaHTMLpages creates the KaptsjaHome page, KaptsjaSuccess page and KaptsjaFilure page
#  Kaptsja is the Dutch phonetic pronunciation of the English word Captcha.
#
#  WARNING: BEFORE CHANGING ANYTHING IN THIS FILE MAKE A BACKUP SO YOU CAN RESTORE !
#  Read the comments in this file as they contain valuable information to understand the effects 
###################################################################################################

import sys
# sys.path.append("/path/to/your/package_or_module")
sys.path.append(r"./scripts")
import os
import time
import logging
# import the configuration
from KaptsjaConfiguration import *
############################################################################################################################################################
#  SETTINGS  (start) See /Kaptsja/scripts/KaptsjaConfiguration.py 
############################################################################################################################################################
# When needed change level level=logging.INFO or level=logging.DEBUG)
# get the directory in which the script was started.
serve_path = os.getcwd()  
try:
    logging.basicConfig(filename=log_file, level=logging.ERROR)
except PermissionError as e:
    print("Check permissions for Kaptsja and its subdirectories.\n\n%s\n\n" % e)
    sys.exit()
except Exception as e:
    print("Start this program from Kaptsja home directory. It was started in %s.\n\n%s\n\n" %(serve_path, e) )
    sys.exit()
############################################################################################################################################################
#  SETTINGS  (End)
############################################################################################################################################################

##########################################
# START of validation of the configuration
##########################################  

if 360 <= int(input_picture_rescale_width) <= 598:
    modal_content_width = input_picture_rescale_width + 2 
if int(input_picture_rescale_width) == 0: # 
    modal_content_width = 600  # this is the default value
text = "Home"
if not "home_page_tab1" in globals():
    home_page_tab1 = text
if home_page_tab1 == "":
    home_page_tab1 = text
if home_page_tab1 is None:
    home_page_tab1 = ""

text = "1. Kaptsja Page"
if not "home_page_tab2" in globals():
    home_page_tab2 = text
if home_page_tab2 == "":
    home_page_tab2 = text
if home_page_tab2 is None:
    home_page_tab2 = ""
    
text = "2. Kaptsja Modal Page"
if not "home_page_tab3" in globals():
    home_page_tab3 = text
if home_page_tab3 == "":
    home_page_tab3 = text
if home_page_tab3 is None:
    home_page_tab3 = ""

text = "3. Kaptsja inside page element &lt;div&gt ... &lt;/div&gt;"
if not "home_page_tab4" in globals():
    home_page_tab4 = text
if home_page_tab4 == "":
    home_page_tab4 = text
if home_page_tab4 is None:
    home_page_tab4 = ""

text = "To select the activated Kaptsja model click on tab "
if not "home_page_click_tab_text" in globals():
    home_page_click_tab_text = text
if home_page_click_tab_text == "":
    home_page_click_tab_text = text
if home_page_click_tab_text is None:
    home_page_click_tab_text = ""

text = "Only one model can be active at a time. To activate another model, "
if not "home_page_one_model_active_text" in globals():
    home_page_one_model_active_text = text
if home_page_one_model_active_text == "":
    home_page_one_model_active_text = text
if home_page_one_model_active_text is None:
    home_page_one_model_active_text = ""

text = "change setting 'active_captcha_model' in configuration file KaptsjaConfiguration.py."
if not "home_page_change_setting_text" in globals():
    home_page_change_setting_text = text
if home_page_change_setting_text == "":
    home_page_change_setting_text = text
if home_page_change_setting_text is None:
    home_page_change_setting_text = ""
    
##########################################
# END of validation of the configuration
##########################################

def create_KaptsjaHome_html_file():
    # All braces for css and javascript itself MUST be double notation like {{ // some css or javascript code }} to escape the first. 
    # Only ony brace will be generated in the output. All formatting keys like .format(key= ) MUST have a single brace {key} notation.
    captcha_page_url_active = "#"
    modal_page_url_active = "#"
    div_page_url_active = "#"
    if active_captcha_model == 1:
        captcha_page_url_active = captcha_page_url 
    elif active_captcha_model == 2:
        modal_page_url_active = modal_page_url 
    elif active_captcha_model == 3:
        div_page_url_active = div_page_url 
    
    html_1 = '''
    <html>
<!-- this file is generated by KaptsjaHTMLpages.py -->
    <head>
    <!-- Include Bootstrap 3.3.7 CSS here in the head section -->
    <link rel="stylesheet" href="/captsite/css/bootstrap.min-3.3.7.css"> 
    <style>
    .nav-tabs > li > a {{
    margin-right: 2px;
    line-height: 1.42857143;
    border-left: 1px solid #00000038;
    border-right: 1px solid #00000038;
    border-top: 1px solid #00000038;
    border-radius: 4px 4px 0 0;
    }}
    </style>
    </head>
    <body>
    <div>
        <ul class="nav nav-tabs">
          <li role="presentation" class="active"><a href="#">{home_page_tab1}</a></li>
          <li role="presentation"><a href="{captcha_page_url}">{home_page_tab2}</a></li>
          <li role="presentation"><a href="{modal_page_url}">{home_page_tab3}</a></li>
          <li role="presentation"><a href="{div_page_url}">{home_page_tab4}</a></li>
        </ul>
    </div>
    <div><h3>{home_page_click_tab_text} {active_captcha_model}.</h3>
    <h5>{home_page_one_model_active_text}</h5>
    <h5>change setting 'active_captcha_model' in configuration file KaptsjaConfiguration.py.<h5></div>
    <!-- Include First the jQuery and Second Bootstrap javascript libraries. Order is important! -->
    <script src="/captsite/js/jquery.min-3.5.1.js"></script>
    <script src="/captsite/js/bootstrap.min-3.3.7.js"></script>
     </body>
</html>     
    '''.format(captcha_page_url=captcha_page_url_active, \
    modal_page_url=modal_page_url_active, \
    div_page_url=div_page_url_active, \
    active_captcha_model=active_captcha_model, \
    home_page_click_tab_text=home_page_click_tab_text, \
    home_page_one_model_active_text=home_page_one_model_active_text, \
    home_page_change_setting_text=home_page_change_setting_text, \
    home_page_tab1=home_page_tab1, \
    home_page_tab2=home_page_tab2, \
    home_page_tab3=home_page_tab3, \
    home_page_tab4=home_page_tab4
    )

    try:
        htmlfile = open(gen_home_page_file,"w", encoding="utf-8") 
        htmlfile.write(html_1)
        htmlfile.close()
        logging.info(r"Generation Kaptsja Home HTML page file success: %s" % gen_home_page_file)
        return True
    except:
        logging.error(r"Generation Kaptsja Home HTML page file failure: %s" % gen_home_page_file)
        return False

def create_KaptsjaSuccess_html_file():
    # All braces for css and javascript itself MUST be double notation like {{ // some css or javascript code }} to escape the first. 
    # Only ony brace will be generated in the output. All formatting keys like .format(key= ) MUST have a single brace {key} notation.
    html='''<!doctype html>
<html>
<!-- this file is generated by KaptsjaHTMLpages.py -->
  <head>
  </head>
    <style>
    body {{
        text-align: center;
        padding: 40px 0;
        background: #EBF0F5;
    }}
    h1 {{
        color: #88B04B;
        font-family: "Nunito Sans", "Helvetica Neue", sans-serif;
        font-weight: 900;
        font-size: 40px;
        margin-bottom: 10px;
    }}
    p {{
        color: #404F5E;
        font-family: "Nunito Sans", "Helvetica Neue", sans-serif;
        font-size:20px;
        margin: 0;
    }}
    .card {{
        background: white;
        padding: 60px;
        border-radius: 4px;
        box-shadow: 0 2px 3px #C8D0D8;
        display: inline-block;
        margin: 0 auto;
    }}
    .checkmark {{
        font-family: "Nunito Sans", "Helvetica Neue", sans-serif;
        color: #ffffff;
        font-size: 150px;
        line-height: 200px;
        margin-left: 0px;;
    }}
    </style>
    <body>
      <div class="card">
      <div style="border-radius:200px; height:200px; width:200px; background: #9ABC66; margin:0 auto;">
        <span class="checkmark">✓</span>
      </div>
        <h1>Success</h1> 
        <p>You solved the CaptCha successfully;<br/> You may now continue. Click <a href="{success_cont_url}">here.</a></p>
      </div>
    </body>
</html>
    '''.format(success_cont_url=success_cont_url)
    
    try:
        htmlfile = open(gen_success_page_file,"w", encoding="utf-8") 
        htmlfile.write(html)
        htmlfile.close()
        logging.info(r"Generation Kaptsja Success HTML page file success: %s" % gen_success_page_file)
        return True
    except:
        logging.error(r"Generation Kaptsja Success HTML page file failure: %s" % gen_success_page_file)
    return False

def create_KaptsjaFailure_html_file():
    # All braces for css and javascript itself MUST be double notation like {{ // some css or javascript code }} to escape the first. 
    # Only ony brace will be generated in the output. All formatting keys like .format(key= ) MUST have a single brace {key} notation.
    if max_captcha_sets > 0: 
        time_message = ";"
    else:
        time_message = " within {max_time_to_solve} seconds;".format(max_time_to_solve=max_time_to_solve)
    html='''<!doctype html>
<html>
<!-- this file is generated by KaptsjaHTMLpages.py -->
  <head>
  </head>
    <style>
    body {{
        text-align: center;
        padding: 40px 0;
        background: #EBF0F5;
    }}
    h1 {{
        color: #f54242;
        font-family: "Nunito Sans", "Helvetica Neue", sans-serif;
        font-weight: 900;
        font-size: 40px;
        margin-bottom: 10px;
    }}
    p {{
        color: #404F5E;
        font-family: "Nunito Sans", "Helvetica Neue", sans-serif;
        font-size:20px;
        margin: 0;
    }}
    .card {{
        background: white;
        padding: 60px;
        border-radius: 4px;
        box-shadow: 0 2px 3px #C8D0D8;
        display: inline-block;
        margin: 0 auto;
    }}
    .falsemark {{
        font-family: "Nunito Sans", "Helvetica Neue", sans-serif;
        color: #ffffff;
        font-size: 150px;
        line-height: 200px;
        margin-left: 0px;;
    }}
    </style>
    <body>
      <div class="card">
      <div style="border-radius:200px; height:200px; width:200px; background: #f54242; margin:0 auto;">
        <span class="falsemark">X</span>
      </div>
        <h1>Failure</h1> 
        <p>You did not solve the CaptCha successfully{time_message}<br/> You may now retry. Click <a href="{failure_cont_url}">here.</a></p>
      </div>
    </body>
</html>
    '''.format(failure_cont_url=failure_cont_url, time_message=time_message)
    
    try:
        htmlfile = open(gen_failure_page_file,"w", encoding="utf-8") 
        htmlfile.write(html)
        htmlfile.close()
        logging.info(r"Generation Kaptsja Failure HTML page file success: %s" % gen_failure_page_file)
        return True
    except:
        logging.error(r"Generation Kaptsja Failure HTML page file failure: %s" % gen_failure_page_file)
        return False

if __name__ == '__main__':
    retcode = create_KaptsjaHome_html_file()
    if retcode == True:
       print(r"Generation of Kaptsja Home HTML page file succeeded.")
    else:
       print(r"Generation of Kaptsja Home HTML page file failed.")

    retcode = create_KaptsjaSuccess_html_file()
    if retcode == True:
       print(r"Generation of Kaptsja Success HTML page file succeeded.")
    else:
       print(r"Generation of Kaptsja Success HTML page file failed.")

    retcode = create_KaptsjaFailure_html_file()
    if retcode == True:
       print(r"Generation of Kaptsja Failure HTML page file succeeded.")
    else:
       print(r"Generation of Kaptsja Failure HTML page file failed.")
