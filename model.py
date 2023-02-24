import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle
import csv

# Load the dataset
df = pd.read_csv("data.csv")

# Extract the features and labels
X = df.drop("results", axis=1)
y = df["results"]

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Create the classifier
clf = RandomForestClassifier(n_estimators=100)

# Train the classifier
clf.fit(X_train, y_train)

accuracy = clf.score(X_test, y_test)
print("Accuracy:", accuracy)

with open("model.pkl", "wb") as f:
    pickle.dump(clf, f)
