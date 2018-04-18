import pandas as pd

from clean_data import featurize, clean_data
from get_wikipedia_categories import get_wikipedia_article

df = pd.read_csv('JEOPARDY_CSV.csv')

# clean the data
df = clean_data(df)

# create basic features from the data
#df = featurize(df)

# get wikipedia
get_wikipedia_article(df)





