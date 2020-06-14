import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

# Importing the data set with pandas and taking the necessary variables
url = 'D:\Programming Tutorials\Machine Learning\Projects\Datasets\Pickles\Salary_Data.csv'
dataset = pd.read_csv(url)
x = dataset.iloc[:, :-1].values
y = dataset.iloc[:, 1].values

xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size = 0.2, random_state = 10)

# Fitting Simple Linear Regression model to training set
regressor = LinearRegression()
regressor.fit(xTrain, yTrain)

# Predicting results from test set
yPred = regressor.predict(xTest)

'''Creating & saving the model using joblib into a file'''

fileName = 'joblib_file.pkl'
joblib.dump(regressor, open(fileName, 'wb'))

# loading the saved model using joblib
saved_model1 = joblib.load(open(fileName, 'rb'))
#yPred_model1 = saved_model.predict([[4.6]])