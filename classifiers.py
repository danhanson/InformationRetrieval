from documents import StringDocumentFrequencies
from extractors import NGramExtractor

class Classifier:
	def __init__(self,corpus):
		self.corpus = corpus
		self.categories = corpus.documents.keys()
		self.extractor = corpus.extractor

	def scoreString(self,string,category):
		return self.scoreDocument(StringDocumentFrequencies(string,self.extractor),category)

	def scoreDocument(self,doc,category):
		raise NotImplementedError()

	def getStringScores(self,string):
		return self.getDocumentScores(StringDocumentFrequencies(string,self.extractor));

	def getDocumentScores(self,document):
		ls = [
			(category,self.scoreDocument(document,category))
			for category in self.categories
		]
		ls.sort(lambda x,y: cmp(y[1],x[1]))
		return ls

def bm25formula(corpus,doc,word,b=0.75,k1=1.5):
	freq = doc[word]
	return max(0,corpus.idfs[word]*freq*(k1+1)/(freq+k1*(1+b*(len(doc)/corpus.averageDocumentLength-1))))


class BM25Classifier(Classifier):
	def __init__(self,corpus,b=0.75,k1=1.5):
		Classifier.__init__(self,corpus)
		self.b = b
		self.k1 = k1

	def scoreDocument(self,query,category):
		doc = self.corpus.documents[category]
		return sum(
			freq*bm25formula(self.corpus,doc,term,self.b,self.k1)
			for (term,freq) in query.iteritems()
		)

class GramMatchClassifier(Classifier):
	def __init__(self,corpus):
		Classifier.__init__(self,corpus)

	def scoreDocument(self,query,category):
		doc = self.corpus.documents[category]
		intersection = sum(1 for word in query if word in doc)
		try:
			scorep = intersection / float(len(doc))
			scoreq = intersection / float(len(query))
			return 2*(scorep*scoreq)/(scorep+scoreq)
		except ZeroDivisionError:
			return None;

"""
class TermMatchingClassifier(Classifier):
	def __init__(self,corpus,n):
		Classifier.__init__(self,corpus,n)

	def scoreDocument(self,query,document):
		idfs = self.idfs
		def scoreWords(queryTerm,passageTerm):
			if queryTerm is passageTerm:
				return idfs[queryTerm]
			elif queryTerm is None:
				return -idfs[passageTerm]
			elif passageTerm is None:
				return -idfs[queryTerm]
			else:
				return -idfs[passageTerm]

		def nonePadder(gen):
			gram = next(gen)
			for i in xrange(len(gram)-1,0,-1):
				yield i*(None,)+gram[i:]
			yield gram
			try:
				while True:
					gram = next(gen)
					yield gram
			except StopIteration:
				for i in xrange(`


		scores = [[0 for i in xrange(len(query))] for j in xrange(len(document))]

		ex = NGramExtractor(len(query))
		query = [next(ex.termsFromString(query.string))]
		
		for passage in ex.termsFromFile(document.filename):
			
"""
