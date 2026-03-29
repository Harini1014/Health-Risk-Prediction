from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)

# Load model and encoders
model = pickle.load(open("model.pkl", "rb"))
le = pickle.load(open("encoder.pkl", "rb"))
le_con = pickle.load(open("consciousness_encoder.pkl", "rb"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input values
        respiratory_rate = float(request.form['respiratory_rate'])
        oxygen_saturation = float(request.form['oxygen_saturation'])
        o2_scale = float(request.form['o2_scale'])
        systolic_bp = float(request.form['systolic_bp'])
        heart_rate = float(request.form['heart_rate'])
        temperature = float(request.form['temperature'])

        # Encode consciousness properly
        # Consciousness (manual encoding)
        consciousness_input = request.form['consciousness']

        if consciousness_input == "A":
            consciousness = 0
        else:
            consciousness = 1

# On Oxygen (manual encoding)
        on_oxygen_input = request.form['on_oxygen']

        if on_oxygen_input == "Yes":
            on_oxygen = 1
        else:
            on_oxygen = 0

       

        # Create dataframe
        input_data = pd.DataFrame([{
            'Respiratory_Rate': respiratory_rate,
            'Oxygen_Saturation': oxygen_saturation,
            'O2_Scale': o2_scale,
            'Systolic_BP': systolic_bp,
            'Heart_Rate': heart_rate,
            'Temperature': temperature,
            'Consciousness': consciousness,
            'On_Oxygen': on_oxygen
        }])

        # Prediction
        prediction = model.predict(input_data)
        result = le.inverse_transform(prediction)[0]

        return render_template('index.html',
                               prediction_text=f"Predicted Risk Level: {result}")

    except Exception as e:
        print("ERROR:", e)
        return render_template('index.html',
                           prediction_text="Invalid Input!")

if __name__ == "__main__":
    app.run(debug=True)