import en_core_web_md
import numpy as np
import re
import textacy.keyterms

from collections import Counter
from gensim.models.keyedvectors import KeyedVectors
from gensim import matutils
from stopwords import stopwords

nlp = en_core_web_md.load()
word_vectors = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin.gz', binary=True, limit=300000)


def vectorize(keyterms):
    kv = np.zeros(word_vectors.vector_size)
    for k, w in keyterms.items():
        try:
            kv += word_vectors.word_vec(k) * w
        except KeyError:
            pass
    return matutils.unitvec(kv)


def featurize(text):
    text = re.sub(r'… \[\+\d+ chars\]', '', text) # remove '... [+1000 chars]'
    doc = nlp(text)

    entities = {}
    for label in ['PERSON', 'NORP', 'FACILITY', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT']:
        ents = Counter([e.string.strip().lower() for e in doc.ents if e.label_==label])
        for name, count in ents.most_common():
            if len(name) > 1 and name not in stopwords:
                entities[label + ":" + name] = count

    keyterms = {k:w for (k, w) in textacy.keyterms.key_terms_from_semantic_network(doc, n_keyterms=20)
        if len(k) > 1 and k not in stopwords}
        
    return {'text': doc.text, 'entities': entities, 'keyterms': keyterms, 'vector': vectorize(keyterms)}
