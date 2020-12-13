###################################################################################################
#  KaptsjaGenerator creates Dynamically Captcha puzzles. They cen be served dynamically or as a pre-generated CaptCha set
#  Kaptsja is the Dutch phonetic pronunciation of the English word Captcha.
#
#  WARNING: BEFORE CHANGING ANYTHING IN THIS FILE MAKE A BACKUP SO YOU CAN RESTORE !
#  Read the comments in this file as they contain valuable information to understand the effects 
###################################################################################################

import sys
# sys.path.append("/path/to/your/package_or_module")
sys.path.append(r".")
# import pytesseract  # only used to parse generated Kaptsja Image false for analysis purposes only. Program tesseract must be installed!
from PIL import Image, ImageDraw, ImageFont  #,  ImageFilter
from bs4 import BeautifulSoup as bs  # prettify/complete broken HTML output
import random
import re
import string
from base64 import b64decode
import os
import glob
import time
import logging
import threading
from KaptsjaEncDec import Cripto
# import the configuration
from KaptsjaConfiguration import *
#
############################################################################################################################################################
#  SETTINGS  (start) See ./scripts/Kaptsja_configuration.py 
############################################################################################################################################################
# end of imports
logging.basicConfig(filename=log_file, level=logging.ERROR, \
    format='%(asctime)s %(levelname)-8s %(message)s', \
    datefmt='%Y-%m-%d %H:%M:%S')
# make directory for encryption key when it doesn't exists
if not os.path.exists(key_dir):
    os.makedirs(key_dir)
# make directory for temporary files when it doesn't exists
if not os.path.exists(work_dir):
    os.makedirs(work_dir)
##########################################
# START of validation of the configuration
##########################################  
syserrmsg = "Error! Look in log file."
# Function to validate 
# hexadecimal color code . 
def isValidHexaCode(str):
    # Regex to check valid 
    # hexadecimal color code.
    regex = "^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
    # Compile the ReGex 
    p = re.compile(regex)
    # If the string is empty 
    # return false
    if(str == None):
        return False
    # Return if the string 
    # matched the ReGex
    if(re.search(p, str)):
        return True
    else:
        return False
#
if type(active_captcha_model) != int:
    text = "active_captcha_model %s is not an integer. Change the value to 1, 2 or 3." % active_captcha_model
    logging.info(text)
    sys.exit(syserrmsg)
if not active_captcha_model in (1,2,3):
    active_captcha_model = 2  # default 2    
# create empty picture list
picture_list = []
allowed_file_extensions = (".png", ".jpg", ".jpeg", ".bmp", 'tiff', 'gif', 'eps', 'pcx')  # The dot is required! Use only lower case! See for more https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html
if randomlist == True: # all all
    for filename in glob.glob(randomlist_dir +'*'):
        infile_name, infile_ext = os.path.splitext(filename)
        if infile_ext.lower() in allowed_file_extensions:
            picture_list.append(filename)
else:
        picture_list.append(input_picture_file)
if not len(picture_list) > 0:
    text = "Are there pictures in %s?\nAre these settings defined/correct?\n input_picture, input_picture_file, randomlist, randomlist_dir." % randomlist_dir
    logging.error(text)
    sys.exit(syserrmsg) 
if os.path.exists(input_picture_file) == False:
    text = "input_picture_file %s does not exist in directory %s. Check media_dir setting and spelling of file name (upper/lower case sensitive) or put an own picture with the exact name in the directory." % (input_picture_file, media_dir)
    logging.error(text)
    sys.exit(syserrmsg)
if type(input_picture_rescale_width) != int:
    text = "Value input_picture_rescale_width %s must be an integer! Minimum 360 and maximum 598.\nValues > maximum are automatically reset to maximum." % input_picture_rescale_width
    logging.error(text)
    sys.exit(syserrmsg)
if 360 <= int(input_picture_rescale_width) <= 599 or int(input_picture_rescale_width) == 0: # when true we skip else
    pass
else:
    text = "Value input_picture_rescale_width %s should be minimum 360 and maximum 598.\nValues > maximum are automatically reset to maximum." % input_picture_rescale_width
    logging.error(text)
    sys.exit(syserrmsg)
if os.path.exists(font_textzone) == False:
    text = "Font file defined %s does not exist. Check font_textzone setting and spelling of file name (upper/lower case sensitive)." % font_textzone
    logging.error(text)
    sys.exit(syserrmsg)
if os.path.exists(font_circle) == False:
    text = "Font file defined %s does not exist. Check font_circle setting and spelling of file name (upper/lower case sensitive)." % font_circle
    logging.error(text)
    sys.exit(syserrmsg)
if type(font_pnts_circle) != int:
    text = "font_pnts_circle %s is not an integer. Change the value." % font_pnts_circle
    logging.error(text)
    sys.exit(syserrmsg)
if type(font_pnts_textzone) != int:
    text = "font_pnts_textzone %s is not an integer. Change the value." % font_pnts_textzone
    logging.error(text)
    sys.exit(syserrmsg)
if type(number_of_letters) != int:
    text = "number_of_letters %s is not an integer. Change the value." % number_of_letters
    logging.error(text)
    sys.exit(syserrmsg)
if type(number_of_digits) != int:
    text = "number_of_digits %s is not an integer. Change the value." % number_of_digits
    logging.error(text)
    sys.exit(syserrmsg)
if type(border_circle) != int:
    text = "border_circle %s is not an integer. Change the value." % border_circle
    logging.error(text)
    sys.exit(syserrmsg)
if type(border_line) != int:
    text = "border_line %s is not an integer. Change the value." % border_line
    logging.error(text)
    sys.exit(syserrmsg)
if type(max_retries) != int:
    text = "max_retries %s is not an integer. Change the value." % max_retries
    logging.error(text)
    sys.exit(syserrmsg)
if type(max_time_to_solve) != int:
    text = "max_time_to_solve %s is not an integer. Change the value." % max_time_to_solve
    logging.error(text)
    sys.exit(syserrmsg)
if type(circle_color_trans) != int:
    text = "circle_color_trans %s is not an integer. Change the value." % circle_color_trans
    logging.error(text)
    sys.exit(syserrmsg)
if  circle_color_trans not in range(-1,101):
    text = "circle_color_trans %s must be in range 0 - 100. It reflects the percentage of transparency." % circle_color_trans
    logging.error(text)
    sys.exit(syserrmsg)
if type(char_circle_color_trans) != int:
    text = "char_circle_color_trans %s is not an integer. Change the value." % char_circle_color_trans
    logging.error(text)
    sys.exit(syserrmsg)
if  char_circle_color_trans not in range(-1,101):
    text = "char_circle_color_trans %s must be in range 0 - 100. It reflects the percentage of transparency." % char_circle_color_trans
    logging.error(text)
    sys.exit(syserrmsg)
if type(textzone_color_trans) != int:
    text = "textzone_color_trans %s is not an integer. Change the value." % textzone_color_trans
    logging.error(text)
    sys.exit(syserrmsg)
if  textzone_color_trans not in range(-1,101):
    text = "textzone_color_trans %s must be in range 0 - 100. It reflects the percentage of transparency." % textzone_color_trans
    logging.error(text)
    sys.exit(syserrmsg) 
if  not isValidHexaCode(str(textzone_text_color)):
    text = "textzone_text_color %s is not a correct hexadecimal color code" % textzone_text_color
    logging.error(text)
    sys.exit(syserrmsg) 
if  not isValidHexaCode(str(line_color)):
    text = "line_color %s is not a correct hexadecimal color code" % line_color
    logging.error(text)
    sys.exit(syserrmsg) 
if  not isValidHexaCode(str(textzone_bg_color)):
    text = "textzone_bg_color %s is not a correct hexadecimal color code" % textzone_bg_color
    logging.error(text)
    sys.exit(syserrmsg) 
if type(max_morphing_pie_slices) != int:
    text = "max_morphing_pie_slices %s is not an integer. Change the value." % max_morphing_pie_slices
    logging.error(text)
    sys.exit(syserrmsg)
if  max_morphing_pie_slices < 3:
    text = "max_morphing_pie_slices %s must be 3 or higher integer. Change the value." % max_morphing_pie_slices
    logging.error(text)
    sys.exit(syserrmsg)
if type(allowed_evals_per_char) != int:
    text = "allowed_evals_per_char %s is not an integer. Change the value." % allowed_evals_per_char
    logging.error(text)
    sys.exit(syserrmsg)
Unicode_Characters_found = False    
if  len(re.findall(r'[\u4e00-\u9fff]+', used_letters) ) > 0:
    Unicode_Characters_found = True
    if any([x in string.digits for x in used_letters]) == True:
        text = u"used_letters %s may not contain digits. Change the value." % used_letters.encode("utf8")
        logging.error(text)
        sys.exit(syserrmsg)
if  Unicode_Characters_found == False:
    if used_letters.isalpha() == False:
        text = u'used_letters %s may only contain alpha letters. Change the value!\nNote: Unicode characters like Chinese are also possible :-), but then the string in the configuration file must start with u"...." to identify it as Unicode. ' % ( used_letters.encode("utf8"))
        logging.error(text)
        sys.exit(syserrmsg)
if all([x in string.digits for x in used_digits]) == False:
    text = "used_digits %s may only contain digits. Change the value." % used_digits
    logging.error(text)
    sys.exit(syserrmsg)
if  number_of_letters + number_of_digits < 1:
    text = "number_of_letters + number_of_digits (%s and %s) must be minimal 1, else no Circles will be drawn. Increase the number of letters or digits or both." % (number_of_letters, number_of_digits)
    logging.error(text)
    sys.exit(syserrmsg)
if  number_of_letters + number_of_digits > 10:
    text = "number_of_letters + number_of_digits (%s and %s) is maximized 10 to avoid overcrowded Kaptsja's. Decrease the number of letters or digits or both." % (number_of_letters, number_of_digits)
    logging.error(text)
    sys.exit(syserrmsg)
