from flask import Flask, render_template
import numpy as np
import keras
app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index2.html',title = 'Proyect')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)