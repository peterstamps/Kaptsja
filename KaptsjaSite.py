import sys
# sys.path.append("/path/to/your/package_or_module")
sys.path.append(r"./scripts")
from bottle import Bottle, route, run, static_file
from bottle import get, post, request, response, abort, redirect # or route
import KaptsjaGenerator as Captgen
import base64
from bottle import run
import os
import logging
from KaptsjaHTMLpages import *  # we are regenerating the HTML pages so latest settings are used
# import the configuration
from KaptsjaConfiguration import *
#
# uncomment following 2 lines if you have installed gevent and want to use items
# Gevent uses greenlet to provide a high-level synchronous API on top of the libev event loop
# greenlets are lightweight coroutines for in-process sequential concurrent programming
# The main advantage of gevent is its high performance, especially in comparison with traditional threading solutions.
# When gevent is used for network and I/O bound functions which are scheduled cooperatively, it shows its power
# import gevent.monkey;
# gevent.monkey.patch_all()

app = application = Bottle()
# When needed change level level=logging.INFO or level=logging.DEBUG)
# get the directory in which the script was started.
serve_path = os.getcwd()  
try:
    logging.basicConfig(filename=log_file, level=logging.DEBUG, \
        format='%(asctime)s %(levelname)-8s %(message)s', \
        datefmt='%Y-%m-%d %H:%M:%S')
except PermissionError as e:
    print("Check permissions for Kaptsja and its subdirectories.\n\n%s\n\n" % e)
    sys.exit()
except Exception as e:
    print("Start this program from Kaptsja home directory. It was started in %s.\n\n%s\n\n" %(serve_path, e) )
    sys.exit()
##########################################
# START of validation of the configuration
##########################################
syserrmsg = "Error! Look in log file."
if type(siteport) != int:
    text = "siteport %s is not an integer. Change the value." % siteport
    logging.error(text)
    sys.exit(syserrmsg)
if type(sitedebug) != bool:
    text = "sitedebug %s is not an boolean. Change the value to True of False." % sitedebug
    logging.error(text)
    sys.exit(syserrmsg)
if type(site_reloader) != bool:
    text = "site_reloader %s is not an boolean. Change the value to True of False." % site_reloader
    logging.error(text)
    sys.exit(syserrmsg)
##########################################
# END of validation of the configuration
##########################################

# return the home page when url has only a single slash ('/')
@app.route('/')
def index():
    redirect(home_page_url)
 
# return the home page when url equals to site url with and without ending slash  
@app.route(site_url)
@app.route(site_url[:-1]) # without end-slash route also to home page
def index():
    redirect(home_page_url)
    
#############################################################################    
# Start block:  URL requests containing a direct file reference in it (*.html, *.js, *.css, *.png, etcetera) 
# Keep this block before the block URL requests without a file reference.
# return the Kaptsja.ico file when the request url equals to requested favicon.ico file
@app.route('/favicon.ico')
def send_ico_form_media_dir(filename=ico_file):
    return static_file(filename=filename, root=media_dir, mimetype='image/ico')

# return png image file from media_dir when the request url starts with media_url  
@app.route(media_url + '<filename:re:.*\.png>')
def send_image_from_media_dir(filename):
    return static_file(filename, root=media_dir, mimetype='image/png')

# return requested css file from css_dir when the request url starts with ccs_url  
@app.route(css_url + '<filename:re:.*\.css>')
def send_css_from_css_dir(filename):
    return static_file(filename, root=css_dir, mimetype='text/css')

# return javascript file from js_dir when the request url starts with js_url      
@app.route(js_url + '<filename:re:.*\.js>')
def send_javascript_from_js_dir(filename):
    return static_file(filename, root=js_dir, mimetype='text/javascript')

# return requested html file from html_dir when the request url starts with html_url          
@app.route(html_url + '<filename:re:.*\.html>')
def send_html_from_html_dir(filename):
    return static_file(filename, root=html_dir, mimetype='text/html')

# return requested png image file from work_dir when the request url starts with work_url  
@app.route(work_url + '<filename:re:.*\.png>')
def send_image_from_work_dir(filename):
    return static_file(filename, root=work_dir, mimetype='image/png')

# return requested css file from work_dir when the request url starts with work_url      
@app.route(work_url + '<filename:re:.*\.css>')
def send_css_from_work_dir(filename):
    return static_file(filename, root=work_dir, mimetype='text/css')

# return requested javascript file from work_dir when the request url starts with work_url          
@app.route(work_url + '<filename:re:.*\.js>')
def send_javascript_from_work_dir(filename):
    return static_file(filename, root=work_dir, mimetype='text/javascript')

