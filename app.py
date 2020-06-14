# Experience & Pay
import numpy as np
import joblib
from flask import request, jsonify, Flask, render_template
from flask_restful import Resource, Api
import psycopg2

host = '127.0.0.1'
port = 8000
app = Flask(__name__)

api = Api(app)

@app.route('/salary', methods = ['GET'])
def home_page():
    return render_template('index.html')

@app.route('/', methods = ['POST'])
def predict():
    fileName = 'joblib_file.pkl'
    with open(fileName, 'rb') as file:
        saved_model = joblib.load(file)
    name = request.form['nme']
    experience = float(request.form['exp'])
    prediction = saved_model.predict([[np.array(experience)]])
    output = round(prediction[0], 2) # Take first value of prediction
    connection = psycopg2.connect(host = 'localhost', port = '5432', database = 'My DB', user = 'postgres', password = 'Srees1!')
    cursor = connection.cursor()
    query = 'create table IF NOT EXISTS sal_prediction(prediction_id serial primary key, user_name varchar(50), work_experience integer, predicted_sal integer)'
    cursor.execute(query)
    query1 = "insert into sal_prediction(user_name, work_experience, predicted_sal) values('{}', {}, {})".format(name, experience, output)
    cursor.execute(query1)
    connection.commit()
    connection.close()
    return render_template('prediction.html', exp = experience, nme = name, out = output)

@app.route('/salary/all', methods = ['GET'])
def fetch_all_users():
    connection = psycopg2.connect(host = 'localhost', port = '5432', database = 'My DB', user = 'postgres', password = 'Srees1!')
    cursor = connection.cursor()
    query = "select * from sal_prediction"
    cursor.execute(query)
    data = cursor.fetchall()
    return render_template('getall.html', lis = data)

@app.route('/salary/<string:auser>/', methods = ['GET', 'POST'])
def fetch_single(auser):
    if request.method == 'GET':
        connection = psycopg2.connect(host = 'localhost', port = '5432', database = 'My DB', user = 'postgres', password = 'Srees1!')
        cursor = connection.cursor()
        query = "select * from sal_prediction where user_name = '{}'".format(auser)
        cursor.execute(query)
        result = cursor.fetchone()
        connection.close()
        return render_template('1_user.html', res = result)
    else:
        new_exp = float(request.form['experience'])
        fileName = 'joblib_file.pkl'
        with open(fileName, 'rb') as file:
            saved_model = joblib.load(file)
        prediction = saved_model.predict([[np.array(new_exp)]])
        output = round(prediction[0], 2)
        connect = psycopg2.connect(host = 'localhost', port = '5432', database = 'My DB', user = 'postgres', password = 'Srees1!')
        cursor = connect.cursor()
        query = "update sal_prediction set work_experience = {}, predicted_sal = {} where user_name = '{}'".format(new_exp, output, auser)
        cursor.execute(query)
        connect.commit()
        connect.close()
        return render_template('2_user.html', exp = new_exp, user = auser, out = output)

@app.route('/salary/<string:auser>/del', methods = ['GET'])
def delete_user(auser):
    connect = psycopg2.connect(host = 'localhost', port = '5432', database = 'My DB', user = 'postgres', password = 'Srees1!')
    cursor = connect.cursor()
    query = "delete from sal_prediction where user_name = '{}'".format(auser)
    cursor.execute(query)
    connect.commit()
    connect.close()
    return render_template('delete.html', us = auser)

if __name__ == '__main__':
    app.run(debug = True, port = port, host = host, use_reloader = False)