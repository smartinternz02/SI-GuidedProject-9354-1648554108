from flask import Flask , request,render_template
import joblib
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


if __name__ ==  '__main__':
    app.run(host='0.0.0.0',debug=True)