# return requested html file from work_dir when the request url starts with work_url              
@app.route(work_url + '<filename:re:.*\.html>')
def send_html_from_work_dir(filename):
    return static_file(filename, root=work_dir, mimetype='text/html')
#
# END block:  URL requests containing a direct file reference in it

#############################################################################
# Start block: URL requests without a file reference in it.
#
# return the home page when request url starts with home_page_url 
# the home page is created automatically at start of KaptsjaSite.py or when running KaptsjaHTMpages.py
@app.route(home_page_url)
@app.route(site_url + '<filename:path>')
def send_static_home_page(filename=gen_home_page_file):
    return static_file(filename, root='.')

    
# return the success page when request url starts with success_page_url 
# the success page is created automatically at start of ChatChaSite.py or when running KaptsjaHTMpages.py
@app.route(success_page_url)
def send_static_success_page(filename=gen_success_page_file):
    return static_file(filename, root='.')

    
# return the failure page when request url starts with failure_page_url 
# the failure page is created automatically at start of KaptsjaSite.py or when running KaptsjaHTMpages.py
@app.route(failure_page_url)
def send_static_failure_page(filename=gen_failure_page_file):
    return static_file(filename, root='.')


# return the Kaptsja page when request url starts with captcha_page_url 
# the Kaptsja page is created or has been pre-created automatically by KaptsjaGenerator.py
# Captgen.create_captcha : a dynamic page is created for each call
# Captgen.get_captcha    : a pre-generated page is randomly served from the Kaptsja sets 
@app.route(captcha_page_url, method='GET')
@app.route(captcha_page_url, method='POST')
def send_static_captcha_page(filename=gen_captcha_page_file):
    if not active_captcha_model == 1: redirect(home_page_url)
    if max_captcha_sets < 1:
        retcode, gen_captcha_page_file = Captgen.create_captcha(mode=captcha_page_url)
    else:
        retcode, gen_captcha_page_file = Captgen.get_captcha(mode=captcha_page_url)
    response.set_header("Cache-Control", "no-cache, no-store, must-revalidate, max-age=0, s-maxage=0, proxy-revalidate")               
    response.set_header("Pragma", "no-cache")
    response.set_header("Expires", "Sat, 12 Oct 1991 05:00:00 GMT")
    response.set_header("Vary", "*")
    if retcode > 0:
        return "<p>An error has occured. Check the log file.</p>"
    return static_file(filename=gen_captcha_page_file, root='.')


# return the modal page when request url starts with modal_page_url 
# the modal page is created or has been pre-created automatically by KaptsjaGenerator.py 
# Captgen.create_captcha : a dynamic page is created for each call
# Captgen.get_captcha    : a pre-generated page is randomly served from the Kaptsja sets 
@app.route(modal_page_url)
def send_static_modal_page(filename=gen_modal_page_file):
    if not active_captcha_model == 2: redirect(home_page_url)
    if max_captcha_sets < 1:
        retcode, gen_modal_page_file = Captgen.create_captcha(mode=modal_page_url)
    else:
        retcode, gen_modal_page_file = Captgen.get_captcha(mode=modal_page_url)
    if retcode > 0:
        return "<p>An error has occured. Check the log file.</p>"
    response.set_header("Cache-Control", "no-cache")
    response.set_header("Cache-Control", "must-revalidate, private, max-age=0, no-store")
    return static_file(filename=gen_modal_page_file, root='.')


# return the Kaptsja page (invoked from the modal page) when request url starts with modal_captcha_page_url 
# the Kaptsja page is created or has been pre-created automatically by KaptsjaGenerator.py 
# Captgen.create_captcha : a dynamic page is created for each call
# Captgen.get_captcha    : a pre-generated page is randomly served from the Kaptsja sets 
@app.route(modal_captcha_page_url, method='GET' )
@app.route(modal_captcha_page_url, method='POST' )
def send_static_modal_captcha_page(filename=gen_captcha_page_file):
    if not active_captcha_model == 2: redirect(home_page_url)
    if max_captcha_sets < 1:
        retcode, gen_captcha_page_file = Captgen.create_captcha(mode=modal_captcha_page_url)
    else:
        retcode, gen_captcha_page_file = Captgen.get_captcha(mode=modal_captcha_page_url)
    if retcode > 0:
        return "<p>An error has occured. Check the log file.</p>"
    response.set_header("Cache-Control", "no-cache, no-store, must-revalidate, max-age=0, s-maxage=0, proxy-revalidate")
    response.set_header("Pragma", "no-cache")
    response.set_header("Expires", "Sat, 12 Oct 1991 05:00:00 GMT")
    response.set_header("Vary", "*")
    return static_file(filename=gen_captcha_page_file, root='.')


