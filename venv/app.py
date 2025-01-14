import os
from pyexpat import model
import numpy as np
import flask
import pickle
from flask import Flask, redirect, url_for, request, render_template


# creating instance of the class
app = Flask(__name__, template_folder='templates')

# to tell flask what url should trigger the function index()

@app.route('/')
@app.route('/index')
def index():
    return flask.render_template('index.html')


# prediction function
def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1, 5)
    loaded_scaler = pickle.load(open("./model/scaler.pkl", "rb"))  # load the scaler
    loaded_model = pickle.load(open("./model/model.pkl", "rb"))  # load the model
    # predict the values using loded model
    to_predict_std = loaded_scaler.fit_transform(to_predict)
    result = loaded_model.predict(to_predict_std)
    return result[0]


@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        bmi = request.form['BMI']
        glucose = request.form['Glucose']
        age = request.form['Age']
        name = request.form['name']
        pregnancies = request.form['Pregnancies']
        insulin = request.form['Insulin']

        to_predict_list = list(map(float, [glucose, bmi, age, pregnancies, insulin]))
        result = ValuePredictor(to_predict_list)

        if float(result) == 0:
            prediction = 'Your chances of getting Diabetes are Low. Keep Healty ...'
        elif float(result) == 1:
            prediction = 'Your chances of getting Diabetes are Medium. Please consult a Doctor.'
        elif float(result) == 2:
            prediction = 'Your chances of getting Diabetes are High, Please consult a Doctor Immediately'

        return render_template("result.html", prediction=prediction, name=name)


if __name__ == "__main__":
    app.run(debug=False)  # use debug = False for jupyter notebook
