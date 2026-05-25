### Quick checking phonemes
```bash
poetry run python
```
```python
>>> import nltk
>>> from nltk.corpus import cmudict
>>> d = cmudict.dict()
>>> d['hello']
[['HH', 'AH0', 'L', 'OW1'], ['HH', 'EH0', 'L', 'OW1']]
```

### Note about NLTK
https://www.nltk.org/_modules/nltk/corpus/reader/cmudict.html

Each vowel has a stress marker: 0, 1, or 2
Where 0 means no stress, 1 means primary stress, and 2 means secondary stress.