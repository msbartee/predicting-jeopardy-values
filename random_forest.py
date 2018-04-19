import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import export_graphviz
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier

# https://towardsdatascience.com/random-forest-in-python-24d0893d51c0


def random_forest_regressor(train_features, train_labels, test_features, test_labels):
    rf = RandomForestRegressor(n_estimators = 1000, random_state = 42)
    rf.fit(train_features, train_labels)


    # Use the forest's predict method on the test data
    predictions = rf.predict(test_features)

    # Calculate the absolute errors
    errors = abs(predictions - test_labels)

    # Print out the mean absolute error (mae)
    print('Mean Absolute Error:', round(np.mean(errors), 2), 'degrees.')


    # Calculate mean absolute percentage error (MAPE)To put our predictions in perspective, we can calculate an accuracy using the mean average percentage error subtracted from 100 %. 
    mape = 100 * (errors / test_labels)
    # Calculate and display accuracy
    accuracy = 100 - np.mean(mape)
    print('Accuracy:', round(accuracy, 2), '%.')

    return rf

def random_forest_classifier(X_train, X_test, y_train, y_test):
    # Create a random forest Classifier. By convention, clf means 'Classifier'
    clf = RandomForestClassifier(n_jobs=2, random_state=0)

    clf.fit(X_train, y_train)

    clf.predict(X_test)

    # View the predicted probabilities of the first 10 observations
    clf.predict_proba(X_test)[0:10]

    preds = y_test[clf.predict(X_test)]

    # Create confusion matrix
    pd.crosstab(y_test, preds, rownames=['Actual'], colnames=['Predicted'])

    # View a list of the features and their importance scores
    list(zip(X_train, clf.feature_importances_))

    return clf

def make_image_tree():
    # Import tools needed for visualization
    import pydot
    # Pull out one tree from the forest
    tree = rf.estimators_[5]
    # Import tools needed for visualization
    from sklearn.tree import export_graphviz
    import pydot
    # Pull out one tree from the forest
    tree = rf.estimators_[5]
    # Export the image to a dot file
    export_graphviz(tree, out_file = 'tree.dot', feature_names = feature_list, rounded = True, precision = 1)
    # Use dot file to create a graph
    (graph, ) = pydot.graph_from_dot_file('tree.dot')
    # Write graph to a png file
    graph.write_png('tree.png')


    # limited tree
    # Limit depth of tree to 3 levels
    rf_small = RandomForestRegressor(n_estimators=10, max_depth = 3)
    rf_small.fit(train_features, train_labels)
    # Extract the small tree
    tree_small = rf_small.estimators_[5]
    # Save the tree as a png image
    export_graphviz(tree_small, out_file = 'small_tree.dot', feature_names = feature_list, rounded = True, precision = 1)
    (graph, ) = pydot.graph_from_dot_file('small_tree.dot')
    graph.write_png('small_tree.png');


def get_forest_importance():
    # Get numerical feature importances
    importances = list(rf.feature_importances_)
    # List of tuples with variable and importance
    feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]
    # Sort the feature importances by most important first
    feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
    # Print out the feature and importances 
    [print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances];


def forest_plot():
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

def plot_actual_predicted():
    # Use datetime for creating date objects for plotting
    import datetime
    # Dates of training values
    months = features[:, feature_list.index('month')]
    days = features[:, feature_list.index('day')]
    years = features[:, feature_list.index('year')]
    # List and then convert to datetime object
    dates = [str(int(year)) + '-' + str(int(month)) + '-' + str(int(day)) for year, month, day in zip(years, months, days)]
    dates = [datetime.datetime.strptime(date, '%Y-%m-%d') for date in dates]
    # Dataframe with true values and dates
    true_data = pd.DataFrame(data = {'date': dates, 'actual': labels})
    # Dates of predictions
    months = test_features[:, feature_list.index('month')]
    days = test_features[:, feature_list.index('day')]
    years = test_features[:, feature_list.index('year')]
    # Column of dates
    test_dates = [str(int(year)) + '-' + str(int(month)) + '-' + str(int(day)) for year, month, day in zip(years, months, days)]
    # Convert to datetime objects
    test_dates = [datetime.datetime.strptime(date, '%Y-%m-%d') for date in test_dates]
    # Dataframe with predictions and dates
    predictions_data = pd.DataFrame(data = {'date': test_dates, 'prediction': predictions})
    # Plot the actual values
    plt.plot(true_data['date'], true_data['actual'], 'b-', label = 'actual')
    # Plot the predicted values
    plt.plot(predictions_data['date'], predictions_data['prediction'], 'ro', label = 'prediction')
    plt.xticks(rotation = '60'); 
    plt.legend()
    # Graph labels
    plt.xlabel('Date'); plt.ylabel('Maximum Temperature (F)'); plt.title('Actual and Predicted Values');
