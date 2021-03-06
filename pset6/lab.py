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
            self.typ = key[0:0]
        if not isinstance(key, type(self.typ)):
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
                temp.typ = key[0:0]

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
        if type(key) != type(self.typ):
            raise TypeError
        if key[:1] not in self.children.keys():
            raise KeyError
        return (self.children[key[:1]])[key[1:]]

    def get_trie(self, key):
        """
        Return the value for the specified prefix.  If the given key is not in
        the trie, raise a KeyError.  If the given key is of the wrong type,
        raise a TypeError.
        """
        if len(key) == 0:
            return self
        # if len >= 1
        # if gone down entire path, no word
        if type(key) != type(self.typ):
            raise TypeError
        if key[:1] not in self.children.keys():
            return []
        return (self.children[key[:1]]).get_trie(key[1:])

    def __delitem__(self, key):
        """
        Delete the given key from the trie if it exists. If the given key is not in
        the trie, raise a KeyError.  If the given key is of the wrong type,
        raise a TypeError.
        """
        if self.typ == None:
            self.typ = key[0:0]
        if not isinstance(key, type(self.typ)):
            raise TypeError
        if self[key] == None:
            raise KeyError
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
                temp.typ = key[0:0]
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
        def help_iter(tree, subword):
            # base case
            if tree.value != None:
                yield (subword, tree.value)
            # recursive
            for key, val in tree.children.items():
                yield from help_iter(val, subword+key)
        # self.typ = empty of same type
        yield from help_iter(self, self.typ)

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
                t[word] = t[word] + 1
            else:
                t[word] = 1
    return t

def make_phrase_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    sentences in the text (as tuples of individual words) and whose values are
    the number of times the associated sentence appears in the text.
    """
    t = Trie()
    sentences = tokenize_sentences(text)
    for sentence in sentences:
        words = tuple(sentence.split())
        if words in t:
            t[words] = t[words] + 1
        else:
            t[words] = 1
    return t

def autocomplete(trie, prefix, max_count=None):
    """
    Return the list of the most-frequently occurring elements that start with
    the given prefix.  Include only the top max_count elements if max_count is
    specified, otherwise return all.

    Raise a TypeError if the given prefix is of an inappropriate type for the
    trie.
    """
    # print(trie.children.keys())
    # wrong type
    if not isinstance(prefix, type(trie.typ)):
        raise TypeError

    # build pre-list
    lis = []
    prefix_trie = trie.get_trie(prefix)
    for key, value in prefix_trie:
        lis.append((prefix+key, value))

    # return any list of most frequent keys 
    # beginning with prefix (len == max_count)
    # or all (if less than max_count in trie)
    if max_count == None:
        return [word for word, v in lis]
    else:
        lis.sort(key=lambda x: x[1], reverse = True)
        return [word for word, v in lis[:max_count]]

def autocorrect(trie, prefix, max_count=None):
    """
    Return the list of the most-frequent words that start with prefix or that
    are valid words that differ from prefix by a small edit.  Include up to
    max_count elements from the autocompletion.  If autocompletion produces
    fewer than max_count elements, include the most-frequently-occurring valid
    edits of the given word as well, up to max_count total elements.
    """
    lis = autocomplete(trie, prefix, max_count)
    if len(lis) == max_count or lis == None:
        return lis
    else:
        lis_set = set(lis)
        lis_edits = set()
        lis_valid_edits = set()
        alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        # make possible editsac
        for i in range(0, len(prefix)):
            # single character deletion
            lis_edits.add(prefix[:i]+prefix[i+1:])
            # two-character transpose
            lis_edits.add(prefix[:i]+prefix[i+1:i+2]+prefix[i:i+1]+prefix[i+2:])
            # alphabet-dependent
            for char in alphabet:
                # single character insertion
                lis_edits.add(prefix[:i]+char+prefix[i:])
                # single character replacement
                lis_edits.add(prefix[:i]+char+prefix[i+1:])
        valid = set((key for key, value in trie))
        valid_dict = {key: value for key, value in trie}
        # print()
        # print("valid", valid)
        # print("edits", lis_edits)
        for edit in lis_edits:
            if edit in valid and edit not in lis_valid_edits and edit not in lis_set:
                lis_valid_edits.add(edit)
        lis_valid_edits = list(lis_valid_edits)
        lis_valid_edits.sort(key=lambda x: valid_dict[x], reverse = True)
        if max_count == None:
            return lis + lis_valid_edits
        else:
            return lis + [word for word in lis_valid_edits[:max_count-len(lis)]]

def word_filter(trie, pattern, subword = ''):
    """
    Return list of (word, freq) for all words in trie that match pattern.
    pattern is a string, interpreted as explained below:
         * matches any sequence of zero or more characters,
         ? matches any single character,
         otherwise char in pattern char must equal char in word.
    """
    result = []
    # base case - pattern match, valid value
    if pattern == '':
        if trie.value != None:
            result.append((subword, trie.value))
        return result
    # recursive cases
    # two cases of '*' using up or not using up letter
    # not use up letter
    if pattern[0] == '*':
        result = result + word_filter(trie, pattern[1:], subword)
    # check if ? or a fit otherwise try not using up
    for key, value in trie.children.items():
        if pattern[0] == '?' or pattern[0] == key:
             result = result + word_filter(value, pattern[1:], subword+key)
        elif pattern[0] == '*':
            # use up letter
             result = result + word_filter(value, pattern, subword+key)
    # set for no repeats
    return list(set(result))

# you can include test cases of your own in the block below.
if __name__ == '__main__':
    with open("11-0.txt", encoding="utf-8") as f:
        pass
