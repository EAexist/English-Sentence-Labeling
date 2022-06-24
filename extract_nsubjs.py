import nltk
from nltk.parse.stanford import StanfordDependencyParser

# Paths  
# Standford CoreNLP .jar
jar_path = 'corenlp/stanford-corenlp.jar' 
# Stanford CoreNLP model .jar
models_jar_path = 'corenlp/corenlp-english-default/stanford-corenlp-models-english-default.jar'
# Data
data_path = 'data/data.txt'

parser = StanfordDependencyParser(path_to_jar = jar_path, path_to_models_jar = models_jar_path)

# Sub-Problem 1. Compute number of clauses in a sentence

# Approach 1. Use dependency parsing and nsubj relation  
#
# 1. Number of clauses = number of nsubj relations with different head of verb 
#
# 2.
# Assumption. 
# 1. There exists at most 1 nsubj for a verb. 
# 2. At least one of the subjects in a clause is dependent of nsubj.
# TODO : Verify that the assumptions 1, 2 reasonable
#
# Under the assumptions, number of clauses = number of nsubj relations 
#
# Issue 1. Running time of dependency parser
# TODO : Modularize the choice of dependency parser 
# TODO : Quantitative Anlalysis of running time

# Extract number of clauses and instances of nsubjs in a single sentence
def extract_nsubjs(sentence):
  sentence_parsed = parser.raw_parse(sentence)
  dependencies = sentence_parsed.__next__()

  list_nsubjs = []

  for dep in list(dependencies.triples()):
    if(dep[1] == 'nsubj'): 
      num_clauses += 1
      list_nsubjs.append(dep)

  result = len(list_nsubjs), list_nsubjs

  print(result)

  return(result)