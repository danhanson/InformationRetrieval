
from itertools import combinations

def normalize(word):
	return word.translate(None,",<.>/?;:'\"").lower()

class Extractor:

	def termsFromString(self,string):
		return self.getTerms(normalize(word) for word in string.split())

	def getTerms(self,iterator):
		raise NotImplementedError()

	def termsFromFile(self,file):
		def gen(file):
			for line in file:
				for word in line.split():
					yield normalize(word)

		return self.getTerms(gen(file))

class NGramExtractor(Extractor):

	def __init__(self,n):
		self.n = n

	def getTerms(self,words):
		gram = tuple(next(words) for i in xrange(self.n))
		while True:
			yield gram
			gram = gram[1:] + (next(words),)

class Nto1GramExtractor(Extractor):

	def __init__(self,n):
		self.n = n

	def getTerms(self,words):
		gram = ()
		try:
			for i in xrange(self.n):
				gram = gram + (next(words),)
				yield gram
			while True:
				gram = gram[1:]+(next(words),)
				for i in xrange(self.n):
					yield gram[:i+1]
		except StopIteration:
			for i in xrange(1,self.n):
				yield gram[i:]

class SkipGramExtractor(Extractor):

	def __init__(self,skip,n):
		self.skip = skip
		self.n = n

	def getTerms(self,words):
		gram = ()
		try:
			for i in xrange(self.n+self.skip):
				gram = gram + (next(words),)
			while True:
				for end in combinations(gram[1:],self.n-1):
					yield gram[:1]+end
				gram = gram[1:] + (next(words),)
		except StopIteration:
			if len(gram) == self.n:
				yield gram
			else:
				while len(gram) > self.n:
					gram = gram[1:]
					for end in combinations(gram[1:],self.n-1):
						yield gram[:1]+end

