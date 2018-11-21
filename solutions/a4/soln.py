#Author: Andrew Runka
#Student#: 100123456
#This program contains all of the solutions to assignment 4, fall2018 comp1005/1405
	#and probably some other scrap I invented along the way


def loadTextFile(filename):
	try:
		f = open(filename)
		text = f.read()
		f.close()
		return text
	except IOError:
		print(f"File {filename} not found.")
		return ""
		

def countWords(filename):
	text = loadTextFile(filename)
	text = text.split()
	return len(text)
	
def countCharacters(filename):
	text = loadTextFile(filename)
	return len(text)
	
def countCharacter(text,key):
	count=0
	for c in text:
		if c==key:
			count+=1
	return count
	
def countSentences(filename):
	text = loadTextFile(filename)
	count = 0
	count+=countCharacter(text,'.')   
	count+=countCharacter(text,'?')
	count+=countCharacter(text,'!')
	return count
	#return text.count(".")+text.count('?')+text.count('!')  #also valid

def removePunctuation(text):  
	text = text.replace(".","")
	text = text.replace(",","")
	text = text.replace("!","")
	text = text.replace("?","")
	text = text.replace(";","")
	text = text.replace("-","")
	text = text.replace(":","")
	text = text.replace("\'","")
	text = text.replace("\"","")
	return text	
	
def wordFrequency(filename):
	text = loadTextFile(filename)
	text = removePunctuation(text.lower())
	d = {}
	for w in text.split():
		if w not in d:
			d[w]=1
		else:
			d[w]+=1
	return d

def countUniqueWords(filename):
	dict = wordFrequency(filename)
	return len(dict.keys())

	
def countKWords(filename,k):
	dict = wordFrequency(filename)
	count=0
	for key in dict.keys():
		if key[0] == k:
			count+=1
	return count
	
def kWords(filename,k):
	dict = wordFrequency(filename)
	result = []
	for word in dict.keys():
		if word[0] == k:
			result.append(word)
	return result
	
def longestWord(filename):
	text = loadTextFile(filename)
	text = removePunctuation(text).split()
	longest = ""
	for w in text:
		if len(w)>len(longest):
			longest=w
	return longest
	
def startingLetter(filename):
	dict = wordFrequency(filename)
	#letters = {'a':0,'b':0,'c':0,'d':0,'e':0,'f':0,'g':0,'h':0,'i':0,'j':0,'k':0,'l':0,'m':0,'n':0,'o':0,'p':0,'q':0,'r':0,'s':0,'t':0,'u':0,'v':0,'w':0,'x':0,'y':0,'z':0}   #26 counters, one for each letter
	letters = {}
	
	#count frequencies
	for key in dict:
		if key[0] in letters:
			letters[key[0]] +=1
		else:
			letters[key[0]] = 1
		
	
	#find largest
	largest='a'
	for key in letters.keys():
		if letters[key]>letters[largest]:
			largest=key
			
	return largest
	
def letterFrequency(filename):
	text = loadTextFile(filename)
	d = {}
	for c in text:
		if c in d:
			d[c]+=1
		else:
			d[c]=1
			
	return d
	
def followsWord(filename, keyWord):
	keyWord = keyWord.lower()    
	text = loadTextFile(filename)
	text = removePunctuation(text).lower()
	text = text.split()
	
	follows = []
	for i in range(len(text)-1):
		if text[i] == keyWord:
			if text[i+1] not in follows:
				follows.append(text[i+1])
			
	return follows
		
def writeLines(filename,list):
	file = open(filename,'w')
	
	#out = "\n".join(list)
	out = ""
	for line in list:
		out+=line+"\n"
	file.write(out)
	file.close()
	
def reverseFile(filename):
	text = loadTextFile(filename)  #or readlines
	text = text.split("\n")
	text.reverse()
	writeLines("reversed_"+filename, text)
		