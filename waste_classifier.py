import pickle
from sklearn import svm
from vector2Py import toDict,fruitToDict

ignore = [word for word in open('ignore.txt')]
compost_trigger_words = {"wooden", "compostable"}
cans_and_bottles_trigger_words = {"glass", "bottle" , "water", "tin", "can"}
paper_trigger_words = {"paper", "card", "cardboard"}
trash_trigger_words = {"battery"}

def invertPlurality(word):
    """
    inverts the plurality of a word if it follows standard convention
    in English; plural words become nonplural and nonplurals become plural
    eg  dog => dogs
        dogs => dog
    """
    if len(word) > 0:
        if word[-1] == 's':
            #it is plural right now
            word.pop()
            word = word[:-1]
            #keep all but last s
        else: 
            #it isn't plural so make it plural
            word += "s"

    return word

def waste_sorter(trash):
    suggestion = None
    content = trash.split()
    print content
    content = [word.lower() for word in content if word not in ignore]

    for word in content:
        #sometimes we don't need the classifier, because a word gives it away for sure
        if word in compost_trigger_words:
            return "compost"
        if word in cans_and_bottles_trigger_words: 
            return "cans"
        if word in paper_trigger_words:
            return "paper"
        if word in trash_trigger_words:
            return "trash"
    
    
    if len(content) == 1:
        if content[0] in d:
            suggestion = model.predict( d[content[0]])[0]
    else: 
        if len(content) == 2:
            #special combination for ngrams of length 2
            combined = "_".join(content)
            if combined in d: 
                suggestion = model.predict(d[combined])[0]
                return suggestion 
                

        for word in reversed(content):
            #more descriptive words tend to be at end of phrase
            if word in d:
                suggestion = model.predict(d[word])[0]
                break

    if suggestion == None:  
        print ("unrecognized")
        suggestion = "trash"
                
    return suggestion

with open("./waste_sorter_SVM.pickle") as infile:
    model = pickle.load(infile)

d = toDict("./vectors_100k.txt")
