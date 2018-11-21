from solutions.a4 import soln
import inspect

filename = "phrases.txt"

with open(f"solutions/a4/{filename}", "r") as f:
    phrases = f.read().split("\n")


def check(output, sol):
    return output == sol

def loadTxt():
    return soln.loadTextFile(filename) 

def countWords():
    return soln.countWords(filename)

def countSentences():
    return soln.countSentences(filename)

def rmPunctuation():
    return [soln.removePunctuation(p) for p in phrases]

def freq():
    return soln.wordFrequency(filename)

def unique():
    return soln.countUniqueWords(filename)

def kWords():
    return soln.kWords(filename, "time")

def longest():
    return soln.longestWord(filename)

def writeLines():
    return soln.writeLines(filename, ["Test", "Does", "this", "Work"])

def reverse():
    return soln.reverseFile(filename)

def followsWord():
    return soln.followsWord(filename, "time")

def grade(attempts):
    # [input() for _ in range(12)]
    check_fns = [loadTxt, countWords, countSentences, rmPunctuation, freq, unique, kWords, longest, writeLines, reverse, followsWord]
    graded, solns = [], []
    for o, s in zip(attempts, check_fns):
        res = s()
        graded.append(check(o, res))
        solns.append(res)
        with open("phrases_copy.txt", "r") as f:
                with open("phrases.txt", "w") as f2:
                    f2.write(f.read())
    
    return graded, solns

 





