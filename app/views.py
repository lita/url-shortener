import json

from flask import render_template, flash, redirect, request, url_for
from forms import UrlForm

from url_shortener import UrlManager
import map_funcs
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
        title = "Lita's URL Shortener")

@app.route('/urlForm', methods = ['GET', 'POST'])
def urlForm():
    form = UrlForm()
    if form.validate_on_submit():
        result, adminKey = UrlManager.processUrl(form.url.data)
        if result:
            flash('URL Accepted!')
            flash(('Shorten Url: <strong> http://' 
                    + app.config['HOSTNAME'] 
                    + '/' 
                    + str(result) 
                    + '</strong>'))
            flash(('Admin URL: <strong> http://'
                    + app.config['HOSTNAME']
                    + url_for('adminPage', adminKey=adminKey)
                    + '</strong>'))
            return redirect('/index')
        else:
            flash('Url is not valid.')
    return render_template('urlForm.html', 
        title = 'Shorten Your URL',
        form = form)


@app.route('/<key>')
def goToNewSite(key):
    url =  UrlManager.getUrl(key, request)
    return redirect(url)

@app.route('/admin/<adminKey>')
def adminPage(adminKey):
    if not UrlManager.redis.exists(adminKey):
        flash("No one used your URL yet!")
        return render_template("index.html",
                               title = "Lita's URL Shortener")
    ips = UrlManager.getAdminData(adminKey)
    locations = map_funcs.getLongLat(ips)
    return render_template("admin.html", locations = json.dumps(locations))
