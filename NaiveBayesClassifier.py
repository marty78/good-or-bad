from __future__ import division
import sys
import math
import re
import time

def trainClassifier(training_file):
	training_raw = open(training_file, 'r')
	raw_data = training_raw.readlines()
	start_time = time.time()

	word_freq = {}
	word_count = {} #Used to count occurrences pr document only. Not used in final edition
	words_covered = []
	noOfPositiveWords = 0
	noOfNegativeWords = 0

	for document in raw_data:
		words_covered = []
		document = removeSym(document)
		words = document.split()

		if(words[0] == '1'):	#This is a good review
			category = 1
			noOfPositiveWords += len(words)-1
		else:					#This is a bad review
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

	training_raw.close()

	# for word in word_freq:
	# 	if(word_freq[word][1] != 0):
	# 		print word, ':',word_freq[word][1]
	# print word_freq
	# print noOfNegativeWords
	# print noOfPositiveWords
	execution_time = time.time() - start_time
	return noOfPositiveWords, noOfNegativeWords, word_freq, execution_time



def classify(testing_file, num_good_training, num_bad_trainig, word_count, flag_test):
	testing_raw = open(testing_file, 'r')
	raw_data = testing_raw.readlines()
	start_time = time.time()
	correctly_classified = 0
	num_documents = 0

	prior_good = num_good_training/(num_good_training + num_bad_trainig)
	prior_bad = num_bad_trainig/(num_good_training + num_bad_trainig)

	for document in raw_data:
		document = removeSym(document)
		words = document.split()

		if(words[0] == '1'):	#This is a good review
			category = 1
		else:					#This is a bad review
			category = 0
		words.pop(0)

		sum_good = 0
		sum_bad = 0
		for word in words:
			word = stemming(word)
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

		if(sum_good > sum_bad):
			if(flag_test == 1):
				print(1)
			if(category == 1):
				correctly_classified += 1

		else:
			if(flag_test ==1):
				print(0)
			if(category == 0):
				correctly_classified += 1

		num_documents += 1
	testing_raw.close()
	execution_time = time.time() - start_time

	return correctly_classified, num_documents, execution_time



def stemming(word):
	if(word[-1] == 's'):
		if(word[-4:] == 'sses'):
			word = word[:-2]
	return word

def removeSym(document):
	legalChars = "[^A-Za-z0-9\s]"
	cleanDocument = re.sub(legalChars,'',document.strip("\n")).lower()
	return cleanDocument			



def main():
	training_file = sys.argv[1]
	testing_file = sys.argv[2]
	num_good_training, num_bad_training, word_freq, time_training = trainClassifier(training_file)
	correctly_classified_train, num_documents_train, _ = classify(training_file, num_good_training, num_bad_training, word_freq,0)
	correctly_classified_test, num_documents_test, time_testing = classify(testing_file, num_good_training, num_bad_training, word_freq,1)
	print "%1.f"% time_training, 'seconds (training)'
	print "%1.f"% time_testing, 'seconds (labeling)'
	print correctly_classified_train/num_documents_train, '(training)'
	print correctly_classified_test/num_documents_test, '(testing)'


main()
