class LanguageHelper:
    """A class that gets a set of words that will be used as a dictionary.
There are also methods to see if the word is in the dictionary.
Another method gives suggestions based off of a given word that is not in the dictionary."""
    i = 0
    def __init__(self, wordlist):
        """Initializes the Language Helper class with a set of words"""
        
        self._words = wordlist.getWords()

    def __contains__(self, query):
        """Returns True if query is found in self._words. Else returns False."""
        
        if query in self._words:
            return True
        else:
            return False
        
    def __getSuggestions__(self, query):
        """Returns a list of suggestions for words based off of query."""
        i = i + 1
        
        suggestions = list()
        le = len(query) - 1
        tf1 = False
        tf2 = False
            
        for x in range(le): #Inverting letters
            testword = query[:x] +query[x + 1] +query[x] +query[x + 2:]
            if self.__contains__(testword):
                if(not(testword in suggestions)):
                    suggestions.append(testword)
                   

        for x in range(le): #add one letter to the word
            for y in range(26):
                if x == 0:
                    testword = chr(97 + y) +query
                else: 
                    testword = query[:x+1] +chr(97 + y) +query[x + 1:]
                if self.__contains__(testword):
                    if (not (testword in suggestions)):
                        suggestions.append(testword)
                        tf1 = True
      
        for x in range(le): #deletes a letter from the word
            testword = query[:x] +query[x+1:]
            if self.__contains__(testword):
                if(not(testword in suggestions)):
                    suggestions.append(testword)
      
        for x in range(le+1): #changes just one letter
            for y in range(26): 
                testword = query[:x] +chr(97+y) +query[x+1:]
                if x == (le+1):
                    testword = testword[:len(testword)-1]
                if self.__contains__(testword):
                    if(not(testword in suggestions)):
                        suggestions.append(testword)

        if self.__contains__(query.capitalize()):
            suggestions.append(query.capitalize())
            
        if i%2 != 0:
           if query.islower():
              suggestions.extend(self.__getSuggestions__(query.capitalize))
           else:
              suggestions.extend(self.__getSuggestions__(query.lower()))
              
        suggestions.sort()
        return suggestions
            
class WordSetCreator:
    """Creates a set of words that are used as a dictionary to compare to."""
    
    def __init__(self):
        """Creates a set of words from the file: English.txt"""
        
        self._words = set(line.strip() for line in open("English.txt")) #line.strip() removes spaces and \n from the read text

    def getWords(self):
        """Returns a set of words."""
        
        return self._words

class Controller:
    """Has the control of flow of the program."""
    
    def __init__(self):
        """Creates varibles, query, wsc, and lh to get the word that is being compared, a WordSetCreator, and a LanguageHelper."""
        
        query = raw_input("Please enter your word: ")
        wsc = WordSetCreator()
        lh = LanguageHelper(wsc)
        if (lh.__contains__(query)):
            print '%s is a valid word.' %(query)
        elif (query[0].isupper() and lh.__contains__(query.lower())):
            print '%s is a valid word.' %(query.lower())
        else:
            if query[0].isupper():
                lst = lh.__getSuggestions__(query)
                lst.extend(lh.__getSuggestions__(query.lower()))
                lst.sort()
                for word in lst:
                    print word.capitalize()
            else:
                for word in lh.__getSuggestions__(query):
                    print word
            

        
if __name__ == '__main__':
    control = Controller()
