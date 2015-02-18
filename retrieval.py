
from classifiers import BM25Classifier
from classifiers import GramMatchClassifier
from extractors import NGramExtractor
from extractors import Nto1GramExtractor
from extractors import SkipGramExtractor
from documents import Corpus
import sys

presidents = 'Presidents'
queries = [
	'adams',
	'lincoln',
	'president',
	'assassinated president',
	'great president',
	'first president',
	'civil war president',
	'the greatest president',
	'america',
	'vietnam war president',
	'terrorism',
	'world war',
	'united nations',
	'great depression',
	'impeachment',
	'second term',
	'first president after civil war'
]

def test(classifier,name):
	print '\n'
	print name
	classifier
	for query in queries:
		print '\n'
		print 'Query:',query
		for (cat,score) in classifier.getStringScores(query):
			print cat,':',score
		raw_input('Press Enter To Continue')

def main():
	corpus = Corpus(presidents)
	c = BM25Classifier(corpus)
	test(c, 'Term Matching with BM25')
	ex = NGramExtractor(2)
	corpus = Corpus(presidents,ex)
	c = BM25Classifier(corpus)
	test(c, 'bigrams with BM25')
	c = GramMatchClassifier(corpus)
	test(c, 'bigrams with length normalized match count')
	ex = Nto1GramExtractor(2)
	corpus = Corpus(presidents,ex)
	c = GramMatchClassifier(corpus)
	test(c, 'unigrams and bigrams')
	ex = SkipGramExtractor(1,2)
	corpus = Corpus(presidents,ex)
	c = GramMatchClassifier(corpus)
	test(c,'skip bigrams')
	ex = SkipGramExtractor(2,2)
	corpus = Corpus(presidents,ex)
	c = GramMatchClassifier(corpus)
	test(c,'two skip bigrams')

if __name__ == "__main__":
	main()

