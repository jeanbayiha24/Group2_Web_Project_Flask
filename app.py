from flask import Flask, request, render_template, redirect, url_for, session
from joblib import load
import numpy as np
import pandas as pd

# Lod the model
model = load('elastic_poly_model.joblib')

app = Flask(__name__)
app.secret_key = 'Very secret' #To secure the sessions

# default id
USERNAME = "client"
PASSWORD = "1234"


@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error = "Invalid credentials."
    return render_template('login.html', error=error)


@app.route("/index", methods=['GET','POST'])
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            # Retrieve the form data
            car_features = {
                "symboling": int(request.form['symboling']),
                "fueltype": request.form["fueltype"],
                "aspiration": request.form["aspiration"],
                "doornumber": request.form["doornumber"],
                "carbody": request.form["carbody"],
                "drivewheel": request.form["drivewheel"],
                "enginelocation": request.form["enginelocation"],
                "wheelbase": float(request.form["wheelbase"]),
                "carlength": float(request.form["carlength"]),
                "carwidth": float(request.form["carwidth"]),
                "carheight": float(request.form["carheight"]),
                "curbweight": int(request.form["curbweight"]),
                "enginetype": request.form["enginetype"],
                "cylindernumber": request.form["cylindernumber"],
                "enginesize": int(request.form["enginesize"]),
                "fuelsystem": request.form["fuelsystem"],
                "boreratio": float(request.form["boreratio"]),
                "stroke": float(request.form["stroke"]),
                "compressionratio": float(request.form["compressionratio"]),
                "horsepower": int(request.form["horsepower"]),
                "peakrpm": request.form["peakrpm"],
                "citympg": request.form["citympg"],
                "highwaympg": request.form["highwaympg"],
                "CarBrand": request.form["CarBrand"]
            } 

            #Conversion in DF
            input_df = pd.DataFrame([car_features])

            # Prediction
            prediction = model.predict(input_df)[0]
            prediction = round(prediction, 2)

            return render_template('index.html', prediction=prediction)
        
        except Exception as e:
            return render_template('index.html', error=str(e))
    
    return render_template('index.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)


