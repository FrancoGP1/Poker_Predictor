# -*- coding: utf-8 -*-
"""PokerMaster-checkpoint.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Jy-wvunpeV7Jts3NcaPAJP8jkUUSJBT-
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import  train_test_split

"""### About the Data

![Alt text](https://farm4.staticflickr.com/3585/3299226824_4637597b74_z_d.jpg "Cards by bl0ndeeo2, Creative Commons License (https://flic.kr/p/62xpc7) ")

The [dataset](http://archive.ics.uci.edu/ml/datasets/Poker+Hand) we'll be exploring in this post is the Poker Hand data from the UCI Machine Learning Repository.

Each record in the dataset is an example of a hand consisting of five playing cards drawn from a standard deck of 52. Each card is described using two attributes (suit and rank), for a total of 10 predictive attributes. The target column describes the hand, with the possibilities being:    

    0: Nothing in hand; not a recognized poker hand     
    1: One pair; one pair of equal ranks within five cards     
    2: Two pairs; two pairs of equal ranks within five cards     
    3: Three of a kind; three equal ranks within five cards     
    4: Straight; five cards, sequentially ranked with no gaps     
    5: Flush; five cards with the same suit     
    6: Full house; pair + different rank three of a kind     
    7: Four of a kind; four equal ranks within five cards     
    8: Straight flush; straight + flush     
    9: Royal flush; {Ace, King, Queen, Jack, Ten} + flush     
    
The order of cards is important, which is why there are 480 possible Royal Flush hands as compared to 4 (one for each suit).
"""

from google.colab import drive
drive.mount('/content/drive')

poker_df= pd.read_csv('/content/drive/My Drive/TEC_9_Sem/Sistemas Inteligentes/poker-hand-training-true .data',header=None)
test = pd.read_csv('/content/drive/My Drive/TEC_9_Sem/Sistemas Inteligentes/poker-hand-testing.data',header=None)

poker_df.columns =['S1', 'C1','S2', 'C2','S3', 'C3','S4', 'C4','S5', 'C5','Hand']
test.columns = ['S1', 'C1','S2', 'C2','S3', 'C3','S4', 'C4','S5', 'C5','Hand']

"""### Separate the Data into Features and Targets"""

# Manually label the columns and classes based on the dataset description from the UCI Repository
#columns: 'first_suit', 'first_rank', 'second_suit', 'second_rank', 'third_suit', 'third_rank',
#columns:  'fourth_suit', 'fourth_rank', 'fifth_suit', 'fifth_rank', 'hand'

#labels: 'zilch', 'one_pair', 'two_pair', 'three_of_a_kind', 'straight', 'flush', 'full_house',
#labels: 'four_of_a_kind', 'straight_flush', 'royal_flush'

                   
labels = ['zilch', 'one_pair', 'two_pair', 'three_of_a_kind', 'straight', 'flush', 'full_house',
           'four_of_a_kind', 'straight_flush', 'royal_flush']

# Separate the data into features (X) and targets (y)
#X = poker_df.iloc[:,0:9]
#y = test['hand']

X_train = poker_df.loc[:,poker_df.columns != 'Hand']
X_test = test.loc[:,test.columns != 'Hand']
Y_train = poker_df['Hand']
Y_test = test['Hand']

poker_df

"""### Evaluating Class Balance"""

from yellowbrick.classifier import ClassBalance, ROCAUC, ClassificationReport, ClassPredictionError
balance = ClassBalance(size=(1080, 720), labels=labels)

balance.fit(Y_train)   
#balance.score(X, y)
balance.poof()

"""### Upsampling from Minority Classes"""

poker_df.loc[poker_df['Hand'] >= 7, 'Hand'] = 7
test.loc[test['Hand'] >= 7, 'Hand'] = 7

labels = ['zilch', 'one_pair', 'two_pair', 'three_of_a_kind', 'straight','flush',"full_house",'poker_or_better']

X_train = poker_df.loc[:,poker_df.columns != 'Hand']
X_test = test.loc[:,test.columns != 'Hand']
Y_train = poker_df['Hand']
Y_test = test['Hand']

from yellowbrick.classifier import ClassBalance, ROCAUC, ClassificationReport, ClassPredictionError
balance = ClassBalance(size=(1080, 720), labels=labels)

balance.fit(Y_train)   
#balance.score(X, y)
balance.poof()

"""### Training the Random Forests Classifier

### Classification Accuracy
"""

from sklearn.model_selection import train_test_split as tts
from sklearn.ensemble import RandomForestClassifier

#X_train, X_test, Y_train, Y_test = tts(X, y, test_size=0.2)

clf = RandomForestClassifier(n_estimators=100, class_weight='balanced', n_jobs=-1)
clf.fit(X_train, Y_train)
# prediction on test set
Y_pred=clf.predict(X_test)

#Import scikit-learn metrics module for accuracy calculation
from sklearn import metrics
# Model Accuracy, how often is the classifier correct?
print("Accuracy:",metrics.accuracy_score(Y_test, Y_pred))

"""### ROC Curve and AUC"""

from yellowbrick.classifier import ROCAUC, ClassificationReport, ClassPredictionError
labels = ['zilch', 'one_pair', 'two_pair', 'three_of_a_kind', 'straight','flush',"full_house",'poker_or_better']
rocauc = ROCAUC(clf, size=(1080, 720), classes=labels)

rocauc.score(X_test, Y_test)  
r = rocauc.poof()

"""### Classification Report Heatmap"""

report = ClassificationReport(clf, size=(720, 640), classes=labels, cmap='PuBu')

report.score(X_test, Y_test)
c = report.poof()

"""### Class Prediction Error"""

error = ClassPredictionError(clf, size=(1080, 720), classes=labels)

error.score(X_test, Y_test)
e = error.poof()

"""Preprocess the Data to sort the values"""

def preprocess_data(data:pd.DataFrame):
    df = data.copy()
    dfc = df[['C1', 'C2', 'C3', 'C4', 'C5']]
    dfc.values.sort()
    df[['C1', 'C2', 'C3', 'C4', 'C5']] = dfc
    df = df[['C1', 'C2', 'C3', 'C4', 'C5', 'S1', 'S2', 'S3', 'S4', 'S5', 'Hand']]
    return df

X_train_pre = preprocess_data(poker_df)
X_test_pre = preprocess_data(test)
X_train = X_train_pre.loc[:,X_train_pre.columns != 'Hand']
X_test = X_test_pre.loc[:,X_test_pre.columns != 'Hand']

X_train.head(20)

def add_unique_count(df:pd.DataFrame):
    tmp = df[['S1', 'S2', 'S3', 'S4', 'S5']]
    df['UniqueS'] = tmp.apply(lambda x: len(np.unique(x)) , axis=1)

add_unique_count(X_test)

add_unique_count(X_train)

X_train.head(20)

def add_diffs(df:pd.DataFrame):
    df['Diff1'] = df['C5'] - df['C4']
    df['Diff2'] = df['C4'] - df['C3']
    df['Diff3'] = df['C3'] - df['C2']
    df['Diff4'] = df['C2'] - df['C1']

add_diffs(X_train)

add_diffs(X_test)

X_train.head()

clf2= DecisionTreeClassifier(random_state=1, criterion='gini')

clf2.fit(X_train, Y_train)

y_pred = clf2.predict(X_test)
# Model Accuracy, how often is the classifier correct?
print("Accuracy:",metrics.accuracy_score(Y_test, y_pred))

report = ClassificationReport(clf2, size=(720, 640), classes=labels, cmap='PuBu')

report.score(X_test, Y_test)
c = report.poof()

rf2 = RandomForestClassifier(criterion='gini', n_estimators=8, random_state=1, n_jobs=5)

rf2.fit(X_train, Y_train)

yf_pred = rf2.predict(X_test)

# Model Accuracy, how often is the classifier correct?
print("Accuracy:",metrics.accuracy_score(Y_test, yf_pred))

report = ClassificationReport(rf2, size=(720, 640), classes=labels, cmap='PuBu')

report.score(X_test, Y_test)
c = report.poof()



def predictionThree2(X_test, clf2):
    yt2_pred = clf2.predict(X_test)
    #print(yf_pred)
    return yt2_pred

def predictionForest(X_test, rf2):
    yf_pred = rf2.predict(X_test)
    #print(yf_pred)
    return yf_pred

def preprocess_dataT(data:pd.DataFrame):
    df = data.copy()
    dfc = df[['C1', 'C2', 'C3', 'C4', 'C5']]
    dfc.values.sort()
    df[['C1', 'C2', 'C3', 'C4', 'C5']] = dfc
    df = df[['C1', 'C2', 'C3', 'C4', 'C5', 'S1', 'S2', 'S3', 'S4', 'S5']]
    return df

#Suit (1-4) representing {Hearts, Spades, Diamonds, Clubs}
#Numerical (1-13) representing (Ace, 2, 3, ... , Queen, King)

Eti= ['S1', 'C1','S2', 'C2','S3', 'C3','S4', 'C4','S5', 'C5']
X1_test1=np.array([[1,1,2,1,3,1,4,1,2,2],#4 ACES + 2 of SPADES 7
                   [1,1,1,2,1,3,1,4,1,5],#Straight Flush 7
                   [1,1,1,13,1,12,1,11,1,10], #Royal Flush 7 
                   [2,2,3,2,4,2,1,4,2,4], #Full House 6
                   [2,4,2,6,2,10,2,12,2,7], #Flush 5
                   [1,2,2,3,3,4,1,5,4,6], #Straight 4
                   [1,6,2,6,3,6,1,1,4,7], #Three of Kind 3
                   [4,5,3,5,2,13,2,1,3,13], #TwoPair 2
                   [3,6,3,7,4,7,1,13,1,10], #One Pair 1
                   [1,2,3,4,2,6,1,9,1,10] #Nothing 0
                   ])


X1_test=pd.DataFrame(X1_test1,columns=Eti)



preprocess_dataT(X1_test)
add_unique_count(X1_test)

#yThree1=predictionThree1(X1_test,clf1)

add_diffs(X1_test)

yThree2=predictionThree2(X1_test,clf2)
yForest=predictionForest(X1_test,rf2)


print("Random Forest ",yForest)
#print("First Three   ",yThree1)
print("Second Three  ",yThree2)
X1_test.head(10)