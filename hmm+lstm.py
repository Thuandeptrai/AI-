# -*- coding: utf-8 -*-
"""HMM+LSTM.ipynb

Automatically generated by Colaboratory.

Original file is located at
https://colab.research.google.com/drive/1vtSA5qdaOD8A25H8bxR9TZC7DJMp6LFk
"""

import math
import matplotlib.pyplot as plt
import keras
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.layers import *
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from keras.callbacks import EarlyStopping
from hmmlearn import hmm
import matplotlib.pyplot as plt

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import uuid

import sys

cred = credentials.Certificate(
{
  "type": "service_account",
  "project_id": "website-126d7",
  "private_key_id": "6f0d6ea11e711face40cc97aca19cee5a091fa1b",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDE80Y44d41HTKB\nmGSLBbFsVTGj1q/a3EARnN3veA7O6yoM0y1jzAC/TTukPeOw95ewPHGRWddZEmZP\n6ZTLtJkl0FxlZC9Wo7DLxd1HY9ZB6aZciM1bunZIJ1QM6Jar0P6HPRlQRiDe4ILj\ntPz9qchmu3OI5sR05vgx+fOsefdjpu+sQJ++AgVXbcNybMhnLxwPY8jdxCYuZt7P\n0R8C/sL2O+FkvatknG69tHmikMbl5WHZdd2U74kjzm7WFQWQfrbiwIZP/1Vjs0JV\nAMvBDTYmsPLKrC/Wq+c/YHit3EpLssDPx0uLmiUvPRIKzGmRz1wGFAto9kc0NLRK\nYjDQ1Q5JAgMBAAECgf9k5L3AzIBmFwNdmFJGiMSqmhrF/c7S8qAg3rkwMJarRIej\nPX29XFmj597iW/K9F3H65IxOARVaIPb5rrQW0NjgSby3zeV2+pLYlIkWTzQWmV8B\n7IdshExU/hHm3scLPeTSjQFFhLDP0EZwfDlWO8SX154XFDOi0CQm/QD873UW/VSs\nYAxiaIYVOJHa6aMrygV1VvKcqO2ssn+/V92B9Ljg3yHQljTUYp9fUp0HzYJl59iU\nHeQzFfZWHQTn5jqzB8dChqGtEJgPU6nLsasA0ue3iWwdkCSrCLALOlOWd6mg7Z6f\nwkJsmsRZ14NW30c3+Gljd7EkktKKWYrCIVZ1ip0CgYEA4cw39CvyrD6LxVdjcxVJ\nN5D3CiLygDpMmv4QfhLaHPjkyO6SkuQetXwuMuj0v3tO4pNYXG6g7aAJOngMYxf+\nuncO9nzzjfQA5gp8B/QMk9bfsp5GmMjJobhS/o6pG8doUljqdHIyQ+8t1m4J6b64\ndova9FHoOEevMnLvMtA4jecCgYEA30tCfySitd8Rjg1soqJpcFgQUDuaSp6yCt/w\nBT6Anpx/AMMYR4gaR/qc6YJjgIL6CSLEdjRDpOmEzacpzcXcgKnHEZPTNf9O0KQ3\nzTGVYVYEehmUUv3i4+qF0ML4KuL25ZiM9pz9WgIS+f1lejeT1pSLhY4AP7cXEwDw\njQ3EHE8CgYEAhKqirZosyTsukFJaIkH9dOJ947zI0sJuRBrGwex9rswmUFCsWhYi\nXOuLkWoCc4cVwFZmclilwThoc6wZSxfMGO7fIcAkseENrhu26E1iHnL/mEkanaZL\nofNVAC/9+E5fYxLPHoACPJwJSJX6yRW/+BcQHMELOhYUQAX7uNVShT0CgYBP3smw\nVNhmmZ3b4+1h1xpD9xwOtuMfodgpj6R5G7xB/9Rl32MF4ycTbA9Ibz1MMI1jSy5e\n4Z74lBbOwOZxFj8jPpdYMDoybFoywyq6mOvH307GpfOqI+pOgArRe4vtOzX5NjHl\n3I267lb/WKY9qzeUX5nwcbShFcqJH6LrsWrefQKBgQCBzxtfInH0sRKU+/R/4lf8\nHiDORwjjsO9L8G8hjPKLTtURCy16/DAbRZi/VKOz5zZUST+RriXrrdXnLSYCR9MR\nFGtF9chXnPaNEbCq/whUnb1NITGJ7vgyONW9UWKNX/PRY4n4iHmlafqvWwpzKBaW\npefilL1g3QC6fkI5XPFQUA==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-ny59g@website-126d7.iam.gserviceaccount.com",
  "client_id": "102762875440238012558",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ny59g%40website-126d7.iam.gserviceaccount.com"
}


)


