# Noah Santos, 101110798


def loadTextFile(filename):  # problem 1
    """this function takes a filename as an argument, and returns the text of that file"""
    try:
        data = ""
        file = open(filename,'r')
        for line in file:
            data = data + line.strip()
    except:
        print("File not found")

    return data
filename = 'test.txt'

def countWords(filename):#problem 2
    """this function takes a filename as an argument and counts the number of words in that file"""
    try:
        total = 0
        file = open(filename, 'r')
        for line in file:
            line = line.strip().split()
            print(line)
            total = total + len(line)

    except:
        print("File not found")

    return total


def countSentences(filename):#problem 3
    """this function takes a filename as an argument and counts the number of sentences in that file"""
    try:
        data=""
        total = 0
        file = open(filename, 'r')
        for line in file:
            data = data + line.strip()
        for ch in data:
            if ch in [".", "?", "!"]:
                total = total + 1
    except:
        print("File not found")

    return total

def removePunctuation(string):#problem 4
    """this function takes a string of text as an argument and returns everything except for the punctuation"""
    punc = ".,?!;:\'\'"
    new_string=""
    for ch in string:
        if ch not in punc:
            new_string = new_string + ch
    return new_string
# used to test
# string = "Knock, knock! Who's there? Etch. Etch who? Gesundheit!"
# print(removePunctuation(string))

def wordFrequency(filename):#problem 5
    """this function takes a filename as an arugment and returns a dict with each unique word, as well as the # of times it occured"""
    f = open(filename, "r")
    file = f.read()
    text = file.lower()
    text = text.split()

    wordfreq = [text.count(p) for p in text]
    word_freq = zip(text, wordfreq)
    word_freq = dict(word_freq)

    return word_freq

def countUniqueWords(filename):#problem 6
    """this function takes a filename as an arugument and returns the number of unique words in that file"""
    lst = []
    try:
        file = open(filename, "r")
        for line in file:
            line = line.strip().split()
            for word in line:
                if word.lower() not in lst:
                    lst.append(word.lower())
    except:
        print("File not found")

    return len(lst)

def kWords(filename,letter):#problem 7
    """this function takes a filename and a letter and returns a list of unique words that start with the given letter"""
    lst = []
    try:
        file = open(filename, "r")
        for line in file:
            line = line.strip().split()
            for word in line:
                if word.lower()[0] == letter:
                    lst.append(word.lower())
    except:
        print("File not found")

    return lst

def longestWord(filename):#problem 8
    """this function takes a filename as an argument and returns the longest word in that file"""
    file = open(filename)
    maxLen = 0
    word = ""
    for line in file:
        line.replace(".", " ").replace(","," ")
        line.replace("?", " ").replace("!", " ")
        line.replace("\'", " ").replace("\"", " ")
        line.replace(" ", " ")
        temp = line.split()
        for w in temp:
            w = w.strip()
            if len(w) > maxLen:
                maxLen = len(w)
                word = w
    return word

def writeLines(filename, strings):#problem 9
    """this function takes a filename and a list of strings as arguments and prints the given list to the given file"""
    file = open(filename, "w")
    for line in strings:
        file.write(line + "\n")

def reverseFile(filename):#problem 10
    """this function takes a filename and creates a new file called reverse_filename, where the text is printed in reverse"""
    file = open(filename)
    allLines = []
    for line in file:
        allLines.append(line)

    file = open("reverse_"+filename, "w")
    i = len(allLines) - 1
    while 1 >=0:
        file.write(allLines[i] + "\n")
        i -= 1
