from flask import Flask, render_template, url_for, request, jsonify, session
import sqlite3
import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
from keras.models import load_model  # Ensure to import load_model
from feature import FeatureExtraction
import os
import socket

# Load the Keras model (.h5 file)
model = load_model('model\model.h5')  # Adjust path to your .h5 file

# Remove the code related to pickle since we're using the Keras model
# Remove the following lines:
# file = open("user/model/model.pkl", "rb")
# gbc = pickle.load(file)
# file.close()

# Connect to SQLite database
connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()

command = """CREATE TABLE IF NOT EXISTS user(name TEXT, password TEXT, mobile TEXT, email TEXT)"""
cursor.execute(command)

app = Flask(__name__)
app.secret_key = os.urandom(24)

def getData():
    while True:
        try:
            data = client_socket.recv(1024)
            break
        except:
            print("something went wrong")
    return data

@app.route('/',methods=['GET','POST'])
def get_data():
     data = getData()
     data = data.decode()
     print(data)

     obj = FeatureExtraction(data)
     x = np.array(obj.getFeaturesList()).reshape(1,30) 

     # Use the Keras model for prediction (instead of the previous GBC model)
     y_pred = model.predict(x)[0]
     y_pro_phishing = model.predict(x)[0,0]  # Assuming `predict_proba` is defined in your model
    # y_pro_non_phishing = model.predict(x)[0,1]
     perc = y_pro_phishing * 100

     print([data, perc])
     return render_template('index.html')

@app.route('/logout')
def logout():
    return render_template('index.html')

if __name__ == "__main__":
    # Set up the server socket for communication with the User (Intruder)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('192.168.0.104', 8080)  # Update the IP to match your Main Laptop's IP address
    server_socket.bind(server_address)
    server_socket.listen(1)
    print("Server is running and listening for connections...")
    
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address} established.")

    app.run(debug=True, use_reloader=False)
