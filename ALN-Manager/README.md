ALN-Manager
===========

A web-based application for managing student data in Special Needs departments in UK High Schools

Installation
============

As of yet, I haven't gotten around to making a build script for this application. The 
application is still in its infancy. However, for those who are interested in getting this 
application working here are a few pointson how one might go about installing it.

Dependencies
------------
* Django 1.3.0
* Apache Webserver
* mod_wsgi module for apache
* Python 2.7
* Numpy maths module
* Some relational database management system (e.g. MySQL) for the web application

Copying files into default directories
---------------------------------------
The main Django files are located in 
* aln_manager (contains the python code)
* django_views (contains all of the html/rtf templates used by the web application)
* django-wsgi (the file that ties this django application to apache wsgi)

For the default install these three artefacts should be copied to

	C:\wsgi_scripts

on a windows machine.

<b>Note:</b> For future versions this will be subject to change and should be 
configurable by the Systems Administrator.


Preparing the web server
------------------------
To prepare Apache for the web application you need to ensure that you've included the 
mod_wsgi module in the installation. If you've downloaded a binary of this module as I 
did you have to make sure it's compatible with your version of apache. The module should be 
downloaded and placed in the /modules directory, whever that is on your apache install.

To include the module in your apache install, add the line:

LoadModule wsgi_module modules/mod_wsgi.so

Once you've done this, you should configure apache to use wsgi to access the django 
application. The file django.wsgi should work fine and should by now be placed in your 
wsgi_scripts directory. To link it up with apache, add this line to your httpd.conf:

Include conf/httpd-wsgi.conf

The file httpd-wsgi.conf should be created in the same directory as your httpd.conf 
file. An example of this file is available in the root directory of this repository 
(httpd-wsgi.conf).

Note, this is tailored to a windows environment and should be modified slighly for a 
linux environment
