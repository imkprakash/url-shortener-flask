from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, jsonify
import json
import os.path
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'fbfjhbscb'


# means we are showing homepage, the function after this will be called if someone goes to home page
@app.route('/')
def home():              # this function returns the content we want the user to see
    return render_template('home.html', codes=session.keys())


# this is the page we will show for 'about' section on our website. The name of the route and functions
# do not have to match
@app.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        urls = {}

        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)

        if request.form['code'] in urls:
            flash('That short name is already in use')
            return redirect(url_for('home'))

        if 'url' in request.form.keys():
            urls[request.form['code']] = {'url': request.form['url']}
        else:
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            f.save('D:/learn-flask/url-shortener/static/user_files/' + full_name)
            urls[request.form['code']] = {'file': full_name}

        with open('urls.json', 'w') as url_file:
            session[request.form['code']] = True
            json.dump(urls, url_file)
        return render_template('your_url.html', code=request.form['code'])
    else:
        return redirect(url_for('home'))


@app.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls:
                if 'url' in urls[code]:
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static', filename='user_files/' + urls[code]['file']))
    return abort(404)


@app.errorhandler(404)
def page_not_founde(error):
    return render_template('page_not_found.html'), 404


@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))
