from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, abort
from PiControl import dispense, fullness
import xml.etree.cElementTree as Xml


app = Flask(__name__)


@app.route('/')
def webapp():
    tree = Xml.parse('spices.xml')
    root = tree.getroot()
    return render_template('home.html', jarFullness1=fullness(1), jarFullness2=fullness(2), jarFullness3=fullness(3),
                           spice_name_1=root[0][0].attrib['name'],
                           spice_name_2=root[0][1].attrib['name'],
                           spice_name_3=root[0][2].attrib['name'])


@app.route('/dispense_jar_1', methods=['POST'])
def dispense_jar_1():
    success = dispense(1, (int(request.form['Jar-1-Whole']) + int(request.form['Jar-1-Fraction'])))
    if not success:
        print("Unable to dispense from Jar 1")
    return webapp()


@app.route('/dispense_jar_2', methods=['POST'])
def dispense_jar_2():
    success = dispense(2, (int(request.form['Jar-2-Whole']) + int(request.form['Jar-2-Fraction'])))
    if not success:
        print("Unable to dispense from Jar 2")
    return webapp()


@app.route('/dispense_jar_3', methods=['POST'])
def dispense_jar_3():
    success = dispense(3, (int(request.form['Jar-3-Whole']) + int(request.form['Jar-3-Fraction'])))
    if not success:
        print("Unable to dispense from Jar 3")
    return webapp()


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/blends')
def blends():
    tree = Xml.parse('spices.xml')
    root = tree.getroot()
    return render_template('blends.html',
                           spice_name_1=root[0][0].attrib['name'],
                           spice_blend_1=root[0][0].text,
                           spice_name_2=root[0][1].attrib['name'],
                           spice_blend_2=root[0][1].text,
                           spice_name_3=root[0][2].attrib['name'],
                           spice_blend_3=root[0][2].text)


@app.route('/blends_save', methods=['POST'])
def blends_save():
    root = Xml.Element("root")
    doc = Xml.SubElement(root, "doc")
    Xml.SubElement(doc, "Spice", name=request.form['Spice_1_Name']).text = request.form['Spice_1_Blend']
    Xml.SubElement(doc, "Spice", name=request.form['Spice_2_Name']).text = request.form['Spice_2_Blend']
    Xml.SubElement(doc, "Spice", name=request.form['Spice_3_Name']).text = request.form['Spice_3_Blend']
    tree = Xml.ElementTree(root)
    tree.write("spices.xml")
    return blends()


if __name__ == '__main__':
    app.run(debug=True)
