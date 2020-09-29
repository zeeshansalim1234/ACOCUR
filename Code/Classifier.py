from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from imblearn.over_sampling import SMOTE
import numpy as np
import pandas as pd
import pickle
import os

# ------ commit -------------
INPUT_FILE_C = "../Data/Commit_TrainingSet.csv"
COMMIT_FILE_PATH = "../Output/Commit/Processed"
OUTPUT_FILE_PATH_C = "../Output/Commit/Compatible"

# ---------- reviews ---------------------------
INPUT_FILE_R = "../Data/Review_TrainingSet.csv"
REVIEW_FILE_PATH = "../Output/Review/Processed"
OUTPUT_FILE_PATH_R = "../Output/Review/Compatible"



def balanceSMOTE(X, y):
    X1, y1 = SMOTE(random_state=42).fit_resample(X, y)
    return X1, y1


def Get_Compatible_Reviews_withNewTrainingSet():

    df_training = pd.read_csv(INPUT_FILE_R)
    trainingSet = df_training.values.tolist()

    train_text = [row[0] for row in trainingSet]
    train_label = [row[1] for row in trainingSet]

    vectorizer = TfidfVectorizer(sublinear_tf=True, min_df=5, max_features=100000)
    x_vector_tdidf = vectorizer.fit_transform(train_text)
    x_vector, y_vector = balanceSMOTE(x_vector_tdidf, train_label)

    clf1 = LogisticRegression(C=100)
    clf1.fit(x_vector, y_vector)
    with open('../Data/model-LR-Review.pkl', 'wb') as fout:
        pickle.dump((vectorizer, clf1), fout)

    clf2 = svm.SVC(gamma=1, kernel='poly', C=100)
    clf2.fit(x_vector, y_vector)
    with open('../Data/model-SVM-Review.pkl', 'wb') as fout:
        pickle.dump((vectorizer, clf2), fout)

    for file in os.listdir(REVIEW_FILE_PATH):
        filename = REVIEW_FILE_PATH + "/" + file
        outputfile = OUTPUT_FILE_PATH_R + "/" + file

        df = pd.read_csv(filename, index_col=None, sep=',', skip_blank_lines=False, )
        df['Processed_Text'] = df['Processed_Text'].replace(np.nan, '   ', regex=True)

        X = vectorizer.transform(df['Processed_Text'])

        X1_Pred = clf1.predict(X)
        df['LR'] = pd.Series(X1_Pred)

        X2_Pred = clf2.predict(X)
        df['SVM'] = pd.Series(X2_Pred)

        df_Compatible = df.loc[(df.SVM == 1) | (df.LR == 1)]
        df_Compatible.to_csv(outputfile, index=False)
        print("# of compatible reviews identified in %s : %d " % (file.replace(".csv", ""), df_Compatible.shape[0]))


def Get_Compatible_Commits_withNewTrainingSet():

    df_training = pd.read_csv(INPUT_FILE_C)
    trainingSet = df_training.values.tolist()

    train_text = [row[0] for row in trainingSet]
    train_label = [row[1] for row in trainingSet]

    vectorizer = TfidfVectorizer(sublinear_tf=True, min_df=5, max_features=100000)
    x_vector_tdidf = vectorizer.fit_transform(train_text)
    x_vector, y_vector = balanceSMOTE(x_vector_tdidf, train_label)

    clf1 = LogisticRegression(C=100)
    clf1.fit(x_vector, y_vector)
    with open('../Data/model-LR-Commit.pkl', 'wb') as fout:
        pickle.dump((vectorizer, clf1), fout)

    clf2 = svm.SVC(gamma=1, kernel='poly', C=10)
    clf2.fit(x_vector, y_vector)
    with open('../Data/model-SVM-Commit.pkl', 'wb') as fout:
        pickle.dump((vectorizer, clf2), fout)

    for file in os.listdir(COMMIT_FILE_PATH):
        filename = COMMIT_FILE_PATH + "/" + file
        outputfile = OUTPUT_FILE_PATH_C + "/" + file

        df = pd.read_csv(filename, index_col=None, sep=',', skip_blank_lines=False, )
        df['Processed_Text'] = df['Processed_Text'].replace(np.nan, '   ', regex=True)

        X = vectorizer.transform(df['Processed_Text'])

        X1_Pred = clf1.predict(X)
        df['LR'] = pd.Series(X1_Pred)

        X2_Pred = clf2.predict(X)
        df['SVM'] = pd.Series(X2_Pred)

        df_Compatible = df.loc[(df.SVM == 1) & (df.LR == 1)]
        df_Compatible.to_csv(outputfile, index=False)

        print("# of compatible fixes identified in %s : %d " % (file.replace(".csv", ""), df_Compatible.shape[0]))


def Get_Compatible_Reviews_withSavedModels():

    with open('SavedModels/model-SVM-Review.pkl', 'rb') as fin:
        vectorizer1, clf1 = pickle.load(fin)

    with open('SavedModels/model-LR-Review.pkl', 'rb') as fin:
        vectorizer2, clf2 = pickle.load(fin)

    for file in os.listdir(REVIEW_FILE_PATH):

        filename = REVIEW_FILE_PATH + "/" + file
        outputfile = OUTPUT_FILE_PATH_R + "/" + file
        df = pd.read_csv(filename, index_col=None, sep=',', skip_blank_lines=False, )
        df['Processed_Text'] = df['Processed_Text'].replace(np.nan, '   ', regex=True)

        X1 = vectorizer1.transform(df['Processed_Text'])
        X1_Pred = clf1.predict(X1)
        df['SVM'] = pd.Series(X1_Pred)

        X2 = vectorizer2.transform(df['Processed_Text'])
        X2_Pred = clf2.predict(X2)
        df['LR'] = pd.Series(X2_Pred)

        df_Compatible = df.loc[(df.SVM == 1) | (df.LR == 1)]
        df_Compatible.to_csv(outputfile, index=False)

        print("# of compatible reviews identified in %s : %d " % (file.replace(".csv", ""), df_Compatible.shape[0]))


def Get_Compatible_Commits_withSavedModels():

    with open('SavedModels/model-SVM-Commit.pkl', 'rb') as fin:
        vectorizer1, clf1 = pickle.load(fin)

    with open('SavedModels/model-LR-Commit.pkl', 'rb') as fin:
        vectorizer2, clf2 = pickle.load(fin)

    for file in os.listdir(COMMIT_FILE_PATH):

        filename = COMMIT_FILE_PATH + "/" + file
        outputfile = OUTPUT_FILE_PATH_C + "/" + file
        df = pd.read_csv(filename, index_col=None, sep=',', skip_blank_lines=False, )
        df['Processed_Text'] = df['Processed_Text'].replace(np.nan, '   ', regex=True)

        X1 = vectorizer1.transform(df['Processed_Text'])
        X1_Pred = clf1.predict(X1)
        df['SVM'] = pd.Series(X1_Pred)

        X2 = vectorizer2.transform(df['Processed_Text'])
        X2_Pred = clf2.predict(X2)
        df['LR'] = pd.Series(X2_Pred)

        df_Compatible = df.loc[(df.SVM == 1) & (df.LR == 1)]
        df_Compatible.to_csv(outputfile, index=False)

        print("# of compatible fixes identified in %s : %d " % (file.replace(".csv", ""), df_Compatible.shape[0]))
