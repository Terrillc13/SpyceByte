from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from data import Blends
from piControl import doDispense, getFullness
app = Flask(__name__)

Blends = Blends()


@app.route('/', methods=['GET', 'POST'])
def webapp():
    if request.method == 'POST':
        print(request.form.get('Jar-1-Whole'))
        return
    return render_template('home.html',
                           jarFullness1=getFullness(1), jarFullness2=getFullness(2), jarFullness3=getFullness(3))


@app.route('/dispense_jar_1')
def dispense_jar_1():
    print(request.form.get('Jar-1-Whole'))
    print("dispense_jar_1")
    return 'Stay!'


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/blends')
def blends():
    return render_template('blends.html', blends=Blends)


@app.route('/blend/<string:id>/')
def blend(id):
    return render_template('blend.html', id=id)


@app.route('/settings')
def settings():
    return render_template('settings.html')


if __name__ == '__main__':
    app.run(debug=True)
