import nltk
import stanza
from graphviz import Source

# Visualize dependency graph of parsed sentence with dependency labels
def visualize_dependency(idx, dependencies): 
  dot_def = dependencies.to_dot()
  source = Source(dot_def, filename="graphs/dependency_graph%s"%(idx), format="png")
  source.view()

# Visualize dependency graph of a sentence with dependency labels
def visualize_sentence(idx, sentence, parser): 
  sentence_parsed = parser(sentence)
  dependencies = sentence_parsed.__next__()
  dot_def = dependencies.to_dot()
  source = Source(dot_def, filename="graphs/dependency_graph%s"%(idx), format="png")
  source.view()

# Print dependency graph of a sentence with dependency labels using stanza parser
def visualize_sentences_stanza(idx, sentences): 
  parser = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,lemma,depparse')
  for sentence in sentences:
    doc = parser(sentence)
    print(*[f'id: {word.id}\tword: {word.text}\thead id: {word.head}\thead: {sent.words[word.head-1].text if word.head > 0 else "root"}\tdeprel: {word.deprel}' for sent in doc.sentences for word in sent.words], sep='\n')

# Apply a function to every lines of a file and return list of outputs
# If func(line), use_idx = False
# else if func(index, line), use_idx = True
def apply_function(func, path, use_idx = False): 
  list_results = []
  with open(path, 'r', encoding='utf-8') as f:
      for idx, line in enumerate(f):
        line = line.split('\t')[1]
        result = func(idx, line) if use_idx else func(line)
        list_results.append(result)
        print(result)