from flask import Flask, render_template, request
import pickle
import random
import pandas as pd
import os

app = Flask(__name__)

# Load the preprocessing pipeline
with open('full_pipeline.pkl', 'rb') as f:
    pipeline = pickle.load(f)

# Load the trained model
with open('rand_forest_model.pkl', 'rb') as f:
    model = pickle.load(f)

columns = [
    'person_age', 'person_income', 'person_home_ownership', 
    'person_emp_length', 'loan_intent', 'loan_grade', 
    'loan_amnt', 'loan_int_rate', 'loan_percent_income', 
    'cb_person_default_on_file', 'cb_person_cred_hist_length'
]

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    error = None
    try:
        if request.method == 'POST':
            # Extract input data from form
            data = {
                'person_age': int(request.form['person_age']),
                'person_income': float(request.form['person_income']),
                'person_home_ownership': request.form['person_home_ownership'],
                'person_emp_length': float(request.form['person_emp_length']),
                'loan_intent': request.form['loan_intent'],
                'loan_grade': request.form['loan_grade'],
                'loan_amnt': float(request.form['loan_amnt']),
                'loan_int_rate': float(request.form['loan_int_rate'])
            }

            # Compute additional fields
            data['loan_percent_income'] = data['loan_amnt'] / data['person_income']
            data['cb_person_default_on_file'] = random.choice(['Y', 'N'])
            data['cb_person_cred_hist_length'] = round(random.uniform(0, 30), 2)

            # Convert the data to a format suitable for model prediction
            input_data = {column: [data[column]] for column in columns}
            input_df = pd.DataFrame(input_data)

            # Transform the input data using the pipeline
            transformed_data = pipeline.transform(input_df)

            # Make prediction
            prediction = model.predict(transformed_data)

    except Exception as e:
        error = str(e)

    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 8080)),host='0.0.0.0',debug=True)
