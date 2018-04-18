import pandas as pd
import search_google.api
import wikipediaapi
import pickle
import re

def get_wikipedia_article(df):
    """
    this script queries wikipedia for each of the answers in the Jeopardy dataset,
    if the article is found, its name and the categories it is associated with are
    returned. If it is not found, a google search is performed to find the most likely
    wikipedia article, and then the categories are returned.
    """

    with open('SECRET_API_KEY', 'r') as f:
        SECRET_API_KEY = f.read()

    answers = list(df['Answer'])
    wiki_wiki = wikipediaapi.Wikipedia('en')
    buildargs = {
      'serviceName': 'customsearch',
      'version': 'v1',
      'developerKey': SECRET_API_KEY
    }

    try:
        wikipedia_articles = pickle.load( open("wikipedia_articles.pickle","rb"))
    except:
        wikipedia_articles = {}


    for answer in answers:
        if answer not in wikipedia_articles:
            page_py = wiki_wiki.page(answer)
            if page_py.exists():
                wikipedia_articles[answer] = answer
                get_wikipedia_categories(answer, answer, page_py)
            else:
                try:
                    # Define cseargs for search
                    cseargs = {
                      'q': answer,
                      'cx': '014712677646867345626:3owqempv_5c',
                      'num': 1
                    }
                    results = search_google.api.results(buildargs, cseargs)
                    url = results.metadata['items'][0]['link']
                    result = re.findall("wiki\/(.*)$", url)[0]
                    wikipedia_articles[answer] = result
                    page_py = wiki_wiki.page(result)
                    get_wikipedia_categories(answer, result, page_py)
                except:
                    print("Google scrape failed for {}".format(answer))

    pickle.dump(wikipedia_articles, open("wikipedia_articles.pickle", "wb"))

def get_wikipedia_categories(answer, article_name, page_py):
    """
    this takes a wikipedia article object and gets the categories associated with it.
    """

    try:
        wikipedia_categories = pickle.load( open("wikipedia_categories.pickle","rb"))
    except:
        wikipedia_categories = {}

    try:
        wikipedia_categories_as_key = pickle.load( open("wikipedia_categories_as_key.pickle","rb"))
    except:
        wikipedia_categories_as_key = {}

    categories = page_py.categories
    if answer not in wikipedia_categories:
        wikipedia_categories[answer] = set()
        for title in categories.keys():
            wikipedia_categories[answer].add(title)
            if title not in wikipedia_categories_as_key:
                wikipedia_categories_as_key[title] = set()
                wikipedia_categories_as_key[title].add(answer)
            else:
                wikipedia_categories_as_key[title].add(answer)


    pickle.dump(wikipedia_categories, open("wikipedia_categories.pickle", "wb"))
    pickle.dump(wikipedia_categories_as_key, open("wikipedia_categories_as_key.pickle", "wb"))

def featurize_wikipedia(df):
    try:
        wikipedia_articles = pickle.load( open("wikipedia_articles.pickle","rb"))
    except:
        wikipedia_articles = {}
    try:
        wikipedia_categories = pickle.load( open("wikipedia_categories.pickle","rb"))
    except:
        wikipedia_categories = {}
    try:
        wikipedia_categories_as_key = pickle.load( open("wikipedia_categories_as_key.pickle","rb"))
    except:
        wikipedia_categories_as_key = {}

    if len(wikipedia_articles) != len(df):
        print("Looks like you don't have all the articles yet.")
        print("Wikipedia Articles Collected: {}".format(len(wikipedia_articles)))
        print("Length of Database: {}".format(len(df)))
    else:
        print("Working through {} Wikipedia categories".format(len(wikipedia_categories_as_key)))
        for index, cat in enumerate(wikipedia_categories_as_key.keys()):
            print("Progress: {}".format(index/len(wikipedia_categories_as_key)))
            df[cat] = np.where(df['Answer'].isin(wikipedia_categories_as_key[cat]),1,0)
