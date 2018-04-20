import pandas as pd
# basic libraries
import pandas as pd
import numpy as np
from itertools import chain
import pickle

# nlp libraries
import re, nltk, spacy, gensim
from nltk.corpus import stopwords
from textblob import Word, TextBlob
from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.models import KeyedVectors # load the Stanford GloVe model
from gensim import corpora, models, similarities

# sklearn
from sklearn.decomposition import LatentDirichletAllocation, TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

# plotting/printing
from pprint import pprint
import pyLDAvis
import pyLDAvis.sklearn
import matplotlib.pyplot as plt

from wordfreq import word_frequency


import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import export_graphviz
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score
from clean_data import featurize, clean_data
from get_wikipedia_categories import get_wikipedia_article
from sklearn.model_selection import train_test_split

def get_forest_importance(rf):
    # Get numerical feature importances
    importances = list(rf.feature_importances_)
    # List of tuples with variable and importance
    feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]
    # Sort the feature importances by most important first
    feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
    # Print out the feature and importances 
    [print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances];

    # Set the style
    plt.style.use('fivethirtyeight')
    # list of x locations for plotting
    x_values = list(range(len(importances)))
    # Make a bar chart
    plt.bar(x_values, importances, orientation = 'vertical')
    # Tick labels for x axis
    plt.xticks(x_values, feature_list, rotation='vertical')
    # Axis labels and title
    plt.ylabel('Importance'); plt.xlabel('Variable'); plt.title('Variable Importances');

#df = pd.read_csv('JEOPARDY_CSV.csv')
df = pd.read_csv("jeopardy_cats.csv")

# clean the data
df = clean_data(df, classification=False)

# create basic features from the data
#df = featurize(df)

y = df['Value']

X = df.drop(['Value', 'Show Number', 'Air Date', 'Round', 'Category', 'Question', 'Answer'], axis = 1, inplace=False)

feature_list = list(X.columns)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42)

# regression
rf = RandomForestRegressor(n_estimators = 1000, random_state = 42)
rf.fit(X_train, y_train)
predictions = rf.predict(X_test)
print(rf.scores)
get_forest_importance(rf)
