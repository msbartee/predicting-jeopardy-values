import pandas as pd

from clean_data import featurize, clean_data
from get_wikipedia_categories import get_wikipedia_article
from sklearn.model_selection import train_test_split

df = pd.read_csv('JEOPARDY_CSV.csv')

# clean the data
df = clean_data(df)

# create basic features from the data
#df = featurize(df)

# get wikipedia
get_wikipedia_article(df)




print('Training Features Shape:', train_features.shape)
print('Training Labels Shape:', train_labels.shape)
print('Testing Features Shape:', test_features.shape)
print('Testing Labels Shape:', test_labels.shape)
