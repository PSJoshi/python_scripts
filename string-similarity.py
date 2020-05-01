#!/usr/bine/env python
# https://towardsdatascience.com/calculating-string-similarity-in-python-276e18a7d33a
# https://www.coveros.com/monitoring-system-calls-for-active-authentication-with-detours/
import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
stopwords = stopwords.words('english')

sentences = ['this is Foo bar sentence.','This sentence is similar to the foo bar sentence','this is just another string']

def clean_string(text):
    text = ''.join([word for word in text if word not in string.punctuation])
    text = text.lower()
    text = ' '.join([word for word in text.split() if word not in stopwords])
    return text 

def cosine_sim_vector(vect1,vect2):
    vect1 = vect1.reshape(1,-1)
    vect2 = vect2.reshape(1,-1)
    return cosine_similarity(vect1,vect2)
    
  
cleaned_sentences = list(map(clean_string,sentences))
print(cleaned_sentences)

vectorizer = CountVectorizer().fit_transform(cleaned_sentences)
vectors = vectorizer.toarray()
print(vectors)

print(cosine_sim_vector(vectors[0],vectors[1]))



