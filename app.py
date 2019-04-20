from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, abort
from data import Blends

app = Flask(__name__)

Blends = Blends()


@app.route('/')
def webapp():
    return render_template('home.html', jarFullness1=100, jarFullness2=100, jarFullness3=100, name1=Blends[0]['name'], name2=Blends[1]['name'], name3=Blends[2]['name'])


@app.route('/dispense_jar_1', methods=['POST'])
def dispense_jar_1():
    #save_home_selects()
    print(request.form['Jar-1-Whole'])
    print(request.form['Jar-1-Fraction'])
    print("dispense_jar_1: %d" % (int(request.form['Jar-1-Whole']) + int(request.form['Jar-1-Fraction'])))
    return webapp()


@app.route('/dispense_jar_2', methods=['POST'])
def dispense_jar_2():
    #save_home_selects()
    print(request.form['Jar-2-Whole'])
    print(request.form['Jar-2-Fraction'])
    print("dispense_jar_2: %d" % (int(request.form['Jar-2-Whole']) + int(request.form['Jar-2-Fraction'])))
    return webapp()


@app.route('/dispense_jar_3', methods=['POST'])
def dispense_jar_3():
    #save_home_selects()
    print(request.form['Jar-3-Whole'])
    print(request.form['Jar-3-Fraction'])
    print("dispense_jar_3: %d" % (int(request.form['Jar-3-Whole']) + int(request.form['Jar-3-Fraction'])))
    return webapp()


@app.route('/change_name_1', methods=['POST'])
def change_name_1():
    print(request.form['Spyce_1_Name'])
    Blends[0]['name'] = request.form['Spyce_1_Name']
    with open("data.py", "r+") as file:
        contents = file.read()

    return webapp()


@app.route('/change_name_2', methods=['POST'])
def change_name_2():
    print(request.form['Spyce_2_Name'])
    Blends[1]['name'] = request.form['Spyce_2_Name']
    return webapp()


@app.route('/change_name_3', methods=['POST'])
def change_name_3():
    print(request.form['Spyce_3_Name'])
    Blends[2]['name'] = request.form['Spyce_3_Name']
    return webapp()


#def save_home_selects():
#    session['Jar-1-Whole'] = request.form['Jar-1-Whole']
#    session['Jar-1-Fraction'] = request.form['Jar-1-Fraction']
#    session['Jar-2-Whole'] = request.form['Jar-2-Whole']
#    session['Jar-2-Fraction'] = request.form['Jar-2-Fraction']
#    session['Jar-3-Whole'] = request.form['Jar-3-Whole']
#    session['Jar-3-Fraction'] = request.form['Jar-3-Fraction']


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
    return render_template('settings.html', name1=Blends[0]['name'], name2=Blends[1]['name'], name3=Blends[2]['name'])


if __name__ == '__main__':
    app.run(debug=True)
