from flask import render_template, flash, redirect, request
from app import app
from forms import UrlForm

from url_shortener import UrlManager

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
        title = "Lita's URL Shortener")

@app.route('/urlForm', methods = ['GET', 'POST'])
def urlForm():
    form = UrlForm()
    if form.validate_on_submit():
        result = UrlManager.processUrl(form.url.data)
        if result:
            flash('URL Accepted!')
            flash(('Shorten Url: <strong> http://' 
                    + app.config['HOSTNAME'] 
                    + '/' 
                    + str(result) 
                    + '</strong>'))
            return redirect('/index')
        else:
            flash('Url is not valid.')
    return render_template('urlForm.html', 
        title = 'Shorten Your URL',
        form = form)


@app.route('/<key>')
def goToNewSite(key):
    url =  UrlManager.getUrl(key)
    return redirect(url)