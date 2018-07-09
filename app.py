from flask import Flask, render_template, request, json
import numpy as np
from keras.models import load_model
from sqlalchemy import create_engine
from flask_cors import CORS


app = Flask(__name__)
db_string = 'postgres://mewvehlogtazsx:37a06497f63ce816aabebe0d7ed300f3777f33ddd92b18002bd74f6bcc3cac17@ec2-50-19-105-188.compute-1.amazonaws.com:5432/d1dbg2l6nvp583'
MODEL_PATH = './models/ANN4.h5'
model = load_model(MODEL_PATH)
CORS(app)

@app.route('/')
def homepage():
    return render_template('index2.html',title = 'Proyect')

@app.route('/api/proto2', methods=['POST'])
def proType2():
    if request.method == 'POST':

        year = years(str(request.form.get('year')))
        speedLimit = int(request.form.get('speedLimit'))
        vp = float(request.form.get('vp'))
        vm = float(request.form.get('vm'))
        cars = int(request.form.get('cars'))

        direction = directions(request.form.get('direction'))
        time = hours(request.form.get('time'))
        day = days(request.form.get('day'))
        month = months(request.form.get('month'))

        k = (cars/vp)
        typeC= street(request.form.get('type'))
        res = []
        for i in typeC:
            res.append(i)
        for i in year:
            res.append(i)
        for i in month:
            res.append(i)
        for i in day:
            res.append(i)
        for i in time:
            res.append(i)
        for i in direction:
            res.append(i)
        res.append(speedLimit)
        res.append(vp)
        res.append(vm)
        res.append(cars)
        res.append(k)
        prediction = model.predict(np.array([res]))
        if prediction[[0]] > 0.60:
            prediction = True
        else:
            prediction = False
        response = {
            "response": prediction
        }
        return json.dumps(response)

@app.route('/api/db', methods=['POST'])
def db():
    year = request.form.get('year')
    speedLimit = request.form.get('speedLimit')
    vp = float(request.form.get('vp'))
    vm = request.form.get('vm')
    cars = int(request.form.get('cars'))
    direction = request.form.get('direction')
    time = request.form.get('time')
    day = request.form.get('day')
    month = request.form.get('month')
    k = (cars/vp)
    typeC= request.form.get('type')
    traffic = request.form.get('traffic')
    feedback = request.form.get('feedBack')
    db = create_engine(db_string)
    query = "insert into records(year, speedLimit, vp, vm, cars, direction, time, day, month, k, typeC, traffic,feedBack) values('{}','{}','{}','{}','{}','{}','{}','{}', '{}', '{}', '{}','{}','{}')".format(year,speedLimit,vp,vm,cars,direction,time,day,month,k,typeC, traffic,feedback)
    db.execute(query)
    response = {
        "status": 'Done'
    }
    return json.dumps(response)


def months(month):
    monthToArray = []
    montha = {
        'January': 4,
        'February':3,
        'March':7,
        'April':0,
        'May':8,
        'June':6,
        'July':5,
        'August':1,
        'September':11,
        'October':10,
        'November':9,
        'December':2
    }[month]
    for i in range(montha):
        monthToArray.append(0)
    if len(monthToArray) == 0:
        while len(monthToArray) < 11:
            monthToArray.append(0)
    else:
        monthToArray.pop()
        monthToArray.append(1)
        while len(monthToArray) < 11:
            monthToArray.append(0)
    return monthToArray


def years(year):
    yearToArray = []
    yearA =  {
        '2017': 3,
        '2016': 2,
        '2015': 1,
        '2014': 0
    }[year]
    for k in range(yearA):
        yearToArray.append(0)
    if len(yearToArray) == 0:
        while len(yearToArray) < 3:
            yearToArray.append(0)
    else:
        yearToArray.pop()
        yearToArray.append(1)
        while len(yearToArray) < 3:
            yearToArray.append(0)
    return yearToArray

def days(day):
    dayToArray = []
    dayA = {
        'Monday':1,
        'Tuesday':5,
        'Wednesday':6,
        'Thrusday':4,
        'Friday':0,
        'Saturday':2,
        'Sunday':3
    }[day]
    for i in range(dayA):
        dayToArray.append(0)
    if len(dayToArray) == 0:
        while len(dayToArray) < 6:
            dayToArray.append(0)
    else:
        dayToArray.pop()
        dayToArray.append(1)
        while len(dayToArray) < 6:
            dayToArray.append(0)
    return dayToArray


def directions(dire):
    directionToArray = []
    directA = {
        'E':0,
        'W':3,
        'N':1,
        'O':2
    }[dire]
    for i in range(directA):
        directionToArray.append(0)
    if len(directionToArray) == 0:
        while len(directionToArray) < 3:
            directionToArray.append(0)
    else:
        directionToArray.pop()
        directionToArray.append(1)
        while len(directionToArray) < 3:
            directionToArray.append(0)
    return directionToArray

def hours(hour):
    hourToArray = []
    hourA ={
        '0': 0,
        '1':11,
        '2':16,
        '3':17,
        '4':18,
        '5':19,
        '6':20,
        '7':21,
        '8':22,
        '9':23,
        '10':1,
        '11':2,
        '12':3,
        '13':4,
        '14':5,
        '15':6,
        '16':7,
        '17':8,
        '18':9,
        '19':10,
        '20':12,
        '21':13,
        '22':14,
        '24':15
    }[hour]
    for i in range(hourA):
        hourToArray.append(0)
    if len(hourToArray) == 0:
        while len(hourToArray) < 23:
            hourToArray.append(0)
    else:
        hourToArray.pop()
        hourToArray.append(1)
        while len(hourToArray) < 23:
            hourToArray.append(0)
    return hourToArray

def street(typeS):
    streetToArray = []
    streetA = {
        'Road':7,
        'Avenue':0,
        'Parade':5,
        'Drive':2,
        'Place':6,
        'Street':8,
        'Terrace':9,
        'Crescent':1,
        'Lane':4,
        'Esplanade':3
        }[typeS]
    for i in range(streetA):
        streetToArray.append(0)
    if len(streetToArray) == 0:
        while len(streetToArray) < 9:
            streetToArray.append(0)
    else:
        streetToArray.pop()
        streetToArray.append(1)
        while len(streetToArray) < 9:
            streetToArray.append(0)
    return streetToArray


if __name__ == '__main__':
    app.run(port=9000,debug=False)