if os.path.exists(gen_home_page_file) != True:
    text = "File %s does not exist in directory %s.\nLooking for %s.\nCheck html_dir setting and spelling of file name (upper/lower case sensitive) or create an own failure page with the exact name. Run KaptsjaHTMLpages.py." % (gen_home_page, html_dir, gen_home_page_file)
    logging.error(text)
    sys.exit(syserrmsg)
if os.path.exists(gen_failure_page_file) != True:
    text = "File %s does not exist in directory %s.\nLooking for %s.\nCheck html_dir setting and spelling of file name (upper/lower case sensitive) or create an own failure page with the exact name. Run KaptsjaHTMLpages.py." % (gen_failure_page, html_dir, gen_failure_page_file)
    logging.error(text)
    sys.exit(syserrmsg)
if os.path.exists(gen_success_page_file) != True:
    text = "File %s does not exist in directory %s.\nLooking for %s.\nCheck html_dir setting and spelling of file name (upper/lower case sensitive) or create an own success page with the correct name. Run KaptsjaHTMLpages.py." % (gen_success_page, html_dir, gen_success_page_file)
    logging.error(text)
    sys.exit(syserrmsg)
if not 'copyright_text_picture' in globals(): 
    copyright_text_picture = " "
if  type(copyright_text_picture) != str:
    text = "copyright_text_picture %s is not a string or no text has been defined. Nothing will be displayed." % copyright_text_picture
    logging.info(text)   
if not 'copyright_text_position' in globals(): 
    copyright_text_position = "R"
if copyright_text_position not in  ("R", "L", "r", "l"):
    copyright_text_position = "R"
if not 'textzone_center_text' in globals(): 
    textzone_center_text = True
if not type(textzone_center_text) == bool: 
    textzone_center_text = True
if not type(rotate_char_circle) == bool: 
    rotate_char_circle = True
if not type(rotate_angle_char_circle) == int:
    rotate_angle_char_circle = 30
if -1 <= int(rotate_angle_char_circle) <= 361 : # when true we skip else
    pass
else:
    rotate_angle_char_circle = 30
try:
    import lxml
    beautifulsoup_parser = "lxml"
    text = "BeautifulSoup uses lxml parser"
    logging.info(text)
except:
    beautifulsoup_parser = "html.parser"
    text = "BeautifulSoup uses html.parser"
    logging.info(text)
    #
######################################
### Do not change any text literals here, but only in KaptsjaConfiguration.py!
######################################    
# Defines text literals in English when not set in Configuration or deleted by accident
# When text literal is set to None, no text will be shown
# When text literal is set to "", the default English text will be shown
# Else the "translated text" set in Configuration will be shown
text = "Please check box to continue3"
if not "check_the_box_text" in globals():
    check_the_box_text = text
if check_the_box_text == "":
    check_the_box_text = text
if check_the_box_text is None:
    check_the_box_text = ""

text = "Number of clicks:"
if not "number_of_clicks" in globals():
    number_of_clicks = text
if number_of_clicks == "":
    number_of_clicks = text
if number_of_clicks is None:
    number_of_clicks = ""

text = "Too many clicks. Retry."
if not "too_many_clicks_text" in globals():
    too_many_clicks_text = text
if too_many_clicks_text == "":
    too_many_clicks_text = text
if too_many_clicks_text is None:
    too_many_clicks_text = ""

text = "Clicking the exact number of circles enables Submit button"
if not "exact_nr_circles_submit" in globals():
    exact_nr_circles_submit = text
if exact_nr_circles_submit == "":
    exact_nr_circles_submit = text
if exact_nr_circles_submit is None:
    exact_nr_circles_submit = ""
    
text = "Submitted. Click button New Picture."
if not "submitted_text" in globals():
    submitted_text = text
if submitted_text == "":
    submitted_text = text
if submitted_text is None:
    submitted_text = ""

text = "Too many retries. Click button New Picture."
if not "too_many_retries_text" in globals():
    too_many_retries_text = text
if too_many_retries_text == "":
    too_many_retries_text = text
if too_many_retries_text is None:
    too_many_retries_text = ""

text = "New Picture"
if not "new_pic_button_text" in globals():
    new_pic_button_text = text
if new_pic_button_text == "":
    new_pic_button_text = text
if new_pic_button_text is None:
    new_pic_button_text = ""

text = "Retry"
if not "retry_button_text" in globals():
    retry_button_text = text
if retry_button_text == "":
    retry_button_text = text
if retry_button_text is None:
    retry_button_text = ""

text = "Submit Result"
if not "submit_button_text" in globals():
    submit_button_text = text
if submit_button_text == "":
    submit_button_text = text
if submit_button_text is None:
    submit_button_text = ""

text = "CaptCha for Human recognition"
if not "intro_captcha_text" in globals():
    intro_captcha_text = text
if intro_captcha_text == "":
    intro_captcha_text = text
if intro_captcha_text is None:
    intro_captcha_text = ""

text = "Human Verification"
if not "captcha_hdr_text" in globals():
    captcha_hdr_text = text
if captcha_hdr_text == "":
    captcha_hdr_text = text
if captcha_hdr_text is None:
    captcha_hdr_text = ""
    
# Close modal window character X or use another HTML entity defined as &xxx; 
# Symbol &times; equals to &#215;  text may be used style is H2
text = "&otimes;" 
if not "captcha_hdr_close" in globals():
    captcha_hdr_close = text
if captcha_hdr_close == "":
    captcha_hdr_close = text
if captcha_hdr_close is None:
    captcha_hdr_close = ""

text = "I am a not a robot&nbsp;&nbsp;"
if not "not_a_robot_text" in globals():
    not_a_robot_text = text
if not_a_robot_text == "":
    not_a_robot_text = text
if not_a_robot_text is None:
    not_a_robot_text = ""

text = "#a3ff9e"
if not "submit_button_bgcolor_enabled" in globals():
    submit_button_bgcolor_enabled = text
if submit_button_bgcolor_enabled == "":
    submit_button_bgcolor_enabled = text
if submit_button_bgcolor_enabled is None:
    submit_button_bgcolor_enabled = ""
    
text = "#ff9e9e"
if not "submit_button_bgcolor_disabled" in globals():
    submit_button_bgcolor_disabled = text
if submit_button_bgcolor_disabled == "":
    submit_button_bgcolor_disabled = text
if submit_button_bgcolor_disabled is None:
    submit_button_bgcolor_disabled = ""

text = "#a3ff9e"
if not "retry_button_bgcolor_enabled" in globals():
    retry_button_bgcolor_enabled = text
if retry_button_bgcolor_enabled == "":
    retry_button_bgcolor_enabled = text
if retry_button_bgcolor_enabled is None:
    retry_button_bgcolor_enabled = ""

text = "#ff9e9e"
if not "retry_button_bgcolor_disabled" in globals():
    retry_button_bgcolor_disabled = text
if retry_button_bgcolor_disabled == "":
    retry_button_bgcolor_disabled = text
if retry_button_bgcolor_disabled is None:
    retry_button_bgcolor_disabled = ""

text = "#a3ff9e"
if not "new_pic_button_bgcolor_enabled" in globals():
    new_pic_button_bgcolor_enabled = text
if new_pic_button_bgcolor_enabled == "":
    new_pic_button_bgcolor_enabled = text
if new_pic_button_bgcolor_enabled is None:
    new_pic_button_bgcolor_enabled = ""

text = "#ff9e9e"
if not "new_pic_button_bgcolor_disabled" in globals():
    new_pic_button_bgcolor_disabled = text
if new_pic_button_bgcolor_disabled == "":
    new_pic_button_bgcolor_disabled = text
if new_pic_button_bgcolor_disabled is None:
    new_pic_button_bgcolor_disabled = ""

text = "Are you human? Click in each circle. First Digits then Letters.\n In ASCENDING order (▲).\n Not readable? Click on New Picture button."
if not "text_Ascending" in globals():
    text_Ascending = text
if text_Ascending == "":
    text_Ascending = text
if text_Ascending is None:
    text_Ascending = ""
    
text = "Are you human? Click in each circle. First Letters then Digits.\n In DESCENDING order (▼).\n Not readable? Click on New Picture button."
if not "text_Descending" in globals():
    text_Descending = text
if text_Descending == "":
    text_Descending = text
if text_Descending is None:
    text_Descending = ""

if not "ico_file" in globals():
   ico_file = media_dir + r"Kaptsja.ico" 
