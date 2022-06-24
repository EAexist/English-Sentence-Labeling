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

# Problem 2. Identify existence of dependent clause 
# Problem 3. Identify number of dependent clauses
# 
# Approach 1. Use dependency parsing and advcl relation 
# Assumption. Verb of a dependent clause is a dependent of advcl relation 

# Extract number of dependent clauses and their verbs
def extract_dependent_clauses(sentence):
  sentence_parsed = parser.raw_parse(sentence)
  dependencies = sentence_parsed.__next__()

  list_dependent_clause_verbs = []

  for node in sorted(dependencies.nodes.values(), key=lambda v: v['address']):
    for rel, deps in node['deps'].items():
      if rel == 'advcl':
        for dep in deps:
          dep_node = dependencies.nodes[dep]
          if 'nsubj' in dep_node['deps'].keys():
            list_dependent_clause_verbs.append(dep_node['word'])

  result = len(list_dependent_clause_verbs), list_dependent_clause_verbs
  print(result)
  return(result) 

# Problem 4. Identify existence of independent clause 
# Problem 5. Identify number of independent clauses
# 
# Approach 1. Use dependency parsing and conj relation
# Assumption. Verb of a dependent clause is a dependent of conj relation 

# TODO : What is the correct category for reported speech? e.g. He said "I like it!".
# Extract number of independent clauses and their verbs
def extract_clauses(sentence):
  sentence_parsed = parser(sentence)
  dependencies = sentence_parsed.__next__()

  list_independent_clause_verbs = []
  list_dependent_clause_verbs = []

  # Classify the clause of the graph's root as an independent clause 
  root_address = dependencies.get_by_address(0)['deps']['root'][0]
  root = dependencies.get_by_address(root_address)

  # TODO@Solved : What if input is not even a sentence? @Confirm the first clause consisting of root only if the root has nsubj relation. Classify input with 0(zero) clause as 'not sentence'.
  # TODO : Can clauses share a subject? If not, new clause is defined only if its 'nsubj' relation dependent is unique from previous clauses'. 
  if 'nsubj' in root['deps'].keys(): # Check if a root verb has corresponding subject. Complete sentence requires a subject.   
    list_independent_clause_verbs.append(root['word']) 

  for node in sorted(dependencies.nodes.values(), key=lambda v: v['address']):
    for rel, deps in node['deps'].items():
      if rel == 'conj' or 'advcl' or 'ccomp': # TODO@Solved : Do every clause consists of 'conj' or 'advcl'? @Added 'ccomp' to cover all posibilities according to universal dependency document
        for dep in deps:
          dep_node = dependencies.get_by_address(dep)
          if 'nsubj' in dep_node['deps'].keys(): # Check if a dependent of advcl/conj has corresponding subject. New clause requires a new subject. 
            if rel == 'conj':
              list_independent_clause_verbs.append(dep_node['word'])
            elif rel == 'advcl' or 'ccomp':
              list_dependent_clause_verbs.append(dep_node['word'])              

  result = list_independent_clause_verbs, list_dependent_clause_verbs
  print("Verb of independent clauses: %s\nVerb of dependent clauses:%s"%result)
  return(result)
