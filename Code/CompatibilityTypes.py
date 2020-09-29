from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
import pickle
import os

# ------ commit -------------
COMMIT_TRAINING_FILE = "../Data/Commit-Type-TS.csv"
COMMIT_FILE_PATH = "../Output/Commit/Compatible"
OUTPUT_FILE_PATH_C = "../Output/Commit/CTypes"

# ---------- reviews ---------------------------
REVIEW_TRAINING_FILE = "../Data/Review-Type-TS.csv"
REVIEW_FILE_PATH = "../Output/Review/Compatible"
OUTPUT_FILE_PATH_R = "../Output/Review/CTypes"

FILE_FOR_DICT_TYPE = "../Data/Review_Type_Dict.csv"

def Get_Reviews_Types_withNewTrainingSet():

    with open('SavedModels/reviewTypeDict.pkl', 'rb') as ctype:
        category_to_id, id_to_category = pickle.load(ctype)

    df_training = pd.read_csv(REVIEW_TRAINING_FILE)

    df_training['category_id'] = df_training['Type'].replace(category_to_id)

    vectorizer = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 3),
                                 max_features=100000)
    x_vector = vectorizer.fit_transform(df_training.Processed_Text).toarray()
    x_label = np.asarray(df_training.category_id)

    clf = svm.SVC(gamma=1, kernel='poly', C=100)
    clf.fit(x_vector, x_label)
    with open('../Data/model-SVM-Review-Type.pkl', 'wb') as fout:
        pickle.dump((vectorizer, clf), fout)

    for file in os.listdir(REVIEW_FILE_PATH):
        filename = REVIEW_FILE_PATH + "/" + file
        outputfile = OUTPUT_FILE_PATH_R + "/" + file

        df = pd.read_csv(filename, index_col=None, sep=',', skip_blank_lines=False, )
        df['Processed_Text'] = df['Processed_Text'].replace(np.nan, '   ', regex=True)
        X = vectorizer.transform(df.Processed_Text).toarray()

        X_Pred = clf.predict(X)
        df['Prediction'] = pd.Series(X_Pred)
        df['Type'] = df.Prediction.replace(id_to_category)

        df['Date'] = pd.to_datetime(df['Date'])
        df.sort_values('Date', inplace=True, ascending=True)
        df.insert(0, "SL", "")
        start_row = 1
        for index, row in df.iterrows():
            df.at[index, 'SL'] = start_row
            start_row += 1

        df.drop(df.columns[[2, 4, 5, 6, 7, 8]], axis=1, inplace=True)
        df.to_csv(outputfile, index=False)

        df_Type = df['Type'].value_counts().rename_axis('Type').reset_index(name='Count')
        print(
            "The different types of compatibility issues raised in reviews in this period for %s are :" % (
                file.replace(".csv", "")))
        for index, row in df_Type.iterrows():
            print(row['Type'], " : ", row['Count'])


def Get_Reviews_Types_withSavedModels():

    with open('SavedModels/model-SVM-Review-Type.pkl', 'rb') as fin:
        vectorizer, clf = pickle.load(fin)

    with open('SavedModels/reviewTypeDict.pkl', 'rb') as ctype:
        category_to_id, id_to_category = pickle.load(ctype)


    for file in os.listdir(REVIEW_FILE_PATH):

        filename = REVIEW_FILE_PATH + "/" + file
        outputfile = OUTPUT_FILE_PATH_R + "/" + file
        df = pd.read_csv(filename, index_col=None, sep=',', skip_blank_lines=False, )
        df['Processed_Text'] = df['Processed_Text'].replace(np.nan, '   ', regex=True)

        X = vectorizer.transform(df['Processed_Text']).toarray()
        X_Pred = clf.predict(X)
        df['Prediction'] = pd.Series(X_Pred)

        df['Type'] = df.Prediction.replace(id_to_category)
        df['Date'] = pd.to_datetime(df['Date'])
        df.sort_values('Date', inplace=True, ascending=True)
        df.insert(0, "SL", "")
        start_row = 1
        for index, row in df.iterrows():
            df.at[index, 'SL'] = start_row
            start_row += 1

        df.drop(df.columns[[2, 4, 5, 6, 7, 8]], axis=1, inplace=True)
        df.to_csv(outputfile, index=False)

        df_Type = df['Type'].value_counts().rename_axis('Type').reset_index(name='Count')

        print(
            "The different types of compatibility issues raised in reviews in this period for %s are :" % (file.replace(".csv", "")))
        for index, row in df_Type.iterrows():
            print(row['Type'], " : ", row['Count'])