if os.path.exists(ico_file) == False:
    text = "File %s did not exist in directory %s.\nIt will be created." % (ico_file, media_dir)
    logging.error(text)
    ico_encoded = b'AAABAAEANzwQAAEABADYCAAAFgAAACgAAAA3AAAAeAAAAAEABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD2Bx4A1NTUANXV1QDY2NgA2dnZANra2gDb29sA3NzcAN3d3QDe3t4A39/fAP///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGKqqqqiqqqqqiqqqqoqpmqqoqpY4AAAAAAAAALu7u7u7u7u7u7u7u7u7u7u7u7u7sgAAAAAAAAq7u7u7u7u7u7u7u7u7u7u7u7u7u7EAAAAAAAAKu7u7u7u7u7u7u7u7u7u7u7u7u7uxAAAAAAAACruwAAAAAAAAAAAAAAAAAAAAAAC7sQAAAAAAAAq7sAAAAAAAAAu7AAAAAAAAAAAAu7EAAAAAAAAKu7AAAAAAAAC7u7AAAAAAAAAAALuxAAAAAAAACruwAAAAAAALu7u7AAAAAAAAAAC7sQAAAAAAAAq7sAAAAAAAu7u7u7AAAAAAAAAAu7EAAAAAAAAKu7AAAAAAu7u7u7u7AAAAAAAAALuxAAAAAAAACruwAAAAALu7u7u7u7AAAAAAAAC7sQAAAAAAAAq7sAAAAAu7u7AAu7u7AAAAAAAAu7EAAAAAAAAKu7AAAAu7u7sAAAu7u7AAAAAAALuxAAAAAAAACruwAAALu7uwAAAAu7u7AAAAAAC7sQAAAAAAAAq7sAALu7u7AAAAAAu7u7AAAAAAu7EAAAAAAAAKu7AAC7u7sAAAAAAAu7u7AAAAALuxAAAAAAAACruwALu7uwAAAAAAAAu7u7AAAAC7sQAAAAAAAAq7sAu7u7AAAAAAAAAAu7u7AAAAu7EAAAAAAAAKu7C7u7sAAAAAAAAAAAu7u7AAALuxAAAAAAAACru7u7uwAAAAAAAAAAAAu7u7AAC7sQAAAAAAAAq7u7u7AAAAAAAAAAAAAAu7u7AAu7EAAAAAAAAKu7u7sAAAAAAAAAAAAAAAu7u7ALuxAAAAAAAACru7uwAAAAAAAAAAAAAAAAu7u7C7sQAAAAAAAAq7sAAAAAAAAAAAAAAAAAAAu7u7u7EAAAAAAAAKu7AAAAAAAAAAAAAAAAAAAAu7u7uxAAAAAAAACruwAAAAAAAAAAAAAAAAAAAAu7u7sQAAAAAAAAq7sAAAAAAAAAAAAAAAAAAAAAu7u7EAAAAAAAAKu7AAAAAAAAAAAAAAAAAAAAAAu7u7AAAAAAAACruwAAAAAAAAAAAAAAAAAAAAAAu7uwAAAAAAAAq7sAAAAAAAAAAAAAAAAAAAAAAAu7uwAAAAAAAKu7AAAAAAAAAAAAAAAAAAAAAAALu7u7AAAAAACruwAAAAAAAAAAAAAAAAAAAAAAC7u7uwAAAAAAq7sAAAAAAAAAAAAAAAAAAAAAAAu7u7uwAAAAAKu7AAAAAAAAAAAAAAAAAAAAAAALuxu7uwAAAACruwAAAAAAAAAAAAAAAAAAAAAAC7sQu7sAAAAAq7sAAAAAAAAAAAAAAAAAAAAAAAu7EAu7AAAAAKu7AAAAAAAAAAAAAAAAAAAAAAALuxAAAAAAAACruwAAAAAAAAAAAAAAAAAAAAAAC7sQAAAAAAAAq7u7u7u7u7u7u7u7u7u7u7u7u7u7EAAAAAAAAKu7u7u7u7u7u7u7u7u7u7u7u7u7uxAAAAAAAAAFu7u7u7u7u7u7u7u7u7u7u7u7u7tAAAAAAAAABWd3d3d3d3d3d3d3d3d3d3d3d3ZWAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
    try:
        ico_bin = b64decode(ico_encoded)
        f = open(ico_file, "wb")
        f.write(ico_bin)
        f.close()
    except:
        text = "File %s in directory %s.\nFailure to create. Is import base64 missing? Check ico_encoded in KaptsjaGenerator.py. Maybe corrupt?" % (ico_file, media_dir)
        logging.error(text)

##########################################
# END of validation of the configuration
##########################################

# create the Encryption Cipher object using the secret_key_file
# when a secret_key_file does not exists it will be created automatically in key_dir
cripto = Cripto(secret_key_file)


