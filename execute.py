# Load in libraries
import urllib.request
import os
from IPython.display import clear_output
import pandas as pd
import numpy as np

# Load in files
fileurl = 'https://raw.githubusercontent.com/artusoma/collab_gathering/master/small_stats.csv'
word_df = pd.read_csv(fileurl)

words1 = [] #words lists to store words to show
words2 = []

def get_words(df, size = 1000):
    """Gets the best words from each bin
    """
    top_words = df.sort_values(by = 'Median_Frequency', ascending = False).head(size)
    # w1 is low tau (uniform words), w2 is high tau words
    w1 = top_words.sort_values(by = 'Tau', ascending = True).head(int(.2 * size)).word.values 
    w2 = top_words.sort_values(by = 'Tau', ascending = False).head(int(.2 * size)).word.values
    return w1, w2

def shuffle(l1, l2):
    '''Shuffles words randomly, switches position and creates a key
    '''
    np.random.shuffle(l1)
    np.random.shuffle(l2)

    if l1.shape[0] > l2.shape[0]:
        l1 = l1[:l2.shape[0]]
    else:
        l2 = l2[:l1.shape[0]]

    key = np.random.randint(low = 0, high = 2, size = l1.shape[0])

    for i in range(key.shape[0]):
        if key[i] == 1:
            placeholder1 = l1[i]
            placeholder2 = l2[i]

            l1[i] = placeholder2
            l2[i] = placeholder1

    return l1, l2, key

words1, words2 = get_words(word_df, size = 10000) # get words
words1, words2, key = shuffle(words1, words2) # shuffles words

def present_words(words1, words2, key):
    w1s = []
    w2s = []
    c = []

    for w1, w2 in zip(words1, words2):
        print("1 or 2? Type '3' if equal, type '4' if unsure/skip. 'exit' to exit")
        print('word 1' + '         ' + 'word 2')
        print(w1 + '          ' + w2 )
        a = input()
        clear_output(wait=False)

        if a == 'exit':
            # Create final dataframe
            output = pd.DataFrame()
            output['W1'] = w1s
            output['W2'] = w2s
            output['Choice'] = c
            output['Swap'] = key[:len(w1s)]

            return output
        
        w1s.append(w1); w2s.append(w2)
        c.append(a[0])
        clear_output(wait=False) 

def output_results(df):
    text_output = ''
    for i in range(df.shape[0]):
        text_output += (str(df.iloc[i,2]) + ' ' + str(df.iloc[i,3]) + '\n')
    return text_output

df = present_words(words1, words2, key)
text = output_results(df)
print(text)
