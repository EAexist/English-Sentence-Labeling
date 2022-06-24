import nltk
import stanza
from nltk.parse.stanford import StanfordDependencyParser
import pandas as pd

# Helper function to handle dep relation
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

# Classify the structure of a sentence to 1 of 4 categories.
# Label = 0 : simple. 1 : compound, 2: complex, 3 : compound-complex
def classify_sentence_structure(sentence, parser):
  sentence_parsed = parser(sentence)
  dependencies = sentence_parsed.__next__()

  label = -1
  num_dependent_clause = 0
  num_independent_clause = 1 

  for node in sorted(dependencies.nodes.values(), key=lambda v: v['address']):
    for rel, deps in node['deps'].items():
      if rel in ['conj', 'advcl', 'ccomp', 'csubj', 'dep']:
        for dep in deps:
          dep_node = dependencies.get_by_address(dep)
          if 'nsubj' in dep_node['deps'].keys():
            if rel == 'conj':
              num_independent_clause += 1
            elif rel in ['advcl', 'ccomp', 'csubj']:
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
  return label, num_dependent_clause, num_independent_clause
    
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
  parser_name = 'corenlp'
  parser = None

  if parser_name == 'corenlp':
    jar_path = 'corenlp/stanford-corenlp.jar' 
    models_jar_path = 'corenlp/corenlp-english-default/stanford-corenlp-models-english-default.jar'
    parser = StanfordDependencyParser(path_to_jar = jar_path, path_to_models_jar = models_jar_path).raw_parse

  elif parser_name == 'stanza': # Didn't use stanza as its dependency graph didn't show meaningful improvement from corenlp.
    print('Current Algorithm doesn\'t support stanza. Available parsers are:\ncorenlp')
    exit(0)
    # stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma,depparse')

  data_path = 'data.txt'
  # data_path = 'data_dep.txt'

  # apply_function(visualize_sentence_stanza, path = 'data/%s'%(data_path), use_idx=True)

  df_sentences = pd.read_csv('data/%s'%(data_path), sep='\t', header=0)
  df_sentences.insert(0, 'label_int', None)
  df_sentences.insert(0, 'label', None)

  label_int_to_str = {-1: 'not a sentnece', 0 : 'simple', 1 : 'compound', 2: 'complex', 3 : 'compound-complex'}

  for row in df_sentences.itertuples(): 
    label_int = classify_sentence_structure(row.sentence.strip(), parser)
    # print(row.Index, label_int, a, b)
    label_str = label_int_to_str[label_int]
    df_sentences.at[row.Index, 'label_int'] = label_int
    df_sentences.at[row.Index, 'label'] = label_str
  print(df_sentences)
  df_sentences.to_csv('output/output_%s'%(data_path) , sep='\t', header=0, index=False)

if __name__ == "__main__":
	main()  

exit(0)

test_sentence = 'A dog and cat chases a chicken'
test_sentence = 'Although it hurt when she bent her wrist, she could still move her fingers'

# apply_function(visualize_parsed, use_idx=True)
# apply_function(extract_dependent_clauses, use_idx=False)
apply_function(classify_sentence_structure, use_idx=False)
# extract_dependent_clauses(test_sentence)




# Parse the sentence
result = parser.raw_parse(test_sentence)
dependency = result.__next__()


print ("{:<15} | {:<10} | {:<10} | {:<15} | {:<10}".format('Head', 'Head POS','Relation','Dependent', 'Dependent POS'))
print ("-" * 75)
  
# Use dependency.triples() to extract the dependency triples in the form
# ((head word, head POS), relation, (dependent word, dependent POS))  
for dep in list(dependency.triples()):
  print ("{:<15} | {:<10} | {:<10} | {:<15} | {:<10}"
         .format(str(dep[0][0]),str(dep[0][1]), str(dep[1]), str(dep[2][0]),str(dep[2][1])))

def traverse_tree(tree):
    print(tree)
    for subtree in tree:
        if type(subtree) == nltk.tree.Tree:
            traverse_tree(subtree)

