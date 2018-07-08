from flask import Flask, render_template, request, json
import numpy as np
import keras
app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index2.html',title = 'Proyect')

@app.route('/api/proto2', methods=['POST'])
def proType2():
    model = keras.models.load_model('ANN4.h5')
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
    db = create_engine(db_string)
    query = "insert into records(year, speedLimit, vp, vm, cars, direction, time, day, month, k, typeC, traffic) values('{}','{}','{}','{}','{}','{}','{}','{}', '{}', '{}', '{}','{}')".format(year,speedLimit,vp,vm,cars,direction,time,day,month,k,typeC, traffic)
    db.execute(query)
    response = {
        "status": 'Done'
    }
    return json.dumps(response)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)