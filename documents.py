
from os import path
from os import listdir
from math import log
from extractors import NGramExtractor

unigramExtractor = NGramExtractor(1)

class zerodict(dict):
	def __init__(self,arg={}):
		dict.__init__(self,arg)

	def __missing__(self,key):
		return 0

class DocumentFrequencies(zerodict):
	def __init__(self,extractor=unigramExtractor):
		zerodict.__init__(self)
		self.termCount = 0
		self.extractor = extractor

	def addTerms(self,gen):
		for term in gen:
			self[term] += 1
			self.termCount += 1

	def __len__(self):
		return self.termCount

class FileDocumentFrequencies(DocumentFrequencies):
	def __init__(self,filename,extractor=unigramExtractor):
		DocumentFrequencies.__init__(self)
		f = open(filename,'r')
		self.filename = filename
		self.addTerms(extractor.termsFromFile(f))
		f.close()

class StringDocumentFrequencies(DocumentFrequencies):
	def __init__(self,string,extractor=unigramExtractor):
		DocumentFrequencies.__init__(self)
		self.string = string
		self.addTerms(extractor.termsFromString(string))


class Corpus:
	def __init__(self,dirName,extractor=unigramExtractor):
		self.documents = {}
		for filename in listdir(dirName):
			self.documents[filename] = FileDocumentFrequencies(path.join(dirName,filename),extractor)
		numDocuments = len(self.documents)
		self.averageDocumentLength = sum(len(doc) for doc in self.documents.values())/float(numDocuments)
		self.extractor = extractor
		self.termFrequencies = zerodict()
		for document in self.documents.values():
			for (term,count) in document.iteritems():
				self.termFrequencies[term]+=count

		self.tdfs = zerodict({
				term:sum((1 if term in doc else 0) for (name,doc) in self.documents.iteritems())
				for term in self.termFrequencies
		})

		self.idfs = zerodict({
				term:log((numDocuments-self.tdfs[term]+0.5)
			              /(self.tdfs[term]+0.5))
				for term in self.termFrequencies
		})

