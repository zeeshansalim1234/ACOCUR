import Code.PreprocessData as ppd
import pandas as pd
import os
import numpy as np
import Code.KeywordMatch as keycount

Input_Raw_File_Path = "../Output/Commit/Raw"
Clean_File_Path = "../Output/Commit/Processed"


def CleanCommitMessage():

    for file in os.listdir(Input_Raw_File_Path):

        filename = Input_Raw_File_Path + "/" + file
        output_filename = Clean_File_Path + "/" + file
        headers = ['Text', 'Date', 'Processed_Text']
        df = pd.read_csv(filename)

        df = keycount.get_matched_records(df)

        df['Processed_Text'] = df['Text'].map(lambda a: ppd.clean_commitmsg(a.replace(' _ ', ',').replace('----', ' \n')))  # reconstruct the original msg
        df['Processed_Text'] = df['Processed_Text'].replace(np.nan, ' ', regex=True)
        df.to_csv(output_filename, index=False, header=headers)
