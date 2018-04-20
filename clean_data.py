import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from textblob import Word, TextBlob

def clean_data(df, small=False, classification=False):
    """
    cleans the Jeopardy! csv file so that it has only the categories that are needed.
    """

    # remove final jeopardy
    df.drop(df[df['Round'] == 'Final Jeopardy!'].index, inplace=True)

    # remove tiebreakers
    df.drop(df[df['Round'] == 'Tiebreaker'].index, inplace=True)

    # change values from text to numbers
    df['Value'] = pd.to_numeric(df['Value'])

    # make sure that the answer is a string
    df['Answer'] = df['Answer'].astype(str)
    df['Question'] = df['Question'].astype(str)

    # drop questions with urls in them
    #df.drop(df[df['Question'].str.contains('http')].index, inplace=True)

    # double values before show number 3966, when values increased
    df['Value'] *= np.where(df['Show Number'] < 3966, 2, 1)

    # remove daily doubles as best i can
    df.drop(df[df['Value'] % 200 != 0].index, inplace=True)

    # remove daily doubles as best i can
    df.drop(df[df['Value'] > 2000].index, inplace=True)

    if set(df['Value'].unique()) != set([200,400,600,800,1000,1200,1400,1600,1800,2000]):
        print("There seems to have been an error correcting the values.")

    # drop unneeded columns
    #df.drop(['Show Number', 'Air Date'], axis = 1, inplace=True)

    df = df.dropna(axis=1, how='any')
    df = df.dropna(axis=0, how='any')

    if small:
        df = df.sample(frac=1).reset_index(drop=True)[:5000]

    if classification:
        df['Value'] = np.where(df['Value'] >= 1200, 1, 0)

    return df

def avg_word(sentence):
  words = sentence.split()
  return sum(len(word) for word in words)/len(words)

def featurize(df):
    # create a feature with the word count of the question
    df['word_count_question'] = df['Question'].apply(lambda x: len(x.split()))
    
    # create a feature with the character count of the question
    df['char_count_question'] = df['Question'].str.len()

    #df['avg_word_len_question'] = df['Question'].apply(lambda x: avg_word(x))
    
    # see if there is a date in the question
    df['has_date'] = np.where(df['Question'].str.contains('\d{4}'), 1, 0)
    
    # see if there is a "" in the category
    #df['has_quotes'] = np.where(df['Category'].str.contains('"'), 1, 0)
    
    # remove punctuation
    df['Question'] = df['Question'].str.replace('[^\w\s]','')
    df['Question'] = df['Question'].str.replace('"','')
    df['Category'] = df['Category'].str.replace('[^\w\s]','')
    #df['answer'] = df['answer'].str.replace('[^\w\s]','')
    #df['answer'] = df['answer'].str.replace('"','')
    
    # remove stopwords
    stop = stopwords.words('english')
    df['Question'] = df['Question'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
    df['Category'] = df['Category'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
    #df['answer'] = df['answer'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))

    # lowercase
    df['Question'] = df['Question'].apply(lambda x: x.lower())
    df['Category'] = df['Category'].apply(lambda x: x.lower())
    #df['answer'] = df['answer'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))

    # create tokenized and lemmatized questions
    df['lem_question'] = df['Question'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))
  
    # create tokenized lists from lemmatized questions
    df['tok_question'] = df['lem_question'].apply(lambda x: [Word(word).lemmatize() for word in x.split()])
    
    return df
