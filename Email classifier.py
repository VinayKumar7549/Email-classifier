# -*- coding: utf-8 -*-
"""task3 (1).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1fnEieDDYb2glhWbkYoQMnCoHs3oEsL0o

Step 0. Unzip enron1.zip into the current directory.

Step 1. Traverse the dataset and create a Pandas dataframe. This is already done for you and should run without any errors. You should recognize Pandas from task 1.
"""

import pandas as pd
import os
import zipfile

with zipfile.ZipFile('/content/enron1.zip', 'r') as zip_ref:
    zip_ref.extractall('/content/')

def read_spam():
    category = 'spam'
    directory = './enron1/spam'
    return read_category(category, directory)

def read_ham():
    category = 'ham'
    directory = './enron1/ham'
    return read_category(category, directory)

def read_category(category, directory):
    emails = []
    for filename in os.listdir(directory):
        if not filename.endswith(".txt"):
            continue
        with open(os.path.join(directory, filename), 'r') as fp:
            try:
                content = fp.read()
                emails.append({'name': filename, 'content': content, 'category': category})
            except:
                print(f'skipped {filename}')
    return emails

ham = read_ham()
spam = read_spam()

df = pd.DataFrame.from_records(ham)
# Use concat to combine the two DataFrames
df = pd.concat([df, pd.DataFrame.from_records(spam)], ignore_index=True)

"""Step 2. Data cleaning is a critical part of machine learning. You and I can recognize that 'Hello' and 'hello' are the same word but a machine does not know this a priori. Therefore, we can 'help' the machine by conducting such normalization steps for it. Write a function `preprocessor` that takes in a string and replaces all non alphabet characters with a space and then lowercases the result."""

import re

def preprocessor(e):
    pass

"""Step 3. We will now train the machine learning model. All the functions that you will need are imported for you. The instructions explain how the work and hint at which functions to use. You will likely need to refer to the scikit learn documentation to see how exactly to invoke the functions. It will be handy to keep that tab open."""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# The CountVectorizer converts a text sample into a vector (think of it as an array of floats).
# Each entry in the vector corresponds to a single word and the value is the number of times the word appeared.
# Instantiate a CountVectorizer. Make sure to include the preprocessor you previously wrote in the constructor.
# TODO

# Assuming a simple preprocessor that lowercases the text
def preprocessor(text):
    return text.lower()

vectorizer = CountVectorizer(preprocessor=preprocessor)


# Use train_test_split to split the dataset into a train dataset and a test dataset.
# The machine learning model learns from the train dataset.
# Then the trained model is tested on the test dataset to see if it actually learned anything.
# If it just memorized for example, then it would have a low accuracy on the test dataset and a high accuracy on the train dataset.
# TODO

# Features are the email content, labels are the category (ham/spam)
X = df['content']
y = df['category']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Use the vectorizer to transform the existing dataset into a form in which the model can learn from.
# Remember that simple machine learning models operate on numbers, which the CountVectorizer conveniently helped us do.
# TODO

X_train_transformed = vectorizer.fit_transform(X_train)
X_test_transformed = vectorizer.transform(X_test)


# Use the LogisticRegression model to fit to the train dataset.
# You may remember y = mx + b and Linear Regression from high school. Here, we fitted a scatter plot to a line.
# Logistic Regression is another form of regression.
# However, Logistic Regression helps us determine if a point should be in category A or B, which is a perfect fit.
# TODO

model = LogisticRegression()
model.fit(X_train_transformed, y_train)

# Validate that the model has learned something.
# Recall the model operates on vectors. First transform the test set using the vectorizer.
# Then generate the predictions.
# TODO

y_pred = model.predict(X_test_transformed)


# We now want to see how we have done. We will be using three functions.
# `accuracy_score` tells us how well we have done.
# 90% means that every 9 of 10 entries from the test dataset were predicted accurately.
# The `confusion_matrix` is a 2x2 matrix that gives us more insight.
# The top left shows us how many ham emails were predicted to be ham (that's good!).
# The bottom right shows us how many spam emails were predicted to be spam (that's good!).
# The other two quadrants tell us the misclassifications.
# Finally, the `classification_report` gives us detailed statistics which you may have seen in a statistics class.
# TODO



# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')

# Generate the confusion matrix
cm = confusion_matrix(y_test, y_pred)
print('Confusion Matrix:')
print(cm)

# Generate the classification report
report = classification_report(y_test, y_pred)
print('Classification Report:')
print(report)

"""Step 4."""

# Let's see which features (aka columns) the vectorizer created.
# They should be all the words that were contained in the training dataset.
# TODO

# List all features (words) created by the vectorizer
feature_names = vectorizer.get_feature_names_out()
print("Features (words):")
print(feature_names)



#  You may be wondering what a machine learning model is tangibly. It is just a collection of numbers.
#  You can access these numbers known as "coefficients" from the coef_ property of the model
#  We will be looking at coef_[0] which represents the importance of each feature.
#  What does importance mean in this context?
#  Some words are more important than others for the model.
#  It's nothing personal, just that spam emails tend to contain some words more frequently.
#  This indicates to the model that having that word would make a new email more likely to be spam.
#  TODO

# Access the coefficients (importance of each feature)
coefficients = model.coef_[0]



# Iterate over importance and find the top 10 positive features with the largest magnitude.
# Similarly, find the top 10 negative features with the largest magnitude.
# Positive features correspond to spam. Negative features correspond to ham.
# You will see that `http` is the strongest feature that corresponds to spam emails.
# It makes sense. Spam emails often want you to click on a link.
# TODO


import numpy as np

# Get the indices of the top 10 positive (spam) and top 10 negative (ham) features
top_positive_coefficients = np.argsort(coefficients)[-10:]
top_negative_coefficients = np.argsort(coefficients)[:10]

# Print the top features for spam and ham
print("Top 10 words associated with spam:")
for i in top_positive_coefficients:
    print(f"{feature_names[i]}: {coefficients[i]:.3f}")

print("\nTop 10 words associated with ham:")
for i in top_negative_coefficients:
    print(f"{feature_names[i]}: {coefficients[i]:.3f}")

"""Submission
1. Upload the jupyter notebook to Forage.

All Done!
"""