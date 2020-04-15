# NO ADDITIONAL IMPORTS!
from text_tokenize import tokenize_sentences


class Trie:
    def __init__(self):
        # set value, children, type
        self.value = None
        self.children = {}
        # some way to keep track of the type of the keys 
        # without explicitly storing the entire keys themselves
        self.typ = None

    def __setitem__(self, key, value):
        """
        Add a key with the given value to the trie, or reassign the associated
        value if it is already present in the trie.  Assume that key is an
        immutable ordered sequence.  Raise a TypeError if the given key is of
        the wrong type.
        """
        if self.typ == None:
            self.typ = type(key)
        if not isinstance(key, self.typ):
            raise TypeError
        if len(key) == 0:
            self.value = value
        else:
            # [:1] instead of [0] for tuples
            if key[:1] in self.children:
                # recursive statement
                (self.children[key[:1]])[key[1:]] = value
            else:
                temp = Trie()
                self.children[key[:1]] = temp
                # temp.typ = type(key)
                # recursive statement
                temp[key[1:]] = value
                temp.typ = type(key)

    def __getitem__(self, key):
        """
        Return the value for the specified prefix.  If the given key is not in
        the trie, raise a KeyError.  If the given key is of the wrong type,
        raise a TypeError.
        """
        if len(key) == 0:
            return self.value
        # if len >= 1
        # if gone down entire path, no word
        if type(key) != self.typ:
            raise TypeError
        if key[:1] not in self.children.keys():
            raise KeyError
        return (self.children[key[:1]])[key[1:]]

    def __delitem__(self, key):
        """
        Delete the given key from the trie if it exists. If the given key is not in
        the trie, raise a KeyError.  If the given key is of the wrong type,
        raise a TypeError.
        """
        if self.typ == None:
            self.typ = type(key)
        if not isinstance(key, self.typ):
            raise TypeError
        if len(key) == 0:
            self.value = None
        else:
            # [:1] instead of [0] for tuples
            if key[:1] in self.children:
                # recursive statement
                (self.children[key[:1]])[key[1:]] = None
            else:
                temp = Trie()
                self.children[key[:1]] = temp
                temp.typ = type(key)
                # recursive statement
                temp[key[1:]] = None
        # if key not in self.children.values():
        #     raise KeyError
        # if type(key) != self.typ:
        #     return TypeError
        # del self.children["key"]

    def __contains__(self, key):
        """
        Is key a key in the trie? return True or False.
        """
        # hint - repeats previous code; use other functions
        try:
            return self[key] != None
        except:
            return False

    def __iter__(self):
        """
        Generator of (key, value) pairs for all keys/values in this trie and
        its children.  Must be a generator!
        """
        def help_iter(t):
            for key, value in t.children.items():
                if self[key] == None:
                    yield help_iter(value)
                yield (key, t[key])
        return help_iter(self)


def make_word_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    words in the text, and whose values are the number of times the associated
    word appears in the text
    """
    t = Trie()
    sentences = tokenize_sentences(text)
    for sentence in sentences:
        words = sentence.split()
        for word in words:
            if word in t:
                print()
    return t


def make_phrase_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    sentences in the text (as tuples of individual words) and whose values are
    the number of times the associated sentence appears in the text.
    """
    raise NotImplementedError


def autocomplete(trie, prefix, max_count=None):
    """
    Return the list of the most-frequently occurring elements that start with
    the given prefix.  Include only the top max_count elements if max_count is
    specified, otherwise return all.

    Raise a TypeError if the given prefix is of an inappropriate type for the
    trie.
    """
    raise NotImplementedError


def autocorrect(trie, prefix, max_count=None):
    """
    Return the list of the most-frequent words that start with prefix or that
    are valid words that differ from prefix by a small edit.  Include up to
    max_count elements from the autocompletion.  If autocompletion produces
    fewer than max_count elements, include the most-frequently-occurring valid
    edits of the given word as well, up to max_count total elements.
    """
    raise NotImplementedError


def word_filter(trie, pattern):
    """
    Return list of (word, freq) for all words in trie that match pattern.
    pattern is a string, interpreted as explained below:
         * matches any sequence of zero or more characters,
         ? matches any single character,
         otherwise char in pattern char must equal char in word.
    """
    raise NotImplementedError


# you can include test cases of your own in the block below.
if __name__ == '__main__':
    pass
