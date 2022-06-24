import nltk 
from collections import defaultdict

nltk.download('ppattach')

entries = nltk.corpus.ppattach.attachments('training')
table = defaultdict(lambda: defaultdict(set))
for entry in entries:
    key = entry.noun1 + '-'+ entry.prep+'-'+entry.noun2
    table[key][entry.attachment].add(entry.verb)

