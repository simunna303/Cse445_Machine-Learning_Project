# -*- coding: utf-8 -*-
"""Cse445_Predict_the_positions_and_speeds_of_600_satellites.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UKQjuNnJmoShObrgZ-tE20lBz1pmtvxZ
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from math import sqrt
# %matplotlib inline
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
from sklearn import metrics
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from google.colab import drive
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score, r2_score
from sklearn.model_selection import cross_val_score, cross_validate
from sklearn import metrics

drive.mount('/content/drive',force_remount=True)

satellite = pd.read_csv('/content/drive/MyDrive/445ml/jantrain.csv')

#check unique values
satellite.apply(lambda x: len(x.unique()))

satellite.head()

#info about datatype
satellite.info()

#missing values
satellite.isnull().sum()

# Distribution graphs (histogram/bar graph) of column data
def plotPerColumnDistribution(df, nGraphShown, nGraphPerRow):
    nunique = df.nunique()
    df = df[[col for col in df if nunique[col] > 1 and nunique[col] < 50]] # For displaying purposes, pick columns that have between 1 and 50 unique values
    nRow, nCol = df.shape
    columnNames = list(df)
    nGraphRow = (nCol + nGraphPerRow - 1) / nGraphPerRow
    plt.figure(num = None, figsize = (6 * nGraphPerRow, 8 * nGraphRow), dpi = 80, facecolor = 'w', edgecolor = 'k')
    for i in range(min(nCol, nGraphShown)):
        plt.subplot(nGraphRow, nGraphPerRow, i + 1)
        columnDf = df.iloc[:, i]
        if (not np.issubdtype(type(columnDf.iloc[0]), np.number)):
            valueCounts = columnDf.value_counts()
            valueCounts.plot.bar()
        else:
            columnDf.hist()
        plt.ylabel('counts')
        plt.xticks(rotation = 90)
        plt.title(f'{columnNames[i]} (column {i})')
    plt.tight_layout(pad = 1.0, w_pad = 1.0, h_pad = 1.0)
    plt.show()

# Correlation matrix
def plotCorrelationMatrix(df, graphWidth):
    filename = df.dataframeName
    df = df.dropna('columns') # drop columns with NaN
    df = df[[col for col in df if df[col].nunique() > 1]] # keep columns where there are more than 1 unique values
    if df.shape[1] < 2:
        print(f'No correlation plots shown: The number of non-NaN or constant columns ({df.shape[1]}) is less than 2')
        return
    corr = df.corr()
    plt.figure(num=None, figsize=(graphWidth, graphWidth), dpi=80, facecolor='w', edgecolor='k')
    corrMat = plt.matshow(corr, fignum = 1)
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.gca().xaxis.tick_bottom()
    plt.colorbar(corrMat)
    plt.title(f'Correlation Matrix for {filename}', fontsize=15)
    plt.show()

# Scatter and density plots
def plotScatterMatrix(df, plotSize, textSize):
    df = df.select_dtypes(include =[np.number]) # keep only numerical columns
    # Remove rows and columns that would lead to df being singular
    df = df.dropna('columns')
    df = df[[col for col in df if df[col].nunique() > 1]] # keep columns where there are more than 1 unique values
    columnNames = list(df)
    if len(columnNames) > 10: # reduce the number of columns for matrix inversion of kernel density plots
        columnNames = columnNames[:10]
    df = df[columnNames]
    ax = pd.plotting.scatter_matrix(df, alpha=0.75, figsize=[plotSize, plotSize], diagonal='kde')
    corrs = df.corr().values
    for i, j in zip(*plt.np.triu_indices_from(ax, k = 1)):
        ax[i, j].annotate('Corr. coef = %.3f' % corrs[i, j], (0.8, 0.2), xycoords='axes fraction', ha='center', va='center', size=textSize)
    plt.suptitle('Scatter and Density Plot')
    plt.show()

nRowsRead = 1000 # specify 'None' if want to read whole file
# answer_key.csv may have more rows in reality, but we are only loading/previewing the first 1000 rows
df1 = pd.read_csv('/content/drive/MyDrive/445ml/jantrain.csv', delimiter=',', nrows = nRowsRead)
df1.dataframeName = 'jantrain.csv'
nRow, nCol = df1.shape
print(f'There are {nRow} rows and {nCol} columns')

df1.head(5)

plotPerColumnDistribution(df1, 10, 5)

plotCorrelationMatrix(df1, 8)

plotScatterMatrix(df1, 18, 10)

print(satellite.shape)

data=satellite.drop(columns = ['id'])
data.head()

print(data.shape)

data['epoch'] = pd.to_datetime(data['epoch'])    
data['epoch'] = (data['epoch'] - data['epoch'].min())  / np.timedelta64(1,'D')
data.head(10000)

data.values

data.columns

x = data[['x', 'y', 'z', 'Vx', 'Vy', 'Vz']]

y = data[['x_sim', 'y_sim', 'z_sim', 'Vx_sim', 'Vy_sim', 'Vz_sim']]

data = data[['x', 'y', 'z', 'Vx', 'Vy', 'Vz', 'x_sim', 'y_sim', 'z_sim', 'Vx_sim', 'Vy_sim', 'Vz_sim']]

data.info()

print(x)

print(y)

#pairplot
sns.pairplot(data)

# split into train test sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33)
print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)

def train (model, x_train, y_train):
  model.fit(x_train, y_train)
  predictions = model.predict(x_test)
  print("Accuracy: ",model.score(y_test, predictions)*100)
  print("RMSE : %.4g" % np.sqrt(metrics.mean_squared_error(y_test, predictions)))
  print("MAE:",metrics.mean_absolute_error(y_test, predictions))
  print("MSE:",metrics.mean_squared_error(y_test, predictions))

model = LinearRegression(normalize=True)
print("Model Report: Linear Regression")
train(model, x_train, y_train)

predictions = model.predict(x_test)

plt.scatter(y_test, predictions)



model = Ridge(normalize=True)
print("Model Report: Ridge")
train(model, x_train, y_train)

model = Lasso()
print("Model Report: Lasso")
train(model, x_train, y_train)

# Fitting Decision Tree Regression to the dataset
from sklearn.tree import DecisionTreeRegressor
model = DecisionTreeRegressor()
print("Model Report: Decision Tree")
train(model, x_train, y_train)

# fit the model
model = RandomForestRegressor()
print("Model Report: Random Forest")
train(model, x_train, y_train)