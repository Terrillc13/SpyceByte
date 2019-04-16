from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, abort
from data import Blends
import os

app = Flask(__name__)

Blends = Blends()


@app.route('/')
def webapp():
    return render_template('home.html',
        jarFullness1=100, jarFullness2=100, jarFullness3=100)


@app.route('/dispense_jar_1', methods=['POST'])
def dispense_jar_1():
    print(request.form['Jar-1-Whole'])
    print(request.form['Jar-1-Fraction'])
    print("dispense_jar_1")
    return webapp()


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
