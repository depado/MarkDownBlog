# MarkDownBlog #

[![Join the chat at https://gitter.im/Depado/MarkDownBlog](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/Depado/MarkDownBlog?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)  

This repository is associated to the website [markdownblog.com](http://markdownblog.com). 

## Purpose and Technologies ##
**TLD;DR : A blog-platform engine which uses markdown as the main article format that you can install on your own or use the main website.**  

The main goal of this application was, in the first place, to allow people to easily create a markdown-based blog using the main site. It would create a subdomain for each user and each user could customize their own blog (background, pagination, truncated articles, information about the author). Now some people are asking me how to install this for their own use. This GitHub repository which was basically just used to version the project files is now an open-source project that people can fork, modify, and use.  

This application has been developped using the [Flask](http://flask.pocoo.org/) micro-framework. It uses several plugins such as [Flask-Login](https://flask-login.readthedocs.org/en/latest/) and [Flask-SQLAlchemy](http://pythonhosted.org/Flask-SQLAlchemy/). For more informations used during the development of this project, see the [requirements.txt](https://github.com/Depado/MarkDownBlog/blob/master/requirements.txt) file. 

## Installation and usage ##
### Installing ###
To install this application, you'll need a Python environment. For now the application is running in Python 3.4.3 (which is the latest stable revision at the moment). I didn't test the application to run with Python 2.7, but feel free to try and open some issues in case there is something wrong. I strongly recommend you to create a virtualenv to run this application. Installing python libraries system-wide has several cons. (Can't have two different versions, if you upgrade once, it will apply to everything on your system, you need root access, etc...). Here is how you can install the application.

```bash
# First of all, clone the repo using the https url or ssh.
$ git clone https://github.com/Depado/MarkDownBlog.git
$ cd MarkDownBlog/
# Next command can differ, it may be virtualenv-3.4, pyvenv-3.4 or something like that. 
$ virtualenv env
# If using fish shell, use 'activate.fish'.
# If 'source' command doesn't exist, use '.' instead.
$ source env/bin/activate
# Install all the libs.
(env)$ pip install -r requirements.txt
# Create the database and log folders.
# If not using SQLite, database folder isn't needed.
(env)$ mkdir database log
# Now you need to create the 'manage.py' file. Refer to the 'manage.py.example' file. Same with the 'config.py' file. 
# Modify the content of those files before saving them !
(env)$ python manage.py create_db
```

Will add further explanation later.

### Running in production ###
I recommend using `Gunicorn` with `Supervisor` and `Nginx`. Gunicorn choice may be arguable but I like it because it's simple to setup and runs fine. Will add further explanation later.

### License ###
See the [LICENSE.md](https://github.com/Depado/MarkDownBlog/blob/master/LICENSE.md) file for license rights and limitations (MIT).
