# -*- encoding: utf-8 -*-

# all the imports necessary
from flask import json, url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from werkzeug.exceptions import HTTPException, NotFound, abort

import os

from app  import app

from flask       import url_for, redirect, render_template, flash, g, session, jsonify, request, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from app         import app, lm, db, bc
from . models    import User
from . common    import COMMON, STATUS
from . assets    import *
from . forms     import LoginForm, RegisterForm

import os, shutil, re, cgi
        
# provide login manager with load_user callback
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# authenticate user
@app.route('/logout.html')
def logout():
    logout_user()
    return redirect(url_for('login'))

# register user
@app.route('/register.html', methods=['GET', 'POST'])
def register():
    
    # define login form here
    form = RegisterForm(request.form)

    msg = None

    # custommize your pate title / description here
    title       = 'Recover password - ipNX vCPE'
    description = 'Online ipNX virtual Customer Premises Equipment.'

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str) 
        name     = request.form.get('name'    , '', type=str) 
        email    = request.form.get('email'   , '', type=str) 

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        # filter User out of database through username
        user_by_email = User.query.filter_by(email=email).first()

        if user:
            msg = 'Username exists!'
        
        elif user_by_email:
            msg = 'The emaill entered already has an account. Choose another one.'
        
        else:                    
            pw_hash = bc.generate_password_hash(password).decode(utf-8)

            user = User(username, pw_hash, name, email)

            user.save()

            msg = flash('Your account has been created. You can now login.', 'success')
            return redirect(url_for('login'))

    # try to match the pages defined in -> themes/light-bootstrap/pages/
    return render_template( 'layouts/default.html',
                            title=page_title,
                            content=render_template( 'pages/register.html', 
                                                     form=form,
                                                     msg=msg) )

# authenticate user
@app.route('/index.html')
def index():
    
    content = None
    
    try:
        # try to match the pages defined in -> themes/light-bootstrap/pages/
        return render_template('layouts/default.html',
                                content=render_template( 'pages/index.html') )
    except:
        abort(404)
    
# Used only for static export
@app.route('/wifi.html')
def user():

    # custommize your page title / description here
    title = 'wifi settings - ipNX vCPE'
    description = 'Online ipNX virtual Customer Premises Equipment.'

    # try to match the pages defined in -> pages/
    return render_template('layouts/default.html',
                            content=render_template( 'pages/wifi.html') )


# Used only for static export
@app.route('/DNS.html')
def DNS():

    # custommize your page title / description here
    title = 'DNS servers - ipNX vCPE'
    description = 'Online ipNX virtual Customer Premises Equipment.'

    # try to match the pages defined in -> pages/
    return render_template('layouts/default.html',
                            content=render_template( 'pages/DNS.html') )

# Used only for static export
@app.route('/DHCP.html')
def DHCP():

    # custommize your page title / description here
    title = 'DHCP - ipNX vCPE'
    description = 'Online ipNX virtual Customer Premises Equipment.'

    # try to match the pages defined in -> pages/
    return render_template('layouts/default.html',
                            content=render_template( 'pages/DHCP.html') )

# Used only for static export
@app.route('/device.html')
def device():

    # custommize your page title / description here
    title = 'Device settings - ipNX vCPE'
    description = 'Online ipNX virtual Customer Premises Equipment.'

    # try to match the pages defined in -> pages/
    return render_template('layouts/default.html',
                            content=render_template( 'pages/device.html') )

# App main route + generic routing
@app.route('/', methods=['GET', 'POST'], defaults={'path': 'login.html'})
@app.route('/<path>')
def login(path):

    try:
        # define login form here
        form = LoginForm(request.form)
        # Flask message injected into the page, in case of any errors
        msg = None
        # custommize your page title / description here
        page_title = 'Login - ipNX vCPE'
        page_description = 'Online ipNX virtual Customer Premises Equipment.'
        # check if both http method is POST and form is valid on submit
        if form.validate_on_submit():
            # assign form data to variables
            username = request.form.get('username', '', type=str)
            password = request.form.get('password', '', type=str)
            # filter User out of database through username
            user = User.query.filter_by(user=username).first()
            if user:
                if bc.check_password_hash(user.password, password):
                    login_user(user)
                    return redirect(url_for('index'))
                else:
                    msg = "Wrong password. Please try again."
            else:
                msg = "Unknown user. Check again and re-enter."
        # try to match the pages defined in -> themes/light-bootstrap/pages/
        return render_template( 'layouts/logindefault.html',
                            title=page_title,
                            content=render_template( 'pages/'+path, form=form,
                                                    msg=msg) )
    except:
        abort(404)


def http_err(err_code):
	
    err_msg = 'Oups !! Some internal error ocurred. Thanks to contact support.'
	
    if 400 == err_code:
        err_msg = "It seems like you are not allowed to access this link."

    elif 404 == err_code:    
        err_msg  = "The URL you were looking for does not seem to exist."
        err_msg += "<br /> Define the new page in /pages"
    
    elif 500 == err_code:    
        err_msg = "Internal error. Contact the manager about this."

    else:
        err_msg = "Forbidden access."

    return err_msg
    
@app.errorhandler(401)
def e401(e):
    return http_err( 401) # "It seems like you are not allowed to access this link."

@app.errorhandler(404)
def e404(e):
    return http_err( 404) # "The URL you were looking for does not seem to exist.<br><br>
	                      # If you have typed the link manually, make sure you've spelled the link right."

@app.errorhandler(500)
def e500(e):
    return http_err( 500) # "Internal error. Contact the manager about this."

@app.errorhandler(403)
def e403(e):
    return http_err( 403 ) # "Forbidden access."

@app.errorhandler(410)
def e410(e):
    return http_err( 410) # "The content you were looking for has been deleted."

	