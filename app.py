# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 06:31:50 2021

@author: Nikhil
"""

from flask import Flask,render_template,request
import jsonify
import pickle
import requests
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
model = pickle.load(open('random_forest_regressor_model.pkl','rb'))

@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    fuel_type_diesel = 0
    if request.method == 'POST':
        year = int(request.form['year'])
        present_price = float(request.form['present_price'])
        kms_driven = int(request.form['kms_driven'])
        owner = request.form['owner']
        
        fuel_type_petrol = request.form['fuel_type']
        if(fuel_type_petrol == 'Petrol'):
            fuel_type_petrol = 1
            fuel_type_diesel = 0
        elif(fuel_type_petrol == 'Diesel'):
            fuel_type_petrol = 0
            fuel_type_diesel = 1
        else:
            fuel_type_petrol = 0
            fuel_type_diesel = 0
        year = 2021-year
        
        seller_type_individual = request.form['seller_type_individual']
        if(seller_type_individual == 'Individual'):
            seller_type_individual = 1
        else:
            seller_type_individual = 0
        
        transmission_manual = request.form['transmission_manual']
        if(transmission_manual == 'Manual'):
            transmission_manual = 1
        else:
            transmission_manual = 0
        
        prediction = model.predict([[present_price,kms_driven,owner,year,fuel_type_petrol, fuel_type_diesel,seller_type_individual,transmission_manual]])
        output = round(prediction[0],2)
        
        if (output < 0):
            return render_template('index.html', prediction_texts='Sorry you cannot sell this car')
        else:
            return render_template('index.html', prediction_texts='You can sell the car at {}'.format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)

