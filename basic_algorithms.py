"""
CAPP 121: Analyzing Election Tweets

Daniel Munoz Batista

Basic algorithms module

Algorithms for efficiently counting and sorting distinct 'entities',
or unique values, are widely used in data analysis.
"""

import math
from util import sort_count_pairs

# Task 1.1
def count_tokens(tokens):
    '''
    Counts each distinct token (entity) in a list of tokens.

    Inputs:
        tokens: list of tokens (must be immutable)

    Returns: dictionary that maps tokens to counts
    '''
    tokens_dict = {}
    for t in tokens:
        if t in tokens_dict:
            tokens_dict[t] += 1
        else:
            tokens_dict[t] = 1  
    return tokens_dict

# Task 1.2
def find_top_k(tokens, k):
    '''
    Find the k most frequently occuring tokens.

    Inputs:
        tokens: list of tokens (must be immutable)
        k: a non-negative integer

    Returns: list of the top k tokens ordered by count.
    '''

    #Error checking (DO NOT MODIFY)
    if k < 0:
        raise ValueError("In find_top_k, k must be a non-negative integer")

    tokens_dict = count_tokens(tokens)
    complete_lst = list(tokens_dict.items())
    complete_lst.sort(key=lambda x: (-x[1], x[0]))
    #Get the top k tokens
    top_tokens = complete_lst[:k]
    top_tokens = [token for token, _ in top_tokens]
    return top_tokens


# Task 1.3
def find_min_count(tokens, min_count):
    '''
    Find the tokens that occur *at least* min_count times.

    Inputs:
        tokens: a list of tokens  (must be immutable)
        min_count: a non-negative integer

    Returns: set of tokens
    '''

    #Error checking (DO NOT MODIFY)
    if min_count < 0:
        raise ValueError("min_count must be a non-negative integer")

    tokens_dict = count_tokens(tokens)
    #Add token to the set using comprehension list
    tokens_min_set = {token for token, count in tokens_dict.items()
                      if count >= min_count}
    return tokens_min_set


# Task 1.4
def find_salient(docs, threshold):
    '''
    Compute the salient words for each document.  A word is salient if
    its tf-idf score is strictly above a given threshold.

    Inputs:
      docs: list of list of tokens
      threshold: float

    Returns: list of sets of salient words
    '''
    lst_salient_words = []
    #Find number of docs
    n_docs = len(docs)
    n_doc_appears = {}
    for doc in docs:
        tokens_dict = count_tokens(doc)
        set_doc = find_min_count(doc, 1)
        #Count the number of documents token appears
        for token in set_doc:
            if token in n_doc_appears:
                n_doc_appears[token] += 1
            else:
                n_doc_appears[token] = 1

    for doc in docs:
        if len(doc) == 0:
            lst_salient_words.append(set())
            continue
        set_salient_words = set()
        tokens_dict = count_tokens(doc)
        #Find the max n in the document
        max_count = max(tokens_dict.values())
        #Calculate tf_idf for each token
        for token, count in tokens_dict.items():
            aug_freq_token = 0.5 + 0.5 * (count/max_count)
            idf = math.log(n_docs/n_doc_appears[token])
            tf_idf = aug_freq_token * idf
            if tf_idf > threshold:
                set_salient_words.add(token)
        lst_salient_words.append(set_salient_words)
    return lst_salient_words