def Get_Commit_Types_withSavedModels():

    with open('SavedModels/model-SVM-Commit-Type.pkl', 'rb') as fin:
        vectorizer, clf = pickle.load(fin)

    with open('SavedModels/commitTypeDict.pkl', 'rb') as ctype:
        category_to_id, id_to_category = pickle.load(ctype)


    for file in os.listdir(COMMIT_FILE_PATH):

        filename = COMMIT_FILE_PATH + "/" + file
        outputfile = OUTPUT_FILE_PATH_C + "/" + file
        df = pd.read_csv(filename, index_col=None, sep=',', skip_blank_lines=False, )
        df['Processed_Text'] = df['Processed_Text'].replace(np.nan, '   ', regex=True)

        X = vectorizer.transform(df['Processed_Text']).toarray()
        X_Pred = clf.predict(X)
        df['Prediction'] = pd.Series(X_Pred)

        df['Type'] = df.Prediction.replace(id_to_category)
        df['Date'] = pd.to_datetime(df['Date'])
        df.sort_values('Date', inplace=True, ascending=True)
        df.insert(0, "SL", "")
        start_row = 1
        for index, row in df.iterrows():
            df.at[index, 'SL'] = start_row
            start_row += 1

        df.drop(df.columns[[3, 4, 5, 6]], axis=1, inplace=True)
        df.to_csv(outputfile, index=False)

        df_Type = df['Type'].value_counts().rename_axis('Type').reset_index(name='Count')

        print("The different types of compatibility fixes done in this period for %s are :" % (file.replace(".csv", "")))
        for index, row in df_Type.iterrows():
            print(row['Type'], " : ", row['Count'])


def Get_Commit_Types_withNewTrainingSet():

    with open('SavedModels/commitTypeDict.pkl', 'rb') as ctype:
        category_to_id, id_to_category = pickle.load(ctype)

    df_training = pd.read_csv(COMMIT_TRAINING_FILE)
    df_training['category_id'] = df_training['Type'].replace(category_to_id)

    vectorizer = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 3),
                            max_features=100000)
    x_vector = vectorizer.fit_transform(df_training.Processed_Text).toarray()
    x_label = np.asarray(df_training.category_id)

    clf = svm.SVC(gamma=1, kernel='poly', C=10)
    clf.fit(x_vector, x_label)
    with open('../Data/model-SVM-Commit-Type.pkl', 'wb') as fout:
        pickle.dump((vectorizer, clf), fout)

    for file in os.listdir(COMMIT_FILE_PATH):
        filename = COMMIT_FILE_PATH + "/" + file
        outputfile = OUTPUT_FILE_PATH_C + "/" + file

        df = pd.read_csv(filename, index_col=None, sep=',', skip_blank_lines=False, )
        df['Processed_Text'] = df['Processed_Text'].replace(np.nan, '   ', regex=True)
        X = vectorizer.transform(df.Processed_Text).toarray()

        X_Pred = clf.predict(X)
        df['Prediction'] = pd.Series(X_Pred)
        df['Type'] = df.Prediction.replace(id_to_category)
        df['Date'] = pd.to_datetime(df['Date'])
        df.sort_values('Date', inplace=True, ascending=True)
        df.insert(0, "SL", "")
        start_row = 1
        for index, row in df.iterrows():
            df.at[index, 'SL'] = start_row
            start_row += 1

        df.drop(df.columns[[3, 4, 5, 6]], axis=1, inplace=True)
        df.to_csv(outputfile, index=False)

        df_Type = df['Type'].value_counts().rename_axis('Type').reset_index(name='Count')

        print("The different types of compatibility fixes done in this period for %s are :" % (file.replace(".csv", "")))
        for index, row in df_Type.iterrows():
            print(row['Type'], " : ", row['Count'])


def Create_Dict_Types():

    df_type = pd.read_csv(FILE_FOR_DICT_TYPE)
    df_type['category_id'] = df_type['Type'].factorize()[0]
    category_id_df = df_type[['Type', 'category_id']].drop_duplicates().sort_values('category_id')
    category_to_id = dict(category_id_df.values)
    id_to_category = dict(category_id_df[['category_id', 'Type']].values)

    f = open("../Data/TypeDict.pkl", "wb")
    pickle.dump((category_to_id, id_to_category), f)
    f.close()

