
import tensorflow as tf
from tensorflow import keras
import string
import re
import nltk
import pickle
from flask import Flask, render_template, request, redirect, url_for
from nltk.corpus import stopwords
from tensorflow import keras
from tensorflow.keras.preprocessing import sequence
from resources import clean_text2
from flask_oidc import OpenIDConnect

stopword=set(stopwords.words('english'))
stemmer = nltk.SnowballStemmer("english")


'''
client id: 0oa139fvnvtROUVdF5d7
client secret: C1adgcNox_VAFEwhGYv5BNSVDgGwNEPEXsmUVirX
token: 00DbaYjDGGeTuH7GxbAchcUPkDHd_4_k4hBvnJKRQf
url: https://dev-64968246.okta.com
'''

app = Flask(__name__)
app.config["OIDC_CLIENT_SECRETS"] = "client_secrets.json"
app.config["OIDC_COOKIE_SECURE"] = False
app.config["OIDC_CALLBACK_ROUTE"] = "/oidc/callback"
app.config["OIDC_SCOPES"] = ["openid", "email", "profile"]
app.secret_key = "0averylongrandomstring"
app.config["OIDC_ID_TOKEN_COOKIE_NAME"] = "oidc_token"
oidc = OpenIDConnect(app)
# client_config = {
#                  "orgUrl": "https://geddylee.rush.toronto",
#                  "token": "yyzyyzyyzyyzyyzyyz"    
#                  }
# okta_client = UsersClient(client_config)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/model")
def model():
    return render_template("model.html")

@app.route("/model", methods=['POST'])
def getpicture():
    global txt
    txt = request.form["text"]
    print(txt)
    return render_template("loading.html")

@app.route("/result")
def getresult():
    new_model = tf.keras.models.load_model('saved_model/speech_model')
    with open('tokenizer.pickle', 'rb') as handle:
        load_tokenizer = pickle.load(handle)
    text=[clean_text2(txt)]
    seq = load_tokenizer.texts_to_sequences(text)
    padded = sequence.pad_sequences(seq, maxlen=300)
    print(seq)
    pred = new_model.predict(padded)[0][0]
    score = "Cleared!"
    print(pred)
    if pred<0.2:
        score = "Offensive and/or Hate Speech"
    return render_template("result.html", s=score)
@app.route("/dashboard")
@oidc.require_login
def dashboard():
    return render_template("dashboard.html")

@app.route("/login")
@oidc.require_login
def login():
    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    oidc.logout()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)

import re
import nltk
from nltk.corpus import stopwords
import string

stopword=set(stopwords.words('english'))
stemmer = nltk.SnowballStemmer("english")


