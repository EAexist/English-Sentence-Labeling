import nltk
from nltk.parse.stanford import StanfordDependencyParser
import stanza
import pandas as pd

# Helper function to handle dep relation in classifier for stanza
# If a verb precedes nsubj dependent: classify as independent clause (e.g. Will you go?) 
# Else classify as dependent clasue (e.g. that I will go)
def is_dep_tree_dependent_stanza(words, word):
  nsubj_id = 0
  verb_id = 0
  
  for dependent in words:
    if dependent.head == word.id:
      if dependent.deprel == 'nsubj':
        nsubj_id = dependent.id
      elif ('VB' in dependent.xpos or dependent.xpos == 'MD'):
        verb_id = dependent.id   
    if nsubj_id != 0 and verb_id != 0:
      break

  return nsubj_id < verb_id

# Parser : stanza
# Classify the structure of a sentence to 1 of 4 categories.
# Label = 0 : simple. 1 : compound, 2: complex, 3 : compound-complex
def classify_sentence_structure_stanza(sentence, parser):

  doc = parser(sentence)
  words = doc.sentences[0].words

  label = -1
  num_dependent_clause = 0
  num_independent_clause = 1 

  for word in words:
    if word.deprel == 'acl:relcl':
      num_dependent_clause += 1
    elif word.deprel in ['advcl', 'ccomp', 'csubj', 'conj', 'dep', 'obj'] or 'acl' in word.deprel:
      for dependent in words:
        if dependent.head == word.id and dependent.deprel == 'nsubj':
          if word.deprel == 'conj':
            num_independent_clause += 1
          elif word.deprel in ['advcl', 'ccomp', 'csubj', 'acl'] or 'acl' in word.deprel:
            print(word.deprel)
            num_dependent_clause += 1    
          elif word.deprel == 'obj': 
            if is_dep_tree_dependent_stanza(words, word):
              num_dependent_clause += 1
            else:
              num_independent_clause += 1
              
    if num_independent_clause > 1 and num_dependent_clause > 0:
      label = 3
      return label

  if num_independent_clause == 1:
    label = 0 if num_dependent_clause == 0 else 2
  elif num_independent_clause > 1:
    label = 1 if num_dependent_clause == 0 else 3
  
  return label

# Helper function to handle dep relation in classifier for corenlp local
# If a verb precedes nsubj dependent: classify as independent clause (e.g. Will you go?) 
# Else classify as dependent clasue (e.g. that I will go)
def is_dep_tree_dependent(dependencies, dep_node, nsubj_address):
  for add in dep_node['deps']['nsubj']: # Save address of the first nsubj dependent
    if add < nsubj_address: 
      nsubj_address = add
  for _, find_verbs in dep_node['deps'].items():
    for find_verb in find_verbs:
      find_verb_node = dependencies.get_by_address(find_verb)
      if ('VB' in find_verb_node['tag'] or find_verb_node['tag'] == 'MD') and find_verb < nsubj_address:       
        return False
  return True

# Parser : corenlp local
# Classify the structure of a sentence to 1 of 4 categories.
# Label = 0 : simple. 1 : compound, 2: complex, 3 : compound-complex
def classify_sentence_structure_corenlp_local(sentence, parser):

  sentence_parsed = parser(sentence)
  dependencies = sentence_parsed.__next__()
  
  label = -1
  num_dependent_clause = 0
  num_independent_clause = 1 

  for node in sorted(dependencies.nodes.values(), key=lambda v: v['address']):
    for rel, deps in node['deps'].items():
      if rel in ['conj', 'advcl', 'ccomp', 'csubj', 'dep'] or 'acl' in rel:
        for dep in deps:
          dep_node = dependencies.get_by_address(dep)
          if 'nsubj' in dep_node['deps'].keys():
            if rel == 'conj':
              num_independent_clause += 1
            elif rel in ['advcl', 'ccomp', 'csubj'] or 'acl' in rel:
              num_dependent_clause += 1    
            elif rel == 'dep': 
              nsubj_address = len(dependencies.nodes.keys())
              if is_dep_tree_dependent(dependencies, dep_node, nsubj_address):
                num_dependent_clause += 1
              else:
                num_independent_clause += 1
              
    if num_independent_clause > 1 and num_dependent_clause > 0:
      label = 3
      return label

  if num_independent_clause == 1:
    label = 0 if num_dependent_clause == 0 else 2
  elif num_independent_clause > 1:
    label = 1 if num_dependent_clause == 0 else 3
  
  return label

# Parser : corenlp client
# Classify the structure of a sentence to 1 of 4 categories.
# Label = 0 : simple. 1 : compound, 2: complex, 3 : compound-complex
def classify_sentence_structure_corenlp_client(sentence, parser):
  raise NotImplementedError

# (Main) Label sentence by 4 category of sentence structure.
def main():
  # Format of input data
  # 1. Unlabeled data
  # sentence (*head)
  # I love cats
  # I love dogs because they are cute
  # ...
  # 2. Labeled data
  # label_human /t sentence (*head)
  # 0 /t I love cats
  # 2 /t I love dogs because they are cute
  # ...

  # Choose parser from 'stanza' (default), 'corenlp_local'
  parser_name = 'stanza' 
  parser = None
  classifier = None

  if parser_name == 'stanza': # Didn't use stanza as its dependency graph didn't show meaningful improvement from corenlp.
    parser = stanza.Pipeline(lang='en', processors='tokenize,pos,lemma,depparse')
    classifier = classify_sentence_structure_stanza


  elif parser_name == 'corenlp_local':
    jar_path = 'corenlp/stanford-corenlp.jar' 
    models_jar_path = 'corenlp/corenlp-english-default/stanford-corenlp-models-english-default.jar'
    parser = StanfordDependencyParser(path_to_jar = jar_path, path_to_models_jar = models_jar_path).raw_parse
    classifier = classify_sentence_structure_corenlp_local

  elif parser_name == 'corenlp_client':
    print('Current Algorithm doesn\'t support corenlp_client. Available parsers are:\nstanza\ncorenlp_local')
    exit(0)

  data_path = 'data.txt'

  df_sentences = pd.read_csv('data/%s'%(data_path), sep='\t', header=0)
  df_sentences.insert(0, 'label_int', None)
  df_sentences.insert(0, 'label', None)

  label_int_to_str = {-1: 'not a sentnece', 0 : 'simple', 1 : 'compound', 2: 'complex', 3 : 'compound-complex'}

  for row in df_sentences.itertuples(): 
    label_int = classifier(row.sentence.strip(), parser)
    label_str = label_int_to_str[label_int]
    df_sentences.at[row.Index, 'label_int'] = label_int
    df_sentences.at[row.Index, 'label'] = label_str
  print(df_sentences)
  df_sentences.to_csv('output/%s/output_%s'%(parser_name, data_path) , sep='\t', header=0, index=False)

if __name__ == "__main__":
	main()  