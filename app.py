from flask import Flask, render_template
from data import Blends

app = Flask(__name__)

Blends = Blends()


@app.route('/')
def webapp():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/blends')
def blends():
    return render_template('blends.html', blends=Blends)


@app.route('/blend/<string:id>/')
def blend(id):
    return render_template('blend.html', id=id)


if __name__ == '__main__':
    app.run(debug=True)
