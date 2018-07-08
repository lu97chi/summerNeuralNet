import numpy as np
from flask import Flask, abort, jsonify, request,Response, json
from sqlalchemy import create_engine

app = Flask(__name__)


@app.route('/')
def homepage():
	return render_template("index2.html", title = 'Prediction Module Test1')





if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

