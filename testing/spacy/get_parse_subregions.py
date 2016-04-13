from __future__ import print_function, unicode_literals

# Answer:
# The easiest way is to find the head of the subtree you want, and then use the
# `.subtree`, `.children`, `.lefts` and `.rights` iterators. `.subtree` is the
# one that does what you're asking for most directly:

from spacy.en import English
nlp = English()

doc = nlp(u'displaCy uses CSS and JavaScript to show you how computers understand language')
for word in doc:
    if word.dep_ in ('xcomp', 'ccomp'):
        print(''.join(w.text_with_ws for w in word.subtree))

# It'd probably be better for `word.subtree` to return a `Span` object instead
# of a generator over the tokens. If you want the `Span` you can get it via the
# `.right_edge` and `.left_edge` properties. The `Span` object is nice because
# you can easily get a vector, merge it, etc.

doc = nlp(u'displaCy uses CSS and JavaScript to show you how computers understand language')
for word in doc:
    if word.dep_ in ('xcomp', 'ccomp'):
        subtree_span = doc[word.left_edge.i : word.right_edge.i + 1]
        print(subtree_span.text, '|', subtree_span.root.text)
        print(subtree_span.similarity(doc))
        print(subtree_span.similarity(subtree_span.root))


# You might also want to select a head, and then select a start and end position by
# walking along its children. You could then take the `.left_edge` and `.right_edge`
# of those tokens, and use it to calculate a span.
