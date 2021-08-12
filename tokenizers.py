import numpy as np
import pandas as pd
from sudachipy import tokenizer
from sudachipy import dictionary
import re
import neologdn
import string




def surface_sudachitokens(df):
    tokenizer_obj = dictionary.Dictionary().create()
    mode = tokenizer.Tokenizer.SplitMode.C #(Mode = B or C)
    for i in range(df.shape[0]):
        a = df.iloc[i].to_string()
        a = neologdn.normalize(a)
        df['text'][i] = [m.surface() for m in tokenizer_obj.tokenize(a, mode)]
        print(i)
    df.columns = ['sudachi']
    return df

def normalized_sudachitokens(df):
    tokenizer_obj = dictionary.Dictionary().create()
    mode = tokenizer.Tokenizer.SplitMode.C #(Mode = B or C)
    for i in range(df.shape[0]):
        a = df.iloc[i].to_string()
        a = neologdn.normalize(a)
        df['text'][i] = [m.normalized() for m in tokenizer_obj.tokenize(a, mode)]
        print(i)
    return df


def stopwords_removal(df, columns,  en_stopwords, ja_stopwords, en_dictionary):
    for wt in range(len(columns)):
        for i in range(df.shape[0]):
            df[cols[wt]][i] = [str(r) for r in df[cols[wt]][i]]
            df[cols[wt]][i] = [w for w in df[cols[wt]][i] if (re.findall(r"([ぁ-んァ-ン]+)",w) or re.findall(r"([一-龯]+)",w)
                                                            or re.findall(r"(\d+)",w)) or w.lower() in en_dictionary or not w.isalpha()]
            df[cols[wt]][i] = [w for w in df[cols[wt]][i] if(re.findall(r"([a-zA-Z]+)",w) or re.findall(r"([ぁ-んァ-ン]+)",w)
                                                           or re.findall(r"([一-龯]+)",w) or re.findall(r"(\d+)",w))]
            df[cols[wt]][i] = [word for word in df[cols[wt]][i] if word not in en_stopwords and word not in string.punctuation
                             and word not in ja_stopwords]
            df[cols[wt]][i] = ' '.join(df[cols[wt]][i]).split()
            print(cols[wt],i)
        df[cols[wt]] = df[cols[wt]].apply(lambda y: np.nan if len(y)==0 else y)
    return df

def multiple_tokenize(df, tokenizers, word_tokenizers):
    tokenizers = [w.lower() for w in tokenizers]
    df = pd.concat([df, pd.DataFrame(columns = tokenizers)])
    for wt in range(len(word_tokenizers)):
        for i in range(df.shape[0]):
            df[columns[wt]][i] = neologdn.normalize(df['text'][i])
            df[columns[wt]][i] = word_tokenizers[wt].tokenize(df[columns[wt]][i])
            print(columns[wt],i)
    return df

