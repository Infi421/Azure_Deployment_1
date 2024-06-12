from flask import Flask, request, render_template
import pickle
import numpy as np
model = pickle.load(open(r"D:\deploy_model\uni_admission.pkl", 'rb'))
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/predict', methods=['POST'])
def predict_admission():
    GRE=int(request.form.get('greScore'))
    TOEFL =int(request.form.get('toeflScore'))
    Rating=int(request.form.get('universityRating'))
    SOP=float(request.form.get('sop'))
    LOR=float(request.form.get('lor'))
    CGPA=float(request.form.get('cgpa'))
    Research=int(request.form.get('research'))
    
    if GRE < 260 or GRE > 340:
        output = "GRE score must be between 260 and 340"
    elif TOEFL < 0 or TOEFL > 120:
        output = "TOEFL score must be between 0 and 120"
    elif Rating < 1 or Rating > 5:
        output = "University Rating must be between 1 and 5"
    elif SOP < 0 or SOP > 5:
        output = "SOP Strength must be between 0 and 5"
    elif LOR < 0 or LOR > 5:
        output = "LOR Strength must be between 0 and 5"
    elif CGPA < 0 or CGPA > 10:
        output = "CGPA must be between 0 and 10"
    elif Research < 0 or Research > 1:
        output = "Research experience must be either 0 (no) or 1 (yes)"
    else:
        prediction = model.predict(np.array([[GRE, TOEFL, Rating, SOP, LOR, CGPA, Research]]))*100
        if prediction[0]>100:
            prediction[0]=100
        output = "{:.2f}%".format(prediction[0]) 
    return render_template('index.html', prediction='The chance of admission is {}'.format(output))
if __name__ == '__main__':
    app.run(debug=True)

 