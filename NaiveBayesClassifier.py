from __future__ import division
import sys
import math

def trainClassifier(training_file):
	training_raw = open(training_file, 'r')
	raw_data = training_raw.readlines()
	num_good = 0
	num_bad = 0
	word_count = {}
	for document in raw_data:
		document = document.replace('.','')
		document = document.replace(',','')
		document = document.replace(':','')
		document = document.replace('?','')
		document = document.replace('!','')
		words = document.split()

		if(words[0] == '1'):	#This is a good review
			num_good += 1
			category = 1
		else:					#This is a bad review
			num_bad += 1
			category = 0
		words.pop(0)

		for word in words:
			if(word in word_count):
				word_count[word][category] += 1
			else:
				word_count[word] = [0,0]
				word_count[word][category] += 1

	training_raw.close()
	prior_good = num_good/(num_good + num_bad)
	prior_bad = num_bad/(num_bad + num_good)

	return num_good, num_bad, word_count

def classify(testing_file, num_good_training, num_bad_trainig, word_count):
	training_raw = open(testing_file, 'r')
	raw_data = training_raw.readlines()

	num_classified_good = 0
	num_classified_bad = 0
	num_good = 0
	num_bad = 0

	correctly_classified = 0
	num_documents = 0

	prior_good = num_good_training/(num_good_training + num_bad_trainig)
	prior_bad = num_bad_trainig/(num_good_training + num_bad_trainig)
	counter = 0
	for document in raw_data:
		document = document.replace('.','')
		document = document.replace(',','')
		document = document.replace(':','')
		document = document.replace('?','')
		document = document.replace('!','')
		words = document.split()

		if(words[0] == '1'):	#This is a good review
			num_good += 1
			category = 1
		else:					#This is a bad review
			num_bad += 1
			category = 0
		words.pop(0)

		sum_good = 0
		sum_bad = 0

		for word in words:
			counter += 1
			# print word_count[word]
			if(word in word_count):
				# print counter
				# print word
				# print word_count[word]

				if(word_count[word][1] == 0):
					prob_word_good == 0.0000001
				else:
					prob_word_good = word_count[word][1]/num_good_training

				if(word_count[word][0] == 0):
					prob_word_bad == 0.0000001
				else:
					prob_word_bad = word_count[word][0]/num_bad_trainig

				sum_good += math.log(prob_word_good)
				sum_bad += math.log(prob_word_bad)

		sum_good += math.log(prior_good)
		sum_bad += math.log(prior_bad)

		if(sum_good > sum_bad):
			num_classified_good += 1
			if(category == 1):
				correctly_classified += 1
		else:
			num_classified_bad += 1
			if(category == 0):
				correctly_classified += 1
		num_documents += 1

	return correctly_classified, num_documents





def main():
	training_file = sys.argv[1]
	testing_file = sys.argv[2]

	num_good_training, num_bad_training, word_count = trainClassifier(training_file)

	correctly_classified, num_documents = classify(testing_file, num_good_training, num_bad_training, word_count)

	print 'Accuracy:', correctly_classified/num_documents


main()