# return the div page when request url starts with div_page_url 
# the div page is created or has been pre-created automatically by KaptsjaGenerator.py 
# Captgen.create_captcha : a dynamic page is created for each call
# Captgen.get_captcha    : a pre-generated page is randomly served from the Kaptsja sets 
@app.route(div_page_url, method='GET')
@app.route(div_page_url, method='POST')
def send_static_div_page(filename=gen_div_page_file):
    if not active_captcha_model == 3: redirect(home_page_url)
    if max_captcha_sets < 1:    
        retcode, gen_div_page_file = Captgen.create_captcha(mode=div_page_url)
    else:
        retcode, gen_div_page_file = Captgen.get_captcha(mode=div_page_url)
    if retcode > 0:
        return "<p>An error has occured. Check the log file.</p>"
    response.set_header("Cache-Control", "no-cache, no-store, must-revalidate, max-age=0, s-maxage=0, proxy-revalidate")               
    response.set_header("Pragma", "no-cache")
    response.set_header("Expires", "Sat, 12 Oct 1991 05:00:00 GMT")
    response.set_header("Vary", "*")
    return static_file(filename=gen_div_page_file, root='.')


# return the Kaptsja page (invoked from the div page) when request url starts with div_captcha_page_url 
# the Kaptsja page is created or has been pre-created automatically by KaptsjaGenerator.py 
# Captgen.create_captcha : a dynamic page is created for each call
# Captgen.get_captcha    : a pre-generated page is randomly served from the Kaptsja sets 
@app.route(div_captcha_page_url, method='GET')
@app.route(div_captcha_page_url, method='POST')
def send_static_div_captcha_page(filename=gen_captcha_page_file):
    if not active_captcha_model == 3: redirect(home_page_url)
    if max_captcha_sets < 1:
        retcode, gen_captcha_page_file = Captgen.create_captcha(mode=div_captcha_page_url)
    else:
        retcode, gen_captcha_page_file = Captgen.get_captcha(mode=div_captcha_page_url)
    if retcode > 0:
        return "<p>An error has occured. Check the log file.</p>"
    response.set_header("Cache-Control", "no-cache, no-store, must-revalidate, max-age=0, s-maxage=0, proxy-revalidate")               
    response.set_header("Pragma", "no-cache")
    response.set_header("Expires", "Sat, 12 Oct 1991 05:00:00 GMT")
    response.set_header("Vary", "*")
    return static_file(filename=gen_captcha_page_file, root='.')


# redirect to the url for the success or failure page when the Kaptsja has been verified resp. true or false
# return to failure in case the checkvalue has length of zero (means not checkvalue was generated, for example due to manual manipulation of the url)
@app.route(captcha_check_url, method='GET')
@app.route(captcha_check_url, method='POST')
def verify_captcha():
    checkvalue = request.forms.get('checkvalue')
    controlvalue = request.forms.get('controlvalue')
    reverse = request.forms.get('reverse')
    mode = request.forms.get('mode')
    if len(checkvalue) != number_of_letters + number_of_digits:
        redirect(failure_page_url)
    else:
        retcode = Captgen.checkcaptcha(checkvalue, controlvalue, reverse)
        if retcode == True:
            redirect(success_page_url)
        else:
            redirect(failure_page_url)
    return static_file(staticFile, filePath)
 
 
# here we redirect to the home page, normally that would be your next logical site page 
# this url is set by the Success page "Click here to continue"  
@app.route(success_cont_url)
def send_success_cont_url():
    redirect(site_url)


#  here we redirect to the home page, normally that would be a retry or no access page 
# this url is set by the Failure page "Click here to continue"     
@app.route(failure_cont_url)
def send_failure_cont_url():
    redirect(site_url)
#    
# END block: URL requests without a file reference in it.
#
if __name__ == "__main__":
    try:        
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
        
        run(app, server='%s' % siteserver, host='%s' % sitehost, port=siteport, debug=sitedebug, reloader=site_reloader)
    except Exception as e:
        text = "\nRunning the bottle Web server failed. Is there a Python error message? Check that first then all start up setttings. Is sitehost correct (name or IP address)?\nPython error message is:\n%s" % e
        logging.error(text)
        print (text)
