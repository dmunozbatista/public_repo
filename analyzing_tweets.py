"""
CAPP 121: Analyzing Election Tweets

Diego Daniel Munoz Batista

Analyze module

Functions to analyze tweets. We use functions defined in basic_algorithms
"""

import unicodedata
import sys

from basic_algorithms import find_top_k, find_min_count, find_salient

##################### DO NOT MODIFY THIS CODE #####################

def keep_chr(ch):
    '''
    Find all characters that are classifed as punctuation in Unicode
    (except #, @, &) and combine them into a single string.
    '''
    return unicodedata.category(ch).startswith('P') and \
        (ch not in ("#", "@", "&"))

PUNCTUATION = " ".join([chr(i) for i in range(sys.maxunicode)
                        if keep_chr(chr(i))])

# When processing tweets, ignore these words
STOP_WORDS = ["a", "an", "the", "this", "that", "of", "for", "or",
              "and", "on", "to", "be", "if", "we", "you", "in", "is",
              "at", "it", "rt", "mt", "with"]

# When processing tweets, words w/ a prefix that appears in this list
# should be ignored.
STOP_PREFIXES = ("@", "#", "http", "&amp")


#####################  MODIFY THIS CODE #####################


############## Part 2 ##############

# Task 2.1
def find_top_k_entities(tweets, entity_desc, k):
    '''
    Find the k most frequently occuring entitites.

    Inputs:
        tweets: a list of tweets
        entity_desc: a triple such as ("hashtags", "text", True),
          ("user_mentions", "screen_name", False), etc.
        k: integer

    Returns: list of entities
    '''

    entities_complete_lst = []
    general_type, subkey, case_sensitive = entity_desc
    for tweet in tweets:
        entities = tweet["entities"] #This is a dict
        lst_gen_type = entities[general_type] #List of the type
        for element in lst_gen_type:
            entities_complete_lst.append(element[subkey])
    if not case_sensitive:
        entities_complete_lst = (entity.lower()
                                 for entity in entities_complete_lst)
    top_k_entities = find_top_k(entities_complete_lst, k)
    return top_k_entities


# Task 2.2
def find_min_count_entities(tweets, entity_desc, min_count):
    '''
    Find the entitites that occur at least min_count times.

    Inputs:
        tweets: a list of tweets
        entity_desc: a triple such as ("hashtags", "text", True),
          ("user_mentions", "screen_name", False), etc.
        min_count: integer

    Returns: set of entities
    '''
    entities_complete_lst = []
    general_type, subkey, _ = entity_desc
    for tweet in tweets:
        entities = tweet["entities"]
        lst_gen_type = entities[general_type]
        for element in lst_gen_type:
            entities_complete_lst.append(element[subkey])
    set_entities_min = find_min_count(entities_complete_lst, min_count)
    return set_entities_min



############## Part 3 ##############

# Pre-processing step and representing n-grams

# YOUR HELPER FUNCTIONS HERE


def remove_prefixes(tweet_tokens):
    """
    Removes words that start wiht specific characters such as @
    
    Inputs:
        tweet_tokens (list): list with each word as one element
    
    Returns:
        tokens (list): list with each word as one element after removing
        the words with prefixes
    """
    tokens = []
    for token in tweet_tokens:
        if (("http" not in token) and ("@" not in token)
            and token[0] != "&"):
            if token[0] not in STOP_PREFIXES:
                tokens.append(token)
    return tokens


def strip_punctuation(word):
    """
    Strips punctuation of words

    Inputs:
        word (str): word that will be cleaned
    
    Return:
        cleaned_word: word after removing punctuation
    """
    cleaned_word = word.strip(PUNCTUATION)
    return cleaned_word


def find_n_grams(cleaned_tokens, n):
    """
    Find the n-grams in a list of strings
    
    Inputs:
        cleaned_tokens (lst): list with cleaned words of the tweet
        n (int): value that indicates the length of the n-grams
    
    Returns:
        List of tuples with the n-grams of the tweet
    """
    #Check if n has a valid length
    if n <= len(cleaned_tokens):
        n_grams = list((cleaned_tokens[i:i + n] for i in
                        range(0, len(cleaned_tokens) - n + 1)))
        n_grams = [tuple(gram) for gram in n_grams]
        return n_grams    
    return []      


def eliminate_stop_words(cleaned_tokens):
    """
    Eliminate specific words that generally have high frequency in english

    Inputs:
        cleaned_tokens (list): list of tuples of cleaned tokens
    
    Return:
        tokens_lst (list): list of tokens after removing stop words
    """
    tokens_lst = []
    for token in cleaned_tokens:
        if token not in STOP_WORDS:
            tokens_lst.append(token)
    return tokens_lst


def cleaned_n_grams(tweet, case_sensitive, stop_w, n):
    """
    Use other functions (including find_n_grams) to clean tweet and return the
    n-grams of the text
    
    Inputs: 
        tweet (str): abridged text of the tweet
        case_sensitive (boolean): indicates if we differentiate lowercase from
                                  upper case
        stop_w (boolean): indicates if we are removing stoping words
        n (int): indicates the n in n-grams
    
    Return:
        n_grams (list): list of tuples with the cleaned n-grams of the tweet
    """
    #Transform text to list of strings divided by spaces
    tokens = remove_prefixes(tweet.split())
    cleaned_tokens = [strip_punctuation(word) for word in tokens]
    #Remove empty strings of the list
    cleaned_tokens = list(filter(None, cleaned_tokens))
    if stop_w:
        cleaned_tokens = eliminate_stop_words(cleaned_tokens)
    if not case_sensitive:
        cleaned_tokens = [token.lower()for token in cleaned_tokens]
    n_grams = find_n_grams(cleaned_tokens, n)
    return n_grams



# Task 3.1
def find_top_k_ngrams(tweets, n, case_sensitive, k):
    '''
    Find k most frequently occurring n-grams.

    Inputs:
        tweets: a list of tweets
        n: integer
        case_sensitive: boolean
        k: integer

    Returns: list of n-grams
    '''
    total_lst_grams = []
    for tweet in tweets:
        text = tweet["abridged_text"]
        grams = cleaned_n_grams(text, case_sensitive, True, n)
        for gram in grams:
            total_lst_grams.append(gram)
    top_grams = find_top_k(total_lst_grams, k)
    return top_grams


# Task 3.2
def find_min_count_ngrams(tweets, n, case_sensitive, min_count):
    '''
    Find n-grams that occur at least min_count times.

    Inputs:
        tweets: a list of tweets
        n: integer
        case_sensitive: boolean
        min_count: integer

    Returns: set of n-grams
    '''
    total_lst_grams = []
    for tweet in tweets:
        text = tweet["abridged_text"]
        grams = cleaned_n_grams(text, case_sensitive, True, n)
        for gram in grams:
            total_lst_grams.append(gram)
    min_count_grams = find_min_count(total_lst_grams, min_count)
    return min_count_grams


# Task 3.3
def find_salient_ngrams(tweets, n, case_sensitive, threshold):
    '''
    Find the salient n-grams for each tweet.

    Inputs:
        tweets: a list of tweets
        n: integer
        case_sensitive: boolean
        threshold: float

    Returns: list of sets of strings
    '''
    docs = []
    for tweet in tweets:
        text = tweet["abridged_text"]
        grams = cleaned_n_grams(text, case_sensitive, False, n)
        docs.append(grams)
    salient_grams = find_salient(docs, threshold)
    return salient_grams