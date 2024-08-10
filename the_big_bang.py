import re
from nltk.stem import PorterStemmer
from collections import defaultdict
from typing import List


def _generate_data(db):
    for i, row in enumerate(open("./transcript.txt", 'r').readlines()):
        if row.strip():
            index(db, row.strip(), id_=i)


### Your Code ###
db = defaultdict(set)


def index(db, text: str, id_: int):
    db[id_] = text

def match(db, text: str):
    stemmer = PorterStemmer()
    stemmed_words = {stemmer.stem(word.lower()) for word in re.findall(r'\w+', text)}

    result = set()

    for id_, doc_text in db.items():
        doc_stems = {stemmer.stem(word.lower()) for word in re.findall(r'\w+', doc_text)}

        if stemmed_words.intersection(doc_stems):
            result.add(id_)

    return list(result)



### Sanity Tests ###

# Step 1:

index(db, "Our whole universe was in a hot, dense state", id_=1)

assert match(db, "universe") == [1], "The word 'universe' should appear in the DB"


# Step 2:

index(db, "Then nearly fourteen billion expansion ago expansion started, wait!", id_=1)

assert match(db, "It all started with the big bang!") == [1], "The word 'started' should appear in the DB"
assert match(db, "AGO") == [1], "The word 'ago' should appear in the DB"


# Step 3:

index(db, "Our best and brightest figure that it'll make an even bigger bang!", id_=1)
index(db, "Music and mythology, Einstein and astrology. It all started with the big bang!", id_=2)

assert match(db, "BANG") == [1, 2], 'The word "bang" should appear in the DB multiple times'


# Step 4:

index(db, "It's expanding ever outward but one day", id_=1)
assert match(db, "expanding") == [1], 'Document with id = 1 contains the word "expanding"'

index(db, "Our best and brightest figure that it'll make an even bigger bang!", id_=1)
assert match(db, "expanding") == [], "Document with id = 1 was overridden by a new doc that does not contain the word expanding"
assert match(db, "brightest") == [1], "Document with id = 1 contains the word 'brightest'"


# Step 5:

index(db, "It doesn't need proving", id_=1)
assert match(db, "prove") == [1], "Our search should support variations match, so in this case it should find all documents containing - proving, prove, proves, proved.."


# Step 6:

_generate_data(db)
assert len(match(db, 'jedi')) >= 70, "expected more appearances of the word 'jedi'"


### Performance Tests ###

import time

class Timer:
    def __init__(self):
        self.start = None
        self.end = None
        self.duration = None

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, type, value, traceback):
        self.end = time.time()
        self.duration = self.end - self.start



t = Timer()
with t:
    match(db, "jedi")

assert t.duration < 0.0001, "Too slow :("
