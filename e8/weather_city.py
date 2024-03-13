import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
import sys
from sklearn.preprocessing import StandardScaler

# C:/Users/brand/anaconda3/python.exe weather_city.py monthly-data-labelled.csv monthly-data-unlabelled.csv labels.csv

data_labelled = pd.read_csv(sys.argv[1])
data_unlabelled = pd.read_csv(sys.argv[2])

# setup x and y datasets
x_labelled = data_labelled.drop(['city', 'year'], axis=1) # city and year not relevant for x variable
y_labelled = data_labelled['city']
x_unlabelled = data_unlabelled.drop(['city', 'year'], axis=1)

# standarize datasets
scaler = StandardScaler()
x_labelled_scaled = scaler.fit_transform(x_labelled)
x_unlabelled_scaled = scaler.fit_transform(x_unlabelled)

X_train, X_valid, y_train, y_valid = train_test_split(x_labelled_scaled, y_labelled)

# train model
mlp_model = MLPClassifier(solver='lbfgs', activation='logistic', hidden_layer_sizes=(200,))
mlp_model.fit(X_train, y_train)

# score around 0.74-0.8
score = mlp_model.score(X_valid, y_valid)
print("score: ", score)

# predict based on trained model
predictions = mlp_model.predict(x_unlabelled_scaled)
pd.Series(predictions).to_csv(sys.argv[3], index=False, header=False)