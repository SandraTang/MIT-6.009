import sys
sys.setrecursionlimit(10000)

# NO OTHER IMPORTS!


##################################################
#  Problem 1
##################################################

def get_mode(data):
    """ Finds the mode of a list of numbers. Breaks ties
        by preferring the greatest value. """
    # data is a list
    occurences = {}
    # see how many times each number appears
    for num in data:
        if num in occurences:
            occurences[num] = occurences[num] + 1
        else:
            occurences[num] = 1
    most = max(num for num in occurences.values())
    same = []
    for key, value in occurences.items():
        if value == most:
            same.append(key)
    same.sort()
    same.reverse()
    return same[0]


##################################################
#  Problem 2
##################################################

def letter_frequencies(word):
    letters = {}
    for c in word:
        if c in letters:
            letters[c] = letters[c] + 1
        else:
            letters[c] = 1
    return letters

def find_anagram_groups(words, N):
    """ Given a list of words, returns the index i into 
        words that contains the Nth word of the first 
        appearing anagram group of size N.  """

    # every word is anagram of itself
    if N <= 1:
        return N

    # generate dict of letter freqiencies
    # for each word
    words_freqs = []
    for word in words:
        words_freqs.append(letter_frequencies(word))

    # PART THAT TAKES A LONG TIME
    # compare words
    upper_limit = len(words_freqs)
    seen_anagrams = set()
    for index in range(len(words_freqs)):
        keep_going = True
        # only if anagram not seen yet
        if index not in seen_anagrams and index < upper_limit:
            count = 1
            for index2 in range(index+1, upper_limit):
                if keep_going and index2 not in seen_anagrams:
                    if words_freqs[index] == words_freqs[index2]:
                        count += 1
                        seen_anagrams.add(index2)
                    if count == N:
                        if index2 < upper_limit:
                            upper_limit = index2
                        keep_going = False


    # results
    if upper_limit == len(words_freqs):
        return None 
    else:
        return upper_limit



##################################################
#  Problem 3
##################################################

def find_elements(stream):
    elements = []
    for section in stream:
        if isinstance(section, list) or isinstance(section, tuple) or isinstance(section, set):
            elements = elements + find_elements(section)
        elif isinstance(section, dict):
            elements = elements + find_elements(list(section.keys())) + find_elements(list(section.values()))
        else:  # is primitive
            elements = elements + [section]
    return elements

def find_duplicates(stream):
    """ Finds all duplicated words in an arbitrarily
        nested structure of containers and strings. """
    # recursively build normal list
    elements = find_elements(stream)
    # build dict of frequency of items
    freq = {}
    for e in elements:
        if e in freq:
            freq[e] = freq[e] + 1
        else:
            freq[e] = 1
    # return set of all keys with value >= 2
    dups = set()
    for key, value in freq.items():
        if value >= 2:
            dups.add(key)
    #result
    return dups

if __name__ == "__main__":
    pass
