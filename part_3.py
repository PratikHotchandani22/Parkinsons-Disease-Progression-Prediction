# -*- coding: utf-8 -*-
"""ARIMA model

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1B-NczLfeNEL_zntJU3NyYdgBGfLxhHcW
"""

import numpy as np 
import pandas as pd 
from google.colab import drive
drive.mount('/content/drive')
import warnings
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import statsmodels.api as sm
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.stattools import acf
from math import sqrt

train_clinical_data = pd.read_csv("/content/drive/My Drive/IDMP/train_clinical_data.csv")
train_peptides = pd.read_csv("/content/drive/My Drive/IDMP/train_peptides.csv")
train_protiens = pd.read_csv("/content/drive/My Drive/IDMP/train_proteins.csv")
supplemental_clinical_data = pd.read_csv("/content/drive/My Drive/IDMP/supplemental_clinical_data.csv")
train = train_clinical_data.append(supplemental_clinical_data,ignore_index=True)

train

obs_count = train.groupby("patient_id")['updrs_1'].count()
max_obs_patient = obs_count.idxmax()
print("Patient with the highest number of observations:", max_obs_patient)

df_15009 = train[train['patient_id'] == 15009]

df_15009_final = df_15009[['visit_id','updrs_1']]

len(df_15009_final)

train_df = df_15009_final[:14]
train_df

test_df = df_15009_final.iloc[-3:, :]
test_df

result = adfuller(train_df['updrs_1'])
print(f'Test Statistic: {result[0]}')
print(f'p-value: {result[1]}')

"""train_df is stationary time series dataframe"""

train_df = train_df.set_index('visit_id')
train_df['updrs_1'].plot()

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))
plot_acf(train_df, ax=ax1, lags=6)
plot_pacf(train_df, ax=ax2, lags=6)
plt.show()

!pip install pmdarima

from pmdarima.arima import auto_arima
from sklearn.metrics import mean_absolute_error, mean_squared_error

# fit the best ARIMA model
model = auto_arima(train_df['updrs_1'], start_p=0, start_d=0, start_q=1, max_p=6, max_d=1, max_q=6, 
                   seasonal=False, trace=True)

# print model summary
print(model.summary())

# get predictions for the test data
predictions = model.predict(n_periods=len(test_df))

# Calculate MAE and RMSE
mae = mean_absolute_error(test_df, predictions)
rmse = mean_squared_error(test_df, predictions, squared=False)

print("MAE:", mae)
print("RMSE:", rmse)

model_1 = sm.tsa.ARIMA(train_df, order=(4, 0, 5))
results_1 = model_1.fit()

results_1.summary()

preds = results_1.forecast(steps=len(test_df))
preds = pd.DataFrame(preds)

preds['visit_id'] = ["15009_84","15009_96","15009_108"]

preds = preds.set_index('visit_id')

test_df

mae = mean_absolute_error(test_df['updrs_1'], preds)
rmse = sqrt(mean_squared_error(test_df['updrs_1'], preds))

print("Mean absolute error: ", mae)
print("Root mean squared error: ", rmse)

test_df = test_df.set_index('visit_id')

plt.figure(figsize=(12,6))
plt.plot(test_df.index, test_df.values, label='Original')
plt.plot(preds.index, preds.values, label='Predicted')
plt.title('Comparison of Original and Predicted Values')
plt.xlabel('visits')
plt.ylabel('updrs_1')
plt.legend()
plt.show()

model_2 = sm.tsa.ARIMA(train_df, order=(0, 0, 0))
results_2 = model_2.fit()

results_2.summary()

preds_2 = results_2.forecast(steps=len(test_df))
preds_2 = pd.DataFrame(preds_2)

preds_2['visit_id'] = ["15009_84","15009_96","15009_108"]

preds_2 = preds_2.set_index('visit_id')
mae = mean_absolute_error(test_df['updrs_1'], preds_2)
rmse = sqrt(mean_squared_error(test_df['updrs_1'], preds_2))

print("Mean absolute error: ", mae)
print("Root mean squared error: ", rmse)


plt.figure(figsize=(12,6))
plt.plot(test_df.index, test_df.values, label='Original')
plt.plot(preds_2.index, preds_2.values, label='Predicted from model 2')
plt.title('Comparison of Original and Predicted Values')
plt.xlabel('visits')
plt.ylabel('updrs_1')
plt.legend()
plt.show()

