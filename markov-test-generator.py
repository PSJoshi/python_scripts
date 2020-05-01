#!/usr/bin/env python
from collections import defaultdict, Counter
import os
import logging
import random
# Good links to look at:
# https://eli.thegreenplace.net/2018/elegant-python-code-for-a-markov-chain-text-generator/
# https://gist.github.com/stepchowfun/7213555
# https://www.stephanboyer.com/post/65/generating-domain-names-with-markov-chains
# https://github.com/exp0se/dga_detector

# https://github.com/frknozr/markovy
# https://seclab.bu.edu/people/gianluca/papers/botection-asiaccs2020.pdf
markov_model = defaultdict(Counter)
n_grams = 4
data = "this is a test paragraph that will be used to generate markov test"

print("Learning model..")
for i in range(len(data) - n_grams):
    state = data[i:i + n_grams]
    next = data[i + n_grams]
    markov_model[state][next] += 1

print(markov_model)

state = random.choice(list(markov_model))
#print(state)
#print(markov_model[state],markov_model[state].values())
out = list(state)
for i in range(10):
    out.extend(random.choices(list(markov_model[state]), markov_model[state].values()))
    state = state[1:] + out[-1]
    print("state:%s"%state)
print(''.join(out))