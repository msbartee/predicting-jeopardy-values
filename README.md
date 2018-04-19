# Trivial Pursuit: *Jeopardy!* Questions and the Value of Knowledge

The goal of this project is to predict the dollar value of *Jeopardy!* Questions. This might seem like a trivial endeavor (pun *totally* intended). However, this analysis could tell us a lot about the kind of knowledge that we (or at least the writers of *Jeopardy!*) value in Western society, what is considered common knowledge, and what is considered more difficult.

In addition, this project could be extended to any test for which the questions are ordered or assigned points by difficulty, such as standardized tests, giving students a sense of where to prioritize study efforts.

![I knew I should have studied Central Asian Geography!](jeopardy.png)

## The Dataset

* approximately 217,000 *Jeopardy!* questions from 1984 to 2012
* includes the question, answer, value, category, round, show number, and air date
* by design, the target values are roughly balanced

Fun facts:

* China is the most common answer in *Jeopardy!*, followed by Australia

### Data Cleaning

* *Jeopardy!* questions doubled in value in November 2001, so I doubled all values before that time
* I excluded Daily Double and Final Jeopardy questions, for which the value is determined by the contestant
* Typical NLP tasks: lowercase, remove punctuation, lemmatization

Fun Facts:

* the most common words in the questions are:

```
one        241
first      188
name       173
u          121
2          117
city       111
country    106
called      98
state       91
like        91
```

* the most common words in the categories are:

```
words       80
history     73
world       61
tv          47
century     46
time        45
american    45
science     40
us          39
movie       37
```

* most common bigrams in questions:

```
[(('New', 'York'), 309),
(('became', 'first'), 277),
(('The', 'first'), 248),
(('This', 'country'), 246),
(('The', 'name'), 241),
(('&', 'The'), 194),
(('capital', 'city'), 160),
(('This', 'state'), 151),
(('No.', '1'), 144),
(('country', 'In'), 134)]
```

 * most common trigrams in questions:

```
[(('South', 'American', 'country'), 61),
(('New', 'York', 'City'), 59),
(('World', 'War', 'II'), 39),
(('whose', 'name', 'means'), 38),
(('became', 'first', 'woman'), 28),
(('(Sofia', 'Clue', 'Crew'), 27),
(('(Sarah', 'Clue', 'Crew'), 25),
(('feet', 'sea', 'level'), 24),
(('British', 'prime', 'minister'), 23),
(('(Jimmy', 'Clue', 'Crew'), 22)]
```



## Feature Generation

* number of words in question
* average length of words in question
* frequency in English of words in question or answer

![Average Word Length](average_word_length.png)
![Number of Words in Question](number_words.png)
![Average Frequency of Words in Question](avg_freq_words_question.png)
![Average Frequency of Words in Answer](avg_freq_words_answer.png)

These were not predictive, not even a little...

* linear regression MSE: 

### Named Entity Recognition

* Spacy can identify people, places, organizations, etc.
* But too many answers are not recognized

### Topic Modeling

* unsupervised
* could be interesting to uncover non-obvious clusters of knowledge
* could used predictive value to determine correct number of topics

However, answers themselves could be categorized without topic modeling:

  * Emily Dickinson: poets
  * Albert Einstein: scientists
  * The Blues Brothers: movies

### Wikipedia-Derived Categories

* for every answer in the database, query Wikipedia and get categories:

**Moses**:

* '15th-century BC biblical rulers',
* 'Adoptees',
* 'Ancient Egyptian Jews',
* 'Ancient Egyptian princes',
* 'Angelic visionaries',
* 'Biblical murderers',
* 'Book of Exodus',
* 'Christian royal saints',
* 'Christian saints from the Old Testament',
* 'Founders of religions',
* 'Wonderworkers'
...

However:

* what if answer is not a Wikipedia article:
  * "F-A-N-T-A-S-T-I-K" (cleaner from SC Johnson)
  * "the ant" vs "Ant"

* tried to build fuzzy match algorithm --- did not do well
* built function to query google custom search API to search Wikipedia for answer --- did really well!
* dropped categories that appeared in less than 10 rows and more than 25% of total rows
* dropped non-meaningful categories ("Articles with unsourced statements from June 2017")
* but it's slow and dependent upon connectivity/API responsiveness...up to about 10,000 rows so far


## Exploring the World of *Jeopardy!*

* most common categories overall:

Category:English-language films 
Category:Grammy Award winners 
Category:American male film actors 
Category:American film actresses 
Category:Presidential Medal of Freedom recipients 
Category:Member states of the United Nations 


![Word Cloud of All Questions](all.png)


* most common categories for values of \$500 or less:

Category:American male film actors 547
Category:States of the United States 979
Category:Hall of Fame for Great Americans inductees 559
Category:Presidents of the United States 628
Category:Presidential Medal of Freedom recipients 697
Category:Member states of the United Nations 1558
Category:20th-century American politicians 590
Category:Prophets of Islam 646
Category:American films 929
Category:American television personalities 551
Category:English rock singers 690
Category:Male television writers 584
Category:Princeton University alumni 523
Category:Free speech activists 515
Category:Countries in Europe 593

![Word Cloud of Questions Valued Under 500 Dollars](500.png)

* most common categories for values of \$1,500 or more:

Category:States of the United States 396
Category:19th-century American politicians 203
Category:Hall of Fame for Great Americans inductees 240
Category:Presidents of the United States 297
Category:Presidential Medal of Freedom recipients 249
Category:Member states of the Organisation of Islamic Cooperation 224
Category:Member states of the Union for the Mediterranean 359
Category:Member states of the United Nations 1067
Category:20th-century American politicians 211
Category:New York (state) lawyers 310
Category:American films 329
Category:Countries in the Caribbean 408
Category:American television personalities 229
Category:English rock singers 324
Category:English male dramatists and playwrights 231
Category:Male television writers 253
Category:Princeton University alumni 287
Category:Free speech activists 285
Category:Countries in Europe 375
Category:G20 nations 268
Category:American billionaires 241
Category:Progressive Era in the United States 201

![Word Cloud of Questions Valued Under 1500 Dollars](1500.png)

* most common categories by year

* topic modeling of dataset

## Random Forests

* tried random forest regression and classification algorithms

## Simulation


