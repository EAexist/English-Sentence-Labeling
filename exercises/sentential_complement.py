import nltk
from nltk.corpus import treebank
nltk.donwload('treebank')

# Find verbs that take sentential complements.
# Assume we have production VP -> Vs S
def filter(tree):
    child_nodes = [child.label() for child in tree\
        if isinstance(child, nltk.Tree)]
    return (tree.label() == 'VP') and ('S' in child_nodes)

result = [subtree for tree in treebank.parsed_sents() for subtree in tree.subtrees(filter)]

print(result)