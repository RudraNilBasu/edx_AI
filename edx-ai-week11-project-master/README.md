# edx-ai-week11-project
The task in this assignment is to produce sentiment predictions over a collection of IMDB reviews by various text data representation such as unigram, unigram with tf-idf, bigram and bigram with tf-idf.

## Tasks

- [ ] Combine raw DB into a single CSV file (`imdb_tr.csv` with 3 cols: `row_number`, `text`, `polarity`).
- [ ] Remove all common stopwords.
- [ ] transform text col in `imdb_tr.csv` into a term-document matrix using unigram model.
- [ ] Train a SGC classifier on it with `loss="hinge"` and `penalty="l1"`.
- [ ] train a SGD classifier using unigram representation, predict sentiments on imdb_te.csv, and write output to unigram.output.txt
- [ ] train a SGD classifier using bigram representation, predict sentiments on imdb_te.csv, and write output to unigram.output.txt
- [ ] train a SGD classifier using unigram representation with tf-idf, predict sentiments on imdb_te.csv, and write output to unigram.output.txt
- [ ] train a SGD classifier using bigram representation with tf-idf, predict sentiments on imdb_te.csv, and write output to unigram.output.txt

## References

[Problem Statement](https://courses.edx.org/courses/course-v1:ColumbiaX+CSMM.101x+1T2017/courseware/fc64ad14a2554a359a2af5498fe0bf2b/92d43179d1dd4e1fa385bc85c4fac757/)

[sklearn text feature extraction](http://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction)

[sklearn SGD](http://scikit-learn.org/stable/modules/linear_model.html#stochastic-gradient-descent-sgd)

[pandas cheatsheet](https://github.com/pandas-dev/pandas/blob/master/doc/cheatsheet/Pandas_Cheat_Sheet.pdf)

[Fast streaming of data from big data sources](https://indico.io/blog/fast-method-stream-data-from-big-data-sources/)