firebase_admin.initialize_app(cred)

# Commented out IPython magic to ensure Python compatibility.


# Use a service account

# Fechting data from DB
db = firestore.client()

users = list(db.collection(u'data111').stream())
users_dict = list(map(lambda x: x.to_dict(), users))
data = pd.DataFrame(users_dict, columns=[
                    "Date", "Open", "High", "Low", "Close", "Adj Close", "Volume", "Change"])

data.head(10)

full_len = data.shape[0]
num_val = 360
num_test = 180
num_subtract = 500
num_train = full_len - num_subtract - num_val - num_test
print('Data length = ', full_len - num_subtract)
print('Num train = ', num_train, " Num test = ",
      num_test, " Num validation = ", num_val)


print(data.iloc[500:, :])

market_data = data.iloc[:, 1:5].values
print(market_data)

log_market_data = market_data

plt.figure(figsize=(30, 13))
plt.plot(list(range(full_len)), market_data[:, 3])
plt.title('Close price')
plt.figure(figsize=(30, 13))
for i in range(4):
    plt.plot(list(range(full_len)), log_market_data[:, i])
plt.title('Close price after log')

MA_data = log_market_data[500:, 3]
MA5 = []
MA20 = []
MA50 = []
MA100 = []
for i in range(500, full_len):
    MA5.append(np.mean(log_market_data[i-5:i, 0]))
    MA20.append(np.mean(log_market_data[i-20:i, 0]))
    MA50.append(np.mean(log_market_data[i-50:i, 0]))
    MA100.append(np.mean(log_market_data[i-100:i, 0]))

plt.figure(figsize=(30, 13))
plt.plot(list(range(full_len - num_subtract)), MA_data, label="Close price")
plt.plot(list(range(full_len - num_subtract)), MA5, label="MA5")
plt.plot(list(range(full_len - num_subtract)), MA20, label="MA20")
plt.plot(list(range(full_len - num_subtract)), MA50, label="MA50")
plt.plot(list(range(full_len - num_subtract)), MA100, label="MA100")
plt.rcParams.update({'font.size': 42})
plt.legend(fontsize=28)

volum_change = data.iloc[500:, 6:8].values
print(volum_change)


def std(X):
    avg = np.mean(X)
    sum = 0
    for i in range(len(X)):
        sum = sum + (X[i] - avg)**2
    return math.sqrt(sum/(len(X)-1))


STD5 = []
STD20 = []
STD50 = []
STD100 = []
for i in range(500, full_len):
    STD5.append(std(log_market_data[i-5:i, 0]))
    STD20.append(std(log_market_data[i-20:i, 0]))
    STD50.append(std(log_market_data[i-50:i, 0]))
    STD100.append(std(log_market_data[i-100:i, 0]))

plt.figure(figsize=(30, 13))
plt.plot(list(range(full_len - num_subtract)), MA_data, label="Close price")
plt.plot(list(range(full_len - num_subtract)), STD5, label="STD5")
plt.plot(list(range(full_len - num_subtract)), STD20, label="STD20")
plt.plot(list(range(full_len - num_subtract)), STD50, label="STD50")
plt.plot(list(range(full_len - num_subtract)), STD100, label="STD100")
plt.legend(fontsize=28)


def calculate_ema(prices, days, smoothing=2):
    ema = [sum(prices[:days]) / days]
    for price in prices[days:]:
        ema.append((price * (smoothing / (1 + days))) +
                   ema[-1] * (1 - (smoothing / (1 + days))))
    return ema


EMA5 = calculate_ema(log_market_data[500-4:, 0], 5)
EMA20 = calculate_ema(log_market_data[500-19:, 0], 20)
EMA50 = calculate_ema(log_market_data[500-49:, 0], 50)
EMA100 = calculate_ema(log_market_data[500-99:, 0], 100)

plt.figure(figsize=(30, 13))
plt.plot(list(range(full_len - 500)), MA_data, label='Close price')
plt.plot(list(range(full_len - 500)), EMA5, label='EMA5')
plt.plot(list(range(full_len - 500)), EMA20, label='EMA20')
plt.plot(list(range(full_len - 500)), EMA50, label='EMA50')
plt.plot(list(range(full_len - 500)), EMA100, label='EMA100')

plt.legend(fontsize=28)

MACD0 = np.array(EMA5) - np.array(EMA20)
MACD1 = np.array(EMA5) - np.array(EMA50)
MACD2 = np.array(EMA5) - np.array(EMA100)
MACD3 = np.array(EMA20) - np.array(EMA50)
MACD4 = np.array(EMA20) - np.array(EMA100)
MACD5 = np.array(EMA50) - np.array(EMA100)
plt.figure(figsize=(30, 13))
plt.plot(list(range(full_len - 500)), MACD0, label='MACD0')
plt.plot(list(range(full_len - 500)), MACD1, label='MACD1')
plt.plot(list(range(full_len - 500)), MACD2, label='MACD2')
plt.plot(list(range(full_len - 500)), MACD3, label='MACD3')
plt.plot(list(range(full_len - 500)), MACD4, label='MACD4')
plt.plot(list(range(full_len - 500)), MACD5, label='MACD5')
plt.legend(fontsize=28)

