import re

compatibility = ["compat", "incompat", "support", "sync", "device", "phone", "integr", "android", "version", "upgrade", "update",
"honeycomb", "ice cream sandwich", "jelly bean", "kitkat", "lollipop", "marshmallow", "nougat", "oreo", "pie",
"gingerbread", "froyo", "eclair", "donut", "cupcake", "bluetooth", "platform", "crash", "cloud", "api", "samsung",
                 "nexus", "redmi", "galaxy", "moto", "lenevo", "tablet", "pixel", "huawei", "nova", "htc"]


def Compat_Count(sentence):
    count = 0
    if str(sentence).strip() != '':
        sentence = sentence.lower()
        for word in compatibility:
            pattern = "\\b(" + word + "\\w*)"   # checks if any word in sentence starts with these patterns
            match = re.search(pattern, sentence)
            if match:
                count += 1

    return count


def get_matched_records(df):
    df['Compat_Count'] = 0
    for index, row in df.iterrows():
        text = row['Text']
        df.at[index, 'Compat_Count'] = Compat_Count(text)

    df_Matched = df.loc[(df['Compat_Count'] > 0)]

    df_Matched.drop(['Compat_Count'], axis=1, inplace=True)
    df_Matched.reset_index(drop=True, inplace=True)
    return df_Matched


