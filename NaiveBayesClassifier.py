import sys
training_file = sys.argv[1]
testing_file = sys.argv[2]

def trainClassifier(training_raw):
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
	return num_good, num_bad, word_count


def main():
	training_file = sys.argv[1]
	testing_file = sys.argv[2]
	training_raw = open(training_file, 'r')

	num_good, num_bad, word_count = trainClassifier(training_raw)
	print 'Good:', num_good
	print 'Bad:', num_bad
	# print(dictionary)


main()
