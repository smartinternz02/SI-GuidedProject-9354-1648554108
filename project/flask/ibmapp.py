from flask import Flask , request,render_template
import joblib
import requests
import json
# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "jyBF-OTVvHUB3PNPlDlK_s47U0tqGarDm6lQxtCoFVby"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
app = Flask(__name__)
model = joblib.load("model.save")


app = Flask(__name__)

@app.route('/')
def predict():
    return render_template('Manual.html')

@app.route('/y_predict',methods=['post'])
def y_predict():
    x_test = [[float(x) for x in request.form.values()]]
    print('actual',x_test)
    pred = model.predict(x_test)

    return render_template('Manual.html',
                           prediction_text=('car fuel consumption(L/100km) \
                                            :',pred[0]))
payload_scoring = {"input_data": [{"field": ["distance (km)","speed (km/h)","temp_inside (°C)","temp_outside (°C)","AC","rain","sun","E10"],
                                   "values": [[12.3, 62, 21.5,  6,  0,  0,  0,  1,  0]]}]}

response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/7f9b3da2-bc2c-4a4b-a254-1ca39157d30a/predictions?version=2022-10-21', json=payload_scoring,
 headers={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")
print(response_scoring.json())


if __name__ ==  '__main__':
    app.run(host='0.0.0.0',debug=True)