band_up = np.array(MA20) + 2*np.array(STD20)
band_low = np.array(MA20) - 2*np.array(STD20)

plt.figure(figsize=(30, 13))
plt.plot(list(range(full_len - 500)), MA_data, label='Close Price')
plt.plot(list(range(full_len - 500)), band_up, label='Band_upper')
plt.plot(list(range(full_len - 500)), band_low, label='Band_lower')
plt.legend(fontsize=28)

log_close_price = np.log(log_market_data[500:, 0])
plt.figure(figsize=(30, 8))
plt.plot(list(range(full_len - 500)), log_close_price)

# Using HMM to predict optimal sequence of hidden state

likelihood_vect = np.empty([0, 1])
aic_vect = np.empty([0, 1])
bic_vect = np.empty([0, 1])
STATE_SPACE = range(2, 20)
NUM_ITERS = 10000
dataset = MA_data[num_val:num_val+num_train]
dataset = np.reshape(dataset, (-1, 1))

for states in STATE_SPACE:
    num_params = states**2 + states
    dirichlet_params_states = np.random.randint(1, 50, states)
    #model = hmm.GaussianHMM(n_components=states, covariance_type='full', startprob_prior=dirichlet_params_states, transmat_prior=dirichlet_params_states, tol=0.0001, n_iter=NUM_ITERS, init_params='mc')
    model = hmm.GaussianHMM(
        n_components=states, covariance_type='full', tol=0.0001, n_iter=NUM_ITERS)
    model.fit(dataset)

    if model.monitor_.iter == NUM_ITERS:
        print('Increase number of iterations')
        sys.exit(1)
    likelihood_vect = np.vstack((likelihood_vect, model.score(dataset)))
    aic_vect = np.vstack(
        (aic_vect, -2 * model.score(dataset) + 2 * num_params))
    bic_vect = np.vstack(
        (bic_vect, -2 * model.score(dataset) + num_params * np.log(dataset.shape[0])))

opt_states = np.argmin(bic_vect) + 2
print('Optimum number of states are {}'.format(opt_states))

plt.figure(figsize=(30, 13))
plt.plot(STATE_SPACE, bic_vect, label="BIC")
plt.legend(fontsize=28)


model = hmm.GaussianHMM(n_components=opt_states,
                        covariance_type='full', n_iter=1000)
model.fit(np.reshape(MA_data, (-1, 1)))

range_color = ['brown', 'red', 'deeppink', 'violet', 'aqua', 'gold', 'blue',
               'orangered', 'purple', 'lawngreen', 'dodgerblue', 'lightcoral', 'lime', 'black']
hid_state = model.predict(np.reshape(
    MA_data, (-1, 1)), full_len - num_subtract)
state_color = list(range(num_train+num_val))
for i in range(num_val+num_train):
    state_color[i] = range_color[hid_state[i]]
    # print(range_color[hid_state[i]])

print(hid_state)

plt.figure(figsize=(30, 13))
x_range = list(range(num_train+num_val))
# print(x_range)
plt.scatter(x_range, MA_data[:num_val+num_train], color=state_color)
# plt.scatter([1,5,3],[5,15,35], color = ['aqua','navy','violet'])

plt.figure(figsize=(30, 8))
plt.plot(hid_state)

#hid_state = hid_state.reshape(-1,1)
print(hid_state.shape)
#hid_state = sc.fit_transform(hid_state)

X = np.random.rand(full_len - num_subtract, 9)
# ------------Market Data----------
X[:, 0] = log_market_data[500:, 3]
X[:, 1:4] = log_market_data[500:, 0:3]
X[:, 4:6] = volum_change
X[:, 6] = log_market_data[500:, 1] - log_market_data[500:, 2]
X[:, 7] = hid_state

# Technical Indicator Feature
# -----Moving Average-------------
# X[:,8] = MA5
# X[:,9] = MA20
# X[:,10] = MA50
# X[:,11] = MA100
# --------Standard Deviation------
# X[:,12] = STD5
# X[:,13] = STD20
# X[:,14] = STD50
# X[:,15] = STD100
# -------Exponential Moving Average---
# X[:,16] = EMA5
# X[:,17] = EMA20
# X[:,18] = EMA50
# X[:,19] = EMA100
# ------------Moving Average Covergence Divergence--------
X[:, 8] = MACD1
# X[:,21] = MACD1
# X[:,22] = MACD2
# X[:,23] = MACD3
# X[:,24] = MACD4
# X[:,25] = MACD5
# ---------Boillinger Bands-----------------
# X[:,26] = band_up
# X[:,27] = band_low
# ---------Log Close Price----------
# X[:,13] = log_close_price

