import sys
training_file = sys.argv[1]
testing_file = sys.argv[2]
training_raw = open(training_file, 'r')

def readInput():
	documents = training_raw.readlines()
	class_good = 0
	class_bad = 0
	for i in documents:
		document = i.split()
		if (document[0] == '1'):
			class_good += 1
		else:
			class_bad += 1

	print('Good rewievs:', class_good)
	print('Bad rewievs:', class_bad)


readInput()
