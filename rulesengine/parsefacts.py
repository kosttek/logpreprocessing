__author__ = 'kosttek'
from dataschema import Fact

class ParseFacts():

    def __init__(self):
        self.knowledgelist = list()

    def commentedLine(self,line):
        if  len(line.lstrip()) ==0 or line.lstrip()[0]=='#':
            return True
        return False


    def find(self, s, ch):
        '''finds all indexes of char in string'''
        return [i for i, ltr in enumerate(s) if ltr == ch]

    def findWithOutSpecialQuestionMarks(self,s):
        indexes = self.find(s,"\"")
        newindexes= list()
        for ind in indexes:
            if ind != 0 and s[ind-1]=="\\":
                pass
            else:
                newindexes.append(ind)
        return newindexes

    def parseLine(self,line):
        '''before "  sign in knowledgebase you have tu put \" '''
        if self.commentedLine(line):
            return None
        [factnameraw,argsraw] = line.split("(",1)
        factname = factnameraw.lstrip().rstrip()

        args = list()
        indexes = self.findWithOutSpecialQuestionMarks(argsraw)

        for i in range(0,len(indexes)/2):
            ind_start = indexes[i*2]
            ind_end   = indexes[i*2+1]
            args.append(argsraw[ind_start+1:ind_end])
        self.addFact(factname,args)

    def parseFile(self,filename):
        f = open(filename,'r')
        for line in f.readlines():
            self.parseLine(line)


    def addFact(self,factname,arguments):
        fact = Fact(factname,arguments)
        self.knowledgelist.append(fact)

if __name__ == "__main__":
    pf = ParseFacts()
    pf.parseLine("extend(\"lol kind of shit\", \"arg nr 1\", \"arg nr 2\")")
    pf.parseLine("extend(\"lol2\", \"arg nr 1\", \"arg nr 2\")")
    pf.parseLine("extend(\"lol3 kind of shit\", \"arg nr 1\", \"arg nr 2\")")
    for fa in pf.knowledgelist:
        print fa.factname, fa.arglist