plt.figure(figsize=(30, 13))
plt.plot(volum_change[:, 0])

a = band_low
print("Min = ", np.amin(a))
print("Max = ", np.amax(a))
print("Mean = ", np.mean(a))
print("Std = ", np.std(a))

print(a)

sc = MinMaxScaler(feature_range=(0, 1))
sc_prc = MinMaxScaler(feature_range=(0, 1))

X[:, 0:1] = sc_prc.fit_transform(X[:, 0:1])
X[:, 1:] = sc.fit_transform(X[:, 1:])

X_train = X[num_val:num_val+num_train, :]
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
y_train = X[num_val+1:num_val+num_train + 1, 0:1]

X_val = X[:num_val, :]
X_val = np.reshape(X_val, (X_val.shape[0], X_val.shape[1], 1))
y_val = X[1:num_val+1, 0:1]

X_test = X[num_val+num_train:num_val+num_train+num_test, :]
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
y_test = sc_prc.inverse_transform(X[:, 0:1])[num_val+num_train:]

LSTM_model = Sequential()
# Adding the first LSTM layer and some Dropout regularisation
LSTM_model.add(LSTM(units=50, return_sequences=True,
                    input_shape=(X_train.shape[1], 1)))
LSTM_model.add(Dropout(0.2))
# Adding a second LSTM layer and some Dropout regularisation
LSTM_model.add(LSTM(units=50, return_sequences=True))
LSTM_model.add(Dropout(0.2))
# Adding a third LSTM layer and some Dropout regularisation
LSTM_model.add(LSTM(units=50, return_sequences=True))
LSTM_model.add(Dropout(0.2))
# Adding a fourth LSTM layer and some Dropout regularisation
LSTM_model.add(LSTM(units=50))
LSTM_model.add(Dropout(0.2))
# Adding the output layer
LSTM_model.add(Dense(units=1))
# Compiling the RNN
LSTM_model.compile(optimizer='adam', loss='mean_squared_error')

LSTM_model.summary()

LSTM_model.fit(X_train, y_train, epochs=1, batch_size=100,
               validation_data=(X_val, y_val))

LSTM_model.save('HMM_LSTM_final.h5')

LSTM_model.load_weights('HMM_LSTM_final.h5')

X_total = X[:full_len - 201, :]
X_total = np.reshape(X_total, (X_total.shape[0], X_total.shape[1], 1))

predict_price = LSTM_model.predict(X_test)
print(predict_price.shape)
predict_price = sc_prc.inverse_transform(predict_price)

# predict_price = sc.inverse_transform(predict_price)

# predict_price = np.exp(predict_price)
# real_price = np.exp(y_test)
# real_price = sc_prc.inverse_transform(y_train)

real_price = y_test


plt.figure(figsize=(30, 13))
plt.plot(list(range(180)), predict_price, 'r', label='Predict Price')
plt.plot(list(range(180)), real_price, 'b--', label='Real Price')
plt.legend()

MAPE = np.abs(predict_price - real_price)
RMSE = np.multiply(MAPE, MAPE)
RMSE = math.sqrt(np.mean(RMSE))/np.mean(real_price)
MAE = (MAPE)/(real_price)  # Real
MAPE = np.divide(MAPE, real_price)
MAPE = np.mean(MAPE)
doctId = str(uuid.uuid4())
sum = 0
sumpredict = 0
# updating the data from client to db.
for x in real_price:
    print("Real", x)
    outputData = db.collection(u'Output11').document(str(sum))

    h = str(x)
    new = h.replace("[", "")
    g = new.replace("]", "")

    data = {
        'Realprice': g
    }
    outputData.set(data)
    sum = sum + 1
for x in predict_price:

    outputData = db.collection(u'Output111').document(str(sumpredict))
    x = x / 1.25
    h = str(x)

    new = h.replace("[", "")
    g = new.replace("]", "")

   ## g = re.findall(r'\d+',str(x))
  # if(len(g) == 2):
    ##    f = g[0] +"." +g[1]
    # else:
   ##     f = g[0]

    data = {
        'Predictprice': g
    }
    outputData.set(data)
    sumpredict = sumpredict + 1
# data = {
# data = {
#    u'MAPE': MAPE,

 #   u'RMSE': RMSE*100,
# }

# outputData.set(data)

#print('MAPE = ', MAPE)
#print('MAE = ', MAE*100, '%')
#print('RMSE = ', RMSE*100, '%')
# Create an Event for notifying main thread.
callback_done = threading.Event()

# Create a callback on_snapshot function to capture changes
