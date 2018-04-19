# Trivial Pursuit: *Jeopardy!* Questions and the Value of Knowledge

The goal of this project is to predict the dollar value of *Jeopardy!* Questions. This might seem like a trivial endeavor (pun *totally* intended). However, this analysis could tell us a lot about the kind of knowledge that we (or at least the writers of *Jeopardy!*) value in Western society, what is considered common knowledge, and what is considered more difficult.

In addition, this project could be extended to any test for which the questions are ordered or assigned points by difficulty, such as standardized tests, giving students a sense of where to prioritize study efforts.

![I knew I should have studied Central Asian Geography!](jeopardy.png)

## The Dataset

* approximately 217,000 *Jeopardy!* questions from 1984 to 2012
* includes the question, answer, value, category, round, show number, and air date
* by design, the target values are roughly balanced

### Data Cleaning

* *Jeopardy!* questions doubled in value in November 2001, so I doubled all values before that time
* I excluded Daily Double and Final Jeopardy questions, for which the value is determined by the contestant

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
* but it's slow and dependent upon connectivity/API responsiveness...up to about 10,000 rows so far

## Exploring the World of *Jeopardy!*

* most common categories by value
* most common categories by year
* topic modeling of dataset

## Random Forests

* tried random forest regression and classification algorithms

## Simulation


