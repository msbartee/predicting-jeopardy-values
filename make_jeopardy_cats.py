import pickle

wikipedia_articles = pickle.load( open("wikipedia_articles.pickle","rb"))
wikipedia_categories = pickle.load( open("wikipedia_categories.pickle","rb"))
wikipedia_categories_as_key = pickle.load( open("wikipedia_categories_as_key.pickle","rb"))



def make_jeopardy_cats(min_len = 24, max_len = 500):
    """
    takes Jeopardy categories available for answers in the database and constructs a csv/feature set.
    """

    cats = []
    for cat in wikipedia_categories_as_key.keys():
        length = len(wikipedia_categories_as_key[cat])
        if length > min_len and length < max_len and "article" not in cat.lower() and "page" not in cat.lower() and \
        "biography" not in cat.lower() and "source" not in cat.lower() and "dmy" not in cat.lower() and "cs1" not in \
        cat.lower() and "wiki" not in cat.lower() and "mdy" not in cat.lower() and "template" not in cat.lower() and \
        "archive" not in cat.lower() and "element" not in cat.lower() and "accuracy" not in cat.lower():
            cats.append(cat)
    print(len(cats))

    infile = open("JEOPARDY_CSV.csv", "r")
    outfile = open("jeopardy_cats.csv", "w")

    start = True
    for line in infile.readlines():
        if start:
            outfile.write(line.strip())
            for cat in cats:
                outfile.write("," + cat)
            outfile.write("\n")
            start = False
        else:
            vals = line.strip().split(",")
            answer = vals[6]
            if answer in wikipedia_categories.keys():
                outfile.write(line.strip())
                for cat in cats:
                    if cat in wikipedia_categories[answer]:
                        outfile.write(",1")
                    else:
                        outfile.write(",0")
                outfile.write("\n")

    infile.close()
    outfile.close()    

    print("Done!")

if __name__ == '__main__':
    make_jeopardy_cats()
