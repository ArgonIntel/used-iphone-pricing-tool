from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pandas as pd
import pickle

def model_train(data):
    X = data[["battery", "rom", "model", "warranty", "charger"]]
    y = data["price"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    preprocessor = ColumnTransformer(
        transformers= [
            ("model", OneHotEncoder(), ["model"])
        ],
        remainder = "passthrough"
    )

    model = Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", LinearRegression())
    ])

    model.fit(X_train, y_train)

    score = model.score(X_test, y_test)
    with open("regresija.pkl", "wb") as file:
        pickle.dump(model, file)
    return score

def predict_price(dataframe):

    with open('regresija.pkl', 'rb') as file:
        loaded_model = pickle.load(file)

    predictions = loaded_model.predict(dataframe)
    return predictions

