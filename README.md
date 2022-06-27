# English-Sentence-Labeling

Label an english sentence as one of the four structures; simple, complex, compound, compound-complex


## How to run

`pip install nltk`

`pip install pandas`

`pip install stanza`

`python main.py`

Input data < data/

Output > output/

main.py has two options of using\
1.python stanza (default)\n 2.python nltk.parse.stanford package.\ However, option 2 requires a model file in local which is large and thus not shared in this repository.

### Input format

texts delimeted by tab('/t')

There are two options. **The first line of the input file should be exactly same as the following exmaples.** 

**Option 1. Unlabeled data**

sentence\
I love cats\
I love dogs because they are cute\
...

**Option 2. Labeled data**

label_human /t sentence\
0 /t  I love cats\
2 /t  I love dogs because they are cute\
...

### Dependencies

python 3.9.12

nltk 3.7 

pandas 1.4.2

stanza 1.4.0

## Definitions

**Simple sentence :** A sentence with one independent clause and no dependent clauses.

**Compound sentence :** A sentence with at least two independent clauses and no dependent clauses.

**Complex sentence :** A sentence with at least one independent clause and one or more dependent clauses. 

**Compound-complex sentence :** A sentence with at least two independent clauses and one or more dependent clauses.

**Clause :** A group of words, consisting of a subject and a finite form of a verb

**Dependent clause :** A clause that cannot form a separate sentence but can form a sentence when joined with a main clause.

**Independent clause :** A clause in a sentence that would form a complete sentence by itself.

## Reference

Wikipedia. Sentence clause structure. [https://en.wikipedia.org/wiki/Sentence_clause_structure](https://en.wikipedia.org/wiki/Sentence_clause_structure)

Cambridge Dictionary. Clause, Independent clause, Dependent clause.  

[https://dictionary.cambridge.org/dictionary/english/clause](https://dictionary.cambridge.org/dictionary/english/clause)

[https://dictionary.cambridge.org/dictionary/english/independent-clause](https://dictionary.cambridge.org/dictionary/english/independent-clause)

[https://dictionary.cambridge.org/dictionary/english/dependent-clause](https://dictionary.cambridge.org/dictionary/english/dependent-clause)

Universal Dependencies contributors. Universal Dependencies. [https://universaldependencies.org/u/overview/complex-syntax.html#ellipsis-in-clause-coordination](https://universaldependencies.org/u/overview/complex-syntax.html#ellipsis-in-clause-coordination)

Stanfordnlp. CoreNLP. [https://github.com/stanfordnlp/CoreNLP]
