#flask file backend
import pickle
import math
import numpy as np
import mysql.connector
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
model = pickle.load(open('taxi.pkl','rb'))


@app.route('/')
def login():
    return render_template('index.html')

@app.route('/PredictionDetailForm',methods=['POST'])
def PredictionDetailForm():
    data = []
    for formdata in request.form.values():
        data.append(formdata)
    print(data)
    username = data[0]
    password = data[1]

    print('username', username)
    print('password', password)

    connection = mysql.connector.connect(host='localhost', user='project', password='project', database='uber')
    mycursor = connection.cursor()
    sql = "INSERT INTO user_login (name, password) VALUES (%s, %s)"
    val = (username, password)
    mycursor.execute(sql, val)
    connection.commit()
    print(mycursor.rowcount, "row affected.")

    return render_template('predictUberRideForm.html')

@app.route('/',methods=['POST'])
def StoringDataToDatabase():


    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():


    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    print('final_features.........', final_features)
    prediction = model.predict(final_features)
    output = round(prediction[0], 2)
    print('output.........', output)
    return render_template('predictUberRideForm.html',prediction_text="Number of Weekly Rides Should be : {} ".format(math.floor(output)))




if __name__=='__main__':
    app.run(debug=True)