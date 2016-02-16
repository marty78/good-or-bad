from __future__ import division
import sys
import math
import re

def trainClassifier(training_file):
	training_raw = open(training_file, 'r')
	raw_data = training_raw.readlines()
	num_good = 0
	num_bad = 0

	word_freq = {}
	word_count = {}
	words_covered = []
	noOfPositiveWords = 0
	noOfNegativeWords = 0

	for document in raw_data:
		words_covered = []
		document = removeSym(document)
		document = document.lower()

		words = document.split()

		if(words[0] == '1'):	#This is a good review
			num_good += 1
			category = 1
			noOfPositiveWords += len(words)-1
		else:					#This is a bad review
			num_bad += 1
			category = 0
			noOfNegativeWords += len(words)-1
		words.pop(0)

		for word in words:
			word = stemming(word)

			if(word not in words_covered):
				if(word in word_count):
					word_count[word][category] += 1
					word_freq[word][category] += 1
					words_covered.append(word)
				else:
					word_freq[word] = [0,0]
					word_count[word] = [0,0]
					word_freq[word][category] += 1
					word_count[word][category] += 1
					words_covered.append(word)
			else:
				word_freq[word][category] += 1

			# if(word in word_count):
			# 	word_freq[word][category] += 1
			# 	if(word not in words_covered):
			# 		word_count

			# else:
			# 	word_freq[word] = [0,0]
			# 	word_freq[word][category] += 1
	training_raw.close()

	for word in word_freq:
		if(word_freq[word][1] != 0):
			print word, ':',word_freq[word][1]

	# print word_count
	print noOfNegativeWords
	print noOfPositiveWords
	return noOfPositiveWords, noOfNegativeWords, word_freq



def classify(testing_file, num_good_training, num_bad_trainig, word_count):
	testing_raw = open(testing_file, 'r')
	raw_data = testing_raw.readlines()

	correctly_classified = 0
	num_documents = 0

	prior_good = num_good_training/(num_good_training + num_bad_trainig)
	prior_bad = num_bad_trainig/(num_good_training + num_bad_trainig)

	counter = 0

	# print word_count

	for document in raw_data:
		document = removeSym(document)
		document = document.lower()

		words = document.split()

		if(words[0] == '1'):	#This is a good review
			category = 1
			# print "Actual value: GOOD"
		else:					#This is a bad review
			category = 0
			# print 'Actual value: BAD'
		words.pop(0)

		sum_good = 0
		sum_bad = 0
		print words
		for word in words:
			#word = stemming(word)

			if(word in word_count):
				if(word_count[word][1] == 0):
					prob_word_good = 0.00000001
				else:
					prob_word_good = word_count[word][1]/num_good_training

				if(word_count[word][0] == 0):
					prob_word_bad = 0.00000001
				else:
					prob_word_bad = word_count[word][0]/num_bad_trainig

				sum_good += math.log(prob_word_good)
				sum_bad += math.log(prob_word_bad)

		sum_good += math.log(prior_good)
		sum_bad += math.log(prior_bad)
		# print sum_good
		# print sum_bad,


		if(sum_good > sum_bad):
			#print 'sum_good > sum_bad'
			if(category == 1):
				correctly_classified += 1
				#print 'Guess: GOOD\n'

		else:
			#print 'sum_good < sum_bad'
			if(category == 0):
				correctly_classified += 1
				#print 'Guess: GOOD\n'

		num_documents += 1
		counter += 1
		# print num_documents
		# print correctly_classified,'\n'
	testing_raw.close()
	return correctly_classified, num_documents



def stemming(word):
	if(word[-1] == 's'):
		if(word[-4:] == 'sses'):
			word = word[:-2]
	return word

def removeSym(document):
	# document = document.replace('.','')
	# document = document.replace(',','')
	# document = document.replace(':','')
	# document = document.replace('?','')
	# document = document.replace('!','')
	# document = document.replace("'",'')
	# document = document.replace('-','')
	# document = document.replace('<','')
	# document = document.replace('>','')
	# document = document.replace('(','')
	# document = document.replace(')','')
	# document = document.replace('/',' ')
	# document = document.replace('<br /><br />', ' ')
	# document = document.replace('\xc2\x97', ' ')
	legalChars = "[^A-Za-z0-9\s]"
	cleanDocument = re.sub(legalChars,'',document.strip("\n")).lower()
	#print(cleanDocument)
	return cleanDocument			



def main():
	training_file = sys.argv[1]
	testing_file = sys.argv[2]

	num_good_training, num_bad_training, word_count = trainClassifier(training_file)

	correctly_classified, num_documents = classify(testing_file, num_good_training, num_bad_training, word_count)

	print 'Accuracy:', correctly_classified/num_documents


def debug():
	training_file = sys.argv[1]
	testing_file = sys.argv[2]

	num_good_training, num_bad_training, word_count = trainClassifier(training_file)


main()

#debug()