class Kaptsja(object):
    def __init__(self, plainstring="", mode=captcha_page_url):
        self.plainstring = plainstring
        self.charlist = []
        self.reverse = "0"
        self.randomlist = randomlist
        ##print("self.randomlist=", self.randomlist)
        self.picture_list = []
        self.mode = mode

    def rcolor(self):
        return '#{:06x}'.format(random.randint(0x011110, 0xFFFFFF))
        #return '#{:06x}'.format(random.randint(0, 256**3))  # alternative 1
        # return f"#{random.randrange(0x010000):06x}"         # alternative 2

    def rgb2hex (self, r,g,b):
        return tuple(lambda r,g,b: f"#{r:02x}{g:02x}{b:02x}")  # create tuple with 3 RGB digits add leading zeros when needed 
        
    def hex2rgb (self, hx):
        # hexcolor = hx.lstrip("#")
        return tuple(int(hx.lstrip("#")[i:i+2], 16) for i in (0, 2, 4)) # create tuple with hexadecimal color code with leading #
        
    def hex2rgb_transparent (self, hx, color_transparency):  # create tuple with 4 RGB digits add leading zeros when needed, last digit is transparency digit
        # hexcolor = hx.lstrip("#")
        T1 = tuple(int(hx.lstrip("#")[i:i+2], 16) for i in (0, 2, 4)) 
        # tuples are immutable, so we make a list and add extra transparancy value (128 means half transparent)
        L1 = list(T1)
        L1.append(int((100-color_transparency)*255/100))
        T1=tuple(L1)
        color = T1
        return color 

    def inverse_rgbcolor(self, rgbcolor):
        return tuple(map(lambda x: 255 - x, rgbcolor))
        
    # Calculate with Pythagoras formula the distance between 2 circle centers x1, y1 and x2, y2 
    # square root of (square X multiplied with Square Y) or in formula:√(x²+ y²) = √r² returns d (istance)
    def distance(self, x1, y1, x2, y2):
        dsq = (x1 - x2) ** 2 + (y1 - y2) ** 2
        d = dsq**(1/2)  # square root
        return d

    def text_wrap(self, text, font, max_width):
            # Wrap text into the text zone width to be display
            lines = []
            
            # When text width is smaller than the max_width (of text zone) no split is needed
            # Text is just added to the list with line list
            if font.getsize(text)[0]  <= max_width:
                lines.append(text)
            else:
                # "\n" in text forces a new line break so split text in multiple lines
                newtextlines = text.split('\n')
                for newtextline in newtextlines:
                    newtextline = newtextline.lstrip(" ") # strip leading spaces at start of a new line
                    # split the line by spaces into list of words
                    words = newtextline.split(' ')
                    i = 0  # index to count the added words in "display" line
                    # append each word to a "display" line as long as it fits (width is shorter than the textzone width)
                    while i < len(words):
                        line = '' # start with empty "display" line
                        while i < len(words) and font.getsize(line + words[i])[0] <= max_width: 
                            # check if there are still words to be added and if the width of the line + word to be added still fit in the text zone using the given font size width.
                            line = line + words[i]+ " " # add word to line plus a space
                            i += 1  # update counter
                        if not line: # in case there
                            line = words[i]
                            i += 1
                        lines.append(line)
            return lines

    def create_unique_file(self, unique_time, infile):
        infile_name, infile_ext = os.path.splitext(infile)
        generated_unique_infile = infile_name + "_" + self.unique_time + infile_ext
        generated_unique_outfile     = work_dir + generated_unique_infile
        generated_unique_outfile_url = work_url + generated_unique_infile
        return generated_unique_outfile, generated_unique_outfile_url

    def create_all_filenames_and_fileurls(self):
        self.unique_time = str(time.time())
        # The file names and urls are generated here
        self.gen_captcha_page_file, self.gen_captcha_page_file_url = self.create_unique_file(self.unique_time, gen_captcha_page) # first is the file, second is url
        self.generated_unique_picture_file, self.generated_unique_picture_file_url = self.create_unique_file(self.unique_time, gen_picture) # first is the file, second is url
        self.gen_div_page_file, self.gen_div_page_file_url = self.create_unique_file(self.unique_time, gen_div_page) # first is the file, second is url
        self.gen_modal_page_file, self.gen_modal_page_file_url = self.create_unique_file(self.unique_time, gen_modal_page) # first is the file, second is url
        self.gen_css_file, self.gen_css_file_url = self.create_unique_file(self.unique_time, gen_css) # first is the file, second is url
        self.gen_javascript_file, self.gen_javascript_file_url = self.create_unique_file(self.unique_time, gen_javascript) # first is the file, second is url

    def set_charlist(self):
        if self.plainstring == None or self.plainstring == " ":
            self.charlist = random.sample(used_letters, number_of_letters)+ random.sample(used_digits, number_of_digits)
            logging.info(r"Create Kaptsja: charlist generated: %s" % self.charlist)
        else:
            self.charlist = list(self.plainstring)   # use the provided characters given to this function
            logging.info(r"Create Kaptsja: charlist provided: %s" % self.charlist)
        random.shuffle(self.charlist)
        self.reverse = random.choice(["0", "1"])
        # Return two values: A checkvalue (charlist) which contains the shuffled and previously entered 6 digits or characters
        # An encrypted controlvalue created from the checkvalue.
        # The controlvalue should be send hidden along with the Kaptsja map to the user.
        # The user clicks on the Kaptsja map in the correct way and returns the clicked result including the controlvalue.
        # The Encryption function expects a single string input. Therefore the numeric digits in charlist 
        # are first converted into string digits and then joined into a single string 
        self.plainstring = ''.join(map(str, self.charlist))
        return self.plainstring
        
    def get_filelist(self, dir, filter="*"):
        filelist =[]
        for filename in glob.glob(randomlist_dir +'*'):
            infile_name, infile_ext = os.path.splitext(filename)
            if infile_ext.lower() in allowed_file_extensions:
                filelist.append(filename)
            ##print(dir, filter, filename)
        return filelist
        
    def create_picturelist(self):
        if self.randomlist:
            self.picture_list = self.get_filelist(randomlist_dir, filter="*")
            ##print("self.picture_list =", self.picture_list )
        else:
            self.picture_list.append(os.path.normpath(input_picture_file))

    def set_random_picture(self):
        self.input_picture = random.choice(self.picture_list) 
        ##print("self.input_picture=",self.input_picture)

    def get_font(self, font_type, font_points, text):
        fnt = ImageFont.truetype(font_type, font_points)
        fw = 0
        fh = 0    
        fw_max = 0 
        fh_max = 0 
        for char in text:
            fw, fh = fnt.getsize(text = char)
            if fw > fw_max: fw_max = fw
            if fh > fh_max: fh_max = fh
        return fnt, fw_max, fh_max
        
    def scale_input_picture(self):
        self.set_random_picture()
        picture = Image.open(self.input_picture)
        # When closing the Bottle server with CTRL-C this error might appear: 
        # sys:1: ResourceWarning: unclosed file <_io.BufferedReader name='./<dir>/<name>.jpg'>
        # The reason is that Image.open function keeps the file open till picture is closed or saved.
        # This picture must be opened here but it is not (yet) closed when CTRL-C  is used!   
        # Get Width and height of the Input image 
        self.wpic, self.hpic = picture.size
        logging.info(r"Create Kaptsja: picture %s provided with size (w, h): %s" %(picture.filename, picture.size) )
        rescale = False  # default no rescale, unless...
        #  all input pictures will be automatically rescaled once and original will be overwritten!
        if input_picture_rescale_width > 0:       
            # input picture will be rescaled when value is between min and max values (see validation)
            rescale_wpic = input_picture_rescale_width
            rescale      = True
        if self.wpic > 598: 
            rescale_wpic = 598  # This is the maximum allowed width (forced as default maximum of bootstrap modal is 600px)
            rescale      = True
        if rescale == True:
            factor = (rescale_wpic / self.wpic)
            rescale_hpic = int((self.hpic * factor)) # same percentage of resizing as width must be integer not float
            text = "Provided image width %s exceeds the max width of the modal window size which is 600px.\nRezing and saving image %s to %s x %s pixels" % (picture, self.wpic, rescale_wpic, rescale_hpic)
            logging.info(text)     
            picture = picture.resize((rescale_wpic,rescale_hpic), resample=0)
            self.wpic, self.hpic = picture.size
            self.picture = picture
            picture.save(self.input_picture)
        # make a blank image from input picture (might be resized!) to allow opacity with transparency drawings
        self.picRGBA = picture.convert('RGBA')
        self.img = Image.new('RGBA', self.picRGBA.size, (255,255,255,0))
        # Create a Draw object to put text, circles etc on
        self.draw = ImageDraw.Draw(self.img)  
        return 0

    def create_textzone(self):
        # Get Font for text zone 
        fnt_for_textzone, fwt_max, fht_max = self.get_font(font_textzone, font_pnts_textzone, list(text_Ascending+text_Descending))
        # set text for Ascending / Descending
        if self.reverse == "0":  # "0" = Ascending
            text=text_Ascending
        else:                    # "1" = Descending
            text=text_Descending
        # calculate the text zone positioning, based on the number of lines and wrap the text properly so it fits within the given boundaries.    
        text_x_min = border_line    # left start x-position for a text line (in the textzone)
        text_x_max = self.wpic - border_line  # right end x-position for a text line (in the textzone)
        text_max_width = text_x_max - text_x_min
        lines = self.text_wrap(text, fnt_for_textzone, text_max_width)
        line_height = fht_max # a line height is determined by the maximum height of the font
        text_y_min  = self.hpic - (fht_max * len(lines)) # top start y-position for a first text line
        text_y_max  = self.hpic - border_line  # bottom end y-position for the last text line (in the textzone)
        text_y_max  = text_y_max - (len(lines)*line_height) # adjusted y-position. 
        x = text_x_min
        y = text_y_max
        # draw rectangle at bottom, used transparency as defined in configuration setting
        textzone_fill_color_transparent = self.hex2rgb_transparent(textzone_bg_color, textzone_color_trans)
        self.draw.rectangle((0,text_y_min - border_line, self.wpic, self.hpic - border_line), fill=textzone_fill_color_transparent) #, outline = line_color, width=0)
        # position aligned text line by line 
        for line in lines:
            line_fnt_width = fnt_for_textzone.getsize(line)[0]
            if textzone_center_text == True:
                self.draw.text(( text_max_width//2 - line_fnt_width//2   ,y), line, fill=textzone_text_color, font=fnt_for_textzone)
            else:
                self.draw.text((x,y), line, fill=textzone_text_color, font=fnt_for_textzone)
            y = y + line_height    # update y-axis for new line
         # draw top en bottom border_circle of the rectangle, no left, right border_circle    
        self.draw.line((0, text_y_min - border_line, self.wpic, text_y_min  - border_line), fill=line_color, width=border_line)
        self.draw.line((0, self.hpic - border_line//2, self.wpic, self.hpic - border_line//2), fill=line_color, width=border_line)
        
        # draw lines over text to morph the text a little
        for line_h in range (text_y_min  - border_line, self.hpic, 10):
            self.draw.line((0,line_h, self.wpic, line_h), fill=line_color, width=1)
        self.textzone_y_top = text_y_min - border_line//2 # Circles may not be drawn in the textzone and its border_circle  
        return 0
        
    def create_copyright_text(self, text):
        # Position the Copyright Text        
        fnt_for_copyright, copyright_text_width, copyright_text_height = self.get_font(font_textzone, font_pnts_copyright_text, text)
        copyright_text_width = fnt_for_copyright.getsize(copyright_text_picture)[0]
        if copyright_text_position.lower() == "r":
            self.draw.text((self.wpic - copyright_text_width - 5, 5), copyright_text_picture, fill=copyright_text_color, font=fnt_for_copyright)
        else: # left upper corner
            self.draw.text((5, 5), copyright_text_picture, fill=copyright_text_color, font=fnt_for_copyright)
        return 0
        
    def create_circles(self):
        # Get font for circles
        fnt_for_circle, fwc_max, fhc_max = self.get_font(font_circle, font_pnts_circle, self.charlist)
        # circle dimensions depends on max size of fw_max anf hh_max
        if fwc_max > fhc_max:
            cdiam = fwc_max * 2 # cdiam circle diameter excluding a border_circle size, 2 times the max width of selected font
        else:
            cdiam = fhc_max * 2 # cdiam circle diameter excluding a border_circle size, 2 times the max height of selected font
        rad_minimum = cdiam // 3 # the minimum radius of a circle
        # Create a list of mapareas: used in HTML file, maparea's must be "drawn by browser exactly on top of circles in picture")
        self.map_area_list = []
        # Create a list of circles. Each circle is a tuple with 3 components, the x and y coordinate and the radius. Append new circles as long the length of the list is less than n:
        circle_list = []
        # i is index for identify the ID of the HTML area's and when clicked ID is used to create a checkvalue in the HTML form
        i = 0  
        # Counter for the number of evaluations a
        # The allowed_evals_per_char forces a break to prevent an endless loop 
        # in case not all circles will fit on the given space/pictures. 
        evaluations = 0
        max_evaluations = len(self.charlist) * allowed_evals_per_char
        while len(circle_list) < len(self.charlist):
            evaluations = evaluations + 1
            if evaluations > max_evaluations: # evaluation stopped as there is most likely no place on picture anymore
                logging.error(r"Create Kaptsja: Too high number of Circle collisions therefore a break is forced.")
                logging.error(r"Create Kaptsja: Check picture size, font size, given number of characters and adapt their values.")
                logging.error(r"Create Kaptsja: (Width, Height) of picture:%s and font %s, number of characters: %s" %((self.wpic, self.hpic), (fwc_max, fhc_max), len(self.charlist)))
                logging.error(r"Create Kaptsja:   1. Start with reducing the number of characters on the Kaptsja picture.")
                logging.error(r"Create Kaptsja:   2. Reduce font size.")
                pic_minheight = self.hpic - self.textzone_y_top + (cdiam + border_circle+border_line)*3  # recommended height for a picture to avoid too much collisions
                logging.error(r"Create Kaptsja:   3. Increase picture size (Recommended minimum height is %s)." % pic_minheight)
                return 1
     
            try:
                #Create a random x, y position and radius for circles:
                r = rad_minimum # sets the minimum radius
                r = random.randint(r, r + 15)
                x = random.randint(0, self.wpic - (r + border_circle) * 2 )
                y = random.randint(0, self.textzone_y_top - (r + border_circle) * 2)
                d = (r+border_circle) * 2
                char= self.charlist[i]
            except ValueError as e:
                logging.error(r"Create Kaptsja: Text zone doesn't fit on this picture. Calculated value is %s." % self.textzone_y_top)
                logging.error(r"Create Kaptsja: Check picture size, font size, given number of characters and adapt their values.")
                logging.error(r"Create Kaptsja: (Width, Height) of picture:%s and font %s, number of characters: %s" %((self.wpic, self.hpic), (fwc_max, fhc_max), len(self.charlist)))
                logging.error(r"Create Kaptsja:   1. Start with reducing the number of characters on the Kaptsja picture.")
                logging.error(r"Create Kaptsja:   2. Reduce font size.")
                pic_minheight =  self.hpic - self.textzone_y_top + (cdiam + border_circle)*3   # recommended height for a picture to avoid too much collisions
                logging.error(r"Create Kaptsja:   3. Increase picture size (Recommended minimum height is %s)." % pic_minheight)
                return 1
            # Evaluate if the circle intersects with an other circle which is in the list
            collide = False
            # # use Pythagoras formula to calculate distances between new circle and the ones in the circle_list.
            for x2, y2, r2 in circle_list:
                # add each evaluations to counter
                evaluations = evaluations + 1
                d = self.distance(x, y, x2, y2)
                if d < r*1.9//1 + r2 :
                    collide = True
                    break
            # Append the circle to list if it does not collide:
            if not collide:
                circle_list.append((x, y, r))
                # Draw the circle on the image and place character in circle
                circle_fill_color = self.rcolor()
                circle_fill_color_transparent = self.hex2rgb_transparent(circle_fill_color, circle_color_trans)
                fw, fh = self.draw.textsize(text="{0}".format(char),font=fnt_for_circle) 
                # text_color is the inversed value color of circle_fill_color which is a hexcode color
                # Below the hexcode color is converted to rgb code and then change to it's inversed value
                text_color = self.inverse_rgbcolor(self.hex2rgb_transparent( circle_fill_color, char_circle_color_trans))

                # Use ONLY anchor in draw.text (....., anchor="mm") when PIL version is 8.0.0 or higher!
                # The anchor parameter was present in earlier versions of Pillow, but implemented only in version 8.0.0. The anchor parameter is ignored for non-TrueType fonts.
                if rotate_char_circle == True: 
                    # Create a transparent image mask with sizes of a (circle radius + border_circle) * 2 , that's a square 
                    img_mask = Image.new('RGBA', (r * 2+border_circle, r * 2+border_circle), color=(0,0,0,0) )
                    draw_img_mask = ImageDraw.Draw(img_mask)
                    # draw the circle on this square mask and fill circle
                    draw_img_mask.ellipse(((0,0), r * 2, r * 2), fill=circle_fill_color_transparent, outline=self.rcolor(), width=border_circle)
                    # Create a second image with same size as the mask
                    img_char = Image.new('RGBA', (r * 2+border_circle, r * 2+border_circle), color = circle_fill_color_transparent)
                    draw_img_char = ImageDraw.Draw(img_char)
                    # pick a random angle to rotate this second image once the character has been drawn
                    angle = random.randint(int(rotate_angle_char_circle) * -1, int(rotate_angle_char_circle))
                    # calculate the xy position of the character in the circle
                    xy=(r - (fw / 2) , r - (fh / 2))
                    # draw the character on second image
                    draw_img_char.text(xy=(r - (fw / 2) , r - (fh / 2)), text="{0}".format(char), fill=text_color,font=fnt_for_circle)
                        
                    # self.draw_rotated_text(img_char, angle, xy, text="{0}".format(char), fill=text_color,font=fnt_for_circle)
                    # morphing the character with pie slices positioned from the circle center. 
                    # the size of the pie slice is randomly. 
                    num_of_pieslice = random.randint(3, max_morphing_pie_slices)  
                    pieslice_start_angles = random.sample(range(0,360), num_of_pieslice)
                    for pieslice_start_angle in pieslice_start_angles:
                        pieslice_end__angle = pieslice_start_angle+(random.randint(3,15) )
                        draw_img_char.pieslice((border_circle * 2, border_circle * 2, (r - border_circle) * 2 , (r - border_circle) * 2), pieslice_start_angle, pieslice_end__angle, fill=circle_fill_color_transparent)
                    # put a line under numbers 6 and 9 to avoid recognition mistakes when characters are rotated "too" much
                    if char in ("6", "9"):
                        draw_img_char.line((r - (fw / 2), r - (fh / 2) + fh, r - (fw / 2) + fw, r - (fh / 2) + fh), fill=text_color, width=1)
                    img_char = img_char.rotate(angle)

                    self.img.paste(img_char, (x,y), img_mask)
                    # angle = random.randint(int(rotate_angle_char_circle) * -1, int(rotate_angle_char_circle))
                    # xy=(x + r - (fw // 2) , y + r - (fh // 2))
                    # self.draw_rotated_text(self.img, angle, xy, text="{0}".format(char), fill=text_color,font=fnt_for_circle)
                else:
                    self.draw.ellipse(((x,y), x + r * 2, y + r * 2), fill=circle_fill_color_transparent, outline=self.rcolor(), width=border_circle)
                    self.draw.text(xy=(x + r - (fw // 2) , y + r - (fh // 2)), text="{0}".format(char), fill=text_color,font=fnt_for_circle) 
                    # morphing the character with pie slices positioned from the circel center. 
                    # the size of the pie slice is randomly. 
                    num_of_pieslice = random.randint(3, max_morphing_pie_slices)  
                    pieslice_start_angles = random.sample(range(0,360), num_of_pieslice)
                    for pieslice_start_angle in pieslice_start_angles:
                        pieslice_end__angle = pieslice_start_angle+(random.randint(3,15) )
                        self.draw.pieslice((x + border_circle, y + border_circle, x + r * 2 - border_circle, y + r * 2 - border_circle), pieslice_start_angle, pieslice_end__angle, fill=circle_fill_color_transparent)
                # Append the area to maparea list:
                self.map_area_list.append('<area id="A%s" shape="circle" coords="%s, %s, %s" alt="Click here" title="Click area" onclick="fclick(%s);"></area>' % (random.randint(100,200), x + r, y + r, r + border_circle // 2, i) )
                i=i+1  # count this circle
        self.create_copyright_text(copyright_text_picture)
        out = Image.alpha_composite(self.picRGBA, self.img)
        out.save(self.generated_unique_picture_file)
        logging.info(r"Create Kaptsja: generated Kaptsja picture PNG file: %s" % self.generated_unique_picture_file)
        return 0

    # keep this method, however it is not in use 
    def draw_rotated_text(self, image, angle, xy, text, fill, *args, **kwargs):
        """ Draw text at an angle into an image, takes the same arguments
            as Image.text() except for:

        :param image: Image to write text into
        :param angle: Angle to write text at
        """
        # get the size of our image
        width, height = image.size
        max_dim = max(width, height)

        # build a transparency img_mask large enough to hold the text
        img_mask_size = (max_dim * 2, max_dim * 2)
        img_mask = Image.new('L', img_mask_size, 0)

        # add text to img_mask
        draw = ImageDraw.Draw(img_mask)
        draw.text((max_dim, max_dim), text, 255, *args, **kwargs)

        if angle % 90 == 0:
            # rotate by multiple of 90 deg is easier
            rotated_img_mask = img_mask.rotate(angle)
        else:
            # rotate an an enlarged img_mask to minimize jaggies
            bigger_img_mask = img_mask.resize((max_dim*8, max_dim*8),
                                      resample=Image.BICUBIC)
            rotated_img_mask = bigger_img_mask.rotate(angle).resize(
                img_mask_size, resample=Image.LANCZOS)

        # crop the img_mask to match image
        img_mask_xy = (max_dim - xy[0], max_dim - xy[1])
        b_box = img_mask_xy + (img_mask_xy[0] + width, img_mask_xy[1] + height)
        img_mask = rotated_img_mask.crop(b_box)

        # paste the appropriate color, with the text transparency img_mask
        color_image = Image.new('RGBA', image.size, fill)
        image.paste(color_image, img_mask)

                
# All braces for css and javascript itself MUST be double notation like {{ // some css or javascript code }} to escape the first. 
# Only one brace will be generated in the output. All formatting keys like .format(key= ) MUST have a single brace {key} notation.

    def html_header_css(self):
        return '''        
        //  this file/part is generated by KaptsjaGenerator.py       
        area {{
        cursor:pointer;
        }}
        table tr td {{
            border: 5px; 
            text-align: center; 
            vertical-align: middle;
        }}
        #count_clicks_per_try {{
            border:1px;
        }}
        #count_max_retries {{
            border:1px; 
        }}
        #message {{
            border:1px; 
            color: red; 
        }}
        #submitbutton[disabled]
            {{
             background: {retry_button_bgcolor_disabled};  # redish
            }}
        #submitbutton
            {{
             background: {retry_button_bgcolor_enabled}; // greenish
            }}
        #retrybutton[disabled]
            {{
             background: {retry_button_bgcolor_disabled};  # redish
            }}
        #retrybutton
            {{
             background: {retry_button_bgcolor_enabled}; // greenish
            }}
        #reloadbutton[disabled]
            {{
             background: {new_pic_button_bgcolor_disabled};  # redish
            }}
        #reloadbutton
            {{
             background: {new_pic_button_bgcolor_enabled}; // greenish
            }}
        '''.format(submit_button_bgcolor_enabled=submit_button_bgcolor_enabled, \
            submit_button_bgcolor_disabled=submit_button_bgcolor_disabled, \
            retry_button_bgcolor_enabled=retry_button_bgcolor_enabled, \
            retry_button_bgcolor_disabled=retry_button_bgcolor_disabled, \
            new_pic_button_bgcolor_enabled=new_pic_button_bgcolor_enabled, \
            new_pic_button_bgcolor_disabled=new_pic_button_bgcolor_disabled, \
            )
# modal
    def html_header_css_modal(self):
        return ''' 
        {html_header_css}
        .close:focus, button.close:hover {{
            color: #FF0000;
        }}
        .modal-header {{
            padding-left: 15px;
            padding-right: 15px;
            padding-top: 2px;
            padding-bottom: 2px;
        }}
        .modal-body {{
            padding-left: 0px;
            padding-right: 0px;
            padding-top: 2px;
            padding-bottom: 2px;
        }}
        .modal-footer {{
            padding-left: 15px;
            padding-right: 15px;
            padding-top: 2px;
            padding-bottom: 2px;
        }}
        .modal-content {{
        width:{width}px;
        position: relative;
        background-color: #fff;
        -webkit-background-clip: padding-box;
        background-clip: padding-box;
        border: 1px solid #999;
        border: 1px solid rgba(0,0,0,.2);
        border-radius: 6px;
        outline: 0;
        -webkit-box-shadow: 0 3px 9px rgba(0,0,0,.5);
        box-shadow: 0 3px 9px rgba(0,0,0,.5);
        }}
    `   '''.format(html_header_css=self.html_header_css(), \
            width=self.wpic+2, \
            ) 
        # 2 pixels extra are needed to get good right alignment (generated max picture width is 2 pixels than max widt of modal-content
    def javascript_window_onload_modal(self):
        return ''' '''
    def html_header_modal(self):
        return '''<div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true"><h2>{captcha_hdr_close}</h2></button>
                <h3>{captcha_hdr_text}</h3>
                </div>
        '''.format(captcha_hdr_close=captcha_hdr_close, \
            captcha_hdr_text=captcha_hdr_text)
    def html_body_modal(self):
        return '''<div class="modal-body text-center">
                </div>
        '''
    def html_footer_modal(self):
        return '''<!--  OK button not used; uncomment if you want this button to appear  -->
                <div class="modal-footer">
               <!-- <button type="button" class="btn btn-primary" data-dismiss="modal">OK</button>  -->
                </div> 
                <!-- Include first the jQuery and second Bootstrap javascript libraries. Order is important!  
                <script src="{jquery_js_file}"></script>
                <script src="{bootstrap_js_file}"></script> -->
        '''.format (jquery_js_file=jquery_js_file, bootstrap_js_file=bootstrap_js_file)
    def javascript_freload_modal(self):
        return '''
        function freload() {{
            setTimeout(function (){{
            // Delay time of 1.5 seconds between clicks on New Picture button will help to delete meanwhile chached Kaptsja's
            }}, 1500); // How long do you want the delay to be (in milliseconds)? 
        
            // following is required to force browser to reload always the page!
            var tnow = new Date(Date.now());
            var formatted_stamp = tnow.getHours() + "_" + tnow.getMinutes() + "_" + tnow.getSeconds() + "_" +  Math.random() * 1000;
            // Following line shows modal window direct, next block used fancy fade in and out, comment this line and uncomment the block is you want to use it
            $("#myModal").find(".modal-content").load("{modal_captcha_page_url}?random=" + formatted_stamp ).show();
            //  Show modal with fade in and fade out effect This is an alternative for the line above
            //  $('#myModal').fadeOut("slow",function(){{
            //        // specify here actions you need
            //        }}).fadeIn("slow",function(){{
            //            $("#myModal").find(".modal-content").load("{modal_captcha_page_url}?random=" + formatted_stamp ).show();
            //        }});                                               
        }}
        '''.format(modal_captcha_page_url=modal_captcha_page_url )
    def html_reload_button_modal(self):
        return '''\n                        <input type="button" id="reloadbutton" name="reloadbutton" value="{new_pic_button_text}" onclick = "freload();"></input> 
        '''.format(new_pic_button_text=new_pic_button_text)
# div
    def javascript_window_onload_div(self):
        return ''' '''
    def javascript_freload_div(self):
        return '''
        function freload (e) {{
            setTimeout(function (){{ 
            // Delay time of 1.5 seconds between clicks on New Picture button will help to delete meanwhile chached Kaptsja's
            }}, 1500); // How long do you want the delay to be (in milliseconds)? 
        
        // following is required to force browser to reload always the page!
            var tnow = new Date(Date.now());
			var formatted_stamp = tnow.getHours() + "_" + tnow.getMinutes() + "_" + tnow.getSeconds() + "_" +  Math.random() * 1000;

            (e || window.event).preventDefault();
            var con = document.getElementById('content')
            ,   xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function (e) {{ 
                if (xhr.readyState == 4 && xhr.status == 200) {{
                 con.innerHTML = xhr.responseText;
                }}
        }}
        xhr.open("GET", "{div_captcha_page_url}?random=" +  formatted_stamp, true);
        xhr.setRequestHeader('Content-type', 'text/html');
        xhr.send();
        }}
        '''.format(div_captcha_page_url=div_captcha_page_url )
    def html_reload_button_div(self):
        return '''\n                        <input type="button" id="reloadbutton" name="reloadbutton" value="{new_pic_button_text}" onclick = "freload();"> </input> 
        '''.format(new_pic_button_text=new_pic_button_text)
# default
    def javascript_window_onload_default(self):
        return '''
        window.onload = function()  {
             document.getElementById('checkvalue').value = "";
             document.getElementById('count_clicks_per_try').value = "0";
             document.getElementById('submitbutton').disabled = true;
             document.getElementById("count_max_retries").value = "0";
              }
        '''
    def javascript_freload_default(self):
        return '''
        function freload() {{
            setTimeout(function (){{ 
            // Delay time of 1.5 seconds between clicks on New Picture button will help to delete meanwhile chached Kaptsja's
            }}, 1500); // How long do you want the delay to be (in milliseconds)? 
            location.reload(true);             
        }}
        '''   
    def html_reload_button_default(self):
        return '''\n                        <input type="button" id="reloadbutton" name="reloadbutton" value="{new_pic_button_text}" onclick = "freload();"> </input> 
        '''.format(new_pic_button_text=new_pic_button_text)
    def javascript_fretry_default(self):
        return '''
        function fretry()  {{
          if ( document.getElementById("count_clicks_per_try").value > "0") {{ 
            document.getElementById("count_max_retries").value++;
            }}
          document.querySelector("#message > span").innerHTML = "";
          document.getElementById('checkvalue').value = "";
          document.getElementById('count_clicks_per_try').value = "0";
          document.getElementById('submitbutton').disabled = true;
          if (document.getElementById("count_max_retries").value > {max_retries}) {{
                document.querySelector("#message > span").innerHTML = "{too_many_retries_text}";
                document.getElementById('submitbutton').disabled = true;
                document.getElementById('retrybutton').disabled = true;
                // document.getElementById("myForm").submit();        
                return false;        
            }}        
         }} 
        '''.format(max_retries=max_retries, \
            too_many_retries_text=too_many_retries_text)
    def javascript_fclick_default(self):
        return ''' 
        function fclick(value_in) {{
            if (document.querySelector("#message > span").innerHTML == "{submitted_text}")
            {{
                document.getElementById('submitbutton').disabled = true;
                document.getElementById('retrybutton').disabled = true;
                return false;
            }}
            if (document.querySelector("#message > span").innerHTML == "{too_many_retries_text}")
            {{
                document.getElementById('submitbutton').disabled = true;
                document.getElementById('retrybutton').disabled = true;
                return false;
            }}
            document.getElementById("count_clicks_per_try").value++;
            document.getElementById("checkvalue").value =                   document.getElementById("checkvalue").value.concat(value_in);
            if (document.getElementById("count_clicks_per_try").value > {max_clicks_per_try} - 1 )  {{
                document.getElementById('submitbutton').disabled = false;
                }}
            else 
                {{
                document.querySelector("#message > span").innerHTML = "";
                document.getElementById('submitbutton').disabled = true;
                }}
            
            if (document.getElementById("count_clicks_per_try").value > {max_clicks_per_try}) {{
                var retcode = fretry();
                if ( retcode != false ) 
                    {{
                    document.querySelector("#message > span").innerHTML = "{too_many_clicks_text}"; 
                    document.getElementById('submitbutton').disabled = true;
                    }}
                return false;  
            }}
        }}
        '''.format(max_clicks_per_try=number_of_digits+number_of_letters, \
            submitted_text=submitted_text, \
            too_many_clicks_text=too_many_clicks_text, \
            too_many_retries_text=too_many_retries_text ) 
    def javascript_fsubmit_default(self):
        return '''
        function fsubmit() {{
            document.querySelector("#message > span").innerHTML = "{submitted_text}"; 
            document.getElementById("myForm").submit();
            // by exceeding the maximum values a reload of new picture will be forced (to avoid back page in browser)
            document.getElementById("count_max_retries").value = {max_retries} + 1;
            document.getElementById("count_clicks_per_try").value = {max_clicks_per_try} + 1;             
        }}
        '''.format(max_retries=max_retries, max_clicks_per_try=number_of_digits+number_of_letters, \
        submitted_text=submitted_text) 
        
    def gen_javascript(self):
        if self.mode in (modal_page_url, modal_captcha_page_url): 
            javascript_window_onload = self.javascript_window_onload_modal()
            javascript_freload = self.javascript_freload_modal()
            javascript_fretry =self.javascript_fretry_default()
            javascript_fclick =self.javascript_fclick_default()
            javascript_fsubmit =self.javascript_fsubmit_default()
        if self.mode in (div_page_url, div_captcha_page_url): 
            javascript_window_onload = self.javascript_window_onload_div()
            javascript_freload = self.javascript_freload_div()
            javascript_fretry =self.javascript_fretry_default()
            javascript_fclick =self.javascript_fclick_default()
            javascript_fsubmit =self.javascript_fsubmit_default()
        if self.mode == captcha_page_url: 
            javascript_window_onload = self.javascript_window_onload_default()
            javascript_freload = self.javascript_freload_default()
            javascript_fretry =self.javascript_fretry_default()
            javascript_fclick =self.javascript_fclick_default()
            javascript_fsubmit =self.javascript_fsubmit_default()
        return '''//this file is generated by KaptsjaGenerator.py       
        {javascript_window_onload}
        {javascript_freload}
        {javascript_fretry}
        {javascript_fclick}
        {javascript_fsubmit}
        '''.format( javascript_window_onload=javascript_window_onload, \
                    javascript_freload=javascript_freload, \
                    javascript_fretry=javascript_fretry, \
                    javascript_fclick=javascript_fclick, \
                    javascript_fsubmit=javascript_fsubmit )  

    def modal_html(self):
        return '''<!doctype html>
    <html>
    <!-- this file is generated by KaptsjaGenerator.py -->
    <head>
    <meta charset="utf-8" />
    <title>Kaptsja</title>
    <!-- Include Bootstrap 3.3.7 CSS here in the head section -->
    <link rel="stylesheet" href="{bootstrap_css_file}">
    <style>
    .modal-content {{
        width:{modal_content_width}px;
        position: relative;
        background-color: #fff;
        -webkit-background-clip: padding-box;
        background-clip: padding-box;
        border: 1px solid #999;
        border: 1px solid rgba(0,0,0,.2);
        border-radius: 6px;
        outline: 0;
        -webkit-box-shadow: 0 3px 9px rgba(0,0,0,.5);
        box-shadow: 0 3px 9px rgba(0,0,0,.5);
    }}
    </style>
    <script>
    </script
    </head>
    <body>
    <!-- The data-toggle="modal" is necessary and should be copied verbatim to your code!
         The data-target="#modal" is also mandatory, but you should change #modal to #<ID of
         the div with class modal that contains your desired modal>.
         The value of the href attribute is the file Bootstrap will load HTML into the modal from. -->
    <div class="modal-header">
    <h3>{check_the_box_text}<h3>    
    <div> 
        <!-- When not using default settings you might need to adapt href in next line -->
        <a data-toggle="modal" data-target="#myModal" href="{modal_captcha_page_url}">
            <label>{not_a_robot_text}<input type="checkbox" name="checkbox" value="link"></label>
        </a>
    </div> 
    </div>     
    <!-- <a data-toggle="modal" data-target="#myModal" href="{modal_captcha_page_url}">{intro_captcha_text}</a> -->
    <!-- This entire nested div structure is necessary for modals -->
    <div class="modal fade text-center" id="myModal">
        <div class="modal-dialog">
            <div class="modal-content">
                <!-- 
                    The external HTML will be inserted here.
                     Note: you can just place the header-body-footer div structure in the
                     external file. For example: you could place the following in externalfile.html:
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                </div>
                <div class="modal-body">
                    <p>Hello Kaptsja!</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-primary" data-dismiss="modal">OK</button>
                </div> 
                --> 
            </div>
        </div>
    </div>
    <!-- Include First the jQuery and Second Bootstrap javascript libraries. Order is important! -->
    <script src="{jquery_js_file}"></script>
    <script src="{bootstrap_js_file}"></script>
    </body>
    <html>
    '''.format(bootstrap_css_file=bootstrap_css_file, \
        bootstrap_js_file=bootstrap_js_file, \
        jquery_js_file=jquery_js_file, \
        modal_captcha_page_url=modal_captcha_page_url, \
        modal_content_width=input_picture_rescale_width + 2, \
        intro_captcha_text=intro_captcha_text, \
        not_a_robot_text=not_a_robot_text, \
        check_the_box_text=check_the_box_text )  
    # NOTE: 2 extra pixels are added to align picture nicely in the modal Window 
    # The max allowed width of picture is set to 598 as max default width for bootstrap modal is 600 pixels incl. 1px border for left and right )
    
    def div_html(self):
        return '''<!doctype html>
    <html>
    <!-- this file is generated by KaptsjaGenerator.py -->
    <head>
    <meta charset="utf-8" />
    <title>Kaptsja</title>
    <link rel="stylesheet" href="{gen_css_file_url}">
    <script src="{gen_javascript_file_url}">
    <script>
    </script>
    </head>
    <body>
    <div>
    <h1>{intro_captcha_text}<h1>
    </div>
    <table>
      <tr><td>
        <div id="content">
                <label>{not_a_robot_text}</label>
                <a href="{div_captcha_page_url}?random={force_reload}"><input type="checkbox" name="checkbox"  onclick="freload();">
            </a>
        </div>  
      </td></tr>
    </table>
    </body>
    </html>
        '''.format(gen_css_file_url=self.gen_css_file_url, \
        gen_javascript_file_url=self.gen_javascript_file_url, \
        captcha_page_url=captcha_page_url, \
        max_clicks_per_try=number_of_digits+number_of_letters, \
        max_retries=max_retries, \
        div_captcha_page_url=div_captcha_page_url, \
        force_reload=str(time.time()), \
        intro_captcha_text=intro_captcha_text, \
        not_a_robot_text=not_a_robot_text        )

    def captcha_html(self):
        if self.mode in (modal_page_url, modal_captcha_page_url): 
            html_header_css = self.html_header_css_modal()
            gen_javascript = self.gen_javascript()
            modal_header = self.html_header_modal()
            modal_body = self.html_body_modal()
            html_reload_button = self.html_reload_button_modal()
            modal_footer = self.html_footer_modal()
        if self.mode in(div_page_url, div_captcha_page_url): 
            html_header_css = self.html_header_css()
            gen_javascript = self.gen_javascript()
            modal_header = ""
            modal_body = ""
            html_reload_button = self.html_reload_button_div()
            modal_footer = ""
        if self.mode == captcha_page_url: 
            html_header_css = self.html_header_css()
            gen_javascript = self.gen_javascript()
            modal_header = ""
            modal_body = ""
            html_reload_button = self.html_reload_button_default()
            modal_footer = ""
        return '''<html>
            <!-- this file is generated by KaptsjaGenerator.py -->       
            <head>
            <meta charset="utf-8" />
            <style>
            {html_header_css}
            </style>
            <script type="text/javascript">
            {gen_javascript}
            </script>
            </head>
            <body>
                <form id="myForm" class="form-asd" role="form" method="POST" action="{captcheck}" enctype="multipart/form-data">
                {modal_header}
                {modal_body}
                    <div>
                        <table width="{width}">
                        <tr><td colspan="3">
                         <!-- Parameter ?random= is required to ensure a reload by some browsers of a new generated image 
                              An unique time stamp is used to avoide any collissions -->
                         <img src="{gen_picture}?random={force_reload}" usemap="#workmap" width="{width}" height="{height}"/>
                           <map name="workmap">{mapareas}
                           </map>
                        </td></tr>
                        <tr><td colspan="3">{number_of_clicks}
                        <input type="text"  id="count_clicks_per_try" name="count_clicks_per_try" size=1 readonly></input>
                        <div  id="message" name="message" ><span></span></div>
                        <input type="hidden" id="count_max_retries" name="count_max_retries" size=1 readonly></input>
                        <input type="hidden" id="reverse" name="reverse" value="{reverse}" size=1 readonly></input>
                        <input type="hidden" id="checkvalue" name="checkvalue" readonly></input>         
                        <input type="hidden" id="mode" name="mode" value="{mode}" readonly></input>         
                        <input type="hidden" id="controlvalue" name="controlvalue" value="{controlvalue}" readonly></input>{exact_nr_circles_submit}
                        </td></tr>
                        <tr><td>
                        {html_reload_button}
                        </td><td>
                        <input type="button" id="retrybutton" name="retrybutton"  value={retry_button_text} onclick="fretry();"></input> 
                        </td><td>
                        <input type="button" form="myForm"  id="submitbutton" name="submitbutton"  value={submit_button_text} onclick="fsubmit();" disabled></input> 
                        </td></tr>
                        <tr><td colspan="3">&nbsp;</td</tr>
                        </table>
                    </div>
                {modal_footer}
                </form>
            </body>
        </html>
        '''.format(width=self.wpic, height=self.hpic, \
        force_reload=str(time.time()), \
        captcheck=captcha_check_url,\
        site_url=site_url, css_url=css_url,  \
        gen_picture=self.generated_unique_picture_file_url, \
        mapareas=''.join(self.map_area_list), \
        controlvalue=self.encodedstring.decode(encoding='UTF-8'), \
        html_header_css=html_header_css, \
        gen_javascript=gen_javascript, \
        html_reload_button=html_reload_button, \
        modal_header=modal_header, \
        modal_body=modal_body, \
        modal_footer=modal_footer, \
        mode=self.mode, reverse=self.reverse,
        number_of_clicks=number_of_clicks,
        exact_nr_circles_submit=exact_nr_circles_submit,
        new_pic_button_text=new_pic_button_text, \
        retry_button_text=retry_button_text, \
        submit_button_text = submit_button_text)
        
    def write_css_file(self):
        # write the css to file, the Kaptsja DIV content HTML file uses this
        try:
            f = open(self.gen_css_file,"w", encoding="utf-8")
            f.write(self.html_header_css())
            f.close()
        except Exception as e:
            logging.error("Writing file %s failed.\n%s" %(self.gen_css_file, e) )
            return 1
        logging.info(r"Created css file for Kaptsja DIV page: %s:" % self.gen_css_file)     
        return 0
                

    def write_javascript_file(self):
        try:
            f = open(self.gen_javascript_file,"w", encoding="utf-8") 
            f.write(self.gen_javascript())
            f.close()
        except Exception as e:
            logging.error("Writing file %s failed.\n%s" %(self.gen_javascript_file, e) )
            return 1
        logging.info(r"Created javascript file for Kaptsja DIV page: %s" % self.gen_javascript_file)
        return 0

    def write_modal_page_file(self):
        soup = bs(self.modal_html(), features=beautifulsoup_parser)  #make BeautifulSoup
        prettyHTML = soup.prettify()   #prettify the html
        try:
            f = open(self.gen_modal_page_file,"w", encoding="utf-8") 
            f.write(prettyHTML)
            f.close()
        except Exception as e:
            logging.error("Writing file %s failed.\n%s" %(self.gen_modal_page_file, e) )
            return 1
        logging.info(r"Created Kaptsja Modal page: %s" % self.gen_modal_page_file)
        return 0

    def write_div_page_file(self):
        soup = bs(self.div_html(), features=beautifulsoup_parser)  #make BeautifulSoup
        prettyHTML = soup.prettify()   #prettify the html
        try:
            f = open(self.gen_div_page_file,"w", encoding="utf-8") 
            f.write(prettyHTML)
            f.close()
        except Exception as e:
            logging.error("Writing file %s failed.\n%s" %(self.gen_div_page_file, e) )
            return 1
        logging.info(r"Created Kaptsja DIV page: %s" % self.gen_div_page_file)
        return 0

    def write_captcha_html_file(self):
        soup = bs(self.captcha_html(), features=beautifulsoup_parser)  #make BeautifulSoup
        prettyHTML = soup.prettify()   #prettify the html
        try:
            f = open(self.gen_captcha_page_file,"w", encoding="utf-8") 
            f.write(prettyHTML)
            f.close()
        except Exception as e:
            logging.error("Writing file %s failed.\n%s" %(self.gen_captcha_page_file, e) )
            return 1
        logging.info(r"Create Kaptsja: generated Kaptsja HTML file: %s" % self.gen_captcha_page_file)
        return 0
        
        logging.info(r"Create Kaptsja: generated Kaptsja HTML file: %s" % self.gen_captcha_page_file)       

    def captcha_thread_remove_files(self):
        for filename in glob.glob(work_dir +'*'):
            generated_filename, generated_file_extension = os.path.splitext(filename)
            generated_filename, unique_time_file = generated_filename.rsplit("_",1)
            try:       
                if float(self.unique_time) > float(unique_time_file) + float(time_keep_captcha_set):
                    try:
                        os.remove(os.path.normpath(filename))
                    except Exception as e:
                        logging.error("Removing file %s failed.\n%s" %(os.path.normpath(filename), e) )
            except:
                pass # probably files with no unique time stamp in directory, those will not be deleted

    def delete_old_files(self):
        t = threading.Thread(target=self.captcha_thread_remove_files())
        t.start()

## functions
def create_captcha(plainstring=None, mode=captcha_page_url):  # defaults to mode for Kaptsja page
    c = Kaptsja(plainstring=plainstring, mode=mode)
    c.create_all_filenames_and_fileurls()
    # The models 2 and 3 work with HTML pages , which must be created first before a Kaptsja will be created and loaded
    if mode == div_page_url:
        c.write_css_file()
        c.write_javascript_file()
        c.write_div_page_file()
        return 0, os.path.normpath(c.gen_div_page_file)
    if mode == modal_page_url:
        c.write_modal_page_file()
        return 0, os.path.normpath(c.gen_modal_page_file)
    c.plainstring = c.set_charlist()
    if max_captcha_sets > 0:  # the time limit to solve a Kaptsja is NOT used for pre-generated Kaptsja's
        c.encodedstring = cripto.encryption(c.plainstring)
    else:                      # the time limit to solve a Kaptsja is ONLY used for dynamically generated Kaptsja's
        c.encodedstring = cripto.encryption(c.plainstring + "#time:" + str(time.time()) )
    c.create_picturelist()
    c.scale_input_picture()
    c.create_textzone()
    retcode = c.create_circles()
    if retcode > 0:
        return retcode, None
    c.write_captcha_html_file()
    if max_captcha_sets < 1: # when Kaptsja Sets are pre-generated , we do not delete these! 
        c.delete_old_files()
    return 0, os.path.normpath(c.gen_captcha_page_file)

def get_captcha(plainstring=None, mode=captcha_page_url):
    try:
        captcha_page_list = []
        infile_name = None
        infile_ext = None
        filter = "%s*.html" # only HTML pages to be served!
        if mode == captcha_page_url: 
            infile_name, infile_ext = os.path.splitext(gen_captcha_page)
        elif mode == div_page_url:
            infile_name, infile_ext = os.path.splitext(gen_div_page)
        elif mode == div_captcha_page_url:
            infile_name, infile_ext = os.path.splitext(gen_captcha_page)
        elif mode == modal_page_url:
            infile_name, infile_ext = os.path.splitext(gen_modal_page)
        elif mode == modal_captcha_page_url:
            infile_name, infile_ext = os.path.splitext(gen_captcha_page)
        filter = filter % infile_name     
        for filename in glob.glob(work_dir + filter): 
            captcha_page_list.append(filename)
        if len(captcha_page_list) > 0:
            served_captcha_file = os.path.normpath(random.choice(captcha_page_list))
     # update the time stamps of the pre-generated files, 
     # before serving it as it will help to force reloads, 
     # however when browser caching time of 1 second is not yet exceeded then user must refresh page again by clicking new picture
     # Therefore a short delay of 1.5 seconds is programmed	search for "setTimeout" in KaptsjaGenerator.py  
     # Try to use this "dirty trick" when there are still caching issues you cannot solve
            #os.utime(os.path.normpath(served_captcha_file))  
            return 0, served_captcha_file
        else:
            logging.error(r"Something went wrong. No Kaptsja sets filtered. Are the Kaptsja sets generated? Run KaptsjaGenerator.py from the command line.")
            return 1, None
    except Exception as e:
            logging.error(r"Something went wrong. Are the Kaptsja sets generated? Run KaptsjaGenerator.py from the command line. Error: %s" % e)
            return 1, None
        

def checkcaptcha(checkvalue, controlvalue, reverse):
    decoded_string_time = cripto.decryption(controlvalue)
    if max_captcha_sets > 0:  # the time limit to solve a Kaptsja is NOT used for pre-generated Kaptsja's
        decoded_string = decoded_string_time
    else:                     # the time limit to solve a Kaptsja is ONLY used for dynamically generated Kaptsja's
        decoded_string, dec_time = decoded_string_time.split("#time:")  
        if float(dec_time) + float(max_time_to_solve) < time.time():  # When Kaptsja's are not solved within the max_time_to_solve a Failure page will be displayed.
            ## print("Captcha expired")
            return False  
    logging.info(r"Check Kaptsja: checkvalue    : %s" % checkvalue)
    logging.info(r"Check Kaptsja: decoded_string: %s" % decoded_string)
    verify_checkvalue = ""
    inp_sorted = sorted(decoded_string, reverse=int(reverse))
    for i in range(len(inp_sorted)):
        pos = decoded_string.find(str(inp_sorted[i]))
        if pos != -1:
            verify_checkvalue = verify_checkvalue + str(pos)
    logging.info(r"Check Kaptsja: checkvalue       : %s" % checkvalue)
    logging.info(r"Check Kaptsja: verify_checkvalue: %s" % verify_checkvalue)

    if verify_checkvalue == checkvalue:
        return True
    else:
        return False

if __name__ == '__main__':
    if max_captcha_sets > 0:
        print("Please wait till generation of Kaptsja sets has been finished")
        if len(glob.glob(work_dir + "*.html")) > max_captcha_sets:  # there are allready html files generated
            print("Existing Kaptsja sets found. To generate a new set: first delete manually all files in %s" % work_dir)
        if len(glob.glob(work_dir + "*.html")) < 1:  # there are no html files generated when < 1
            for _ in range(max_captcha_sets):
                if active_captcha_model == 1:
                    create_captcha(plainstring=None, mode=captcha_page_url)
                if active_captcha_model == 2:
                    create_captcha(plainstring=None, mode=modal_page_url)
                    create_captcha(plainstring=None, mode=modal_captcha_page_url)
                if active_captcha_model == 3:
                    create_captcha(plainstring=None, mode=div_page_url)
                    create_captcha(plainstring=None, mode=div_captcha_page_url)
            print("Finished!")
        else:
            print("Existing files found (Kaptsja sets?). To generate a new set: first delete manually all files in %s" % work_dir)
            
    else:
        # plainstring = "A123C9" # For test purpose
        plainstring = input("Please provide unique characters from the shown set below.\nAdapt Configuration File when needed. A good number is 6 characters.\nLetters: %s\nDigits : %s\n:" %(used_letters, used_digits))
        # alternative checks
        # if not re.match("^[0-9]*$", plainstring): only digits
        #    logging.info(r"Error! Only digits 0-9 allowed!")
        # if not re.match("^[A-Za-z0-9]+ $", plainstring): #digits and alphabet only      
            # print(r"Error! Only digits 0-9 or alphabet A-Z, a-z are allowed!")
            # sys.exit(syserrmsg)
        for char in plainstring:
            if char not in used_letters + used_digits:
                print ("Character %s is not in the given set. Retry." %char)
                sys.exit(syserrmsg)
            if plainstring.count(char) > 1:
                print ("Character %s occurs more than once which is not allowed. Retry." %char)
                sys.exit(syserrmsg)
        # set the mode you want to test 
        mode=captcha_page_url
        c = Kaptsja(plainstring=plainstring, mode=mode)
        c.create_all_filenames_and_fileurls()
        # The models 2 and 3 work with HTML pages , which must be created first before a Kaptsja will be created and loaded
        if mode == div_page_url:
            c.write_css_file()
            c.write_javascript_file()
            c.write_div_page_file()
            print ("gen_div_page_file", os.path.normpath(c.gen_div_page_file))
        if mode == modal_page_url:
            c.write_modal_page_file()
            print ("gen_modal_page_file", os.path.normpath(c.gen_modal_page_file))
        c.plainstring = c.set_charlist()
        if max_captcha_sets > 0:  # the time limit to solve a Kaptsja is NOT used for pre-generated Kaptsja's
            c.encodedstring = cripto.encryption(c.plainstring)
        else:                      # the time limit to solve a Kaptsja is ONLY used for dynamically generated Kaptsja's
            c.encodedstring = cripto.encryption(c.plainstring + "#time:" + str(time.time()) )
        c.create_picturelist()
        c.scale_input_picture()
        c.create_textzone()
        retcode = c.create_circles()
        if retcode > 0:
            print ("Return code method create_circles not 0!")
            sys.exit(syserrmsg)
        c.write_captcha_html_file()
        if max_captcha_sets < 1: # when Kaptsja Sets are pre-generated , we do not delete these! 
            c.delete_old_files()
        #
        print("plainstring", c.plainstring)
        print("encodedstring", c.encodedstring)
        print("charlist", c.charlist)
        print("generated_unique_picture_file", c.generated_unique_picture_file)

    ### uncomment this together with the import line for pytesseract at the top to "play" with OCR on the generated pictures
    ### some example are provided. In principle a training data set should be created sot the tool can learn to get a better detection result 
    ### however the generated pictures are very unique, so ti won't be simple
    ###
        # print("*"*10, "Start OCR detection results - eng")
        # print(pytesseract.image_to_string(c.img, lang='eng'))
        # print("-"*10, "next result - eng")
        # print(pytesseract.image_to_string(c.img, lang='eng', config='--psm 7 --oem 3 --dpi 600'))
        # print("-"*10, "next result - eng")
        # print(pytesseract.image_to_string(c.img, lang='eng', config='--psm 6 --oem 3 --dpi 300 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQUVWXYZ0123456789'))
        # print("-"*10, "next result - eng")
        # print(pytesseract.image_to_string(c.img, lang='eng', config='--psm 11 --oem 3  -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQUVWXYZ0123456789') )
        # print("-"*10, "next result - osd")
        # print(pytesseract.image_to_string(c.img, lang='osd', config='--psm 11 --oem 3  -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQUVWXYZ0123456789') )
        # print("*"*10, "End OCR detection results")
